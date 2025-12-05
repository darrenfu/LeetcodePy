#Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def btreeGameWinningMove(self, root: TreeNode, n: int, x: int) -> bool:
        def dfs(node: TreeNode) -> TreeNode:
            nonlocal x
            if not node: return None
            if node.val == x: return node
            l = dfs(node.left)
            if l: return l
            r = dfs(node.right)
            if r: return r

        def childnum(node: TreeNode) -> int:
            if not node: return 0
            return childnum(node.left) + childnum(node.right) + 1

        node = dfs(root)
        L, R = childnum(node.left), childnum(node.right)
        # the node divides the whole tree into three part -
        # its left subtree, right subtree, the remaining tree
        # if any part holds more than half of the tree nodes, player B will win.
        return max(L, R, n - 1 - L - R) * 2 > n
