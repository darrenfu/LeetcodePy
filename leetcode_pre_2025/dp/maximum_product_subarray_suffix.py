from typing import List


class Solution:
    """
    Runtime: 56 ms, faster than 15.07%
    Calculate prefix product in A.
    Calculate suffix product in A.
    https://leetcode.com/problems/maximum-product-subarray/discuss/183483/Easy-and-Concise-Python
    """
    def maxProduct(self, nums: List[int]) -> int:
        A = nums
        B = A[::-1]
        for i in range(1, len(A)):
            A[i] *= (A[i - 1] or 1)
            B[i] *= (B[i - 1] or 1)
        return max(A + B)


assert Solution().maxProduct(nums=[2,3,-2,4]) == 6
assert Solution().maxProduct(nums=[-2,0,-1]) == 0
