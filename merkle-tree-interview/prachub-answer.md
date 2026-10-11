# Directory Merkle tree: build, lookup, diff, and tests

## Contract and design

The snapshot is an N-ary tree. Every node stores its name, type, SHA-256 hexadecimal hash, and children. Directory hashes are computed bottom-up and stored, so later lookup and diff never reread disk. SHA-256 returns 32 bytes, represented here as 64 hexadecimal characters; collisions are assumed negligible.

File hashes cover a fixed file-type prefix followed by file contents, read in 1 MiB chunks. Directory hashes cover a distinct directory-type prefix followed by a deterministic JSON list of immediate children’s names, types, and stored hashes. Children are sorted by name. JSON escapes delimiters and Unicode unambiguously; ensure_ascii=True makes ASCII encoding valid. The null byte after each fixed type label is a convention, not a delimiter that must be absent from file data. Type prefixes prevent file contents from reproducing a directory’s exact hash input.

Names contribute to the parent’s hash, not the entry’s own hash. Thus renaming a file changes its parent and ancestors while preserving its content hash. Root location and root name do not affect the snapshot hash. Different nesting or different associations between names and file contents produce different root hashes.

Lookup uses POSIX-style relative paths; '.' and an empty path denote the root. Missing paths raise KeyError. Absolute paths and '..' are rejected. Lookup traverses retained node objects: SHA-256 cannot be decoded to recover tree contents.

Diff reports sorted (relative_path, status) tuples describing A to B. Status is added, removed, or modified. Entire added or removed directories are reported once. A file/directory replacement at the same path is modified. Ancestor directories are not separately reported for descendant changes. BFS compares matched node pairs; equal hashes prune all descendants. Children must be matched by name, not list position or type, because insertions shift indices and replacements retain their names.

Hidden files and empty directories are included. Metadata such as permissions and timestamps is excluded. Symlinks and special files are rejected; filesystem read errors propagate. The filesystem must remain unchanged during build: this implementation does not obtain an atomic filesystem snapshot. The interview assumption is at most 100,000 entries and depth at most 100; arbitrarily deep trees would require iterative build traversal.

## Implementation (Python 3.10+)

```python
import hashlib
import json
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath


@dataclass
class Inode:
    name: str
    type: str
    content: str
    children: list['Inode'] = field(default_factory=list)


class MerkleTree:
    def build(self, path: str | Path) -> Inode:
        root = Path(path)
        if root.is_symlink() or not root.is_dir():
            raise ValueError('Expected a directory, not a symlink')

        def visit(entry):
            if entry.is_symlink():
                raise ValueError(f'Unsupported symlink: {entry}')
            if entry.is_file():
                hasher = hashlib.sha256(b'file\0')
                with entry.open('rb') as stream:
                    while chunk := stream.read(1024 * 1024):
                        hasher.update(chunk)
                return Inode(entry.name, 'file', hasher.hexdigest())
            if entry.is_dir():
                children = [visit(child) for child in
                            sorted(entry.iterdir(), key=lambda p: p.name)]
                records = [[c.name, c.type, c.content] for c in children]
                encoded = json.dumps(records, ensure_ascii=True,
                                     separators=(',', ':')).encode('ascii')
                digest = hashlib.sha256(b'dir\0' + encoded).hexdigest()
                return Inode(entry.name, 'dir', digest, children)
            raise ValueError(f'Unsupported filesystem entry: {entry}')

        return visit(root)

    def get_hash(self, path: str, tree: Inode) -> str:
        relative = PurePosixPath(path)
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Expected a relative path without ..')
        node = tree
        for name in relative.parts:
            if node.type != 'dir':
                raise KeyError(path)
            node = next((c for c in node.children if c.name == name), None)
            if node is None:
                raise KeyError(path)
        return node.content

    def diff(self, tree_a: Inode, tree_b: Inode) -> list[tuple[str, str]]:
        changes = []
        queue = deque([('', tree_a, tree_b)])
        while queue:
            path, a, b = queue.popleft()
            if a.type != b.type:
                changes.append((path or '.', 'modified'))
                continue
            if a.content == b.content:
                continue
            if a.type == 'file':
                changes.append((path, 'modified'))
                continue
            children_a = {c.name: c for c in a.children}
            children_b = {c.name: c for c in b.children}
            for name in sorted(children_a.keys() | children_b.keys()):
                child_path = f'{path}/{name}' if path else name
                if name not in children_a:
                    changes.append((child_path, 'added'))
                elif name not in children_b:
                    changes.append((child_path, 'removed'))
                else:
                    queue.append((child_path, children_a[name], children_b[name]))
        return sorted(changes)
```

## Complexity

Let N be the number of entries, B the total file bytes, d_j the number of immediate children of directory j, and L the total encoded filename bytes. Build takes O(B + N + L + sum_j d_j log d_j), including sorting and encoding. Retained storage is O(N + L), plus a fixed-size file buffer and temporary directory records; recursion depth equals directory depth.

With list children, lookup takes O(sum of child counts along the queried path) in the worst case. A dictionary per directory would reduce lookup to average O(path depth), apart from parsing and string costs.

For diff, let E count child entries examined in directories whose hashes differ, P the compared node pairs, and K the output size. Time is O(P + sum over examined directories of d_j log d_j + K log K). Equal roots take O(1). Worst case traverses all entries; a single change in a very wide directory still requires inspecting that directory’s immediate children. Auxiliary memory is O(N) in the worst case for the BFS queue and dictionaries, plus O(K) results. It is not generally O(number of changed files).

## Tests

The tests use actual temporary directories with automatic cleanup. They cover differing creation order and root names, Unicode and newline filenames, empty files and directories, root and nested lookup, invalid and missing paths, snapshot lookup after disk changes, added/removed files and directories, root and nested edits, replacements in both directions, renames, multi-chunk files, symlink rejection, and the Merkle property. A guarded children container raises if diff visits descendants of an equal subtree, directly proving pruning.

Run: python -m unittest -v test_merkle_tree.py

Validation: all seven tests pass.

```python
import hashlib
import tempfile
import unittest
from pathlib import Path
from merkle_tree import Inode, MerkleTree


class MerkleTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.a = self.root / 'A'
        self.b = self.root / 'B'
        self.a.mkdir()
        self.b.mkdir()
        self.m = MerkleTree()

    def write(self, root, name, data=b'hello'):
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def test_determinism_and_lookup(self):
        for name in ['z.txt', 'sub/a.txt', 'empty.txt', 'space newline\n雪']:
            self.write(self.a, name, b'' if name == 'empty.txt' else b'hello')
        for name in reversed(['z.txt', 'sub/a.txt', 'empty.txt', 'space newline\n雪']):
            self.write(self.b, name, b'' if name == 'empty.txt' else b'hello')
        a, b = self.m.build(self.a), self.m.build(self.b)
        self.assertEqual(a.content, b.content)
        self.assertEqual(self.m.diff(a, b), [])
        self.assertEqual(self.m.get_hash('.', a), a.content)
        expected = hashlib.sha256(b'file\0hello').hexdigest()
        self.assertEqual(self.m.get_hash('sub/a.txt', a), expected)
        for missing in ['missing', 'z.txt/child']:
            with self.assertRaises(KeyError):
                self.m.get_hash(missing, a)
        for invalid in ['/absolute', '../outside']:
            with self.assertRaises(ValueError):
                self.m.get_hash(invalid, a)
        self.write(self.a, 'sub/a.txt', b'changed')
        self.assertEqual(self.m.get_hash('sub/a.txt', a), expected)

    def test_add_remove_modify_and_replace(self):
        for root in [self.a, self.b]:
            self.write(root, 'nested/edit', b'before')
            self.write(root, 'root-edit', b'before')
        self.write(self.b, 'nested/edit', b'after')
        self.write(self.b, 'root-edit', b'after')
        self.write(self.a, 'removed-file')
        self.write(self.a, 'removed-dir/child')
        self.write(self.b, 'added-file')
        self.write(self.b, 'added-dir/child')
        self.write(self.a, 'file-to-dir')
        (self.b / 'file-to-dir').mkdir()
        (self.a / 'dir-to-file').mkdir()
        self.write(self.b, 'dir-to-file')
        expected = [('added-dir', 'added'), ('added-file', 'added'),
                    ('dir-to-file', 'modified'), ('file-to-dir', 'modified'),
                    ('nested/edit', 'modified'), ('removed-dir', 'removed'),
                    ('removed-file', 'removed'), ('root-edit', 'modified')]
        self.assertEqual(self.m.diff(self.m.build(self.a), self.m.build(self.b)), expected)

    def test_merkle_property(self):
        self.write(self.a, 'src/utils/helpers.py', b'before')
        self.write(self.a, 'assets/logo', b'unchanged')
        before = self.m.build(self.a)
        self.write(self.a, 'src/utils/helpers.py', b'after')
        after = self.m.build(self.a)
        for path in ['.', 'src', 'src/utils', 'src/utils/helpers.py']:
            self.assertNotEqual(self.m.get_hash(path, before), self.m.get_hash(path, after))
        for path in ['assets', 'assets/logo']:
            self.assertEqual(self.m.get_hash(path, before), self.m.get_hash(path, after))
        self.assertEqual(self.m.diff(before, after), [('src/utils/helpers.py', 'modified')])

    def test_empty_directory_and_rename(self):
        self.assertEqual(self.m.diff(self.m.build(self.a), self.m.build(self.b)), [])
        self.write(self.a, 'old')
        self.write(self.b, 'new')
        (self.b / 'empty').mkdir()
        self.assertEqual(self.m.diff(self.m.build(self.a), self.m.build(self.b)),
                         [('empty', 'added'), ('new', 'added'), ('old', 'removed')])

    def test_large_file(self):
        data = b'x' * (2 * 1024 * 1024 + 7)
        self.write(self.a, 'large', data)
        tree = self.m.build(self.a)
        self.assertEqual(self.m.get_hash('large', tree), hashlib.sha256(b'file\0' + data).hexdigest())

    def test_equal_subtrees_are_not_traversed(self):
        for root in [self.a, self.b]:
            self.write(root, 'assets/icons/home')
        self.write(self.a, 'src/main', b'before')
        self.write(self.b, 'src/main', b'after')
        a, b = self.m.build(self.a), self.m.build(self.b)

        class FailOnIteration(list):
            def __iter__(self):
                raise AssertionError('Visited children of an equal subtree')

        for tree in [a, b]:
            assets = next(c for c in tree.children if c.name == 'assets')
            assets.children = FailOnIteration(assets.children)
        self.assertEqual(self.m.diff(a, b), [('src/main', 'modified')])

    def test_symlink_rejected(self):
        self.write(self.a, 'file')
        (self.a / 'link').symlink_to('file')
        with self.assertRaises(ValueError):
            self.m.build(self.a)


if __name__ == '__main__':
    unittest.main()
```

## Follow-ups

- Incremental update: rehash the changed file and recompute each ancestor. Reuse unaffected nodes. In this encoding each ancestor still requires hashing all its immediate child records; cost is not merely proportional to depth. Store parent/path indexes to locate the update chain.
- Remote comparison: exchange root hashes first, then child name/type/hash records only for differing directories. Batch requests and transfer only differing content. Whole added directories require their manifest/content if actual synchronization is needed.
- Millions of files: consider bounded parallel file reads, persistent content-addressed nodes, caches with a defensible invalidation policy, iterative traversal, and finer-grained balanced or trie-based indexes for very wide directories. Chunked file trees allow partial transfer and deduplication. Consistent snapshots and canonical versioned encoding become important.
- Moves/renames: correlate added and removed entries using type and content hash. Duplicate content makes matching ambiguous, so define a deterministic policy; ordinary diff still reports deletion/addition.

A Merkle tree is useful for efficient comparison, integrity checks against a trusted root, and membership proofs in suitable tree designs. A hash does not authenticate the creator; signatures or another trust mechanism are needed for that. This directory-shaped design is suitable for the interview and does not attempt the persistence, proof APIs, or synchronization guarantees of specialized production libraries.
