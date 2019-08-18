from typing import List


class Solution:
    """
    Runtime: 72 ms, faster than 6.83% using eval()
    Runtime: 44 ms, faster than 50.93% not using eval()
    """
    def diffWaysToCompute(self, input: str) -> List[int]:
        if input.isdigit():
            return [int(input)]
        res = []

        def op(left: int, right: int, op: str) -> int:
            if op == "+": return left+right
            if op == "-": return left-right
            return left*right
        for i in range(0, len(input)):
            if input[i] in "+-*":
                left = self.diffWaysToCompute(input[:i])
                right = self.diffWaysToCompute(input[i+1:])
                for j in left:
                    for k in right:
                        res += op(j, k, input[i]),
                        # res += int(eval("{}{}{}".format(j, input[i], k))),
        return res


print(Solution().diffWaysToCompute(input="2*3-4*5"))
