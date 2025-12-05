class TrieNode:
    def __init__(self, name: str, val: str):
        self.name = name
        self.val = val
        self.children = [] # TrieNode list

class ZK:
    def __init__(self):
        self.root = TrieNode("", None)  # root

    def create(self, path, value) -> None:
        def traverseTrie(node: TrieNode):
            if len(node_names) == 0:
                return None
            if len(node_names) == 1:
                return node
            if not node.children:
                return None
            cur_name = node_names.pop(0)
            for child in node.children:
                if child.name == cur_name:
                    return traverseTrie(child)
            return None
        # deal with "/" case
        node_names = self.getNodeNames(path)
        nodeContainer = traverseTrie(self.root)
        if not nodeContainer:
            raise Exception("no path found")
        leafNode = TrieNode(node_names[0], value)
        nodeContainer.children.append(leafNode)

    def traverseExistingPath(self, node: TrieNode, node_names):
        if len(node_names) == 0:
            return node
        cur_name = node_names.pop(0)
        for child in node.children:
            if child.name == cur_name:
                print(cur_name)
                return self.traverseExistingPath(child, node_names)
        return None

    def set_value(self, path, value) -> None:
        node_names = self.getNodeNames(path)
        node = self.traverseExistingPath(self.root, node_names)
        if not node:
            raise Exception("no path found")
        node.val = value

    def get_value(self, path) -> str:
        node_names = self.getNodeNames(path)
        node = self.traverseExistingPath(self.root, node_names)
        if not node:
            raise Exception("no path found")
        return node.val

    def getNodeNames(self, path):
        return path.split("/")[1:]


zk = ZK()
zk.create("/a", "aa")
zk.create("/b", "bb")
zk.create("/f", "ff")
print(zk.get_value("/a"))

zk.create("/a/c", "ac")
zk.create("/a/d", "ad")
print(zk.get_value("/a/c"))
print(zk.get_value("/a/d"))
