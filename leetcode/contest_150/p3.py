from typing import List


class Solution:
    def maxDistance(self, grid: List[List[int]]) -> int:
        def isValidMove(x: int, y: int) -> bool:
            nonlocal M, N
            return 0 <= x < M and 0 <= y < N

        def checkSurroundings(i: int, j: int, searchVal: int) -> bool:
            nonlocal M, N
            for ii, jj in moves:
                x, y = i + ii, j + jj
                if isValidMove(x, y):
                    if searchVal == grid[x][y]:
                        return True
            return False

        M, N = len(grid), len(grid[0])
        # check all 1s or all 0s, return false
        initVal = grid[0][0]
        allSame = True
        for i in range(M):
            for j in range(N):
                if grid[i][j] != initVal:
                    allSame = False
                    break
            if not allSame:
                break
        if allSame:
            return -1

        # init queue to get all 0s near 1s
        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        q = []
        lvl = 1
        for i in range(M):
            for j in range(N):
                if grid[i][j] == 0 and checkSurroundings(i, j, 1):
                    q.append((i, j, lvl))
        # bfs
        traversed = dict()
        for i, j, _ in q:
            traversed[(i, j)] = 1
        while q:
            i, j, lvl = q.pop(0)
            for ii, jj in moves:
                x, y = i + ii, j + jj
                if isValidMove(x, y) and (x, y) not in traversed and not checkSurroundings(x, y, 1):
                    # print(x, y, lvl+1)
                    q.append((x, y, lvl + 1))
                    traversed[(x, y)] = 1
        return lvl


print(Solution().maxDistance(grid=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]))
print(Solution().maxDistance(grid=[[1,0,1],[0,0,0],[1,0,1]]))
