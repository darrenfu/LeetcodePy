# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


from collections import defaultdict


class Solution(object):
    def verticalOrder(self, root):
        """
        :type root: TreeNode
        :rtype: List[List[int]]
        """
        if not root: return None
        q = [(root, 0)]  # root's vertical index is 0
        cols = defaultdict(list)  # dict's default value is an empty list
        for node, col in q:  # array is simpler than deque, no need to dequeue (popleft)
            if node:  # binary tree
                # left node, vertical index --;
                # right node, vertical index ++
                q += (node.left, col - 1), (node.right, col + 1)
            cols[col].append(node.val)
        # sort dict's keys, and return values (lists) in key's order
        return [cols[k] for k in sorted(cols)]
