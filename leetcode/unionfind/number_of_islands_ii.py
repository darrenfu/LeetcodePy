from typing import List
from src.main.python import UF


class Solution:
    def numIslands2(self, m: int, n: int, positions: List[List[int]]) -> List[int]:
        grid = [[0 for _ in range(n)] for _ in range(m)]
        uf = UF(m * n, 0)

        def getFlatIdx(i, j):
            return n * i + j

        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        res = []
        input_set = set()
        for pos in positions:
            # edge case - dedupe
            x, y = pos[0], pos[1]
            if (x,y) in input_set:
                res.append(uf.count)
                continue
            input_set.add((x,y))
            grid[x][y] = 1
            uf.count += 1
            for direction in directions:
                u = x + direction[0]
                v = y + direction[1]
                if 0 <= u < m and 0 <= v < n and grid[u][v] == 1:
                    uf.union(getFlatIdx(x, y), getFlatIdx(u, v))
            res.append(uf.count)
        print(res)
        return res


m, n, positions = 3, 3, [[0,0], [0,1], [1,2], [2,1]]
ret = Solution().numIslands2(m, n, positions)
m, n, positions = 3, 3, [[0,0], [0,1], [1,2], [1,2]]
ret = Solution().numIslands2(m, n, positions)
m, n, positions = 8, 4, [[0,0],[7,1],[6,1],[3,3],[4,1]]
ret = Solution().numIslands2(m, n, positions)

