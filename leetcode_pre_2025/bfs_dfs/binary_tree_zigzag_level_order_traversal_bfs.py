# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


from collections import deque


class Solution(object):
    def zigzagLevelOrder(self, root):
        """
        :type root: TreeNode
        :rtype: List[List[int]]
        """
        if not root: return None
        q = deque([root])
        res = []
        depth = 0  # to mark tree depth, if even, prepend the element; if odd, append the element as usual.
        while q:
            l = len(q)  # record all nodes in the same level
            rec = []
            for _ in range(l):
                node = q.popleft()
                if node.left: q.append(node.left)
                if node.right: q.append(node.right)
                if depth % 2:
                    rec.appendleft(node.val)
                else:
                    rec.append(node.val)
            res.append(list(rec))
            depth += 1
        return res
