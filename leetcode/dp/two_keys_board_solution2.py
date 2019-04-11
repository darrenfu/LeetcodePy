import random


class Solution(object):
    def minSteps(self, n):
        """
        :type n: int
        :rtype: int
        """
        if n == 1:
            return 0
        lf = self.largestFactor(n)
        return self.minSteps(lf) + n / lf

    def largestFactor(self, n):
        for d in range(n/2, 1, -1):
            if n % d == 0:
                return d
        return 1


if __name__ == '__main__':
    s = Solution()
    for i in range(40):
        ran = random.randint(50, 1001)
        minStep = s.minSteps(ran)
        # print "random_int: %d, min_steps: %d" % (ran, minStep)
