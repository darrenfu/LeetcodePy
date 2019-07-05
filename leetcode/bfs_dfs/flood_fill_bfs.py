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
        bfs = [[sr, sc]]
        area = set([(sr, sc)])

        for sr, sc in bfs:
            for i, j in [[1,0],[-1,0],[0,1],[0,-1]]:
                x, y = sr + i, sc + j
                if 0 <= x < m and 0 <= y < n and image[x][y] == image[sr][sc]:
                    if (x, y) not in area:
                        area.add((x, y))
                        bfs.append([x, y])

        for r, c in area:
            image[r][c] = newColor
        return image


print(Solution().floodFill([[1,2,3],[1,2,3]], 1, 1, 1))
print(Solution().floodFill([[1,1,1],[1,1,1],[1,1,1]], 1, 1, 2))

