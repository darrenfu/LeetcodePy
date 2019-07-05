class Solution(object):
    def floodFill(self, image, sr, sc, newColor):
        """
        :type image: List[List[int]]
        :type sr: int
        :type sc: int
        :type newColor: int
        :rtype: List[List[int]]
        """
        m, n = len(image), len(image[0])
        area = set()

        def dfs(x, y):
            if not (0 <= x < m and 0 <= y < n and image[x][y] == image[sr][sc]):
                return
            if (x, y) in area:
                return
            area.add((x,y))
            for i, j in [[1,0],[-1,0],[0,1],[0,-1]]:
                dfs(x+i, y+j)
        dfs(sr, sc)
        for r, c in area:
            image[r][c] = newColor
        return image


print(Solution().floodFill([[1,2,3],[1,2,3]], 1, 1, 1))
print(Solution().floodFill([[1,1,1],[1,1,1],[1,1,1]], 1, 1, 2))

