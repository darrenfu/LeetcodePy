import logging
from typing import List, Any

from in_mem_fs.permission import TrieNode

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def ensure_node(self, components: List[str]) -> TrieNode:
        """
        Ensure a node exists for the given component path,
        creating intermediate nodes as needed.
        Returns the final node.
        """
        node = self.root
        # Traverse the trie using the given path (e.g. 'a' -> 'b' -> 'c')
        for comp in components:
            if comp not in node.children:
                # Add a new node to Trie's children set
                node.children[comp] = TrieNode()
            # Go to next level (component)
            node = node.children[comp]
        return node

    def find_node(self, components: List[str]) -> TrieNode | None:
        """
        Return the node for the given component path, or None if not found.
        """
        node = self.root
        for comp in components:
            if comp not in node.children:
                return None
            node = node.children[comp]
        return node

    def has_node(self, components: List[str]) -> bool:
        return self.find_node(components) is not None

    def set_value(self, components: List[str], value: Any) -> None:
        node = self.ensure_node(components)
        node.value = value

    def get_value(self, components: List[str]) -> Any | None:
        node = self.find_node(components)
        if node is None:
            return None
        return node.value

    def list_children(self, components: List[str]) -> List[str]:
        """
        List immediate children names under the given component path.
        """
        node = self.find_node(components)
        if node is None:
            return []
        return sorted(node.children.keys())

# Extend it for:
#     1.	Concurrent access
#     2.	Large files
#     3.	Permissions
#     4.	Invalid path handling
class FileSystem:

    def __init__(self, sep = '/'):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.sep = sep
        # In-memory trie
        # Each leaf file stores content: str
        self.trie = Trie()

    # Strip last '/'; Prepend '/' if not found
    def _normalize_path(self, path: str) -> str:
        if path == "":
            return self.sep
        if not path.startswith(self.sep):
            path = self.sep + path
        if len(path) > 1 and path.endswith(self.sep):
            path = path.rstrip(self.sep)
        return path

    # "/a/b/c.txt" -> ["a", "b", "c.txt"]
    def _split(self, path: str) -> List[str]:
        path = self._normalize_path(path)
        if path == self.sep:
            return []
        return [p for p in path.split(self.sep) if p]

    def ls(self, path: str) -> List[str]:
        """
        If path is a directory, return its immediate children (non-recursive).
        If path is a file, return [basename].
        """
        path = self._normalize_path(path)
        components = self._split(path)

        cur_node = self.trie.find_node(components)
        if cur_node is None:
            return []
        if cur_node.value is not None: # It's a file path
            return components[-1:]
        # It's a dir path
        return self.trie.list_children(components)

    def mkdir(self, path: str) -> None:
        path = self._normalize_path(path)
        components = self._split(path)
        self.trie.ensure_node(components)

    def addContentToFile(self, filePath: str, content: str) -> None:
        path = self._normalize_path(filePath)
        components = self._split(path)
        node = self.trie.ensure_node(components)
        if node.value is None:
            node.value = ""
        node.value += content

    def readContentFromFile(self, filePath: str) -> str:
        path = self._normalize_path(filePath)
        components = self._split(path)
        node = self.trie.find_node(components)
        # File not found or it's a directory
        if node is None or node.value is None:
            return ""
        return node.value

def main() -> None:
    obj = FileSystem()
    logger.info(obj.ls("/"))
    obj.mkdir("/a/b/c")
    obj.addContentToFile("/a/b/c/d", "hello world")
    logger.info(obj.ls("/"))
    assert "hello world" == obj.readContentFromFile("/a/b/c/d")

    obj.addContentToFile("/a/b/c/d", "hello hello world")
    assert "hello worldhello hello world" == obj.readContentFromFile("/a/b/c/d")

    logger.info("============")
    obj.mkdir("/goowmfn")
    logger.info(obj.ls("/goowmfn"))
    logger.info(obj.ls("/"))
    obj.mkdir("/z")
    logger.info(obj.ls("/"))
    logger.info(obj.ls("/"))
    obj.addContentToFile("/goowmfn/c", "shetopcy")
    logger.info(obj.ls("/goowmfn/c"))
    logger.info(obj.ls("/goowmfn"))


if __name__ == "__main__":
    main()
