class Solution(object):
    def updateMatrix(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: List[List[int]]
        """
        visited = set()
        q = []
        R = len(matrix)
        C = len(matrix[0])

        for r in range(R):
            for c in range(C):
                if matrix[r][c] == 0:
                    visited.add((r, c))
                    q.append((r, c))

        for r, c in q:
            for i, j in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
                x, y = r + i, c + j
                if 0 <= x < R and 0 <= y < C and (x, y) not in visited:
                    matrix[x][y] = matrix[r][c] + 1
                    visited.add((x, y))
                    q.append((x, y))
        return matrix
