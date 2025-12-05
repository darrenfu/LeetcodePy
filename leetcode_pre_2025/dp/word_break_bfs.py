from typing import List


class Solution:
    """
    Runtime: 44 ms, faster than 78.28%
    https://leetcode.com/problems/word-break/discuss/43951/Python-BFS-beats-95
    """
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        queue = [0]
        L = len(s)
        visited = [False] * (L+1)
        # optimization: don't have to scan idx by idx, but only check matched word slots
        wlens = [l for l in set(map(len, wordDict))]

        while queue:
            start = queue.pop(0)
            for l in wlens:
                if s[start:start+l] in wordDict:
                    if start+l == L:  # end of str
                        return True
                    if not visited[start+l]:
                        visited[start+l] = True
                        queue.append(start+l)
        return False


print(Solution().wordBreak(s="catsandog", wordDict=["cat", "san", "dog", "cats", "an", "og", "and"]))
