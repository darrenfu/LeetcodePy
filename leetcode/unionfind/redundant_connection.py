from typing import List
from src.main.python import UF


class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        N = len(edges)
        uf = UF(N)
        for edge in edges:
            if not uf.union(edge[0]-1, edge[1]-1):
                print(edge)
                return edge
        return []


edges = [[1,2], [1,3], [2,3]]
Solution().findRedundantConnection(edges)
edges = [[1,2], [2,3], [3,4], [1,4], [1,5]]
Solution().findRedundantConnection(edges)
