from typing import List
from collections import Counter


class Solution:
    def maxEqualRowsAfterFlips(self, matrix: List[List[int]]) -> int:
        # if first number in row is 0, go with it; if 1 then flip all numbers in row
        # `tuple` is to make the list hashable in dictionary
        tuples = [tuple(cell ^ row[0] for cell in row) for row in matrix]
        # use counter to classify how many identical rows after flips
        ret = max(Counter(tuples).values())
        print(ret)
        return ret


matrix = [[0,0,0],[0,0,1],[1,1,0]]
Solution().maxEqualRowsAfterFlips(matrix)
