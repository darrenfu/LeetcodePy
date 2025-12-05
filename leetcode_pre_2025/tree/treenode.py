# Definition for a Node.
class Node:
    def __init__(self, val, children):
        self.val = val
        self.children = children


# https://support.leetcode.com/hc/en-us/articles/360011883654-What-does-1-null-2-3-mean-in-binary-tree-representation-
# https://leetcode.com/problems/recover-binary-search-tree/discuss/32539/Tree-Deserializer-and-Visualizer-for-Python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x, left=None, right=None):
        self.val = x
        self.left = None
        self.right = None

    def __repr__(self):
        return 'TreeNode(val: {}, left: {}, right: {})'.format(self.val, self.left, self.right)

    @staticmethod
    def deserialize(string: str):
        if string == '{}':
            return None
        nodes = [None if val == 'null' else TreeNode(int(val))
                 for val in string.strip('[]{}').split(',')]
        kids = nodes[::-1]
        root = kids.pop()
        for node in nodes:
            if node:
                if kids: node.left = kids.pop()
                if kids: node.right = kids.pop()
        return root

    @staticmethod
    def drawtree(root):
        def height(root: TreeNode):
            return 1 + max(height(root.left), height(root.right)) if root else -1
        def jumpto(x: int, y: int):
            t.penup()
            t.goto(x, y)
            t.pendown()
        def draw(node: TreeNode, x: int, y: int, dx: int):
            if node:
                t.goto(x, y)
                jumpto(x, y-20)
                t.write(node.val, align='center', font=('Arial', 12, 'normal'))
                draw(node.left, x-dx, y-60, dx/2)
                jumpto(x, y-20)
                draw(node.right, x+dx, y-60, dx/2)
        import turtle
        t = turtle.Turtle()
        t.speed(0); turtle.delay(0)
        h = height(root)
        jumpto(0, 30*h)
        draw(root, 0, 30*h, 40*h)
        t.hideturtle()
        turtle.mainloop()


if __name__ == '__main__':
    print(TreeNode.deserialize('[1,2,3,null,null,4,null,null,5]'))
    # drawtree(deserialize('[2,1,3,0,7,9,1,2,null,1,0,null,null,8,8,null,null,null,null,7]'))

