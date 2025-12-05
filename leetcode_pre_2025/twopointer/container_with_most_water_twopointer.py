from typing import List


class Solution:
    """
    Runtime: 64 ms, faster than 60.40%
    """
    def maxArea(self, height: List[int]) -> int:
        L = len(height)
        if L <= 1: return 0
        s, e, maxArea = 0, L-1, 0
        while s < e:
            maxArea = max(maxArea, min(height[s], height[e]) * (e-s))
            if height[s] < height[e]:  # important for pointer move!
                s += 1
            else:
                e -= 1
        return maxArea


print(Solution().maxArea(height=[1,8,6,2,5,4,8,3,7]))

