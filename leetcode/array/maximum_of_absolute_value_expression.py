from typing import List


class Solution:
    """
    max of |arr1[i] - arr1[j]| + |arr2[i] - arr2[j]| + |i - j|, aka:
    (+a1+a2+i) - (+b1+b2+j)
    (+a1-a2+i) - (+b1-b2+j)
    (-a1+a2+i) - (-b1+b2+j)
    (-a1-a2+i) - (-b1-b2+j)
    https://leetcode.com/problems/maximum-of-absolute-value-expression/discuss/340070/topic
    TODO: https://leetcode.com/problems/maximum-of-absolute-value-expression/discuss/339968/JavaC%2B%2BPython-Maximum-Manhattan-Distance
    """
    def maxAbsValExpr(self, arr1: List[int], arr2: List[int]) -> int:
        L = len(arr1)
        res = 0
        dp = [0] * L
        for j in [-1,1]:
            for k in [-1,1]:
                for i in range(L):
                    dp[i] = arr1[i]*j+arr2[i]*k+i
                res = max(res, max(dp) - min(dp))
        return res

print(Solution().maxAbsValExpr(arr1 = [1,-2,-5,0,10], arr2 = [0,-2,-1,-7,-4]))
