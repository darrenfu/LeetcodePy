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
