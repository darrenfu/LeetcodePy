from typing import List


class BinaryIndexTree(object):

    def __init__(self, nums: List[int]):
        self.N = len(nums)
        self.nums = nums[:]  # deep copy
        self.bit = [0] * (self.N + 1)

    def update(self, i: int) -> None:
        while i < self.N+1:
            self.bit[i] += 1
            i += BinaryIndexTree._lowbit(i)  # go to child node

    def getSum(self, i: int) -> int:
        ret = 0
        while i > 0:
            ret += self.bit[i]
            i -= BinaryIndexTree._lowbit(i)  # go to parent node
        return ret

    def countSmaller(self):
        ranks = {v: i + 1 for i, v in enumerate(sorted(self.nums))}
        res = []
        for x in reversed(self.nums):  # scan from right to left to count smaller numbers
            r = ranks[x]
            res.append(self.getSum(r - 1))
            self.update(r)
        return res[::-1]

    @staticmethod
    def _lowbit(x: int):
        return x & (-x)


class Solution:
    """
    Runtime: 160 ms, faster than 45.55%
    """
    def countSmaller(self, nums: List[int]) -> List[int]:
        bit = BinaryIndexTree(nums)
        return bit.countSmaller()


print(Solution().countSmaller(nums=[5, 2, 6, 1]))
