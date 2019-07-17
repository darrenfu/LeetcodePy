from typing import List
import math


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        L, res = len(nums), 1
        if L <= 1:
            return L

        p1, p2, last_val = L - 2, L - 1, nums[-1]
        while p1 >= 0:
            if nums[p1] != last_val:
                p2 = p1
                last_val = nums[p1]
                res += 1
            else:
                del nums[p2]
                p2 -= 1
            p1 -= 1
        return res
