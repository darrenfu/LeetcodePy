import logging

import os
from collections import OrderedDict
from enum import Enum
from typing import Any
import jsonpickle
import pickle
import time

from in_mem_cache.in_memory_cache import InMemoryCache

class FileFormat(Enum):
    JSON = 'json'
    PICKLE = 'pickle'

class DurableCache(InMemoryCache):
    """Durable cache that persists to disk"""
    def __init__(self,
                 capacity: int,
                 ttl: int,
                 snapshot_path: str = '/tmp/cache.json',
                 file_format: FileFormat = FileFormat.PICKLE,
                 write_through: bool=True,
                 enable_wal: bool=False,
                 wal_log_path: str = '/tmp/cache_wal.log'):
        super().__init__(capacity, ttl)
        self.enable_wal = enable_wal
        if enable_wal:
            self.wal_log_path = wal_log_path
            # 1) Rebuild in-memory state from WAL (if enabled)
            self._load_from_disk()
            # 2) Open WAL as append mode
            self._wal_log_file = open(self.wal_log_path, "a", buffering=1)
        else:
            self.snapshot_path = snapshot_path
            self.write_through = write_through
            self.file_format = file_format
            self._load_from_disk()

    # ============= WAL APIs =================
    def _log_set(self, key: str, value: Any) -> None:
        now = time.time()
        expire_at: int | None = None
        if self.ttl is not None:
            expire_at = int(now) + self.ttl
        expire_at_str = "None"
        if expire_at is not None:
            try:
                expire_at_str = str(expire_at)
            except ValueError:
                pass
        line = f"SET {key} {str(value)} {expire_at_str}\n"
        written = self._wal_log_file.write(line)
        self.logger.debug("[WAL] write() returned: %s", written)
        self.logger.debug("[WAL] file.tell() after write: %s", self._wal_log_file.tell())

    def _log_del(self, key) -> None:
        self._wal_log_file.write(f"DEL {key}\n")

    def _log_clear(self) -> None:
        self._wal_log_file.write("CLEAR\n")

    def _save_to_disk(self) -> None:
        if self.enable_wal:
            self.logger.debug("[WAL] flushing %s", self._wal_log_file.name)
            self._wal_log_file.flush()
            # forces the operating system to flush all buffered file data to the physical storage device (disk/SSD).
            os.fsync(self._wal_log_file.fileno())
            size = os.path.getsize(self._wal_log_file.name)
            self.logger.debug("[WAL] size on disk after fsync: %s", size)
            return

        tmp_path = f"{self.snapshot_path}.tmp"
        try:
            json_obj = {
                'cache': self.cache,
                'timestamps': self.timestamps
            }
            match self.file_format:
                case FileFormat.JSON:
                    serialized = jsonpickle.encode(json_obj, indent=2)
                    with open(tmp_path, 'w') as f:
                        f.write(serialized)
                case FileFormat.PICKLE:
                    with open(tmp_path, 'wb') as f:
                        pickle.dump(json_obj, f)
                case _:
                    raise ValueError(f"Unsupported file format: {self.file_format}")
            # MVCC
            os.replace(tmp_path, self.snapshot_path)
            print(f"Saved {len(self.cache)} items to disk")
        except Exception as e:
            print(f"Error saving to disk: {e}")

    def _evict_expired(self) -> None:
        total_serialized_keys = list(self.cache.keys())
        for key in total_serialized_keys:
            if self._is_expired(key):
                del self.cache[key]
                del self.timestamps[key]
        print(f"Evicted {len(total_serialized_keys) - len(self.cache)} expired items from cache")

    # WAL formats:
    #  SET key value expire_at
    #  DEL key
    #  CLEAR
    def _replay_wal_line(self, line: str, now: int):
        if not line:
            return
        parts = line.split(' ')
        op = parts[0]
        print(f"op: {op}")
        if op == "SET":
            if len(parts) < 4:
                return # malformed
            _, key, value, expire_at = parts
            expire_at_int: int | None = None
            if expire_at != "None":
                try:
                    expire_at_int = int(expire_at)
                except ValueError:
                    return
            if expire_at_int is not None and expire_at_int <= now:
                # Skip if it's already expired
                return
            # Replay SET() into in-memory cache
            super().set(key, value)
            # Reconstruct insertion timestamp
            if self.ttl is not None and expire_at_int is not None:
                self.timestamps[key] = expire_at_int - self.ttl
        elif op == "DEL":
            if len(parts) < 2:
                return
            _, key = parts
            super().delete(key)
        elif op == "CLEAR":
            super().clear()
        else:
            print(f"Unsupported op in WAL: {op}")

    def _load_from_disk(self) -> None:
        if self.enable_wal:
            if os.path.exists(self.wal_log_path):
                now = time.time()
                with open(self.wal_log_path, 'r') as f:
                    for line in f:
                        self._replay_wal_line(line.strip(), int(now))

                os.remove(self.wal_log_path)
            return

        if os.path.exists(self.snapshot_path):
            try:
                match self.file_format:
                    case FileFormat.JSON:
                        with open(self.snapshot_path, 'r') as f:
                            serialized = f.read()
                            json_obj = jsonpickle.decode(serialized)
                    case FileFormat.PICKLE:
                        with open(self.snapshot_path, 'rb') as f:
                            json_obj = pickle.load(f)
                    case _:
                        raise ValueError(f"Unsupported file format: {self.file_format}")

                self.cache = json_obj['cache']
                self.timestamps = json_obj['timestamps']
                # Remove expired entries
                self._evict_expired()
            except Exception as e:
                print(f"Error loading from disk: {e}")
                self.cache = OrderedDict()
                self.timestamps = {}

    def flush(self) -> None:
        self._save_to_disk()

    def clear(self) -> None:
        super().clear()
        if self.enable_wal:
            self._log_clear()
            return
        if self.write_through:
            if os.path.exists(self.snapshot_path):
                os.remove(self.snapshot_path)
            # Alternative:
            # from pathlib import Path
            # Path(self.path).unlink(missing_ok=True)

    def delete(self, key: str) -> bool:
        is_del = super().delete(key)
        if self.enable_wal:
            self._log_del(key)
        return is_del

    def set(self, key: str, value: Any) -> str | None:
        old_key = super().set(key, value)
        if self.enable_wal:
            self._log_set(key, value)
            return old_key
        if self.write_through:
            self._save_to_disk()
        return old_key


def main() -> None:
    cache = DurableCache(capacity=3, ttl=3)
    cache.set('1', 1)
    print(f"1 => {cache.get('1')}")

    cache.set('1', 11)
    print(f"1 => {cache.get('1')}")

    # Test disaster recovery
    print("Simulate cache crash ...")
    del cache
    cache = DurableCache(capacity=3, ttl=3, write_through=False)
    print(f"1 => {cache.get('1')}")

    # Test write behind
    cache.set('1', 111)
    cache.set('2', 2)
    print("Simulate cache crash without flush ...")
    del cache
    cache = DurableCache(capacity=3, ttl=3, write_through=False)
    print(f"1 => {cache.get('1')}")
    print(f"2 => {cache.get('2')}")
    # Test write behind with flush
    cache.set('1', 111)
    cache.set('2', 2)
    cache.flush()
    del cache
    cache = DurableCache(capacity=3, ttl=3, write_through=False)
    print(f"1 => {cache.get('1')}")
    print(f"2 => {cache.get('2')}")

    # WAL
    print("Replay WAL")
    cache = DurableCache(capacity=10, ttl=3, enable_wal=True)
    cache.set('1', 1)
    cache.set('2', 2)
    cache.delete('1')
    print(f"1 => {cache.get('1')}")
    cache.set('3', 3)
    cache.flush()
    print("Replay WAL")
    cache = DurableCache(capacity=10, ttl=3, enable_wal=True)
    print(f"1 => {cache.get('1')}")
    print(f"2 => {cache.get('2')}")
    cache.clear()
    cache.flush()
    print("Replay WAL")
    cache = DurableCache(capacity=10, ttl=3, enable_wal=True)
    print(f"1 => {cache.get('1')}")


if __name__ == "__main__":
    main()