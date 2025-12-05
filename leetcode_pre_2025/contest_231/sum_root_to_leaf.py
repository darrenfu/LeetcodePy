# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def sumRootToLeaf(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """
        from collections import deque
        stack = deque()
        binaries = []
        def dfs(node):
            stack.append(str(node.val))
            if not node.left and not node.right:
                print stack
                binaries.append("".join(stack))
                return
            if node.left:
                dfs(node.left)
                stack.pop()
            if node.right:
                dfs(node.right)
                stack.pop()

        dfs(root)

        sum = 0
        for s in binaries:
            sum += int(s, 2)
        return sum % (10**9 + 7)

if __name__ == '__main__':
    s = Solution()
    print s.sumRootToLeaf()