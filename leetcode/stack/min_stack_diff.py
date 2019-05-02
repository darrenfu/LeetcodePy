class MinStack(object):

    def __init__(self):
        """
        initialize your data structure here.
        """
        self.stack = list()
        self.count = 0
        self.min = 0

    def push(self, x):
        """
        :type x: int
        :rtype: None
        """
        if not self.count:
            self.stack.append(0)
            self.min = x
        else:
            self.stack.append(x - self.min)
            if self.min > x:
                self.min = x
        self.count += 1

    def pop(self):
        """
        :rtype: None
        """
        if not self.count:
            return
        top = self.stack.pop()
        if top < 0:
            self.min -= top  # if top is negative, increase min value
        self.count -= 1

    def top(self):
        """
        :rtype: int
        """
        if not self.count:
            return None
        top = self.stack[-1]
        if top < 0:
            return self.min
        return top + self.min

    def getMin(self):
        """
        :rtype: int
        """
        return self.min

