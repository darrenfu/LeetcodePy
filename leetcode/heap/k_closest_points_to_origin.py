from typing import List
import heapq


class Solution:
    def kClosest(self, points: List[List[int]], K: int) -> List[List[int]]:
        def dis(f):
            return lambda args: f(*args)
        return heapq.nsmallest(K, points, dis(lambda x, y: x*x + y*y))


print(Solution().kClosest(points = [[1,3],[-2,2]], K = 1))
print(Solution().kClosest(points = [[3,3],[5,-1],[-2,4]], K = 2))
