from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class TrieNode:
    children: Dict[str, "TrieNode"] = field(default_factory=dict)
    value: Any | None = None
    # when writing to a large file
    is_file: bool = False
    chunks: List[str] = field(default_factory=list)
    size: int = 0
    # permission
    mode: int = 0o644 # rw-r--r--
    owner: str | None = "root"


class PermissionError(Exception):
    pass

def _check_read(self, node: TrieNode) -> None:
    # extremely simplified: owner can always read; others use mode bits
    if self.user == node.owner:
        return
    # world-readable?
    if node.mode & 0o004 == 0:
        raise PermissionError("Read permission denied")

def _check_write(self, node: TrieNode) -> None:
    if self.user == node.owner:
        return
    # world-writable?
    if node.mode & 0o002 == 0:
        raise PermissionError("Write permission denied")
