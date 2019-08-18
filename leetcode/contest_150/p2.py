import math
from collections import defaultdict

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def maxLevelSum(self, root: TreeNode) -> int:
        if not root:
            return 0
        # bfs
        lvl = 1
        q = [(root, lvl)]
        sumMap = defaultdict(int)
        while q:
            head, lvl = q.pop(0)
            sumMap[lvl] += head.val
            if head.left: q.append((head.left, lvl + 1))
            if head.right: q.append((head.right, lvl + 1))
        maxSum = - math.inf
        res = 0
        for lvl in sorted(sumMap.keys()):
            if sumMap[lvl] > maxSum:
                maxSum = sumMap[lvl]
                res = lvl
        return res

