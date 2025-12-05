import logging
from collections import defaultdict
from enum import Enum
from typing import List
from pygtrie import StringTrie

class FileType(Enum):
    FILE = 1
    DIRECTORY = 0

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

class FileSystem:

    def __init__(self, sep = '/'):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.sep = sep
        self.trie = StringTrie(separator=sep)
        # directory_path  →  set of its immediate children (files or subdirs)
        self.children = defaultdict(set)

    # "/a/b/c.txt" -> ["a", "b", "c.txt"]
    def _split(self, path: str) -> List[str]:
        if path == self.sep:
            return []
        return [p for p in path.split(self.sep) if p]

    def _add_to_children(self, path_parts: List[str]):
        cur_path = ""
        for part in path_parts:
            parent_path = cur_path or self.sep
            # self.logger.info(f"parent_path: {parent_path}, part: {part}")
            self.children[parent_path].add(part)
            cur_path = (parent_path if parent_path == self.sep else parent_path + self.sep) + part
        self.logger.info(self.children)

    def ls(self, path: str) -> List[str]:
        if path != self.sep and path.endswith(self.sep):
            path = path.rstrip(self.sep)
        self.logger.info(list(self.trie.iterkeys()))
        self.logger.info(path)
        return sorted(self.children.get(path or self.sep, ()))

    def mkdir(self, path: str) -> None:
        self.trie[path] = (FileType.DIRECTORY, None)
        parts = self._split(path)
        self._add_to_children(parts)

    def addContentToFile(self, filePath: str, content: str) -> None:
        if filePath in self.trie and self.trie[filePath][0] != FileType.FILE:
            raise ValueError(f"{filePath} is not a file")
        # touch and update file
        self.trie[filePath] = (FileType.FILE, content)
        parts = self._split(filePath)
        self._add_to_children(parts)

    def readContentFromFile(self, filePath: str) -> str:
        if filePath not in self.trie or self.trie[filePath][0] != FileType.FILE:
            raise ValueError(f"{filePath} doesn't exist or it is not a file")
        return self.trie[filePath][1]

def main() -> None:
    obj = FileSystem()
    path = "/a/b"
    param_1 = obj.ls(path)
    logger.info(param_1)
    obj.mkdir(path)
    param_1 = obj.ls("/a/")
    logger.info(param_1)
    param_1 = obj.ls("/")
    logger.info(param_1)

    filePath = "/a/b/c.txt"
    content = "BLANK"
    obj.addContentToFile(filePath, content)
    param_4 = obj.readContentFromFile(filePath)
    assert param_4 == content

if __name__ == "__main__":
    main()
