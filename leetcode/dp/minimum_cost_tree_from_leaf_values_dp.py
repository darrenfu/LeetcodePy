from typing import List
import math


class Solution:
    """
    https://leetcode.com/problems/minimum-cost-tree-from-leaf-values/discuss/340004/Python-Easy-DP
    """
    def mctFromLeafValues(self, arr: List[int]) -> int:
        memo = {}

        def dp(i: int, j: int) -> int:  # j included
            if j <= i: return 0
            if (i, j) in memo:
                return memo[(i, j)]
            res = math.inf
            for k in range(i+1, j+1):
                # edge case: dp(i,i), dp(j, j)
                # edge case: max(arr[i:i+1]), max(arr[j:j+1]), i+1 and j+1 excluded
                res = min(res, dp(i, k-1) + dp(k, j) + max(arr[i:k]) * max(arr[k:j+1]))
            memo[(i, j)] = res
            return memo[(i, j)]
        return dp(0, len(arr)-1)  # L-1 included


print(Solution().mctFromLeafValues(arr=[6,2,4]))

