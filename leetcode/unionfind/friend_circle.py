from typing import List
from src.main.python import UF


class Solution:
    def findCircleNum(self, M: List[List[int]]) -> int:
        N = len(M)
        uf = UF(N)
        for i in range(N):
            for j in range(i+1, N):
                if M[i][j]:  # merge as many direct friends as possible into clusters
                    uf.union(i, j)

        # how many root nodes after unions
        clusters = set()
        for i in range(N):
            clusters.add(uf.find(i))
        size = len(clusters)
        print(size)
        return size


M = [[1,1,0],
 [1,1,0],
 [0,0,1]]
Solution().findCircleNum(M)
M = [[1,1,0],
 [1,1,1],
 [0,1,1]]
Solution().findCircleNum(M)
