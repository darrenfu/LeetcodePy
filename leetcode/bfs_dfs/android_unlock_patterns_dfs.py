from typing import List


class Solution:
    """
    consist of minimum of m keys and maximum n keys
    """
    def numberOfPatterns(self, m: int, n: int) -> int:
        skip = {(1, 7): 4, (1, 3): 2, (1, 9): 5, (2, 8): 5, (3, 7): 5, (3, 9): 6, (4, 6): 5, (7, 9): 8}
        res = 0

        def dfs(used: List[int], prev: int) -> None:
            nonlocal res
            if len(used) >= m:
                res += 1
            if len(used) == n:
                return

            for i in range(1, 10):
                if i not in used:
                    # sort the vertices of the edge before lookup `skip`
                    edge = (min(prev, i), max(prev, i))
                    if edge not in skip or skip[edge] in used:
                        dfs(used + [i], i)

        for i in range(1, 10):
            dfs([i], i)
        return res


print(Solution().numberOfPatterns(1, 1))
