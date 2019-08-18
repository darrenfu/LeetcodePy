from typing import List
"""
DFS backtracking
Runtime: 1120 ms, faster than 8.55%
https://leetcode.com/problems/expression-add-operators/discuss/71968/Clean-Python-DFS-with-comments
"""


class Solution:
    def addOperators(self, num: str, target: int) -> List[str]:
        def backtracking(offset: int = 0, path: str = '', value: int = 0, prev: int = None):
            nonlocal target
            nonlocal L
            # exit condition of backtracking
            if offset == L and value == target:  # found match, add expression to res
                res.append(path)
                return
            # partition remainNum into [:i] and [i:]
            for i in range(offset + 1, L + 1):  # specially, i=L means taking the whole remainNum as one number
                tmp = int(num[offset:i])
                if i == offset + 1 or (i > offset + 1 and num[offset] != '0'):  # rule out prefix '0' cases
                    if prev is None:  # initialization
                        backtracking(i, num[offset:i], tmp, tmp)
                    else:
                        # for multiplication, deduct prev before adding the multiplied 'prev'
                        # e.g. 5+3*4 => 5+3 (3 is prev) => 8-3+3*4
                        ops = ["+", "-", "*"]
                        firstOperands = [value, value, value - prev]
                        secondOperands = [tmp, -tmp, prev * tmp]
                        for op, firstOperand, secondOperand in zip(ops, firstOperands, secondOperands):
                            backtracking(i, path + op + num[offset:i], firstOperand + secondOperand, secondOperand)

        res = []
        L = len(num)
        backtracking()
        return res


print(Solution().addOperators(num="105", target=5))
