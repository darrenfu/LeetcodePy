from typing import List
from bisect import bisect_left


class Solution:
    """
    Traverse backwards, and insert each element in sorted order using binary search (do not need insort)
    Runtime: 108 ms, faster than 84.82%
    """
    def countSmaller(self, nums: List[int]) -> List[int]:
        sl = []
        ret = [0] * len(nums)
        for i, v in enumerate(reversed(nums)):
            idx = bisect_left(sl, v)  # Locate the insertion point for v in sl to maintain sorted order.
            sl.insert(idx, v)
            ret[i] = idx
        return ret[::-1]


print(Solution().countSmaller(nums=[5, 2, 6, 1]))
