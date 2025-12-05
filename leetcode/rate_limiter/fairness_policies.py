# 2.1. Preprocessing: effective weights
from collections import defaultdict


def compute_effective_weights(W, P, priority_multiplier):
    # priority_multiplier e.g. {P0: 10.0, P1: 5.0, P2: 1.0, P3: 0.1}
    N = len(W)
    W_eff = [0.0] * N
    for i in range(N):
        W_eff[i] = W[i] * priority_multiplier[P[i]]
    return W_eff

# 2.2. Weighted max-min water-filling (O(N log N))
def weighted_max_min(C, D, W_eff):
    """
    C: total capacity (float)
    D[i]: demand for tenant i (float)
    W_eff[i]: effective weight for tenant i (float)
    returns Q[i]: allocated quota
    """
    N = len(D)
    tenants = []
    for i in range(N):
        if W_eff[i] <= 0:
            continue
        # Sort key = D[i] / W_eff[i]; small means "saturates earlier"
        tenants.append((D[i] / W_eff[i], i))

    tenants.sort(key=lambda x: x[0])  # ascending by saturation level

    Q = [0.0] * N
    remaining_capacity = C
    remaining_weight_sum = sum(W_eff)

    last_level = 0.0

    for level, i in tenants:
        if remaining_weight_sum <= 0 or remaining_capacity <= 0:
            break

        # If we raise the "water level" from last_level to 'level',
        # how much capacity is needed?
        delta = level - last_level
        required = delta * remaining_weight_sum

        if required <= remaining_capacity + 1e-9:
            # We can bring all active tenants up to this level
            for j in range(N):
                if W_eff[j] > 0 and Q[j] < D[j]:
                    Q[j] += delta * W_eff[j]
            remaining_capacity -= required
            last_level = level

            # Tenant i is now fully satisfied (Q[i] == D[i]),
            # remove its weight from the active set
            remaining_weight_sum -= W_eff[i]
            W_eff[i] = 0.0
        else:
            # We cannot reach 'level'; distribute remaining capacity
            # proportionally to current weights and stop
            extra_per_weight = remaining_capacity / remaining_weight_sum
            for j in range(N):
                if W_eff[j] > 0 and Q[j] < D[j]:
                    Q[j] += extra_per_weight * W_eff[j]
            remaining_capacity = 0.0
            break

    # If there is any leftover capacity and some tenants still have demand,
    # distribute again proportionally (this is rare)
    if remaining_capacity > 0 and remaining_weight_sum > 0:
        extra_per_weight = remaining_capacity / remaining_weight_sum
        for j in range(N):
            if W_eff[j] > 0 and Q[j] < D[j]:
                Q[j] += extra_per_weight * W_eff[j]
    # Clamp to demand
    for i in range(N):
        Q[i] = min(Q[i], D[i])
    return Q

# Control Plane Algorithm (Fair-Share Allocator) sketch
# This is a periodic function that computes “what refill rate should each tenant’s bucket have?”
# Every Δt, it recomputes QuotaConfig and pushes it to SR agents.
#
# The algorithm (token bucket math) is always the same; what changes is:
# 	•	What identity you use for buckets (host / tenant / API key / IP / method), and
# 	•	Where you enforce (client vs edge vs server).
#
# “How do you push quotas from the control plane to all the clients? How often do you do it?”
# From control plane to each SR client we want to push:
# 	•	Root_rate for this service on that host
# 	•	Priority_bucket_rate[p] for P0/P1/P2/P3
# 	•	Tenant_bucket_rate[i] + capacity[i] for tenants that host actually cares about
#
# Think: “rate limiter config snapshot vN” + deltas.
#
# From SR client to control plane we send:
# 	•	local_demand, local_usage, local_p99 per tenant (metrics)
#
# So it’s a bi-directional periodic gossip: metrics up, quotas down.
#
# Push/pull model - A Hybrid model:
# 	•	Clients heartbeat upward (metrics) every Δt.
# 	•	Control plane optionally piggybacks new quotas in the heartbeat response.
# 	•	For large fan-outs, use a config service / pub-sub between allocator and regional caches,
# 	but SR still “pulls” from nearby cache.
# In practice:
#  •	SR → Control: POST /metrics (every Δt)
#  •	Control → SR: { ack, maybe_new_quota_config_if_version_advanced }
# Benefits:
# - Natural back-pressure (clients only see updates as fast as they heartbeat).
# - No need to open a million server-initiated streams.
# - Still get near-real-time responsiveness
#
# ** Allocator recompute interval (control plane internal)
# 	Allocator takes:
# 	•	Latest metrics from all SRs
# 	•	Backend p99 / error rate
# 	•	Runs:
# 	•	Capacity estimator
# 	•	Weighted max-min fairness
# 	•	Produces:
# 	•	New Q[i] quotas and per-priority shares
# 	•	New config version epoch = N+1
#
# In a nutshell, we run three loops:
# 1. SR heartbeats every ~1s send aggregated demand & usage up.
# 2. The allocator runs every few seconds, smoothing input metrics and computing
#   new fair-share quotas with weighted max-min.
# 3. Pushdown uses a hybrid model: SR includes its current config epoch in the heartbeat,
#   and the control plane responds with a newer epoch + diff when available.
#   That avoids massive push storms while still giving sub-second to a few-second reaction time.
def allocator_step(policy_config, metrics) -> QuotaConfig:
    # 1. Estimate global capacity C based on health
    C = estimate_capacity(metrics.backend_p99, metrics.error_rate, C_max=policy_config.C_max)

    # 2. Build per-tenant inputs
    D = metrics.tenant_demand      # demand[i]
    W = policy_config.weights      # weight[i]
    P = policy_config.priority     # priority[i]

    # 3. Compute effective weights
    W_eff = {}
    for i in tenants:
        W_eff[i] = W[i] * policy_config.priority_multiplier[P[i]]

    # 4. Run weighted max-min fairness to get Q[i], Per-tenant quota rates (tokens/sec per tenant)
    Q = weighted_max_min(C, D, W_eff)

    # 5. Aggregate per-priority shares (aka. priority-level budgets)
    PriorityShare = defaultdict(float)
    for i in tenants:
        p = P[i]
        PriorityShare[p] += Q[i]

    # 6. Fill (Derived) bucket rates to send to SR agents
    # •	Root_rate (service-level per-host)
    # •	Priority_bucket_rate[p]
    # •	Tenant_bucket_rate[i]
    cfg = QuotaConfig()
    cfg.Root_rate = C
    for p in priorities:
        # optional minimum reservation per priority
        min_res = policy_config.min_priority_reservation.get(p, 0.0)
        cfg.Priority_bucket_rate[p] = max(PriorityShare[p], min_res)

    for i in tenants:
        cfg.Tenant_bucket_rate[i]  = Q[i]
        cfg.Tenant_bucket_capacity[i] = Q[i] * policy_config.burst_factor  # e.g. 5x

    return cfg

def refill_bucket(bucket, now_ts):
    elapsed = now_ts - bucket.last_refill_ts
    if elapsed <= 0:
        return
    # refill by rate * time, but cap at capacity
    bucket.tokens = min(bucket.tokens + elapsed * bucket.refill_rate, bucket.capacity)
    bucket.last_refill_ts = now_ts

# Per-request enforcement algo
def try_consume_path(tenant_id, priority, method=None) -> bool:
    now_ts = now()

    root = buckets["root"]
    prio = buckets[f"priority:{priority}"]
    tenant = buckets[f"tenant:{tenant_id}"]
    method_bucket = buckets.get(f"method:{tenant_id}:{method}", None)

    path = [root, prio, tenant]
    if method_bucket:
        path.append(method_bucket)

    # 1. Refill along the path
    for b in path:
        refill_bucket(b, now_ts)

    # 2. Try to consume 1 token from each bucket
    for b in path:
        if b.tokens < 1.0:
            # fail: not enough tokens at some level
            return False
    # Only after we know all have tokens do we subtract
    for b in path:
        b.tokens -= 1.0

    return True

# Hook it into SR
def handle_request(req):
    T = req.tenant_id
    P = req.priority
    M = req.method

    tenant_state = tenant_states[T]

    # track demand regardless of outcome
    tenant_state.local_demand += 1

    if try_consume_path(T, P, M):
        tenant_state.local_usage += 1
        # forward RPC to backend
        return FORWARD
    else:
        # throttle locally; optionally return error or shed silently
        return THROTTLED

# Periodic metrics reporting
def heartbeat_loop():
    while True:
        time.sleep(HEARTBEAT_INTERVAL)

        metrics_payload = []
        for t in tenant_states.values():
            metrics_payload.append({
                "tenant_id": t.id,
                "local_demand": t.local_demand,
                "local_usage": t.local_usage,
                "local_p99": t.local_p99,  # if measured
            })
            # reset for next window
            t.local_demand = 0
            t.local_usage = 0

        send_to_metrics_store(metrics_payload)
