from leetcode.design.dlinkedlist import DLinkedList, Node
import collections


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


class LFUCache(object):

    def __init__(self, capacity):
        """
        Three things to maintain:

        1. a dict, named as `self._node`, for the reference of all nodes given key.
           That is, O(1) time to retrieve node given a key.

        2. Each frequency has a doubly linked list, store in `self._freq`, where key
           is the frequency, and value is an object of `DLinkedList`

        3. The min frequency through all nodes. We can maintain this in O(1) time, taking
           advantage of the fact that the frequency can only increment by 1. Use the following two rules:
           Rule 1: Whenever we see the size of the DLinkedList of current min frequency is 0, the min frequency must increment by 1.
           Rule 2: Whenever put in a new (key, value), the min frequency must 1 (the new node)

        :type capacity: int
        """
        self._size = 0
        self._capacity = capacity
        self._node = dict()  # (key,Node) pair
        # Using list as the `default_factory` (the arg of `defaultdict`), it is easy to group a sequence of
        # key-value pairs into a dictionary of lists
        self._freq = collections.defaultdict(DLinkedList)
        self._minfreq = 0

    def _update(self, node):
        """
        This is a helper function that used in the following two cases:
            1. when `get(key)` is called; and
            2. when `put(key, value)` is called and the key exists.

        The common point of these two cases is that:
            1. no new node comes in, and
            2. the node is visited one more times -> node.freq changed ->
               thus the place of this node will change

        The logic of this function is:
            1. pop the node from the old DLinkedList (with freq `f`)
            2. append the node to new DLinkedList (with freq `f+1`)
            3. if old DlinkedList has size 0 and self._minfreq is `f`,
               update self._minfreq to `f+1`

        All of the above operations took O(1) time.

        :type node: Node
        :rtype: void
        """
        freq = node.freq
        self._freq[freq].pop(node)
        if self._minfreq == freq and not self._freq[freq]:
            self._minfreq += 1
        self._freq[node.freq + 1].append(node)
        node.freq += 1

    def get(self, key):
        """
        Through checking self._node[key], we can get the node in O(1) time.
        Just performs self._update, then we can return the value of node.

        :type key: int
        :rtype: int
        """
        ret = -1
        if key in self._node:
            node = self._node[key]
            self._update(node)
            ret = node.value
        print("Get {} Return {}".format(key, ret))
        return ret

    def put(self, key, value):
        """
        If `key` already exists in `self._node`, we do the same operations as `get`, except updating the `node.value` to new value.
        Otherwise, the following logic will be performed:
        1. if the cache reaches its capacity, pop the least frequently used item *
        2. add new node to self._node
        3. add new node to the DLinkedList with frequency 1
        4. reset self._minfreq to 1

        * How to pop the least frequently used item? Two facts:
        1. we maintain self._minfreq, the minimum possible frequency in cache.
        2. All cache with the same frequency are stored as a DLinkedList, with recently used order (Always append at head)

        Consequence? => The tail of DLinkedList with self._minfreq is the least recently used one, pop it...

        :type key: int
        :type value: int
        :rtype: void
        """
        if self._capacity == 0:
            return
        if key in self._node:
            node = self._node[key]
            self._update(node)
            node.value = value
        else:
            if self._size == self._capacity:
                node = self._freq[self._minfreq].pop()
                del self._node[node.key]
                self._size -= 1
            node = Node(key, value)
            self._node[key] = node
            self._minfreq = 1
            self._freq[self._minfreq].append(node)
            self._size += 1


capacity = 2
cache = LFUCache(capacity)
cache.put(1, 1)
cache.put(2, 2)
cache.get(1)  # returns 1
cache.put(3, 3)  # evicts key 2
cache.get(2)  # returns -1 (not found)
cache.get(3)  # returns 3.
cache.put(4, 4)  # evicts key 1.
cache.get(1)  # returns -1 (not found)
cache.get(3)  # returns 3
cache.get(4)  # returns 4
