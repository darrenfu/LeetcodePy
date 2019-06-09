from typing import List

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def sufficientSubset(self, root: TreeNode, limit: int) -> TreeNode:
        if not root: return None
        paths = []
        hashmap = {}

        def dfs(node: TreeNode, sum: int, limit_flag) -> None:
            if not node.left and not node.right:
                paths.append(limit_flag)
            if node.left:
                flag = sum + node.left.val < limit
                dfs(node.left, sum + node.left.val, limit_flag+[(node.left, flag)])
            if node.right:
                flag = sum + node.right.val < limit
                dfs(node.right, sum + node.right.val, limit_flag+[(node.right, flag)])

        dfs(root, root.val, [(root, root.val < limit)])

        print(paths)
        for path in paths:
            if not path[-1][1]:
                for node, _ in path:
                    hashmap[node] = True
        for k in hashmap.keys():
            print(k.val)

        def dfs2(node: TreeNode) -> None:
            if node.left:
                if node.left not in hashmap:
                    node.left = None
                else:
                    dfs2(node.left)
            if node.right:
                if node.right not in hashmap:
                    node.right = None
                else:
                    dfs2(node.right)

        dfs2(root)
        return root if root in hashmap else None


# Some edge cases will fail!
# root = TreeNode(5)
# root.left = TreeNode(4)
# root.right = TreeNode(8)
# root.left.left = TreeNode(11)
# root.left.left.left = TreeNode(7)
# root.left.left.right = TreeNode(1)
# root.right.left = TreeNode(17)
# root.right.right = TreeNode(4)
# root.right.right.left = TreeNode(5)
# root.right.right.right = TreeNode(3)
root = TreeNode(5)
root.left = TreeNode(21)
Solution().sufficientSubset(root, 22)

