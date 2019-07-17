from typing import List


class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        L = len(numbers)
        p1, p2 = 0, L-1
        if L <= 1: return []
        while p1 < p2:
            diff = target - numbers[p1]
            if diff < numbers[p2]:
                p2 -= 1
            elif diff > numbers[p2]:
                p1 += 1
            else:
                return [p1+1,p2+1]
        return []
