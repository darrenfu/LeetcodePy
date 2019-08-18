# Definition for a Node.
class Node:
    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """
    Runtime: 732 ms, faster than 47.79%
    https://leetcode.com/articles/convert-binary-search-tree-to-sorted-doubly-linked/
    """
    def treeToDoublyList(self, root: 'Node') -> 'Node':
        """
        links current traversed node into DLL
        """
        def linkDLL(node: Node) -> Node:
            nonlocal init, prev
            if prev:
                prev.right = node  # .right means .next in DLL
                node.left = prev  # .left means .prev in DLL
            else:
                # node 'init' will only be assigned once, i.e. the very left child node
                init = node
            # mark 'prev' as the previous node before going to next node in recursion
            prev = node

        """
        Performs standard inorder traversal: left -> node -> right
        """
        def inorder(node: Node) -> None:
            if node:
                # left
                inorder(node.left)
                # parent
                linkDLL(node)
                # right
                inorder(node.right)

        if not root:
            return None

        init, prev = None, None
        inorder(root)
        # close the circular loop in DLL
        prev.right = init
        init.left = prev
        return init
