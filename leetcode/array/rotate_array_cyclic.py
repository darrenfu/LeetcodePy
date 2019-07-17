from typing import List


class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        Runtime: 52 ms, faster than 78.53%
        https://leetcode.com/problems/rotate-array/discuss/269948/4-solutions-in-python-(From-easy-to-hard)
        Solution #3
        """
        L = len(nums)
        k %= L
        start, cur, prev, count = 0, 0, 0, 0
        while count < L:  # important! jump times should equal to L eventually
            prev = nums[start]
            cur = start
            while True:
                next = (cur + k) % L  # move k steps to the right (or cyclically to the very left)
                tmp = nums[next]
                nums[next] = prev
                prev = tmp

                cur = next
                count += 1  # jump times ++
                if start == cur:
                    break
            start += 1
        print(nums)


nums=[1,2,3,4,5,6,7]
Solution().rotate(nums, k=3)

nums=[-1,-100,3,99]
Solution().rotate(nums, k=2)
