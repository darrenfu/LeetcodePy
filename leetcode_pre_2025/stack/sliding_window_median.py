from typing import List
from bisect import bisect, insort


class Solution:

    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        def getMedian(arr: List[int], k:int) -> int:
            odd = k%2
            # in python 3, / means true division; // means truncating division
            return arr[k // 2] * 1.0 if odd else (arr[k // 2] + arr[(k - 1) // 2]) * .5

        # win is an array maintained in sorted order
        win, rv = nums[:k], []
        win.sort()
        for i, n in enumerate(nums[k:], start=k):
            median = getMedian(win, k)
            rv.append(median)
            # outgoing number is removed from the array using bisect: O(logK)
            idx = bisect(win, nums[i-k])  # faster than remove()
            win.pop(idx-1)
            # incoming number is added in sorted order in the array using insert: O(logK)
            insort(win, nums[i])
        # handle last median element
        median = getMedian(win, k)
        rv.append(median)
        print(rv)
        return rv


Solution().medianSlidingWindow([1,3,-1,-3,5,3,6,7], 3)
