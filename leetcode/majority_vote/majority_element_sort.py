from typing import List


class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        L = len(nums)
        return sorted(nums)[L//2]
