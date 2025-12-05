from typing import List


class Solution:
    """
    Runtime: 432 ms, faster than 67.06%
    Bottom up
    https://leetcode.com/problems/burst-balloons/discuss/76243/Python-DP-N3-Solutions
    """
    def maxCoins(self, nums: List[int]) -> int:
        nums = [1] + nums + [1]
        L = len(nums)
        dp = [[0] * L for _ in range(L)]
        for gap in range(2, L):  # enumerate gap allowable values between 2 to L-1
            for i in range(L-gap):  # one side of the gap
                j = i + gap  # the other side of the gap
                for k in range(i+1, j):  # i and j exclusive
                    dp[i][j] = max(dp[i][j], nums[i]*nums[k]*nums[j] + dp[i][k] + dp[k][j])
        return dp[0][L-1]  # i=0, j=L-1 (gap: L-1)


print(Solution().maxCoins(nums=[3,1,5,8]))
