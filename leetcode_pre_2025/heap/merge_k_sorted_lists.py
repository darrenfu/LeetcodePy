from typing import List
from heapq import *

# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    """
    Runtime: 112 ms, faster than 79.52%
    Time: O(nklog(k))
    """
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        # Python3 Only:
        # If two elements have the same val, the next tuple items will be compared.
        # "i" below is guaranteed to be unique.
        minHeap = [(head.val, head) for i, head in enumerate(lists) if head]
        head = curNode = ListNode(0)
        heapify(minHeap)
        while minHeap:
            v, i, node = minHeap[0]
            if node.next:
                heapreplace(minHeap, (node.next.val, node.next))
            else:
                heappop(minHeap)
            curNode.next = node
            curNode = curNode.next
        return head.next

