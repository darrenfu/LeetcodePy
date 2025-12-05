from typing import List
from collections import deque
import math


class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        if grid[0][0] == 1:
            return -1
        N = len(grid)

        def neighbor8(i:int, j:int) -> None:
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if di == dj == 0:
                        continue
                    newdi, newdj = i + di, j + dj
                    if 0 <= newdi < N and 0 <= newdj < N and grid[newdi][newdj] == 0:
                        yield (newdi, newdj)

        ds = [[math.inf] * N for _ in range(N)]
        queue = deque([(0, 0)])
        ds[0][0] = 1
        while queue:
            i, j = queue.popleft()
            if i == j == N - 1:
                return ds[N-1][N-1]
            for newi, newj in neighbor8(i, j):
                if ds[newi][newj] > ds[i][j] + 1:
                    ds[newi][newj] = ds[i][j] + 1
                    queue.append((newi, newj))
        return -1


grid = [[0,0,0],[1,1,0],[1,1,0]]
res = Solution().shortestPathBinaryMatrix(grid)
print(res)

