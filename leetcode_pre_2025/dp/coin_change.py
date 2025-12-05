from typing import List
import math


class Solution:
    """
    https://leetcode.com/problems/coin-change/discuss/77372/Clean-dp-python-code
    Runtime: 964 ms, faster than 85.26%
    """
    def coinChange(self, coins: List[int], amount: int) -> int:
        if not amount: return 0
        MAX=math.inf
        dp = [0] + [MAX] * amount
        for i in range(1, amount+1):
            dps = [dp[i-c] for c in coins if i-c>=0]
            dp[i] = min(dps) + 1 if dps else MAX
            #dp[i] = min(dp[i-c] if i-c>=0 else MAX for c in coins) + 1
        return [dp[-1], -1][dp[-1] == MAX]
        # return dp[-1] if dp[-1] != MAX else -1


assert Solution().coinChange(coins=[2147483647], amount=2) == -1
assert Solution().coinChange(coins=[1], amount=0) == 0
assert Solution().coinChange(coins=[2], amount=3) == -1
assert Solution().coinChange(coins=[2], amount=4) == 2
assert Solution().coinChange(coins=[1,2,5], amount=11) == 3
