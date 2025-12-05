from __future__ import annotations
from contextlib import contextmanager
from threading import Condition, Lock


class RWLock:
    """
    Reader–writer lock with writer preference:

    - Multiple readers can hold the lock simultaneously.
    - Writers get exclusive access.
    - New readers wait if there is a waiting writer (prevents writer starvation).
    """

    def __init__(self) -> None:
        self._lock = Lock()
        self._cond = Condition(self._lock)
        self._readers = 0
        self._writer = False
        self._write_requests = 0

    # --- low level API ---

    def acquire_read(self) -> None:
        with self._cond:
            # Block if a writer is active or writers are waiting
            while self._writer or self._write_requests > 0:
                self._cond.wait()
            self._readers += 1

    def release_read(self) -> None:
        with self._cond:
            self._readers -= 1
            if self._readers == 0:
                # wake up writers
                self._cond.notify_all()

    def acquire_write(self) -> None:
        with self._cond:
            self._write_requests += 1
            # Wait while a writer is active or readers are present
            while self._writer or self._readers > 0:
                self._cond.wait()
            self._write_requests -= 1
            self._writer = True

    def release_write(self) -> None:
        with self._cond:
            self._writer = False
            # wake up readers and writers
            self._cond.notify_all()

    # --- nice context-manager API ---

    @contextmanager
    def read_lock(self):
        self.acquire_read()
        try:
            yield
        finally:
            self.release_read()

    @contextmanager
    def write_lock(self):
        self.acquire_write()
        try:
            yield
        finally:
            self.release_write()