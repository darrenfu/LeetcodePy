# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


from collections import deque


class Solution(object):
    def levelOrder(self, root):
        """
        :type root: TreeNode
        :rtype: List[List[int]]
        """
        if not root: return None
        q = deque([root])
        res = []
        while q:
            l = len(q)  # record all nodes in the same level
            rec = []
            for _ in range(l):
                node = q.popleft()
                if node.left: q.append(node.left)
                if node.right: q.append(node.right)
                rec.append(node.val)
            res.append(rec)
        return res
