from typing import List


class Solution:
    """
    Runtime: 100 ms, faster than 81.20%
    """
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        L = len(nums)
        lp, rp, res = [1] * L, [1] * L, [1] * L
        prod = 1
        for i in range(L):
            lp[i] = prod
            prod *= nums[i]
        prod = 1
        for i in range(L-1,-1,-1):
            rp[i] = prod
            prod *= nums[i]
        for i in range(L):
            res[i] = lp[i] * rp[i]
        return res


print(Solution().productExceptSelf(nums=[1,2,3,4]))
