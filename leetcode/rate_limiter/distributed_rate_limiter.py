import time
from typing import Optional

import redis  # pip install redis


class RedisTokenBucketLimiter:
    """
    Distributed token bucket using Redis + Lua script for atomicity.
    """
    LUA_SCRIPT = """
    -- KEYS[1] is the Redis key for the user’s bucket, e.g. rate:token_bucket:user123
    -- ARGV[1] = capacity    → max number of tokens in bucket
    -- ARGV[2] = refill_rate → tokens added per second
    -- ARGV[3] = now         → current time (float seconds)
    -- Return: 1 if allowed, 0 if rejected

    local key = KEYS[1]
    local capacity = tonumber(ARGV[1])
    local refill_rate = tonumber(ARGV[2])
    local now = tonumber(ARGV[3])

    -- read existing state
    local data = redis.call("HMGET", key, "tokens", "last_refill_ts")
    -- remaining tokens (float)
    local tokens = tonumber(data[1])
    -- last time refill was applied
    local last_refill_ts = tonumber(data[2])

    if tokens == nil or last_refill_ts == nil then
        -- initialize with full bucket
        tokens = capacity
        last_refill_ts = now
    end

    -- refill
    if now > last_refill_ts then
        local elapsed = now - last_refill_ts
        local added = elapsed * refill_rate
        tokens = math.min(capacity, tokens + added)
        last_refill_ts = now
    end

    local allowed = 0
    if tokens >= 1.0 then
        tokens = tokens - 1.0
        allowed = 1
    end

    -- persist state
    -- https://redis.io/docs/latest/commands/hset/
    -- Usage: HSET key field value [field value ...]
    redis.call("HSET", key,
               "tokens", tokens,
               "last_refill_ts", last_refill_ts)

    -- optional: set TTL to auto-expire inactive users
    redis.call("EXPIRE", key, 3600)

    return allowed
    """

    def __init__(self, redis_client: redis.Redis, prefix: str = "rate:token_bucket") -> None:
        self._r = redis_client
        self._prefix = prefix
        # load script once to get a SHA
        self._script = self._r.register_script(self.LUA_SCRIPT)

    def _key(self, user_id: str) -> str:
        return f"{self._prefix}:{user_id}"

    def allow(
            self,
            user_id: str,
            *,
            capacity: float,
            refill_rate: float,
            now: Optional[float] = None,
    ) -> bool:
        """
        Token bucket for a specific user_id.
        `capacity` and `refill_rate` can be constant or per-user, your choice.
        """
        if now is None:
            now = time.time()

        key = self._key(user_id)
        # invoke Lua: KEYS = [key], ARGV = [capacity, refill_rate, now]
        allowed = self._script(
            keys=[key],
            args=[str(capacity), str(refill_rate), f"{now:.6f}"],
        )
        # redis-py returns int-like
        return bool(int(allowed))

if __name__ == "__main__":
    r = redis.Redis(host="localhost", port=6379, db=0)

    limiter = RedisTokenBucketLimiter(r)

    user_id = "userC"
    capacity = 10.0       # max burst
    refill_rate = 1.0     # 1 token / second

    print("Burst test:")
    for i in range(12):
        allowed = limiter.allow(user_id, capacity=capacity, refill_rate=refill_rate)
        print(f"request {i} -> allowed={allowed}")

    print("After waiting 3 seconds...")
    time.sleep(3)
    for i in range(5):
        allowed = limiter.allow(user_id, capacity=capacity, refill_rate=refill_rate)
        print(f"request {i} -> allowed={allowed}")
