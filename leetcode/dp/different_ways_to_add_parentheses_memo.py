from typing import List


class Solution:
    """
    Runtime: 40 ms, faster than 77.02%
    """
    def diffWaysToCompute(self, input: str) -> List[int]:
        cache = {}

        def op(left: int, right: int, op: str) -> int:
            if op == "+":
                return left + right
            elif op == "-":
                return left - right
            else:
                return left * right

        def dp(s: int, e: int) -> List[int]:
            nonlocal input
            if (s, e) in cache: return cache[(s, e)]
            if input[s:e].isdigit():
                cache[(s, e)] = [int(input[s:e])]
                return cache[(s, e)]
            res = []
            for i in range(s, e):
                if input[i] in "+-*":
                    left = dp(s, i)
                    right = dp(i + 1, e)
                    for j in left:
                        for k in right:
                            res += op(j, k, input[i]),
            cache[(s, e)] = res
            return res
        return dp(0, len(input))


print(Solution().diffWaysToCompute(input="2*3-4*5"))
