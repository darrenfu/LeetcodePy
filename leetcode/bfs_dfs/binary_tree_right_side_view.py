# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


from collections import deque


class Solution(object):
    def rightSideView(self, root):
        """
        :type root: TreeNode
        :rtype: List[int]
        """
        if not root: return None
        q = deque([root])
        res = []
        while q:
            for i in range(len(q)):
                node = q.popleft()
                if i == 0: res.append(node.val)
                if node.right: q.append(node.right)
                if node.left: q.append(node.left)
        return res
