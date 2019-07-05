class Solution(object):
    def colorBorder(self, grid, r0, c0, color):
        """
        :type grid: List[List[int]]
        :type r0: int
        :type c0: int
        :type color: int
        :rtype: List[List[int]]
        """
        n = len(grid)
        m = len(grid[0])
        border, seen = set(), set()

        def dfs(r, c):
            if not (0 <= r < n and 0 <= c < m and grid[r][c] == grid[r0][c0]):
                return False
            if (r, c) in seen:
                return True
            seen.add((r, c))
            if dfs(r + 1, c) + dfs(r - 1, c) + dfs(r, c + 1) + dfs(r, c - 1) < 4:
                border.add((r, c))
            return True

        dfs(r0, c0)
        for r, c in border:
            grid[r][c] = color
        return grid


print(Solution().colorBorder([[1,2,3],[1,2,3]], 1, 1, 1))
print(Solution().colorBorder([[1,1,1],[1,1,1],[1,1,1]], 1, 1, 2))

