# Definition for a Node.
class Node:
    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """
    Runtime: 716 ms, faster than 78.35%
    https://leetcode.com/problems/convert-binary-search-tree-to-sorted-doubly-linked-list/discuss/149151/Concise-Java-solution-Beats-100
    """
    def treeToDoublyList(self, root: 'Node') -> 'Node':
        """
        Performs standard inorder traversal: left -> node -> right
        """
        def inorder(node: Node) -> None:
            nonlocal prev
            if not node:
                return
            # left
            inorder(node.left)
            # parent
            prev.right = node  # prev.next -> node
            node.left = prev  # node.prev -> prev
            prev = node
            # right
            inorder(node.right)

        if not root:
            return None

        prev = dummy = Node(0, None, None)  # create a dummy head node. Its right node is the expecting result
        inorder(root)
        # close the circular loop in DLL
        prev.right = dummy.right  # (last node).next -> dummy.right (first node)
        dummy.right.left = prev  # (first node).prev -> last node
        return dummy.right  # first node
