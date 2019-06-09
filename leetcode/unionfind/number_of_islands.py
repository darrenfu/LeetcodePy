from typing import List
from leetcode.unionfind.uf import UF


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid or not len(grid) or not len(grid[0]):
            return 0
        R = len(grid)
        C = len(grid[0])
        cnt = 0
        for i in range(R):
            for j in range(C):
                if grid[i][j] == '1':
                    cnt += 1
        # Special: uf.count (number of '1's is not equal to len(self.parents) in this case
        uf = UF(R * C, cnt)

        def getFlatIdx(i, j):
            return C * i + j

        directions = [[1, 0], [0, 1]]

        for i in range(R):
            for j in range(C):
                if grid[i][j] == '1':
                    for d in directions:
                        ii, jj = i + d[0], j + d[1]
                        if ii < R and jj < C and grid[ii][jj] == '1':
                            u, v = getFlatIdx(i, j), getFlatIdx(ii, jj)
                            # print((i,j), (ii,jj), u, v)
                            uf.union(u, v)
                            # print(uf.count)
        return uf.count


grid = [['0']]
ret = Solution().numIslands(grid)
print(ret)
grid = [
    ['1', '1', '1', '1', '0'],
    ['1', '1', '0', '0', '0'],
    ['0', '0', '0', '0', '0']
]
ret = Solution().numIslands(grid)
print(ret)
grid = [
    ['1', '1', '0', '0', '0'],
    ['1', '1', '0', '0', '0'],
    ['0', '0', '1', '0', '0'],
    ['0', '0', '0', '1', '1']
]
ret = Solution().numIslands(grid)
print(ret)
