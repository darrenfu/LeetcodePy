from typing import List


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0: return 0
        memo = [1] * n
        for i in range(1, n):
            for j in range(i):
                if nums[j] < nums[i]:
                    memo[i] = max(memo[i], memo[j] + 1)
        return max(memo)


nums = [10,9,2,5,3,7,101,18]
res = Solution().lengthOfLIS(nums)
print(res)
