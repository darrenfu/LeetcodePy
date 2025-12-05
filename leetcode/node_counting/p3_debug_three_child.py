# (3) Fix a buggy algorithm that updates node values in a 3-child tree
# You are given a tree where each node has up to three child pointers (left, mid, right).
# The requirement:
# Update each node’s value field to store the maximum value found anywhere in its subtree, including itself.
# The student’s implementation is incorrect.
# Your task:
# 	•	Identify what the student did wrong.
# 	•	Correct the algorithm so that it performs a proper post-order traversal:
# 	•	Recursively fix children first.
# 	•	Then update the parent based on the children’s corrected values.
# The final algorithm must ensure:
# For every node:
# node.value = max(node.value, leftSubtreeMax, midSubtreeMax, rightSubtreeMax)

class Machine:
    def __init__(self, val, left:"Machine"=None, mid:"Machine"=None, right:"Machine"=None):
        self.val = val
        # Three child nodes
        self.left = left
        self.mid = mid
        self.right = right

    def visit(self):
        """
        Mutates the tree so that each node.val becomes
        the maximum value in its subtree. Returns that max.
        """
        # Interpretation A: “Each node’s value must be the maximum value in its entire subtree, including itself.”
        maxv = self.val
        # Interpretation B: “Each node’s value should become the maximum of its children’s subtrees,
        # EXCLUDING the node’s own value.”
        maxv = float('-inf')

        # Post-order traversal (children → parent)
        for ch in [self.left, self.mid, self.right]:
            if ch:
                ch.visit()
                maxv = max(maxv, ch.val)

        # Option 1: leaf has no subtree → set to None or keep original value
        if maxv == float('-inf'):
            # No child values exist
            # You must decide what requirement means for a leaf.
            self.val = None   # or 0, or keep original; depends on definition
        else:
            self.val = maxv

        return self.val