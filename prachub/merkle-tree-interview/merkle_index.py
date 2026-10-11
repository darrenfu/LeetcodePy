"""Directory Merkle trees with a retained, bounded-fanout hash index.

An index leaf represents one immediate directory entry. Virtual index nodes
are not filesystem directories. Existing file edits update only index branches
and filesystem ancestors; additions, deletions, and renames require build().
Updates mutate the supplied snapshot. Retain a separate build for historical diff.
"""

import hashlib
import json
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath


def _digest(tag: bytes, value) -> str:
    encoded = json.dumps(value, ensure_ascii=True,
                         separators=(",", ":")).encode("ascii")
    return hashlib.sha256(tag + b"\0" + encoded).hexdigest()


def _group_hash(children: tuple["HashNode", ...]) -> str:
    return _digest(b"group", [child.content for child in children])


@dataclass(eq=False)
class HashNode:
    """A virtual index leaf or group, with a cached hash and parent link."""

    content: str
    children: tuple["HashNode", ...] = ()
    parent: "HashNode | None" = field(default=None, repr=False)


@dataclass(eq=False)
class Inode:
    name: str
    type: str
    content: str
    children: dict[str, "Inode"] = field(default_factory=dict)
    parent: "Inode | None" = field(default=None, repr=False)
    # This entry's leaf in its filesystem parent's index.
    entry_leaf: HashNode | None = field(default=None, repr=False)
    # A directory's own index root. Files have no index.
    index_root: HashNode | None = field(default=None, repr=False)
    fanout: int = 16
    source_path: Path | None = field(default=None, repr=False)


class MerkleTree:
    def __init__(self, fanout: int = 16):
        if not isinstance(fanout, int) or isinstance(fanout, bool) or fanout < 2:
            raise ValueError("fanout must be an integer >= 2")
        self.fanout = fanout

    @staticmethod
    def _file_hash(path: Path) -> str:
        hasher = hashlib.sha256(b"file\0")
        with path.open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                hasher.update(chunk)
        return hasher.hexdigest()

    @staticmethod
    def _entry_hash(node: Inode) -> str:
        return _digest(b"entry", [node.name, node.type, node.content])

    @staticmethod
    def _directory_hash(node: Inode) -> str:
        # Fanout is part of the hash format: compare trees using the same fanout.
        return _digest(b"directory", [node.fanout, node.index_root.content])

    def _build_index(self, directory: Inode) -> None:
        level = []
        for child in directory.children.values():
            child.entry_leaf = HashNode(self._entry_hash(child))
            level.append(child.entry_leaf)

        if not level:
            # Empty directories have an explicit, deterministic empty group.
            directory.index_root = HashNode(_group_hash(()))
        else:
            while len(level) > 1:
                next_level = []
                for offset in range(0, len(level), directory.fanout):
                    children = tuple(level[offset:offset + directory.fanout])
                    group = HashNode(_group_hash(children), children)
                    for child in children:
                        child.parent = group
                    next_level.append(group)
                level = next_level
            directory.index_root = level[0]
        directory.content = self._directory_hash(directory)

    def build(self, path: str | Path) -> Inode:
        """Read a stable filesystem tree; reject symlinks and special entries."""
        root = Path(path).absolute()
        if root.is_symlink() or not root.is_dir():
            raise ValueError("Expected a directory, not a symlink")

        def visit(entry: Path, parent: Inode | None) -> Inode:
            if entry.is_symlink():
                raise ValueError(f"Unsupported symlink: {entry}")
            if entry.is_file():
                return Inode(entry.name, "file", self._file_hash(entry),
                             parent=parent, source_path=entry)
            if not entry.is_dir():
                raise ValueError(f"Unsupported filesystem entry: {entry}")
            node = Inode(entry.name, "dir", "", parent=parent,
                         fanout=self.fanout, source_path=entry)
            for child in sorted(entry.iterdir(), key=lambda item: item.name):
                node.children[child.name] = visit(child, node)
            self._build_index(node)
            return node

        return visit(root, None)

    @staticmethod
    def _parts(path: str) -> tuple[str, ...]:
        relative = PurePosixPath(path)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("Expected a relative POSIX path without ..")
        return relative.parts

    def _find(self, path: str, tree: Inode) -> Inode:
        node = tree
        for name in self._parts(path):
            if node.type != "dir" or name not in node.children:
                raise KeyError(path)
            node = node.children[name]
        return node

    def get_hash(self, path: str, tree: Inode) -> str:
        """Read only the retained snapshot, not disk."""
        return self._find(path, tree).content

    def update_file(self, path: str, tree: Inode) -> str:
        """Reread one existing file and mutate its cached ancestor hashes.

        The caller must know that only this file's contents changed on disk.
        Membership changes require a rebuild. No concurrent writers are supported.
        """
        node = self._find(path, tree)
        if node.type != "file":
            raise ValueError("update_file requires an existing file")
        # Reject a replaced symlink/directory before reading the file. This does
        # not eliminate races: callers must provide a stable filesystem view.
        disk_path = tree.source_path
        if disk_path.is_symlink() or not disk_path.is_dir():
            raise ValueError("Root changed type; rebuild required")
        parts = self._parts(path)
        for index, name in enumerate(parts):
            disk_path = disk_path / name
            if disk_path.is_symlink():
                raise ValueError(f"Unsupported symlink: {disk_path}")
            if index < len(parts) - 1 and not disk_path.is_dir():
                raise ValueError("Ancestor changed type; rebuild required")
        if not disk_path.is_file():
            raise ValueError("Entry changed type or was removed; rebuild required")

        new_hash = self._file_hash(disk_path)
        if new_hash == node.content:
            return tree.content
        node.content = new_hash

        while node.parent is not None:
            # Update this inode's record in its parent's virtual index.
            leaf = node.entry_leaf
            leaf.content = self._entry_hash(node)
            group = leaf.parent
            while group is not None:
                group.content = _group_hash(group.children)
                group = group.parent
            directory = node.parent
            directory.content = self._directory_hash(directory)
            node = directory
        return tree.content

    def diff(self, tree_a: Inode, tree_b: Inode) -> list[tuple[str, str]]:
        """Compare filesystem nodes, pruning identical directory hashes."""
        changes = []
        queue = deque([("", tree_a, tree_b)])
        while queue:
            path, a, b = queue.popleft()
            if a.type != b.type:
                changes.append((path or ".", "modified"))
            elif a.content == b.content:
                continue
            elif a.type == "file":
                changes.append((path, "modified"))
            else:
                if a.fanout != b.fanout:
                    raise ValueError("Directory indexes use different fanouts")
                for name in sorted(a.children.keys() | b.children.keys()):
                    child_path = f"{path}/{name}" if path else name
                    if name not in a.children:
                        changes.append((child_path, "added"))
                    elif name not in b.children:
                        changes.append((child_path, "removed"))
                    else:
                        queue.append((child_path, a.children[name], b.children[name]))
        return sorted(changes)
