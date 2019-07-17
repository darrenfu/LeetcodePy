from typing import List


class Solution:
    """
    Runtime: 48 ms, faster than 98.65%
    """
    def maxArea(self, height: List[int]) -> int:
        L = len(height)
        if L <= 1: return 0
        s, e, area, maxArea = 0, L-1, 0, 0
        while s < e:
            l, r = height[s], height[e]
            if l < r:
                area = l * (e-s)
                while height[s] <= l:
                    s += 1  # skip area calc for lower heights
            else:
                area = r * (e-s)
                while height[e] <= r and e:  # edge case check: e must be larger than zero!
                    e -= 1
            maxArea = max(area, maxArea)
        return maxArea


print(Solution().maxArea(height=[1,8,6,2,5,4,8,3,7]))

