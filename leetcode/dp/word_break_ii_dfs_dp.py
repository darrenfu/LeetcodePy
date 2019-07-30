from typing import List


class Solution:
    """
    Runtime: 136 ms, faster than 5.08%
    https://leetcode.com/problems/word-break-ii/discuss/44368/Python-easy-to-understand-solution-(DP%2BDFS%2BBacktracking).
    """
    def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
        res = []
        """
        check whether the remaining string can be splitted using the dictionary
        """
        def check(s) -> bool:
            L = len(s)
            dp = [True] + [False] * L
            for i in range(1, L+1):
                for j in range(i):
                    if dp[j] and s[j:i] in wordDict:
                        dp[i] = True
            return dp[-1]

        def dfs(s: str, path: str) -> None:
            if check(s):  # pruning before dfs to decrease unnecessary computation
                if not s:
                    res.append(path[:-1])  # [:-1] remove last space
                    return  # backtracking
                for i in range(1, len(s)+1):
                    if s[:i] in wordDict:  # if the first part matches in dict
                        dfs(s[i:], path+s[:i]+" ")  # dfs by checking the rest part, and append first part to path
        dfs(s, '')
        return res


Solution().wordBreak(s="catsandog", wordDict=["cat", "san", "dog", "cats", "an", "og", "and"])
