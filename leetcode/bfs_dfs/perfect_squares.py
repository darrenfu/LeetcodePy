import collections
"""https://buptwc.com/2018/07/24/bfs%E7%B3%BB%E5%88%97%E8%AF%A6%E8%A7%A3/"""

class Solution(object):
    def numSquares(self, n):
        """
        :type n: int
        :rtype: int
        """
        q = collections.deque([n])
        visited = set()
        level = 0
        while q:
            for _ in range(len(q)):  # level by level
                cur = q.popleft()
                if not cur:  # exit condition: last node value is zero, return tree min depth
                    print(n, level)
                    return level
                for i in range(1, int(cur**0.5) + 1):
                    val = cur - i**2
                    if val not in visited:
                        q.append(val)
                        visited.add(val)
            level += 1

Solution().numSquares(12)
Solution().numSquares(13)

