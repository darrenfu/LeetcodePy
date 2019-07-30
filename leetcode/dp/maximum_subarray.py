from typing import List


class Solution:
    """
    Runtime: 76 ms, faster than 72.06%
    """
    def maxSubArray(self, nums: List[int]) -> int:
        L = len(nums)
        if L == 0: return 0
        if L == 1: return nums[0]
        dp = nums[0]
        res = nums[0]
        for i in range(1, L):
            if dp > 0: dp += nums[i]
            else: dp = nums[i]
            res = max(res, dp)
        return res


assert Solution().maxSubArray(nums=[-2,1,-3,4,-1,2,1,-5,4]) == 6
assert Solution().maxSubArray(nums=[-1]) == -1
assert Solution().maxSubArray(nums=[-2,1]) == 1
assert Solution().maxSubArray(nums=[-2,-1]) == -1
assert Solution().maxSubArray(nums=[-1,-2]) == -1
assert Solution().maxSubArray(nums=[1,2]) == 3
