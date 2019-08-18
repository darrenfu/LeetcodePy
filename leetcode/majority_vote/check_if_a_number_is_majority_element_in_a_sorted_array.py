from typing import List
from bisect import *


class Solution:
    """
    https://leetcode.com/problems/check-if-a-number-is-majority-element-in-a-sorted-array/discuss/355470/Python%3A-Two-Ways-O(N)-and-O(logN)
    """
    def isMajorityElement(self, nums: List[int], target: int) -> bool:
        # Runtime: 36 ms, faster than 98.11%
        # return nums.count(target) > len(nums) // 2

        # Runtime: 48 ms, faster than 38.57%
        L = len(nums)
        if target != nums[L//2]:
            return False
        lo = bisect_left(nums, target)
        hi = bisect_right(nums, target)
        return hi - lo > L//2


assert Solution().isMajorityElement(nums=[2, 4, 5, 5, 5, 5, 5, 6, 6], target=5)
assert not Solution().isMajorityElement(nums=[10, 100, 101, 101], target=101)
