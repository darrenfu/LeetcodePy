class LRUCache(object):

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.hashmap = {}  # value: address of DoublyLinkedNode
        self.CAPACITY = capacity
        self.head, self.tail = None, None  # DoublyLinkedNode(0, 0), DoublyLinkedNode(0, 0)

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        ret = -1
        if key in self.hashmap:
            node = self.hashmap[key]
            # set to most frequent used Node
            node.remove_self()
            self.__post_remove_self__(node)
            node.add_at_head(self.head)
            self.__post_add_at_top__(node)
            ret = node.value
        print("Get {} Return {}".format(key, ret))
        return ret

    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: None
        """
        if key in self.hashmap:
            node = self.hashmap[key]
            node.value = value
            # set to most frequent used Node
            node.remove_self()
            self.__post_remove_self__(node)
            node.add_at_head(self.head)
            self.__post_add_at_top__(node)
        else:
            node = DoublyLinkedNode(key, value)
            # print("Before put: current map:{}, key:{}, value:{}, head:{}, tail:{}".format(list(self.hashmap.keys()), key, value,
            #                                                                              self.head.key if self.head else -1,
            #                                                                              self.tail.key if self.tail else -1))
            if len(self.hashmap) >= self.CAPACITY and self.tail:
                # evict least frequent node
                self.hashmap.pop(self.tail.key, None)
                self.tail.remove_self()
                self.__post_remove_self__(self.tail)
            # add most frequent used node
            self.hashmap[key] = node
            node.add_at_head(self.head)
            self.__post_add_at_top__(node)
            # print("After  put: current map:{}, key:{}, value:{}, head:{}, tail:{}".format(list(self.hashmap.keys()), key, value,
            #                                                                          self.head.key if self.head else -1,
            #                                                                          self.tail.key if self.tail else -1))

    def __post_add_at_top__(self, node):
        if self.head:
            self.head.left = node
        self.head = node
        if not self.tail:
            self.tail = self.head

    def __post_remove_self__(self, node):
        if not node.left:
            self.head = node.right
        if not node.right:
            self.tail = node.left


class DoublyLinkedNode(object):

    def __init__(self, key, value):
        """
        :param key: int
        :param value: int
        """
        self.left = None
        self.right = None
        self.value = value
        self.key = key

    def remove_self(self):
        #  reassign the right pointer
        if self.left:
            self.left.right = self.right
        #  reassign the left pointer
        if self.right:
            self.right.left = self.left

    def add_at_head(self, head):
        self.right = head
        self.left = None


# Your LRUCache object will be instantiated and called as such:
capacity = 2
cache = LRUCache(capacity)
cache.put(1, 1)
cache.put(2, 2)
cache.get(1)  # returns 1
cache.put(3, 3)  # evicts key 2
cache.get(2)  # returns -1 (not found)
cache.put(4, 4)  # evicts key 1
cache.get(1)  # returns -1 (not found)
cache.get(3)  # returns 3
cache.get(4)  # returns 4
