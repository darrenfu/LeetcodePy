from typing import List


class Solution:
    def minMoves2(self, nums: List[int]) -> int:
        # Runtime: 40 ms, faster than 93.35%
        nums.sort()
        # largest diff (minus smallest) to smallest diff
        return sum(nums[~i] - nums[i] for i in range(len(nums) // 2))


nums = [1,2,3]
print(Solution().minMoves2(nums))
