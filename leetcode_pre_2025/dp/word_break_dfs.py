from typing import List


class Solution:
    """
    Runtime: 56 ms, faster than 23.77%
    https://leetcode.com/problems/word-break/discuss/130922/python-DFS-98
    """
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        start = 0
        stack, visited = [start], set()
        # wlens = [l for l in set(map(len, wordDict))]
        # print(wlens)
        while stack:
            start = stack.pop()
            if start in visited:
                continue
            else:
                visited.add(start)
            for i, w in enumerate(wordDict):
                if s[start:].startswith(w):
                    l = len(w)
                    if l == len(s[start:]):  # it's the last matched word in the sentence
                        return True
                    stack.append(start + l)  # dfs on s[start+l:]
        return False


print(Solution().wordBreak(s="catsandog", wordDict=["cat", "san", "dog", "cats", "an", "og", "and"]))
