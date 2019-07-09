from typing import List


class Solution:
    """
    consist of minimum of m keys and maximum n keys
    Runtime: 416 ms, faster than 78.53%
    """
    def numberOfPatterns(self, m: int, n: int) -> int:
        skip = {(1, 7): 4, (1, 3): 2, (1, 9): 5, (2, 8): 5, (3, 7): 5, (3, 9): 6, (4, 6): 5, (7, 9): 8}
        res = 0

        def dfs(visited: List[int], prev: int) -> None:
            nonlocal res
            if len(visited) >= m:
                res += 1
            if len(visited) == n:
                return

            for i in range(1, 10):
                if i not in visited:
                    # sort the vertices of the edge before lookup `skip`
                    edge = (min(prev, i), max(prev, i))
                    if edge not in skip or skip[edge] in visited:
                        dfs(visited + [i], i)

        # for i in range(1, 10):  # Runtime: 1092 ms, faster than 45.76%
        for i in [1, 2, 5]:
            if i == 5:
                res *= 4
            dfs([i], i)
        return res


print(Solution().numberOfPatterns(1, 1))
