class Solution(object):
    def maxSumAfterPartitioning(self, A, K):
        """
        :type A: List[int]
        :type K: int
        :rtype: int
        """
        from functools import lru_cache
        @lru_cache(None)
        def dp(i, j):
            if j - i <= K:
                return (j - i) * max(A[i:j])
            return max(dp(i, newj) + dp(newj, j) for newj in range(i+1, i+K+1))
        return dp(0, len(A))

    def maxSumAfterPartitioningIteration(self, A, K):
        N = len(A)
        dp = [0] * (N + K)
        for i in range(N):
            curMax = 0
            for k in range(1, min(K, i + 1) + 1):
                curMax = max(curMax, A[i - k + 1])
                dp[i] = max(dp[i], dp[i - k] + curMax * k)
        return dp[N - 1]
