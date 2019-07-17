from typing import List
from collections import Counter

class Solution:
    def relativeSortArray(self, arr1: List[int], arr2: List[int]) -> List[int]:
        dct = Counter(i for i in arr1 if i in arr2)
        rest = sorted(i for i in arr1 if i not in arr2)
        l = [[i] * dct[i] for i in arr2]
        res1 = [item for sublist in l for item in sublist]
        return res1 + rest


print(Solution().relativeSortArray(arr1=[2,3,1,3,2,4,6,7,9,2,19], arr2 = [2,1,4,3,9,6]))
