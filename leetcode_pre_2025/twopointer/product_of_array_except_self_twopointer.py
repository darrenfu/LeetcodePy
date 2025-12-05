from typing import List


class Solution:
    """
    Runtime: 100 ms, faster than 81.20%
    https://leetcode.com/problems/product-of-array-except-self/discuss/65797/Consice-answer-in-Python
    """
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        L = len(nums)
        res = [1] * L
        p1 = p2 = 1
        for i in range(L):
            res[i] *= p1
            p1 *= nums[i]
            res[-i-1] *= p2
            p2 *= nums[-i-1]
        return res


print(Solution().productExceptSelf(nums=[1,2,3,4]))
