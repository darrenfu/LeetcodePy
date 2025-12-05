class Solution(object):
    def minScoreTriangulation(self, A):
        """
        :type A: List[int]
        :rtype: int
        """
        # only pass in python3 in leetcode
        # import functools
        # @functools.lru_cache(None)
        # def dp(i, j):
        #     return min([dp(i, k) + dp(k, j) + A[i]*A[j]*A[k] for k in range(i+1, j)] or [0])
        # return dp(0, len(A)-1)

        cache = dict()

        def dp(i, j):
            if j - i == 1:
                cache[i, j] = 0
                return 0
            cache[i, j] = float('inf')
            for k in range(i+1, j):
                if (i, k) not in cache:
                    cache[i, k] = dp(i, k)
                if (k, j) not in cache:
                    cache[k, j] = dp(k, j)
                cache[i, j] = min(cache[i, k] + cache[k, j] + A[i] * A[j] * A[k], cache[i, j])
            return cache[i, j]
        return dp(0, len(A)-1)


if __name__ == '__main__':
    A = [35,73,90,27,71,80,21,33,33,13,48,12,68,70,80,36,66,3,70,58]
    print(Solution().minScoreTriangulation(A))
