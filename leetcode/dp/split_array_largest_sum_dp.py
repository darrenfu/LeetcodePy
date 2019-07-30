from typing import List
import math


class Solution:
    """
    Memorization + Cumulative Sum (Only Memorization will TLE)
    Runtime: 2280 ms, faster than 5.56%
    """
    def splitArray(self, nums: List[int], m: int) -> int:
        L = len(nums)
        # dp = defaultdict(dict)
        dp = [[0] * (m+1) for _ in range(L+1)]
        # Cumulative Sum
        cums = [0]
        for x in nums:
            cums.append(cums[-1] + x)

        def helper(i: int, m: int) -> int:
            nonlocal L
            if i == L:
                return 0
            if m == 1:
                return sum(nums[i:])
            # if i in dp and m in dp[i]:
            if dp[i][m] > 0:
                return dp[i][m]
            dp[i][m] = math.inf
            for j in range(1, L+1):
                # optimization: sum(nums[a:b]) = cums[b] - cums[a]
                l, r = cums[i+j] - cums[i], helper(i+j, m-1)
                dp[i][m] = min(dp[i][m], max(l, r))
                if l > r:
                    break
            return dp[i][m]

        return helper(0, m)


print(Solution().splitArray(nums=[7,2,5,10,8], m=2))

