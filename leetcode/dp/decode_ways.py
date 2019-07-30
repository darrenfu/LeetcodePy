class Solution:
    """
    https://leetcode.com/problems/decode-ways/discuss/30352/Accpeted-Python-DP-solution
    Runtime: 32 ms, faster than 95.42% (Space O(1))
    Runtime: 40 ms, faster than 54.20% (Space O(N))
    """
    def numDecodings(self, s: str) -> int:
        if s[0] == "0": return 0
        L = len(s)

        # Space Complexity: O(1)
        dp1 = dp2 = 1
        for i in range(1, L):
            if s[i] == "0" and (s[i-1] == "0" or s[i-1] >= "3"): return 0
            dp1, dp2 = [dp2, dp1] if s[i] == "0" else [dp2, dp2+dp1] if "10" <= s[i-1:i+1] <= "26" else [dp2, dp2]
        return dp2
        # Space Complexity: O(N)
        # dp = [1] + [0] * L
        # for i in range(1, L+1):
            # dp[i] += dp[i-1] if s[i-1] != "0" else 0
            # dp[i] += dp[i-2] if i != 1 and "10" <= s[i-2:i] <= "26" else 0
        # return dp[-1]


assert Solution().numDecodings(s="2") == 1
assert Solution().numDecodings(s="10") == 1
assert Solution().numDecodings(s="30") == 0
assert Solution().numDecodings(s="26") == 2
assert Solution().numDecodings(s="226") == 3
