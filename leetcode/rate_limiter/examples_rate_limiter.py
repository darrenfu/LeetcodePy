# examples_rate_limiter.py
import time
from rate_limiter import RateLimiter


def demo_fixed_window():
    print("== Fixed window: limit=3 per 10s ==")
    rl = RateLimiter()
    rl.configure_fixed_window("user_fixed", limit=3, window_size=10.0)

    base = time.time()
    for i in range(5):
        allowed = rl.allow("user_fixed", now=base + i)
        print(f"t={i:2d}s -> allowed={allowed}")


def demo_sliding_window():
    print("\n== Sliding window: limit=3 per 10s ==")
    rl = RateLimiter()
    rl.configure_sliding_window("user_sliding", limit=3, window_size=10.0)

    base = time.time()
    # 4 rapid requests; the 4th should be blocked
    for i in range(4):
        allowed = rl.allow("user_sliding", now=base + i)
        print(f"t={i:2d}s -> allowed={allowed}")

    # jump ahead beyond window – should allow again
    allowed = rl.allow("user_sliding", now=base + 20)
    print(f"t=20s -> allowed={allowed}")


def demo_token_bucket():
    print("\n== Token bucket: capacity=5, refill_rate=1 token/s ==")
    rl = RateLimiter()
    rl.configure_token_bucket("user_bucket", capacity=5.0, refill_rate=1.0)

    base = time.time()

    print("Burst at t=0:")
    for i in range(7):
        allowed = rl.allow("user_bucket", now=base)
        print(f"  request {i} -> allowed={allowed}")

    print("\nWait 3s and try again:")
    t2 = base + 3
    for i in range(5):
        allowed = rl.allow("user_bucket", now=t2)
        print(f"  t=+3s request {i} -> allowed={allowed}")


if __name__ == "__main__":
    demo_fixed_window()
    demo_sliding_window()
    demo_token_bucket()