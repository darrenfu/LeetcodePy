class Node(object):
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.freq = 1
        self.prev, self.next = None, None


class DLinkedList(object):
    def __init__(self):
        # head/tail dummy node
        self._sentinel = Node()
        self._sentinel.next = self._sentinel.prev = self._sentinel
        self._size = 0

    def __len__(self):
        return self._size

    def append(self, node):
        """
        insert at head

        :param node:
        :return:
        """
        node.next = self._sentinel.next
        node.prev = self._sentinel
        self._sentinel.next.prev = node
        self._sentinel.next = node
        self._size += 1

    def pop(self, node=None):
        if self._size == 0:
            return
        if not node:
            node = self._sentinel.prev
        node.next.prev = node.prev
        node.prev.next = node.next
        self._size -= 1
        return node
