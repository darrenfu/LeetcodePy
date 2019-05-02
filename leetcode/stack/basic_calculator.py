class Solution(object):
    def calculate(self, s):
        """
        :type s: str
        :rtype: int
        """
        res, num, sign, stack = 0, 0, 1, []
        for ss in s:
            if ss.isdigit():
                num = 10 * num + int(ss)
            elif ss in ['-', '+']:
                res += num * sign
                num = 0
                sign = [-1, 1][ss == '+']
            elif ss == '(':
                stack.append(res)
                stack.append(sign)
                # reset sign and res as local scope in this pair of Parentheses
                sign, res = 1, 0
            elif ss == ')':
                res += num * sign
                res *= stack.pop()  # sign
                res += stack.pop()  # res
                num = 0
        return res + num * sign


