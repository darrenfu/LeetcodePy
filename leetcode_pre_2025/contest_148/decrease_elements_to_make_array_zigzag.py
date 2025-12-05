from typing import List
import math


class Solution:
    """
    TODO
    """
    def movesToMakeZigzag(self, nums: List[int]) -> int:
        L = len(nums)
        if L <= 1: return 0
        arr = [0] * (L-1)

        def cmp(a: int, b: int) -> int:
            if a > b: return 1
            if a < b: return -1
            return 0
        for i in range(1, L):
            arr[i-1] = cmp(nums[i], nums[i-1])
        print(arr)
        sm = 0
        q = -999
        for j in range(L-1):
            sm += arr[j]
            if sm == 2 or sm == -2 or arr[j] == 0:
                q = j
                break
        if q == -999: return 0
        if q == 0 or q == L - 2:
            return int(math.fabs(nums[q+1] - nums[q])) + 1
        return min(int(math.fabs(nums[q+1] - nums[q])), int(math.fabs(nums[q - 1] - nums[q]))) + 1


# print(Solution().movesToMakeZigzag(nums=[2,2]))
# print(Solution().movesToMakeZigzag(nums=[1,2,1]))
# print(Solution().movesToMakeZigzag(nums=[1,2,3]))
# print(Solution().movesToMakeZigzag(nums=[9,6,1,6,2]))
# print(Solution().movesToMakeZigzag(nums=[6,6,1,6,2]))
print(Solution().movesToMakeZigzag(nums=[7,4,8,9,7,7,5]))

