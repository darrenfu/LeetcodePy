# Indexed directory Merkle tree

```python
from pathlib import Path
from merkle_index import MerkleTree

service = MerkleTree(fanout=16)
tree = service.build('/path/to/directory')
before = tree.content
Path('/path/to/directory/src/main.py').write_text('new contents')
after = service.update_file('src/main.py', tree)
assert after == service.build('/path/to/directory').content
```

The supplied tree is mutated by update_file. Keep a separately built tree if
you need a historical snapshot to diff. Only the notified file's contents may
have changed; additions, removals, renames, and type changes require build().
The filesystem must stay stable while it is read. Symlinks are rejected.

Each directory has a dictionary of its filesystem children, a virtual hash
index, and parent links. Sorted entry leaves are grouped into fanout-sized
chunks, repeatedly, until one index root remains. Empty directories use an
explicit empty group. Entry, group, directory, and file hashes have distinct
type prefixes. The directory hash includes fanout, so compatible comparisons
require the same fanout. Internal nodes are retained to reuse cached hashes.

For M entries and fanout b, updating an existing entry hashes approximately
ceil(log_b M) virtual groups, each containing up to b cached hashes. It also
hashes the changed entry record and the directory wrapper. Repeat this along
the filesystem ancestor path. File hashing still reads the whole changed file.
The index uses O(M) storage, not O(log M). Lookup uses expected constant-time
dictionary access per path component. Diff currently compares filesystem child
dictionaries; it does not use the virtual index to accelerate child matching.
Insertion into a sorted sequence can shift many groups, which is why this
version rebuilds for membership changes rather than promising logarithmic inserts.

## Choosing fanout

For cached memory-resident nodes, try 2, 4, 8, 16, 32, and 64 on representative
directory widths and update workloads. Larger fanout reduces depth and internal
node count but increases bytes hashed per updated node. Measure update latency
(including p95/p99), build time, memory, and bytes hashed. For disk-backed nodes,
choose fanout around the number of encoded references fitting one storage page,
then benchmark page reads and writes as well. Binary 32-byte digests fit more
references per page than this implementation's JSON hexadecimal encoding.

Select a fanout per format or index and retain it. Changing it changes grouping
and root hashes, so it requires rebuilding and coordination between replicas.
Powers of two are convenient, not required; tests also exercise fanout 3.

Run tests with `python -m unittest -v test_merkle_index.py test_merkle_tree.py`.
All 14 tests pass. The 4,096-entry fixture verifies that one edit with fanout 16
rehashes exactly three virtual groups and produces the same root as a fresh build.
