from typing import List
import heapq


class Solution:
    """
    Runtime: 148 ms, faster than 38.66%
    https://leetcode.com/problems/trapping-rain-water-ii/discuss/89472/Visualization-No-Code
    """
    def trapRainWater(self, heightMap: List[List[int]]) -> int:
        M = len(heightMap)
        if M == 0: return 0
        N = len(heightMap[0])
        heap, visited = [], set()

        # initially, put the boundary into min heap
        for i in [0, M - 1]:
            for j in range(N):
                heap.append((heightMap[i][j], i, j))
                visited.add((i, j))
        for j in [0, N - 1]:
            for i in range(M):
                if (i, j) not in visited:
                    heap.append((heightMap[i][j], i, j))
                    visited.add((i, j))
        heapq.heapify(heap)

        def isInGrid(x: int, y: int) -> bool:
            return 0 <= x < M and 0 <= y < N

        dxy = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        ans, mx = 0, 0
        while heap:
            # always traverse from smallest cell from top of min heap
            h, x, y = heapq.heappop(heap)
            # local water level
            mx = max(mx, h)

            for dx, dy in dxy:
                nx, ny = x + dx, y + dy
                if isInGrid(nx, ny) and (nx, ny) not in visited:
                    water = mx - heightMap[nx][ny]
                    if water > 0:
                        ans += water
                    heapq.heappush(heap, (heightMap[nx][ny], nx, ny))
                    visited.add((nx, ny))
        return ans


assert Solution().trapRainWater(heightMap=[
    [1, 4, 3, 1, 3, 2],
    [3, 2, 1, 3, 2, 4],
    [2, 3, 3, 2, 3, 1]
]) == 4
