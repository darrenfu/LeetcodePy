from typing import List


class Solution:
    def duplicateZeros(self, arr: List[int]) -> None:
        """
        Do not return anything, modify arr in-place instead.
        """
        L = len(arr)
        i = 0
        while i < L:
            if arr[i] == 0:
                i += 1
                arr.insert(i, 0)
            i += 1
        for _ in range(L, len(arr)):
            arr.pop(-1)


# arr = [1,0,2,3,0,4,5,0]
arr = [1,2,3]
Solution().duplicateZeros(arr)
print(arr)
