from typing import List


class Solution:
    """
    https://leetcode.com/problems/word-break/discuss/43995/A-Simple-Python-DP-solution
    """
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        """
        check whether the remaining string can be splitted using the dictionary
        """
        def check(s) -> bool:
            L = len(s)
            dp = [True] + [False] * L  # dp[i] means s[:i+1] can be segmented into words in the wordDicts
            for i in range(1, L+1):
                for j in range(i):
                    if dp[j] and s[j:i] in wordDict:
                        dp[i] = True
            return dp[-1]

        return check(s)


print(Solution().wordBreak(s="catsandog", wordDict=["cat", "san", "dog", "cats", "an", "og", "and"]))
