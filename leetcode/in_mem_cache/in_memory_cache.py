import time
import logging
from collections import OrderedDict
from typing import Dict, Any


class InMemoryCache:
    """Basic LRU cache with TTL support"""

    def __init__(self, capacity: int, ttl: int | None = None):
        logging.basicConfig(
            level=logging.DEBUG,
        )
        self.logger = logging.getLogger(__name__)
        self.capacity = capacity
        self.ttl = ttl # in seconds
        self.cache: OrderedDict = OrderedDict()
        self.timestamps: Dict[str, float] = {}
        self.hits = 0
        self.misses = 0

    def _is_expired(self, key: str) -> bool:
        """Check if the cache entry has expired."""
        if not self.ttl:
            return False
        if key not in self.cache:
            return True
        return time.time() - self.timestamps[key] > self.ttl

    def get(self, key: str) -> Any | None:
        if key not in self.cache:
            self.misses += 1
            return None
        if self._is_expired(key):
            # Evict expired item
            del self.cache[key]
            del self.timestamps[key]
            self.misses += 1
            return None
        # Mark as most recent used
        self.cache.move_to_end(key)
        self.hits += 1
        return self.cache[key]

    def set(self, key: str, value: Any) -> str | None:
        if key in self.cache:
            # Update existing entry
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            # Evict least used item
            old_key, _ = self.cache.popitem(last=False)
            del self.timestamps[old_key]
            return old_key
        # Add a new entry
        self.cache[key] = value
        self.timestamps[key] = time.time()
        return None

    def delete(self, key: str) -> bool:
        has_key: bool = key in self.cache
        if has_key:
            self.logger.debug(f"delete {key}")
            del self.cache[key]
            del self.timestamps[key]
        return has_key

    def clear(self) -> None:
        """Clear all cache entries"""
        self.cache.clear()
        self.timestamps.clear()
        self.hits = 0
        self.misses = 0

    def stats(self) -> Dict[str, Any]:
        hit_rate: float = self.hits / (self.hits + self.misses) if (self.hits + self.misses) > 0 else 0
        return {
            'hit_rate': hit_rate,
            'hits': self.hits,
            'missed': self.misses,
            'size': len(self.cache),
            'capacity': self.capacity
        }


def main() -> None:
    cache = InMemoryCache(capacity=3, ttl=3)
    # Test expiry case
    cache.set('1', 1)
    time.sleep(3)
    print(f"1 => {cache.get('1')}")
    print(f"stats: {cache.stats()}")

    cache.set('1', 1)
    cache.set('2', 2)
    cache.set('3', 3)
    # Happy path
    print(f"3 => {cache.get('3')}")
    print(f"stats: {cache.stats()}")

    # Test out of capacity case
    cache.set('4', 4)
    print(f"1 => {cache.get('1')}")
    print(f"stats: {cache.stats()}")

    # Test update existing entry case
    cache.set('2', 22)
    # Test lease used entry evicted case: 2 updated (hit), thus 3 becomes least used -> evicted
    cache.set('5', 5)
    print(f"2 => {cache.get('2')}")
    print(f"3 => {cache.get('3')}")
    print(f"4 => {cache.get('4')}")
    print(f"stats: {cache.stats()}")

    # Test lease used entry evicted case again: hit 2 and 4, thus 5 becomes least used -> evicted
    cache.set('6', 6)
    print(f"5 => {cache.get('5')}")
    print(f"stats: {cache.stats()}")


if __name__ == "__main__":
    main()
