from __future__ import annotations

import time
from dataclasses import dataclass
from threading import Thread
from queue import Queue
from collections import deque
from typing import Deque, Dict, Optional, Tuple, Any


@dataclass
class SlidingWindowConfig:
    limit: int          # max requests in window
    window_size: float  # window length in seconds


class SlidingWindowActorLimiter:
    """
    Sliding-window rate limiter using an actor model.

    - All mutable state (_configs, _events) is owned by a single worker thread.
    - Public methods (configure_user, allow) communicate with the worker
      via a Queue and wait for a response.
    - No locks needed; all internal state is mutated single-threaded in _run().
    """

    def __init__(self) -> None:
        # Actor-owned state (only touched in _run thread)
        self._configs: Dict[str, SlidingWindowConfig] = {}
        self._events: Dict[str, Deque[float]] = {}

        # Message queue: main thread(s) → actor thread
        self._mailbox: Queue[Tuple[str, Any]] = Queue()

        # Start the actor thread
        self._running = True
        self._thread = Thread(target=self._run, daemon=True)
        self._thread.start()

    # ---------- Public API (threadsafe because it only uses Queues) ----------

    def configure_user(self, user_id: str, *, limit: int, window_size: float) -> None:
        """
        Synchronous call: send a config message to the actor and wait for ack.
        """
        response_q: Queue[Optional[Exception]] = Queue(maxsize=1)
        self._mailbox.put((
            "config",
            user_id,
            limit,
            window_size,
            response_q,
        ))
        err = response_q.get()
        if err is not None:
            raise err

    def allow(self, user_id: str, now: Optional[float] = None) -> bool:
        """
        Synchronous call: send an allow request and wait for boolean result.
        """
        if now is None:
            now = time.time()

        response_q: Queue[Tuple[Optional[Exception], Optional[bool]]] = Queue(maxsize=1)
        self._mailbox.put((
            "allow",
            user_id,
            float(now),
            response_q,
        ))
        err, result = response_q.get()
        if err is not None:
            raise err
        # result should never be None if no error
        return bool(result)

    def stop(self) -> None:
        """
        Gracefully stop the actor thread.
        """
        if not self._running:
            return
        self._running = False
        self._mailbox.put(("stop",))  # simple stop message
        self._thread.join(timeout=1.0)

    # ---------- Actor loop (single-threaded state mutation) ----------

    def _run(self) -> None:
        """
        Actor event loop. Runs in a dedicated thread.
        Processes messages one by one, mutating internal state safely.
        """
        while self._running:
            msg = self._mailbox.get()
            if not msg:
                continue

            msg_type = msg[0]

            if msg_type == "stop":
                break

            if msg_type == "config":
                # Unpack
                _, user_id, limit, window_size, response_q = msg
                try:
                    self._handle_config(user_id, int(limit), float(window_size))
                    response_q.put(None)  # no error
                except Exception as e:
                    response_q.put(e)

            elif msg_type == "allow":
                _, user_id, now, response_q = msg
                try:
                    allowed = self._handle_allow(user_id, float(now))
                    response_q.put((None, allowed))
                except Exception as e:
                    response_q.put((e, None))

            # else: ignore unknown message types

    # ---------- Internal logic (only called in actor thread) ----------

    def _handle_config(self, user_id: str, limit: int, window_size: float) -> None:
        """
        Configure or reconfigure a user. Internal, single-threaded.
        """
        self._configs[user_id] = SlidingWindowConfig(limit=limit,
                                                     window_size=window_size)
        # reset their event history
        self._events[user_id] = deque()

    def _handle_allow(self, user_id: str, now: float) -> bool:
        """
        Core sliding window logic, executed only in the actor thread.
        """
        if user_id not in self._configs:
            raise KeyError(f"User {user_id} not configured for SlidingWindowActorLimiter")

        cfg = self._configs[user_id]
        q = self._events.setdefault(user_id, deque())

        # Sliding window core:
        # 1. Drop expired timestamps
        cutoff = now - cfg.window_size
        while q and q[0] <= cutoff:
            q.popleft()

        # 2. Check count in window
        if len(q) < cfg.limit:
            q.append(now)
            return True
        else:
            return False


# ---------- Example usage ----------

if __name__ == "__main__":
    limiter = SlidingWindowActorLimiter()

    try:
        limiter.configure_user("userA", limit=3, window_size=10.0)

        base = time.time()
        print("SlidingWindowActorLimiter demo:")
        for i in range(5):
            t = base + i
            allowed = limiter.allow("userA", now=t)
            print(f"t={i:2d}s -> allowed={allowed}")
        # After 10s, old events drop out of window
        t = base + 15
        allowed = limiter.allow("userA", now=t)
        print(f"t=15s -> allowed={allowed} (should be True, new window)")
    finally:
        limiter.stop()