from typing import List


class Solution:
    """
    Runtime: 48 ms, faster than 56.56%
    https://leetcode.com/problems/word-break/discuss/43808/Simple-DP-solution-in-Python-with-description
    """
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        L = len(s)
        dp = [False] * L
        for i in range(L):
            for w in wordDict:
                # current word matches,
                # and the previous part of str already matched: dp[i-len(w)]
                # or reaches the very left: i-len(w)+1 == 0
                if w == s[i-len(w)+1:i+1] and (dp[i-len(w)] or i-len(w)+1 == 0):
                    dp[i] = True
        return dp[-1]


print(Solution().wordBreak(s="catsandog", wordDict=["cat", "san", "dog", "cats", "an", "og", "and"]))
