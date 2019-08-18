from typing import List


class Solution:
    def minSwaps(self, data: List[int]) -> int:
        cntOne = 0
        L = len(data)
        for i, v in enumerate(data):
            if v == 1:
                cntOne += 1

        for i in range(cntOne, L):
            # count zeros
            # move window to get the min zeros

