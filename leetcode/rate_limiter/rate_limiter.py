# Problem: Rate Limiting for API Requests
# Diﬃculty: Medium
# Tags: Design, Hash Table, Queue
# Problem Statement: Design a rate limiter that can handle different rate limiting
# strategies: fixed window, sliding window, and token bucket. The rate limiter should
# support multiple users and different rate limits per user.
#
# Gist:
# Design a reusable “rate-limiting engine” that can track per-user request activity
# over time and enforce different time-based policies with predictable behavior and performance.

# This is an “events over time” counting problem
# 	•	Multiple policies (fixed window, sliding window, token bucket)
# 	•	Multiple tenants (per-user limits)
# 	•	Potentially different configs per user (e.g., user A: 100 req/min, user B: 1000 req/min)
from __future__ import annotations

import time
import threading
from abc import ABC, abstractmethod
from collections import deque, defaultdict
from dataclasses import dataclass
from typing import Dict, Deque, Optional


# ==============================
# Strategy interfaces & configs
# ==============================

class RateLimitStrategy(ABC):
    @abstractmethod
    def configure_user(self, user_id: str, **config) -> None:
        ...

    @abstractmethod
    def allow(self, user_id: str, now: Optional[float] = None) -> bool:
        ...


# ---------- Fixed Window (thread-safe) ----------

@dataclass
class FixedWindowConfig:
    limit: int
    window_size: float


@dataclass
class FixedWindowState:
    window_start: float
    count: int


class FixedWindowLimiter(RateLimitStrategy):
    def __init__(self) -> None:
        self._configs: Dict[str, FixedWindowConfig] = {}
        self._states: Dict[str, FixedWindowState] = {}
        self._lock = threading.RLock()

    def configure_user(self, user_id: str, **config) -> None:
        limit: int = config["limit"]
        window_size: float = config["window_size"]
        with self._lock:
            self._configs[user_id] = FixedWindowConfig(limit=limit, window_size=window_size)
            self._states[user_id] = FixedWindowState(window_start=0.0, count=0)

    def allow(self, user_id: str, now: Optional[float] = None) -> bool:
        if now is None:
            now = time.time()

        with self._lock:
            if user_id not in self._configs:
                raise KeyError(f"User {user_id} not configured for FixedWindowLimiter")

            cfg = self._configs[user_id]
            state = self._states.get(user_id)

            if state is None or state.window_start == 0.0:
                state = FixedWindowState(window_start=now, count=0)

            # CORE LOGIC:
            # if now - window_start >= window_size:
            #     reset window_start and count
            #
            # if count < limit → count++ → allow
            # else reject
            #
            # Pros: O(1) space, simple
            # Con: Boundary burst (end + start of window)

            # New window?
            if now - state.window_start >= cfg.window_size:
                state.window_start = now
                state.count = 0

            if state.count < cfg.limit:
                state.count += 1
                self._states[user_id] = state
                return True
            else:
                self._states[user_id] = state
                return False


# ---------- Sliding Window (thread-safe) ----------

@dataclass
class SlidingWindowConfig:
    """
    SlidingWindow =
        “At most N requests in the last T seconds (a continuous window).”
    """
    limit: int
    window_size: float

class SlidingWindowLimiter(RateLimitStrategy):
    def __init__(self) -> None:
        self._configs: Dict[str, SlidingWindowConfig] = {}
        # We must store precise timestamps of individual requests.
        # And maintain a deque to keep timestamps in arrival order.
        self._events: Dict[str, Deque[float]] = defaultdict(deque)
        # NOTE: deque is not thread-safe, thus:
        # Mutation of the same deque from multiple threads still needs a lock
        # Concurrency alternatives:
        # 🅰️ Double-layer locking (global + per-user)
        # Pattern:
        # 	1.	Global lock:
        # 	    Protects self._configs and self._events membership / initialization.
        # 	2.	Per-user lock:
        # 	    Protects sliding window logic on that user’s deque.
        # 🅱️ Lock striping
        # Instead of a lock per user, you can have, say, 64 locks and hash user_id:
        # 🅾️ Actor / single-threaded model
        # Put the limiter in a single-threaded event loop (actor)
        # All threads send it “can user X proceed?” messages
        # It processes them sequentially, so no locks needed; logic stays exactly as in the single-threaded version.
        # That’s essentially what Redis + Lua is doing but in a different process.
        # 🅾️ Externalize concurrency to Redis
        self._lock = threading.RLock()

    def configure_user(self, user_id: str, **config) -> None:
        limit: int = config["limit"]
        window_size: float = config["window_size"]
        with self._lock:
            self._configs[user_id] = SlidingWindowConfig(limit=limit, window_size=window_size)
            # self._events[user_id] = deque()
            # optional but explicit: touch events to ensure deque exists
            _ = self._events[user_id]

    def allow(self, user_id: str, now: Optional[float] = None) -> bool:
        if now is None:
            now = time.time()

        with self._lock:
            if user_id not in self._configs:
                raise KeyError(f"User {user_id} not configured for SlidingWindowLimiter")

            cfg = self._configs[user_id]
            # q = self._events.setdefault(user_id, deque())
            q = self._events[user_id]

            # CORE LOGIC:
            # drop all timestamps <= now - window
            # if len(deque) < limit → append(now) → allow
            # else reject
            # Pros: precise
            # Cons: O(N) memory per busy user
            cutoff = now - cfg.window_size
            while q and q[0] <= cutoff:
                q.popleft()

            if len(q) < cfg.limit:
                q.append(now)
                return True
            else:
                return False


# ---------- Token Bucket (thread-safe) ----------

@dataclass
class TokenBucketConfig:
    capacity: float
    refill_rate: float


@dataclass
class TokenBucketState:
    tokens: float
    last_refill_ts: float


class TokenBucketLimiter(RateLimitStrategy):
    def __init__(self) -> None:
        self._configs: Dict[str, TokenBucketConfig] = {}
        self._states: Dict[str, TokenBucketState] = {}
        self._lock = threading.RLock()

    def configure_user(self, user_id: str, **config) -> None:
        capacity: float = config["capacity"]
        refill_rate: float = config["refill_rate"]
        now = time.time()
        with self._lock:
            self._configs[user_id] = TokenBucketConfig(
                capacity=capacity,
                refill_rate=refill_rate,
            )
            self._states[user_id] = TokenBucketState(tokens=capacity, last_refill_ts=now)

    def _refill(self, user_id: str, now: float) -> None:
        cfg = self._configs[user_id]
        state = self._states[user_id]

        if now <= state.last_refill_ts:
            return

        elapsed = now - state.last_refill_ts
        added = elapsed * cfg.refill_rate
        print("new token added: ", added)
        state.tokens = min(cfg.capacity, state.tokens + added)
        state.last_refill_ts = now
        self._states[user_id] = state

    def allow(self, user_id: str, now: Optional[float] = None) -> bool:
        if now is None:
            now = time.time()

        with self._lock:
            if user_id not in self._configs:
                raise KeyError(f"User {user_id} not configured for TokenBucketLimiter")

            if user_id not in self._states:
                cfg = self._configs[user_id]
                self._states[user_id] = TokenBucketState(tokens=cfg.capacity,
                                                         last_refill_ts=now)

            # invariant 3-step structure
            # Refill -> Check -> Consume
            # Step 1: Refill
            #   new_tokens = (now - last_refill_ts) * refill_rate
            #   tokens = min(capacity, tokens + new_tokens)
            #   last_refill_ts = now
            # Step 2 & 3: Check & Consume
            #   if tokens >= 1:
            #     tokens -= 1
            #     allow
            #   else:
            #     reject
            self._refill(user_id, now)
            state = self._states[user_id]

            print("token credit:", state.tokens)
            if state.tokens >= 1.0:
                state.tokens -= 1.0
                self._states[user_id] = state
                return True
            else:
                self._states[user_id] = state
                return False


# ==============================
# Thread-safe RateLimiter facade
# ==============================

class RateLimiter:
    def __init__(self) -> None:
        self._fixed_window = FixedWindowLimiter()
        self._sliding_window = SlidingWindowLimiter()
        self._token_bucket = TokenBucketLimiter()

        self._user_strategy: Dict[str, str] = {}
        # optional global lock for strategy mapping
        self._lock = threading.RLock()

    def configure_fixed_window(self, user_id: str, *, limit: int, window_size: float) -> None:
        with self._lock:
            self._fixed_window.configure_user(user_id, limit=limit, window_size=window_size)
            self._user_strategy[user_id] = "fixed_window"

    def configure_sliding_window(self, user_id: str, *, limit: int, window_size: float) -> None:
        with self._lock:
            self._sliding_window.configure_user(user_id, limit=limit, window_size=window_size)
            self._user_strategy[user_id] = "sliding_window"

    def configure_token_bucket(self, user_id: str, *, capacity: float, refill_rate: float) -> None:
        with self._lock:
            self._token_bucket.configure_user(user_id, capacity=capacity, refill_rate=refill_rate)
            self._user_strategy[user_id] = "token_bucket"

    def allow(self, user_id: str, now: Optional[float] = None) -> bool:
        # UNIVERSAL DESIGN PATTERN:
        # user_id → state
        # strategy(state, now) → allow | reject
        with self._lock:
            strategy_name = self._user_strategy.get(user_id)
        if strategy_name is None:
            raise KeyError(f"User {user_id} is not configured in RateLimiter")

        # Delegate to strategy; each strategy is internally locked
        if strategy_name == "fixed_window":
            return self._fixed_window.allow(user_id, now)
        elif strategy_name == "sliding_window":
            return self._sliding_window.allow(user_id, now)
        elif strategy_name == "token_bucket":
            return self._token_bucket.allow(user_id, now)
        else:
            raise ValueError(f"Unknown strategy {strategy_name!r} for user {user_id}")
        