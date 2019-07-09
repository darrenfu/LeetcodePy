from typing import List


# Runtime: 148 ms, faster than 59.73%
class BinaryIndexTree(object):

    def __init__(self, nums: List[int]):
        self.N = len(nums)
        # skip index 0 as dummy placeholder
        self.nums = [0] * (self.N + 1)
        self.sums = [0] * (self.N + 1)
        for i, v in enumerate(nums):
            self.set(i+1, v)

    def set(self, i: int, val: int) -> None:
        diff = val - self.nums[i]
        self.nums[i] = val
        while i < self.N + 1:
            self.sums[i] += diff
            i += BinaryIndexTree._lowbit(i)  # go to child node

    def get(self, i: int) -> int:
        ret = 0
        while i > 0:
            ret += self.sums[i]
            i -= BinaryIndexTree._lowbit(i)  # go to parent node
        return ret

    @staticmethod
    def _lowbit(x: int):
        return x & (-x)


class NumArray:

    def __init__(self, nums: List[int]):
        self.bit = BinaryIndexTree(nums)

    def update(self, i: int, val: int) -> None:
        self.bit.set(i+1, val)

    def sumRange(self, i: int, j: int) -> int:
        return self.bit.get(j+1) - self.bit.get(i)


# Your NumArray object will be instantiated and called as such:
nums = [1, 3, 5]
obj = NumArray(nums)
print(obj.sumRange(i=0,j=2))
obj.update(i=1,val=2)
print(obj.sumRange(i=0,j=2))
