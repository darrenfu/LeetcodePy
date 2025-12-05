from typing import List


class Solution:
    """
    https://leetcode.com/problems/count-of-range-sum/discuss/77990/Share-my-solution
    Check chipbk10's comments in Page 2
    Same logic to count_of_range_sum
    Runtime: 1160 ms, faster than 92.34%
    """
    def reversePairs(self, nums: List[int]) -> int:
        def mergesort(lo: int, hi: int) -> int:
            mid = (lo + hi) // 2
            if mid == lo: return 0
            count = mergesort(lo, mid) + mergesort(mid, hi)
            j = mid
            for left in nums[lo: mid]:
                while j < hi and 2*nums[j] - left < 0: j += 1
                count += j - mid
            nums[lo:hi] = sorted(nums[lo:hi])
            return count

        return mergesort(0, len(nums))


print(Solution().reversePairs(nums=[1,3,2,3,1]))
print(Solution().reversePairs(nums=[2,4,3,5,1]))
