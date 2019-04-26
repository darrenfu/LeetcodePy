"""
Tag: Airbnb, not in leetcode
"""


class ArrayWithPtrToNextArray(object):
    def __init__(self, size):
        self._size = size
        self.values = [None for _ in range(size)]
        # DO NOT USE the following way to initialize array, which will cause referring to the same Node()
        # return [Node()] * self._FIXED_SIZE
        self._next = None

    def is_at_tail(self, idx):
        return idx == self._size

    # getter
    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, next_array):
        self._next = next_array


class QueueWithFixedSizeOfArrays(object):

    def __init__(self, fixed_size):
        self._FIXED_SIZE = fixed_size
        self._count = 0
        # when queue is empty, head pointer is with tail
        self._head = self._tail = 0
        self._head_list = self._tail_list = ArrayWithPtrToNextArray(self._FIXED_SIZE)

    def enqueue(self, num):
        """
        :type num: int
        :rtype: void
        """
        # tail to enqueue
        if self._tail_list.is_at_tail(self._tail):
            new_list = ArrayWithPtrToNextArray(self._FIXED_SIZE)
            new_list.values[0] = num
            self._tail_list.next = new_list
            self._tail_list = new_list
            self._tail = 0
        else:
            self._tail_list.values[self._tail] = num
        self._tail += 1
        self._count += 1

    def dequeue(self):
        """
        :rtype: int
        :return:
        """
        # head to dequeue
        if not self._count:
            return None
        if self._head_list.is_at_tail(self._head):
            next_list = self._head_list.next
            self._head_list.next = None  # delete current array
            self._head_list = next_list
            self._head = 0
        num = self._head_list.values[self._head]
        self._head += 1
        self._count -= 1
        return num

    def __len__(self):
        return self._count

