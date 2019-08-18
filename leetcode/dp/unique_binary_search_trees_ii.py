from typing import List


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    """
    Runtime: 60 ms, faster than 72.01%
    Runtime: 52 ms, faster than 96.86% if use cache
    """
    def generateTrees(self, n: int) -> List[TreeNode]:
        if not n: return []
        cache = {}

        def gen(start: int, end: int) -> List[TreeNode]:
            if start > end: return [None]
            if (start, end) in cache: return cache[(start, end)]
            trees = []
            for r in range(start, end+1):
                for left in gen(start, r-1):
                    for right in gen(r+1, end):
                        node = TreeNode(r)
                        node.left, node.right = left, right
                        trees += node,
            cache[(start, end)] = trees
            return trees
        return gen(1, n)

