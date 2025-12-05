from typing import List


class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        Runtime: 60 ms, faster than 34.71%
        https://leetcode.com/problems/rotate-array/discuss/269948/4-solutions-in-python-(From-easy-to-hard)
        Solution #4
        """
        L = len(nums)
        k %= L

        def reverse(arr:List[int], start:int, end:int) -> None:
            p1, p2 = start, end
            while p1 < p2:
                tmp = arr[p1]
                arr[p1] = arr[p2]
                arr[p2] = tmp
                p1 += 1
                p2 -= 1

        reverse(nums, 0, L-1)
        reverse(nums, 0, k-1)
        reverse(nums, k, L-1)
        print(nums)


nums=[1,2,3,4,5,6,7]
Solution().rotate(nums, k=3)

nums=[-1,-100,3,99]
Solution().rotate(nums, k=2)
