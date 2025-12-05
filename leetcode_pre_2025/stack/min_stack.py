class Node(object):

    def __init__(self, value):
        self.value = value
        # store local min value in each element of the stack
        # benefit: even if I pop the top elements, the local min will still be stored in bottom elements
        self.min = value


class MinStack(object):

    def __init__(self):
        """
        initialize your data structure here.
        """
        self.stack = list()
        self.count = 0

    def push(self, x):
        """
        :type x: int
        :rtype: None
        """
        new_node = Node(x)
        if self.count:
            top = self.stack[-1]
            if new_node.min > top.min:
                new_node.min = top.min
        self.stack.append(new_node)
        self.count += 1

    def pop(self):
        """
        :rtype: None
        """
        if self.count:
            self.stack.pop()
            self.count -= 1

    def top(self):
        """
        :rtype: int
        """
        if self.count:
            return self.stack[-1].value
        return None

    def getMin(self):
        """
        :rtype: int
        """
        if self.count:
            return self.stack[-1].min
        else:
            return None
