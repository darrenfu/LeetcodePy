class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution(object):

    def lcaDeepestLeaves(self, root: TreeNode) -> TreeNode:
        memo = {None: 0}

        def helper(n: TreeNode) -> TreeNode:
            nonlocal memo
            if not n: return None
            ld, rd = memo[n.left], memo[n.right]
            if ld == rd:  # LCA! left sub tree and right sub tree is the same deep
                return n
            elif ld > rd:  # left sub tree is deeper
                return helper(n.left)
            else:
                return helper(n.right)

        def maxDepth(n: TreeNode) -> int:
            nonlocal memo
            if not n: return 0
            l, r = maxDepth(n.left), maxDepth(n.right)
            d = max(l, r) + 1
            memo[n] = d
            return d

        maxDepth(root)
        return helper(root)
