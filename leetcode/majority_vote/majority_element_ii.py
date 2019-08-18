from typing import List
import math

class Solution:
    """
    Runtime: 136 ms, faster than 74.29%
    https://leetcode.com/problems/majority-element-ii/discuss/63520/Boyer-Moore-Majority-Vote-algorithm-and-my-elaboration
    """
    def majorityElement(self, nums: List[int]) -> List[int]:
        if not nums:
            return []

        L = len(nums)

        def majorityVoting() -> (int, int):
            # scan once to find the top two candidates
            candidate1, candidate2 = math.inf, math.inf
            cnt1, cnt2 = 0, 0
            for v in nums:
                if candidate1 == v:
                    cnt1 += 1
                elif candidate2 == v:
                    cnt2 += 1
                elif cnt1 == 0:
                    candidate1 = v
                    cnt1 = 1
                elif cnt2 == 0:
                    candidate2 = v
                    cnt2 = 1
                else:
                    cnt1 -= 1
                    cnt2 -= 1
            return [(candidate1, cnt1), (candidate2, cnt2)]

        (candidate1, cnt1), (candidate2, cnt2) = majorityVoting()
        return [n for n in (candidate1, candidate2) if nums.count(n) > L//3]


print(Solution().majorityElement(nums=[0,0,0]))
print(Solution().majorityElement(nums=[3,2,3]))
print(Solution().majorityElement(nums=[1,1,1,3,3,2,2,2]))
