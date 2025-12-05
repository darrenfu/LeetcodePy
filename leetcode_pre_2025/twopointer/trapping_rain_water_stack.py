from typing import List


class Solution:
    """
    Runtime: 44 ms, faster than 62.15%
    https://leetcode.com/problems/trapping-rain-water/solution/
    https://leetcode.com/problems/trapping-rain-water/discuss/17414/a-stack-based-solution-for-reference-inspired-by-histogram
    Solution #3 Stack
    To implement this we use a stack that store the indices with decreasing bar height, once we find a bar who's height
    is larger, then let the top of the stack be bot, the cur bar is ir, and the previous bar is il.
    """
    def trap(self, height: List[int]) -> int:
        L = len(height)
        if L < 3: return 0
        i, stack, ans = 0, [], 0
        while i < L:
            if not len(stack) or height[i] <= height[stack[-1]]:
                stack.append(i)
                i += 1
            else:
                valley = height[stack.pop()]
                if not len(stack): continue
                lidx, ridx = stack[-1], i
                peak = min(height[lidx], height[ridx])
                distance = ridx - lidx - 1
                ans += (peak-valley) * distance
        return ans


print(Solution().trap(height=[0,1,0,2,1,0,1,3,2,1,2,1]))
