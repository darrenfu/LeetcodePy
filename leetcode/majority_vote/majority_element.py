from typing import List
import math


"""
Runtime: 216 ms, faster than 14.54%
"""
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        candidate = math.inf
        cnt = 0
        for v in nums:
            if candidate == v:
                cnt += 1
            elif cnt == 0:
                candidate = v
                cnt += 1
            else:
                cnt -= 1
        # there always exists a candidate
        return candidate
