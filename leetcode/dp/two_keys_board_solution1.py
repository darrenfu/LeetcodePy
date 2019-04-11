from collections import deque
import random


class Solution(object):
    def minSteps(self, n):
        """
        :type n: int
        :rtype: int
        """
        if n == 1:
            return 0
        # org_n = n
        prime_list = deque()
        # iteratively divide by 2
        while n % 2 == 0:
            prime_list.append(2)
            n = n / 2
        # iteratively divide by prime (prime > 2)
        for p in range(3, int(n ** 0.5) + 1, 2):
            while n % p == 0:
                prime_list.append(p)
                n = n / p
            # exit condition: n is divisible by all primes which is smaller than sqrt(n) + 1
            # e.g. 18 = 2 x 2 x 3, among which 2 < sqrt(18) + 1 and 3 < sqrt(18) + 1
            if n == 1:  # or if p > n:
                break
        # exit condition: largest_divisible_prime > sqrt(n) + 1
        # e.g. 820 = 2 x 2 x 5 x 41, among which 41 > sqrt(820) + 1
        if n > 2:
            prime_list.append(n)
            # print "%d leftover_n: %d = products of %s" % (org_n, n, prime_list)
        return sum(prime_list)


if __name__ == '__main__':
    s = Solution()
    for i in range(40):
        ran = random.randint(50, 1001)
        minStep = s.minSteps(ran)
        # print "random_int: %d, min_steps: %d" % (ran, minStep)
