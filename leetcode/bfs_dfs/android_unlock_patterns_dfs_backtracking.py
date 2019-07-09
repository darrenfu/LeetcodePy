class Solution:
    """
    consist of minimum of m keys and maximum n keys
    Runtime: 320 ms, faster than 90.68%
    """
    def numberOfPatterns(self, m: int, n: int) -> int:
        pass_keys = dict()
        edges = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7)]
        for p1, p2, p3 in edges:
            pass_keys[(p1, p3)] = p2
            pass_keys[(p3, p1)] = p2

        visited, res = set(), 0

        def dfs(prev: int) -> None:
            nonlocal res
            if m <= len(visited) <= n:
                res += 1
            if len(visited) == n:
                return
            for nxt in range(1, 10):
                if nxt not in visited:
                    ps = pass_keys[(prev, nxt)]
                    if ps is None or ps in visited:
                        visited.add(nxt)
                        dfs(nxt)
                        visited.remove(nxt)

        for start in [1,2,5]:
            if start == 5:  # 1,3,7,9 are symmetric, 2,4,6,8 are also symmetric
                res *= 4
            visited.add(start)
            dfs(start)
            visited.remove(start)
        return res


print(Solution().numberOfPatterns(1, 1))
