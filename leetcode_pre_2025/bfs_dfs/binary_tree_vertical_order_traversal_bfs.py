# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


from collections import deque
from itertools import groupby


class Solution(object):
    def verticalOrder(self, root):
        """
        :type root: TreeNode
        :rtype: List[List[int]]
        """
        if not root: return None
        q = deque([(root, 0)])  # root's vertical index is 0
        res = []
        while q:
            node, col = q.popleft()
            if node.left: q.append((node.left, col + 1))  # left node, vertical index ++
            if node.right: q.append((node.right, col - 1))  # right node, vertical index --
            res.append((node, col))

        def takeSecond(elem):
            return elem[1]
        res.sort(key=takeSecond, reverse=True)  # sort by vertical index
        # group by vertical index, and transform grouped nodes at each vertical index into its values
        return [[ele[0].val for ele in list(g)] for _, g in groupby(res, takeSecond)]

