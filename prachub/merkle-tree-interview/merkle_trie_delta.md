# Canonical Merkle trie delta (discussion draft)

This preserves the latest code delta discussed in the interview. It is NOT a standalone tested module. The runnable tested implementations remain merkle_tree.py and merkle_index.py. Apply these changes to the baseline; import PurePosixPath alongside Path. Calls assume stable filesystem data and negligible SHA-256 collisions. update_file mutates the snapshot. Directory hashes use a new format and cannot be compared with old-format directory hashes.

## Add fields to Inode

```python
parent: "Inode | None" = field(default=None, repr=False)
index: "TrieNode | None" = field(default=None, repr=False)
source_path: Path | None = field(default=None, repr=False)
```

## Add virtual trie and helpers

```python
@dataclass
class TrieNode:
    children: dict[str, "TrieNode"] = field(default_factory=dict)
    value: str | None = None
    content: str = ""


def digest(tag, value):
    encoded = json.dumps(
        value, ensure_ascii=True, separators=(",", ":")
    ).encode("ascii")
    return hashlib.sha256(tag + b"\0" + encoded).hexdigest()


EMPTY_INDEX = digest(b"trie", [None, []])


def set_entry(index, name, entry_hash):
    """Insert/update an entry; entry_hash=None deletes it."""
    route = hashlib.sha256(
        name.encode("utf-8", errors="surrogatepass")
    ).hexdigest()

    def update(node, depth):
        if node is None:
            if entry_hash is None:
                return None
            node = TrieNode()
        if depth == len(route):
            node.value = entry_hash
        else:
            digit = route[depth]
            child = update(node.children.get(digit), depth + 1)
            if child is None:
                node.children.pop(digit, None)
            else:
                node.children[digit] = child
        if node.value is None and not node.children:
            return None
        records = [
            [digit, child.content]
            for digit, child in sorted(node.children.items())
        ]
        node.content = digest(b"trie", [node.value, records])
        return node

    return update(index, 0)


def entry_hash(node):
    return digest(b"entry", [node.name, node.type, node.content])


def directory_hash(node):
    root_hash = node.index.content if node.index else EMPTY_INDEX
    return digest(b"directory", root_hash)
```

## Replace directory aggregation in build

```python
# children is the existing sorted list of built child Inodes.
node = Inode(entry.name, "dir", "", children,
             source_path=entry)
for child in children:
    child.parent = node
    node.index = set_entry(node.index, child.name, entry_hash(child))
node.content = directory_hash(node)
return node
```

Also store source_path=entry when constructing file nodes. Keep original file hashing, get_hash, and diff.

## Add update_file to MerkleTree

```python
def update_file(self, path, tree):
    relative = PurePosixPath(path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("Expected a relative path without ..")
    node = tree
    for name in relative.parts:
        if node.type != "dir":
            raise KeyError(path)
        node = next(
            (child for child in node.children if child.name == name),
            None,
        )
        if node is None:
            raise KeyError(path)
    if node.type != "file":
        raise ValueError("Expected a file")
    hasher = hashlib.sha256(b"file\0")
    with node.source_path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            hasher.update(chunk)
    new_hash = hasher.hexdigest()
    if new_hash == node.content:
        return tree.content
    node.content = new_hash
    while node.parent is not None:
        parent = node.parent
        parent.index = set_entry(
            parent.index, node.name, entry_hash(node)
        )
        parent.content = directory_hash(parent)
        node = parent
    return tree.content
```

Removing an entry requires deleting it from the filesystem child list, invoking set_entry(parent.index, name, None), recomputing the directory hash, and propagating upward. This delta provides the trie primitive, not the full membership API. It also does not carry the indexed implementation's additional replaced-type/symlink validation in update_file; callers must maintain unchanged entry types and a stable filesystem. Uncompressed routes can use substantial memory. Name encoding and rules must be consistent across machines.

## Diagram

```text
Filesystem directory inode
          |
   canonical trie root
     /     |      \
   hex 0  hex 1  ... hex f
     |
   next hexadecimal route digit
     |
   ... 64 hexadecimal digits total ...
     |
   terminal entry hash: H(name, type, content hash)
```

Insertion/deletion updates a route rather than shifting sorted chunk positions. The terminal route length is fixed because SHA-256 digests have fixed length; variable-length direct-name tries would need explicit end-of-key handling.
