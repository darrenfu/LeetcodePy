class Solution:
    def numRollsToTarget(self, d: int, f: int, target: int) -> int:
        memo = {}

        def helper(d: int, target: int) -> int:
            nonlocal f
            if target < 0:
                return 0
            if d == 0:
                if target == 0:
                    return 1
                else:
                    return 0
            if (d, target) in memo:
                return memo[d, target]
            res = 0
            for v in range(f, 0, -1):
                res += helper(d-1, target - v)
            memo[d, target] = res
            return res
        return helper(d, target) % (10**9 + 7)


print(Solution().numRollsToTarget(d=1, f=6, target=3))
print(Solution().numRollsToTarget(d=2, f=6, target=7))
print(Solution().numRollsToTarget(d=2, f=5, target=10))
print(Solution().numRollsToTarget(d=1, f=2, target=3))
print(Solution().numRollsToTarget(d=30, f=30, target=500))
