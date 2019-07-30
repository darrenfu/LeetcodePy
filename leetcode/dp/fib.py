class Solution:
    def fib(self, N: int) -> int:
        if N <= 1: return N
        dp = [0, 1] + [0] * (N-1)
        for i in range(2, N+1):
            dp[i] = dp[i-1] + dp[i-2]
        return dp[-1]


assert Solution().fib(N=0) == 0
assert Solution().fib(N=1) == 1
assert Solution().fib(N=2) == 1
assert Solution().fib(N=3) == 2
assert Solution().fib(N=30) == 832040
