from typing import Any, List
from sortedcontainers import SortedList
from pygtrie import CharTrie
from in_mem_cache.in_memory_cache import InMemoryCache

class ScanableCache(InMemoryCache):
    def __init__(self, capacity: int, ttl: int, use_trie: bool = False):
        super().__init__(capacity, ttl)
        self.use_trie = use_trie
        self.sorted_key_index = SortedList()
        self.trie = CharTrie()

    def set(self, key: str, value: Any) -> None:
        old_key = super().set(key, value)
        if old_key:
            if self.use_trie:
                del self.trie[old_key]
            else:
                # Time: O(logN)
                self.sorted_key_index.remove(old_key)
        if self.use_trie:
            self.trie[key] = True
        else:
            # Time: O(logN)
            self.sorted_key_index.add(key)

    def scan(self, prefix: str | None = None, limit: int | None = None) -> List[str]:
        if prefix is None:
            if limit is None:
                return list(self.cache.keys())
            return list(self.cache.keys())[:limit]

        if self.use_trie:
            if limit:
                return list(self.trie.iterkeys(prefix))[:limit]
            return [k for k in self.trie.iterkeys(prefix)]

        idx_start = self.sorted_key_index.bisect_left(prefix)
        i = idx_start
        idx_end = prefix + chr(0x10FFFF) # "next" prefix upper bound, 0x10FFFF is the highest legal Unicode scalar
        res = []
        while i < len(self.sorted_key_index) and self.sorted_key_index[i] < idx_end:
            k = self.sorted_key_index[i]
            res.append(k)
            if limit and i - idx_start >= limit:
                break
            i += 1
        return res


def main() -> None:
    cache = ScanableCache(capacity=10, ttl=1000, use_trie=True)
    # Happy path
    cache.set('a', 1)
    cache.set('b', 1)
    cache.set('ab', 1)
    cache.set('abc', 1)
    cache.set('abb', 1)
    cache.set('abcd', 1)
    cache.set('aba', 1)
    cache.set('d', 1)

    print(f"full scan, limit 3: => {cache.scan(limit=3)}")
    print(f"full scan, limit 10: => {cache.scan(limit=10)}")
    print(f"full scan, no limit: => {cache.scan()}")

    print(f"prefix: a, limit 3: => {cache.scan('a', limit=3)}")
    print(f"prefix: ab => {cache.scan('ab')}")


if __name__ == "__main__":
    main()

## Next followups
# Follow-up 3.1 — Support TTL Expiration + Background Cleanup
#  	•	Min-heap keyed by expire_at
# 	•	Background thread / scheduler scan
# 	•	event-driven tick（by Redis)
#    	•	Lazy expiration (on get, already implemented)
#   	•	Eager expiration (background)
# How to prevent double delete (heap stale entries), requiring lazy deletion + version check
#
# Follow-up 3.2 — Support Filtering SCAN with Field Filters
# SCAN_BY_FILTER(field=value), e.g. SCAN WHERE age > 18 AND name startswith 'A'
# involves: secondary index, inverted index, bitmap index, storage layout tradeoff (row-store vs column-store)
#
# Follow-up 3.3 — Pagination / Cursor-based SCAN
# E.g. SCAN cursor=xyz MATCH prefix LIMIT 50
# Involves: snapshot view, modification during scan, cusor = index/id
#
# Follow-up 3.4 — Sorting, Ordering, or Composite Keys
# Follow-up 4.1 — Support Concurrency + Multi-thread Correctness
# Option A — coarse lock
# Option B - per-key shard locks
# Option C - reader-writer locks
# Option D - lock-free index (skiplist)
#
# Follow-up 4.2 — Support WAL + Recovery
#  Design WAL format
#  Crash recovery: replay WAL, drop corrupted tail, fsync correctness
#  How to avoid WAL growing too quickly? --> Log compaction, snapshots / checkpoints
#
# Follow-up 4.3 — Memory Management + Eviction
#  LRU, LFU, TTL / size-based eviction
#  When key has many versions (time travel), how to avoid OOM?
#   Bound entries per key
#   Periodic compaction (keep last N versions)
#   Hierarchical storage (cold versions to disk)
#
# Follow-up 4.4 — Distributed Sharding
# 	•	Consistent hashing
# 	•	Replica placement
# 	•	Leader/follower vs leaderless
# 	•	Vector clocks or Lamport timestamps for conflict resolution
#
# Follow-up 4.5 — Strong vs Eventual Consistency
#  When multiple replica set the same key at the same time, how to resolve conflict?
#   last-write-win (timestamp based)
#   CRDT (if complex data structures)
#   per-shard authoritative leader
#
# Follow-up 4.6 — TTL correctness in distributed environment
# Challenge：
# 	•	clock skew
# 	•	logical time vs real time
# 	•	expiration propagation