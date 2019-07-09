from typing import List, Iterator


class Solution:
    def minTotalDistance(self, grid: List[List[int]]) -> int:
        # In python 3, map() returns an iterator
        rowsum, rowcnt = list(map(sum, grid)), len(grid)
        transpose = zip(*grid)  # transposed matrix
        colsum, colcnt = list(map(sum, transpose)), len(grid[0])

        # Use Iterator - Runtime: 36 ms, faster than 96.70%
        def minTotalDistance1D(vec: Iterator[int], vec_len: int) -> int:
            d = L = R = 0
            i, j = -1, vec_len
            while i < j:
                if L < R:
                    i += 1
                    d += L
                    L += vec[i]
                else:
                    j -= 1
                    d += R
                    R += vec[j]
            return d

        return minTotalDistance1D(rowsum, rowcnt) + minTotalDistance1D(colsum, colcnt)


grid = [[1, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 1, 0, 0]]
print(Solution().minTotalDistance(grid))
