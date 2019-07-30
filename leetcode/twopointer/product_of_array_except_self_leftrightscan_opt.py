from typing import List


class Solution:
    """
    Runtime: 92 ms, faster than 97.48%
    https://leetcode.com/problems/product-of-array-except-self/discuss/65625/Python-solution-(Accepted)-O(n)-time-O(1)-space
    """
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        L = len(nums)
        res = [1] * L
        prod = 1
        for i in range(L):
            res[i] = prod
            prod *= nums[i]
        prod = 1
        for i in range(L-1,-1,-1):
            res[i] *= prod
            prod *= nums[i]
        return res


print(Solution().productExceptSelf(nums=[1,2,3,4]))
