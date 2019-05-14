# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution(object):
    def bstToGst(self, root):
        """
        :type root: TreeNode
        :rtype: TreeNode
        """
        self.last_sum = 0
        if not root: return root

        def dfs(node):
            if node.right: dfs(node.right)
            node.val += self.last_sum
            self.last_sum = node.val
            if node.left: dfs(node.left)

        dfs(root)
        return root
