from typing import List


class Solution:
    """
    https://leetcode.com/problems/count-of-range-sum/discuss/77990/Share-my-solution
    Or: https://leetcode.com/problems/count-of-range-sum/discuss/77991/Short-and-simple-O(n-log-n)
    Runtime: 188 ms, faster than 62.82%
    """
    def countRangeSum(self, nums: List[int], lower: int, upper: int) -> int:
        def mergesort(lo: int, hi: int) -> int:
            mid = (lo + hi) // 2
            if mid == lo: return 0
            count = mergesort(lo, mid) + mergesort(mid, hi)
            j = k = mid
            for left in sums[lo: mid]:
                while k < hi and sums[k] - left < lower: k += 1
                while j < hi and sums[j] - left <= upper: j += 1
                count += j - k
            sums[lo:hi] = sorted(sums[lo:hi])  # Pythonic
            return count

        sums = [0]
        for v in nums:
            sums.append(sums[-1] + v)
        return mergesort(0, len(sums))


print(Solution().countRangeSum(nums=[-2, 5, -1], lower=-2, upper=2))
print(Solution().countRangeSum(nums=[2147483647,-2147483648,-1,0], lower=-1, upper=0))
