# Merkle tree interview session summary

Dates: October 10–11, 2026 (UTC).
Problem: https://prachub.com/interview-questions/build-a-merkle-tree-over-a-directory-with-hash-lookup-and-tree-diff

## Archive contents and status

- merkle_tree.py: complete baseline build/get_hash/diff implementation.
- test_merkle_tree.py: seven passing baseline tests.
- prachub-answer.md: full submission draft, implementation, tests, complexity, and follow-ups.
- merkle_index.py: implemented directory hash index with configurable fanout and incremental existing-file edits.
- test_merkle_index.py: seven passing indexed-tree tests.
- merkle_index_usage.md: usage, assumptions, limitations, and fanout tuning.
- merkle_trie_delta.md: latest canonical-trie code delta discussed in chat; an integration draft, not a tested standalone module.
- session-summary.md: this consolidated record of decisions, questions, explanations, and remaining work.
- archive-manifest.json: file sizes and SHA-256 checksums.
- merkle-session-archive.zip: downloadable copy of all the above.

The 14 implemented-code tests were rerun successfully when archiving. This is a summary, not a verbatim conversation export. The original discussion's latest trie snippets are preserved in the delta document. Local generated caches are excluded.

## Interview scope and clarifications

Implement Python build(path), get_hash(path, tree), and diff(tree_a, tree_b) against a real filesystem. The original exercise allows 60 minutes and requires self-written tests. We conducted the interview step by step, then completed code on request.

Interview assumptions supplied during the discussion: at most 100,000 entries, depth at most 100, files potentially larger than memory, SHA-256 hex digests, negligible collisions. Listing order must not affect hashes. Root name and absolute location must not affect equality.

build returns an N-ary Inode tree. get_hash accepts root-relative POSIX paths; '.'/empty denotes root; a missing path raises KeyError, and absolute paths or '..' raise ValueError. diff returns sorted (relative_path, status) tuples from A to B, with added/removed/modified statuses. Report entire added or removed directories once; do not separately report their descendants. File-to-directory or directory-to-file replacement at the same path is modified. Ancestors are not reported merely because descendant hashes change.

Hidden files and empty directories are included. Metadata such as permissions and modification times is excluded. Symlinks and special entries are rejected, not silently ignored; read errors propagate. All implementations assume stable filesystem data during reads, not an atomic snapshot.

## Baseline design and reasoning

Each filesystem node holds name, type, content hash, and children. Files hash a fixed type prefix plus content. Directories hash a different type prefix plus canonical JSON records of sorted immediate children: name, type, hash. Post-order traversal computes and retains every directory hash.

Names belong in their parent's encoding. Identical file content under different names can have identical file hashes; different directory entry names change the parent's hash. A root's own name is excluded. Files with the same overall content set but assigned to different paths must not produce the same directory hash. Separate aggregated name/content streams can lose their association; keep each name paired with its entry hash.

Spaces and newline bytes are valid filename characters, so an 'invisible delimiter' is not inherently safe. Structured serialization (for example a precisely specified Thrift protocol/schema) or deterministic JSON gives unambiguous boundaries. JSON ensure_ascii=True escapes non-ASCII characters, allowing encode('ascii'); consistently using UTF-8 is another choice. Type prefixes separate file and directory hash inputs. The null byte after a fixed label is conventional, not required to be absent from file contents.

SHA-256 output is always 32 bytes or 64 hexadecimal characters, regardless of file size. Stream large files in chunks into one hasher; successive update calls equal hashing concatenated bytes. No temporary file is needed to store the digest. Combining two SHA-256 values can hash their concatenated raw 32-byte digests; order matters unless explicitly sorted. Hashes are one-way: lookup walks retained node objects, not decoding or deserializing the digest, and must not call visit() to reread disk.

## Diff algorithm and edge cases

Use BFS with matched node pairs at the same relative path. Check type replacement, then equality of cached hashes. Equal hashes prune the entire subtree. Unequal file hashes imply modified files. Unequal directories require matching immediate children by name, reporting unmatched names, and queueing matched entries.

Sorted lists cannot simply be compared by position: A=[b,c], B=[a,b,c] should report only a added if matching contents are equal. A two-pointer merge advances the lexically smaller side: A smaller means removed, B smaller means added, equal means compare matched entries. Report remaining tail entries. Partitioning by type before name loses file/directory replacement semantics. Dictionaries make name matching straightforward; keys union (|) includes every name once, and sorted() gives a stable processing order.

Example: only src/utils/helpers.py changes. Compare root and children along src/utils/helpers.py; compare siblings' stored hashes but do not descend beneath matching siblings. helpers.py is an arbitrary example filename; its application purpose is irrelevant. Ancestor hashes change, but diff reports only the modified file.

Equal-subtree example: assets/logo.png and assets/icons/home.svg match between snapshots while src/main.py differs. Compare assets once, then skip its descendants. An empty diff alone does not prove pruning; tests can make equal-subtree children raise when traversed.

## Tests and baseline complexity

Tests cover deterministic builds despite creation order/root name differences; Unicode, space, and newline filenames; empty files/directories; root/nested lookup; missing/invalid paths; lookup remaining a snapshot after disk edits; added/removed files/directories; root/nested edits; replacements both directions; renames; multi-chunk files; symlink rejection; changed hashes only along ancestors; and direct verification of pruning.

Build: total file bytes plus node/filename encoding work and per-directory sorting. List-based lookup scans children at each path component; dictionary children yield expected O(path depth), aside from string handling. Equal-root diff is O(1). Otherwise diff examines child entries of differing directories, including unchanged siblings, plus sorting and output costs. Diff is not generally O(number of changed files).

## Industry context and production enhancements

Merkle trees summarize data with hashes: leaves represent data, parents represent children, root fingerprints the collection. Uses include integrity checks against a trusted root, efficient synchronization, and membership proofs in suitable tree layouts. Examples discussed were Git's Merkle-like object graph, blockchain transaction trees, and Cassandra replica synchronization. Hash consistency does not authenticate an author; signatures or another trusted mechanism are needed.

Production choices include incremental rehashing, chunk-level file hashing, persistent content-addressed storage, deduplication, versioned canonical encodings, distributed/batched comparison, parallel builds, cache invalidation, and explicit filesystem/snapshot policies. These are enhancements rather than baseline correctness requirements.

## Incremental-update checkpoints

1. Receive a reliable event identifying the changed relative path; missed events require reconciliation.
2. Locate its filesystem node by path; dictionary children or a path index avoid whole-tree search.
3. Rehash the changed file. Version/stale fields alone do not update content hashes.
4. Follow filesystem parent pointers and recompute ancestors.
5. A flat directory encoding still rehashes all its immediate child records. Wide directories need a second, virtual hash index.
6. Retain virtual index nodes and parent links so only affected index branches change.
7. Retain old snapshots separately or use copy-on-write if historical comparisons are required. Our updater mutates its snapshot.
8. Distinguish content changes from insertions/deletions/renames. Sorted grouping does not make all operations logarithmic.
9. Verify updates equal fresh rebuilds and count rehashed groups to test efficiency.

## Balanced virtual index and fanout

M is the count of immediate filesystem entries in one directory. Index leaves represent these entries, whether files or directories. Intermediate virtual nodes are bookkeeping, not filesystem directories. A directory inode retains the resulting index root hash.

With fanout b=16 and M=4096:

4096 entry leaves -> 256 group hashes -> 16 group hashes -> 1 root hash.

One content edit changes one branch: three virtual ancestors, hashing up to 16 child hashes each. Retained index storage is O(M), not O(log M). Level count is ceil(log_b M): after h groupings, M/b^h reaches 1. It is a logarithm with base b, not log_b multiplied by M. Work per directory update is O(b log_b M), because each affected level reads up to b child hashes. Fixed b permits O(log M) notation; this excludes file reads and other filesystem ancestors. For M=1 there are no virtual grouping ancestors, only entry/directory wrappers.

Fanout tuning: larger b reduces height and internal-node count but increases per-node hashing. Benchmark representative directory widths and event workloads at b=2,4,8,16,32,64; measure update latency including tails, build time, memory, and bytes hashed. For disk-backed storage, fit encoded references into pages and measure page I/O. Binary digests are more compact than hexadecimal JSON. Powers of two are optional. A format/fanout change alters hashes and needs rebuild/replica coordination.

Our implemented index is deterministic sorted chunking with retained groups, dictionary filesystem children, and filesystem/virtual parent links. update_file rereads one existing file and propagates cached hashes. Unchanged content returns early. Different index fanouts are rejected by diff. Current diff still matches filesystem child dictionaries rather than exploiting virtual-index traversal.

Seven indexed tests cover several fanouts and partial group boundaries, deterministic builds, empty directories, no-op updates, unsupported type/symlink updates, membership diff, fanout validation, and a 4096-entry fixture. That fixture proves exactly three group hashes are recomputed and the root matches a fresh build.

## Shift problem and alternatives

Deterministic sorted chunking: sort records, form consecutive groups of b, repeatedly hash groups. Deleting the first entry can shift all boundaries. For b=2, [a,b][c,d][e,f] becomes [b,c][d,e][f], potentially O(M) rebuild work. The logarithmic guarantee applies only to content edits with unchanged membership. Our indexed implementation rebuilds on membership changes.

Merkle B+ trees permit partially filled nodes, avoiding obligatory repacking. Deleting from [a,b,c,d] can leave [b,c,d] while neighboring leaves stay unchanged. Underflow may borrow/merge; insertion may split. Changes remain local to neighbors and ancestor paths. However ordinary B+ tree shape depends on update history, so identical data does not necessarily yield identical root hashes without additional canonical layout rules.

Canonical Merkle tries route by key bytes or a hash of the key, never sorted-list position. Direct filename routing lets names sharing a prefix follow the same logical branch. Hash routing distributes names and avoids prefix hotspots, but common textual prefixes generally do not share a hash prefix. Stable routing needs fixed encoding, fixed bits consumed per step, deterministic child order and serialization, explicit key endings (for variable-length keys), and canonical empty/compression rules. Physical compressed nodes may change while logical routes stay fixed.

The latest delta uses SHA256(encoded filename).hexdigest(): 64 hexadecimal digits, fanout 16, a fixed-depth uncompressed trie. Terminal values hash [name,type,content hash]. Distinct entry/trie/directory prefixes prevent input ambiguity. Empty branches prune on deletion without moving other routes. The bound is a fixed 64 route steps, not log_b M. Memory can be substantial; path compression is a production enhancement. Hash collisions are assumed negligible. See merkle_trie_delta.md for archived snippets and integration boundaries.

## Publishing/account status

A complete PracHub answer was prepared locally. Posting was requested using the user's Google SSO account; no browser/PracHub authenticated session was available to the assistant. The user reported logging in, but connected-session discovery still found no accessible session. No PracHub submission was performed or verified by the assistant. This archive is a Google Drive save, not evidence of publishing to PracHub.

## Remaining work

- Integrate and test the canonical trie draft as a standalone implementation if desired.
- Implement filesystem membership-change APIs, updating both child containers and trie indexes, and propagate ancestors.
- Choose snapshot/event-consistency policies and persistence/copy-on-write behavior for production.
- Consider path compression and index-aware diff after profiling.
