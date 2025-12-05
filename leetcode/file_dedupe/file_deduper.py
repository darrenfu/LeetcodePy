import os
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Iterable, Tuple
import hashlib
import xxhash


class FileDeduper:
    def __init__(self, max_workers: int | None = None):
        # For I/O-bound workload, a few x CPU count is fine
        self.max_workers = max_workers or (os.cpu_count() or 4) * 4

    def _hash_file(self, path: str, chunk_size: int = 1024 * 1024, algo: str = 'sha256') -> Tuple[str, int, str]:
        """Compute SHA-256 hash of a single file, streaming in chunks.
        Returns (hexdigest, size_bytes, path).
        """
        hasher = hashlib.new(algo)
        total = 0
        # xxhash.xxh64()
        with open(path, 'rb') as f:
            while True:
                # disk I/O is much slower than CPU hashing
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                total += len(chunk)
                hasher.update(chunk)
        return hasher.hexdigest(), total, path

    def _group_by_size(self, paths: Iterable[str]) -> Dict[int, List[str]]:
        groups = defaultdict(list)
        for path in paths:
            try:
                filesize = os.path.getsize(path)
            except OSError:
                continue
            groups[filesize].append(path)
        return groups

    # Time C: O(n*m) where n = number of paths, m = avg path str length
    # Space C: O()
    # Dedup by content size first, then only compare content if sizes match (classic optimization).
    def find_duplicates(self, paths: Iterable[str]) -> List[List[str]]:
        # Stage 1: group by size
        size_groups = self._group_by_size(paths)

        # Stage 2: group by hash
        groups_by_sid = defaultdict(list)
        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            futures = {}
            for size, files in size_groups.items():
                if len(files) < 2: # No dups
                    continue
                for f in files:
                    fut = pool.submit(self._hash_file, f)
                    futures[fut] = f

            for fut in as_completed(futures):
                try:
                    digest, size, path = fut.result()
                except OSError:
                    continue
                sig = (size, digest)
                groups_by_sid[sig].append(path)

        return [group for group in groups_by_sid.values() if len(group) > 1]

if __name__ == "__main__":
    dups = FileDeduper().find_duplicates(['a.txt', 'b.txt', 'c.txt'])
    print(dups)

# followups:
# 1. Different dedupe criteria
# 	•	Dedup by (directory, filename) instead of content.
# 2.	Streaming / iterator-based API
# •	“What if the list of paths is too big to fit in memory?”
# •	How would you change the API so it can process lines as a stream (generator / file handle) instead of an in-memory list?
# 3.	Incremental dedupe
# •	How do you handle incremental updates? e.g. a daemon that sees new files and updates duplicates on the fly.

# Hashing & content comparison
#     •	Why/when use a hash?
#     •	What are the trade-offs between storing full content string vs storing a hash as key?
#     •	Memory vs CPU vs I/O discussion.
#     •	Hash collisions
#     •	“Is SHA-256 collision-free? What if a collision happens?”
#     •	How would you defensively handle collisions? (e.g. store hash → list of candidates; on collision, do byte-by-byte comparison.)
#     •	Hash performance
#     •	How does hashing cost scale with content size?
#     •	Would you still use SHA-256, or choose MD5 / xxHash / CRC for speed?
# SHA-256
# •	~300–500 MB/s
# •	Strong cryptographic safety
# •	Industry standard for dedupe
# Best for reliability
#
# MD5
# •	Faster than SHA-256
# •	Cryptographically broken (intentional collisions possible)
# 	•	An attacker can craft two different files with the same MD5
# 	•	This is a malicious collision
# Still OK for dedupe if source is trusted.
# Dedupe should never produce false positives.
# Crafted collision (due to algorithm weaknesses) vs accidental collision (due to chance)
#
# xxHash / xxHash3 (non-cryptographic hash)
# •	Extremely fast: 20–40 GB/s
# •	Non-cryptographic
# •	Great for large-file chunk hashing, Checksums, Lightweight fingerprinting
# Best for fast scanning, similar to CRC32
#
# CRC32 (checksum, not hash)
# •	Very fast (~10–20 GB/s)
# •	Very small collision space
# •	Good for quick-filter stage only
# Not suitable for final dedupe
# Designed for:
# 	•	Detecting accidental errors in transmission/storage
# 	•	Extremely fast hardware / polynomial arithmetic
# 	•	Protecting against bit rot, not adversarial tampering
# aka.
#   •	Detecting network corruption
#   •	Fast error checks in containers
#   •	Legacy systems

# Scaling up: “billions of files” / system design–style
# Now imagine we have billions of files across many machines. How would you design a system to find duplicates?
#     •	Multi-stage dedupe
#     1.	Stage 1: Group by file size.
#     2.	Stage 2: For each size group, compute a hash of file contents.
#     3.	Stage 3: For hash collisions, do byte-by-byte or chunk-by-chunk comparison.
#     •	Distributed / map-reduce
#     •	Use mappers to emit (hash, filepath) pairs.
#     •	Reducers aggregate duplicates per hash.
#     •	What’s the key choice for map-reduce jobs? (size, hash, etc.)
#     •	Storage systems
#     •	How would you do this if files live in S3 / HDFS / NFS rather than local disk?
#     •	How do you minimize data transfer over the network?
#     •	Online / near-real-time
#     •	Design a service that:
#     •	On each file write, computes hash and checks for existing duplicates.
#         •	Maintains an index of hash → canonical_file & duplicates.
#     •	How to handle concurrent writes and eventual consistency?
#     •	Fault tolerance
#     •	What if a worker crashes mid-scan?
#     •	How do you avoid double counting or missing some files?

# Memory & performance trade-off follow-ups
# More detailed technical pokes:
# 	•	If contents are huge, could you:
# 	•	Store hashes only in memory and spill metadata to disk?
# 	•	Use chunked hashing (rolling hash or content-defined chunks) to avoid reading whole files into RAM?
# 	•	Incremental reading
# 	•	Instead of reading entire file into a string, read in chunks (e.g. 4KB) and update hash.
# 	•	What’s the pattern for this in Python (iter(lambda: f.read(4096), b""))?
# 	•	Back-of-the-envelope estimates
# 	•	If you have 100M files and each hash entry is ~64 bytes hash + path overhead, how much memory do you need roughly?
# 	•	Could you shard by hash prefix (e.g. first 4 bytes) to distribute across servers?

# Answers:
# Chunk size affects syscall overhead, cache behavior, and I/O throughput.
# For file scanning and hashing, I typically choose 1MB chunks because they align well with SSD prefetch and deliver high sequential throughput.
# Hash algorithm depends on goals: for pure dedupe xxHash64 is extremely fast; for integrity SHA-256 is safer.
# To determine if the system is I/O-bound or CPU-bound, I measure read time vs hash time. If read dominates, it’s I/O-bound; if hash dominates, it’s CPU-bound. I also check iostat for disk utilization and system CPU wait time.
# I/O throughput can be measured by reading the file with dd or a Python loop and dividing size by time. This gives an accurate sense of disk sequential read performance.