class Solution(object):
    def colorBorder(self, grid, r0, c0, color):
        """
        :type grid: List[List[int]]
        :type r0: int
        :type c0: int
        :type color: int
        :rtype: List[List[int]]
        """
        n, m = len(grid), len(grid[0])
        bfs, border, component = [[r0, c0]], set(), set([(r0, c0)])

        for r0, c0 in bfs:
            for i, j in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
                r, c = r0 + i, c0 + j
                if 0 <= r < n and 0 <= c < m and grid[r][c] == grid[r0][c0]:
                    if (r, c) not in component:
                        # add new square into connected component
                        bfs.append([r, c])
                        component.add((r, c))
                else:
                    border.add((r0, c0))

        for r, c in border:
            grid[r][c] = color
        return grid


print(Solution().colorBorder([[1,2,3],[1,2,3]], 1, 1, 1))
print(Solution().colorBorder([[1,1,1],[1,1,1],[1,1,1]], 1, 1, 2))

