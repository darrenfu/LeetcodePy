from typing import List


class Solution:
    """
    Runtime: 72 ms, faster than 5.38%
    https://leetcode.com/problems/maximum-product-subarray/discuss/48230/Possibly-simplest-solution-with-O(n)-time-complexity
    """
    def maxProduct(self, nums: List[int]) -> int:
        L = len(nums)
        dp = [(nums[0], nums[0])]
        res = dp[0][0]
        for i in range(1, L):
            prev = dp[i-1]
            v = nums[i]
            lmax = max(v, prev[0] * v, prev[1] * v)
            lmin = min(v, prev[0] * v, prev[1] * v)
            dp.append((lmax, lmin))
            res = max(res, lmax)
        return res


assert Solution().maxProduct(nums=[2,3,-2,4]) == 6
assert Solution().maxProduct(nums=[-2,0,-1]) == 0
