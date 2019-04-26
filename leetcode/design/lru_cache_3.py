from leetcode.design.dlinkedlist import DLinkedList, Node


class LRUCache(object):

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self._size = 0
        self._capacity = capacity
        self._node = dict()
        self._dlist = DLinkedList()

    def _update(self, node):
        """
        Move the node to the head

        :type node: Node
        :rtype: void
        """
        self._dlist.pop(node)
        self._dlist.append(node)

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        node = self._node.get(key, None)
        ret = -1
        if node:
            self._update(node)
            ret = node.value
        print("Get {} Return {}".format(key, ret))
        return ret

    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: void
        """
        if self._capacity == 0:
            return
        node = self._node.get(key)
        if node:
            self._update(node)
            node.value = value
        else:
            new_node = Node(key, value)
            self._node[key] = new_node
            self._dlist.append(new_node)
            self._size += 1
            if self._size > self._capacity:
                # pop the tail
                node = self._dlist.pop()
                del self._node[node.key]
                self._size -= 1


capacity = 2
_node = LRUCache(capacity)
_node.put(1, 1)
_node.put(2, 2)
_node.get(1)  # returns 1
_node.put(3, 3)  # evicts key 2
_node.get(2)  # returns -1 (not found)
_node.put(4, 4)  # evicts key 1
_node.get(1)  # returns -1 (not found)
_node.get(3)  # returns 3
_node.get(4)  # returns 4
