import time
from typing import Optional

import redis

from rate_limiter import RateLimitStrategy
from distributed_rate_limiter import RedisTokenBucketLimiter


class RedisTokenBucketStrategy(RateLimitStrategy):
    def __init__(self, redis_client, prefix="rate:token_bucket"):
        self._impl = RedisTokenBucketLimiter(redis_client, prefix)
        # store per-user configs
        self._configs = {}

    def configure_user(self, user_id: str, **config) -> None:
        capacity: float = config["capacity"]
        refill_rate: float = config["refill_rate"]
        self._configs[user_id] = (capacity, refill_rate)

    def allow(self, user_id: str, now: Optional[float] = None) -> bool:
        if user_id not in self._configs:
            raise KeyError(f"user {user_id} not configured")
        capacity, refill_rate = self._configs[user_id]
        return self._impl.allow(user_id, capacity=capacity, refill_rate=refill_rate, now=now)

def main():
    # Connect to local Redis
    r = redis.Redis(host="localhost", port=6379, db=0)

    # Use a fresh prefix so tests/examples don't collide with your other keys
    limiter = RedisTokenBucketStrategy(redis_client=r, prefix="example:token_bucket")

    user_id = "user_redis"
    limiter.configure_user(user_id, capacity=5.0, refill_rate=1.0)

    base = time.time()

    print("Burst at t=0:")
    for i in range(7):
        allowed = limiter.allow(user_id, now=base)
        print(f"  request {i} -> allowed={allowed}")

    print("\nWait 3s and try again:")
    # t2 = base + 3
    time.sleep(3)
    t2 = time.time()
    for i in range(5):
        allowed = limiter.allow(user_id, now=t2)
        print(f"  t=+3s request {i} -> allowed={allowed}")


if __name__ == "__main__":
    main()