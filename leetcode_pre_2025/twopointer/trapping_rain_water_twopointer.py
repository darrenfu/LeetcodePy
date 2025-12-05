from typing import List


class Solution:
    """
    Runtime: 40 ms, faster than 85.78%
    https://leetcode.com/problems/trapping-rain-water/discuss/17554/Share-my-one-pass-Python-solution-with-explaination
    the water volume of i: vol_i = min(left_max_i, right_max_i) - bar_i
    The left_max array from left to right is always non-descending, the right_max is non-ascending.
    Given i < j, if left_max_i <= right_max_j: vol_i = left_max_i - bar_i, otherwise, vol_j = right_max_j - bar_j
    """
    def trap(self, height: List[int]) -> int:
        L = len(height)
        if L < 3: return 0
        l, r = 0, L-1
        lmax, rmax, ans = height[l], height[r], 0
        while l < r:
            lmax, rmax = max(height[l], lmax), max(height[r], rmax)
            # lmax is non-descending, rmax is non-ascending
            if lmax < rmax:
                ans += lmax - height[l]
                l += 1
            else:
                ans += rmax - height[r]
                r -= 1
        return ans


print(Solution().trap(height=[0,1,0,2,1,0,1,3,2,1,2,1]))
