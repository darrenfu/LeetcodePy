import random


class Solution(object):
    def minSteps(self, n):
        """
        :type n: int
        :rtype: int
        """
        if n == 1:
            return 0
        dp = [0] * (n+1)
        for i in range(2, n+1):
            dp[i] = i
            for j in range(i/2, 1, -1):
                if i % j == 0:
                    dp[i] = dp[j] + (i/j)
                    break
        return dp[n]


if __name__ == '__main__':
    s = Solution()
    for i in range(2):
        ran = random.randint(50, 1001)
        minStep = s.minSteps(ran)
        print "random_int: %d, min_steps: %d" % (ran, minStep)
