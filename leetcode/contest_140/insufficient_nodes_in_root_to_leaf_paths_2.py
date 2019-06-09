class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def sufficientSubset(self, root: TreeNode, limit: int) -> TreeNode:
        def dfs(root: TreeNode, presum: int) -> int:
            if not root:
                return presum  # parent is leaf node, return root-to-parent path's sum
            l = dfs(root.left, presum + root.val)  # max sum among left chains
            r = dfs(root.right, presum + root.val)  # max sum among right chains
            # Post-order traversal - children first, then children are deletable
            if root.left and l < limit:
                root.left = None
            if root.right and r < limit:
                root.right = None
            return max(l, r)

        if dfs(root, 0) < limit:
            root = None
        return root


root = TreeNode(5)
root.left = TreeNode(4)
root.right = TreeNode(8)
root.left.left = TreeNode(11)
root.left.left.left = TreeNode(7)
root.left.left.right = TreeNode(1)
root.right.left = TreeNode(17)
root.right.right = TreeNode(4)
root.right.right.left = TreeNode(5)
root.right.right.right = TreeNode(3)
Solution().sufficientSubset(root, limit=22)

