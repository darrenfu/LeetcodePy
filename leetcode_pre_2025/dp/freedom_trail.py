class Node:
    def __init__(self, val: str):
        self.val = str
        # DLL
        self.next = self
        self.prev = self


class Solution:
    def findRotateSteps(self, ring: str, key: str) -> int:
        L = len(ring)
        KL = len(key)
        halfL = L // 2 if L % 2 == 0 else (L // 2 + 1)
        cur = prev = dummy = Node('')
        for ch in ring:
            cur = Node(ch)
            cur.prev = prev
            prev.next = cur
        cur.next = dummy.next
        dummy.next.prev = cur

        res = 0

        def dp(curNode: Node, nextKeyIdx: int):
            nonlocal halfL, L, res
            if nextKeyIdx == KL:
                return 1
            distance = 0
            minDis1, minDis2 = 0, 0
            nextNode = curNode
            for distance in range(halfL+1):
                res += 1
                if nextNode.val == key[nextKeyIdx]:
                    res += 1  # spell takes one step
                    res += dp(curNode.next, nextKeyIdx + 1)
                curNode.next = nextNode
                nextNode.prev = curNode
