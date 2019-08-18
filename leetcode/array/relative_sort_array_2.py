from typing import List

class Solution:
    def relativeSortArray(self, arr1: List[int], arr2: List[int]) -> List[int]:
        d = {num : i for i, num in enumerate(arr2)}
        return sorted(arr1, key=lambda a : (d.get(a, 4000), a))


print(Solution().relativeSortArray(arr1=[2,3,1,3,2,4,6,7,9,2,19], arr2 = [2,1,4,3,9,6]))
