from typing import List
from leetcode.unionfind.uf import UF


class Solution:
    def minSwapsCouples(self, row: List[int]) -> int:
        N = len(row) // 2  # floor division
        uf = UF(N)
        for i in range(N):
            a, b = row[2*i], row[2*i+1]
            uf.union(a//2, b//2)
        res = N - uf.count
        print(res)
        return res


row = [0, 2, 1, 3]
Solution().minSwapsCouples(row)
row = [3, 2, 0, 1]
Solution().minSwapsCouples(row)
