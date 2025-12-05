from typing import List


class Solution:
    def minMoves2(self, nums: List[int]) -> int:
        # Runtime: 48 ms, faster than 38.14%
        median = sorted(nums)[len(nums) // 2]
        return sum(abs(v - median) for v in nums)


nums = [1,2,3]
print(Solution().minMoves2(nums))
