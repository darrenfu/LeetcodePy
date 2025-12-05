from typing import List
import random


class Solution:
    def kClosest(self, points: List[List[int]], K: int) -> List[List[int]]:
        # https://leetcode.com/problems/k-closest-points-to-origin/discuss/220235/Java-Three-solutions-to-this-classical-K-th-problem.
        # quick select
        dist = lambda i: points[i][0]**2 + points[i][1]**2

        def sort(i: int, j: int, K: int) -> None:
            if i >= j: return
            pivot = random.randint(i, j)
            points[i], points[pivot] = points[pivot], points[i]
            mid = partition(i, j)
            if K < mid - i + 1:
                sort(i, mid - 1, K)
            elif K > mid - i + 1:
                sort(mid + 1, j, K - (mid - i + 1))

        def partition(i: int, j: int) -> int:
            """
            partition by pivot A[i], returning index mid
            ensure A[i] <= A[mid] <= A[j] for i < mid < j
            :param i:
            :param j:
            :return:
            """
            oi = i
            pivot = dist(i)
            i += 1
            while True:
                while i < j and dist(i) < pivot:
                    i += 1
                while i <= j and dist(j) >= pivot:
                    j -= 1
                if i >= j: break
                points[i], points[j] = points[j], points[i]
            points[oi], points[j] = points[j], points[oi]
            return j
        sort(0, len(points) - 1, K)
        return points[:K]


print(Solution().kClosest(points = [[1,3],[-2,2]], K = 1))
print(Solution().kClosest(points = [[3,3],[5,-1],[-2,4]], K = 2))
