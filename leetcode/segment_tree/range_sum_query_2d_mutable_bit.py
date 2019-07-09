from typing import List


# Runtime: 408 ms, faster than 33.02%
class BinaryIndexTree(object):

    def __init__(self, matrix: List[List[int]]):
        if not matrix:
            self.M = self.N = 0
        else:
            self.M = len(matrix)
            self.N = len(matrix[0])
        # skip index 0 as dummy placeholder
        self.matrix = [[0] * (self.N + 1) for _ in range(self.M + 1)]
        self.sums = [[0] * (self.N + 1) for _ in range(self.M + 1)]
        for i in range(self.M):
            for j in range(self.N):
                self.set(i+1, j+1, matrix[i][j])

    def set(self, r: int, c: int, val: int) -> None:
        diff = val - self.matrix[r][c]
        self.matrix[r][c] = val
        i = r
        while i < self.M+1:
            j = c
            while j < self.N+1:
                self.sums[i][j] += diff
                j += BinaryIndexTree._lowbit(j)  # go to child node
            i += BinaryIndexTree._lowbit(i)

    def get(self, r: int, c: int) -> int:
        ret = 0
        i = r
        while i > 0:
            j = c
            while j > 0:
                ret += self.sums[i][j]
                j -= BinaryIndexTree._lowbit(j)  # go to parent node
            i -= BinaryIndexTree._lowbit(i)
        return ret

    @staticmethod
    def _lowbit(x: int):
        return x & (-x)


class NumMatrix:

    def __init__(self, matrix: List[List[int]]):
        self.bit = BinaryIndexTree(matrix)

    def update(self, row: int, col: int, val: int) -> None:
        self.bit.set(row + 1, col + 1, val)

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return self.bit.get(row2 + 1, col2 + 1) + self.bit.get(row1, col1) - \
               self.bit.get(row2 + 1, col1) - self.bit.get(row1, col2 + 1)


# Your NumMatrix object will be instantiated and called as such:
matrix = [
    [3, 0, 1, 4, 2],
    [5, 6, 3, 2, 1],
    [1, 2, 0, 1, 5],
    [4, 1, 0, 1, 7],
    [1, 0, 3, 0, 5]
]
obj = NumMatrix(matrix)
print(obj.sumRegion(2, 1, 4, 3))
obj.update(row=3, col=2, val=2)
print(obj.sumRegion(2, 1, 4, 3))
