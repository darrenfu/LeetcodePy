from typing import List


class Solution:
    """
    Runtime: 744 ms, faster than 27.35%
    Top down
    dp[i][j] = max(dp[i][j], nums[i] * nums[k] * nums[j] + dp[i][k] + dp[k][j]) # i < k < j
    https://leetcode.com/problems/burst-balloons/discuss/76243/Python-DP-N3-Solutions
    """
    def maxCoins(self, nums: List[int]) -> int:
        nums = [1] + nums + [1]
        L = len(nums)
        dp = [[0] * L for _ in range(L)]

        def helper(s: int, e: int) -> int:
            # exit condition: e = s+1, gap < 2
            if dp[s][e] > 0 or e == s + 1: return dp[s][e]
            coins = 0
            for i in range(s+1, e):
                adjMulti = nums[s] * nums[i] * nums[e]
                coins = max(coins, helper(s,i) + helper(i,e) + adjMulti)
            dp[s][e] = coins
            return coins
        res = helper(0, L-1)
        return res


print(Solution().maxCoins(nums=[3,1,5,8]))
