class Solution(object):
    def videoStitching(self, clips, T):
        """
        :type clips: List[List[int]]
        :type T: int
        :rtype: int
        """
        dp = [(T+1)] * (T+1)
        dp[0] = 0
        for i in range(0, T+1):
            for c in clips:
                if c[0] <= i <= c[1]:
                    print("%s, dp[%d]:%d, dp[%d]:%d, dp[%d]:%d" % (c, i, dp[i], c[0], dp[c[0]], i, min(dp[i], dp[c[0]] + 1)))
                    dp[i] = min(dp[i], dp[c[0]] + 1)
            if dp[i] == T + 1:
                return -1
        return dp[T]
