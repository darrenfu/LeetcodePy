class Solution:
    """
    Runtime: 36 ms, faster than 67.22%
    """
    def numTrees(self, n: int) -> int:
        dp = [0] * (n+1)
        dp[0], dp[1] = 1, 1  # empty tree, one-root tree
        for i in range(2, n+1):
            dp[i] = sum(dp[j-1] * dp[i-j] for j in range(1, i+1))
        return dp[n]


print(Solution().numTrees(n=3))
