from typing import List


class Solution:
    """
    Runtime: 48 ms, faster than 56.56%
    https://leetcode.com/problems/word-break/discuss/43788/4-lines-in-Python
    """
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        """
        check whether the remaining string can be splitted using the dictionary
        """
        def check(s) -> bool:
            L = len(s)
            dp = [True]
            for i in range(1, L+1):
                dp += any(dp[j] and s[j:i] in wordDict for j in range(i)),
            return dp[-1]

        return check(s)


print(Solution().wordBreak(s="catsandog", wordDict=["cat", "san", "dog", "cats", "an", "og", "and"]))
