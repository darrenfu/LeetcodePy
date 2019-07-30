from typing import List


class Solution:
    """
    Runtime: 44 ms, faster than 62.15%
    https://leetcode.com/problems/trapping-rain-water/solution/
    Solution #2 DP
    """
    def trap(self, height: List[int]) -> int:
        L = len(height)
        if L < 3: return 0
        lmax, rmax, ans = [0]*L, [0]*L, 0
        lmax[0] = height[0]
        for i in range(1, L):
            lmax[i] = max(lmax[i-1], height[i])
        rmax[-1] = height[-1]
        for i in range(L-2, -1, -1):
            rmax[i] = max(rmax[i+1], height[i])
        for i in range(L):
            ans += min(lmax[i], rmax[i]) - height[i]
        return ans


print(Solution().trap(height=[0,1,0,2,1,0,1,3,2,1,2,1]))
