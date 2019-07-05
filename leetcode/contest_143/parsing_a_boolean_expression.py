
class Solution:
    def parseBoolExpr(self, expression: str) -> bool:
        def eval(i: int) -> (bool, int):
            # 1. When encountering a "t" or "f", we evaluate it right away
            if expression[i] in ['t', 'f']:
                return (True if expression[i] == 't' else False), i+1

            # 2. If its not t or f, then it has to be an operator.
            # In which case, we evaluate everything between '(' and ')' using recursion and by storing them in a stack.
            op = expression[i]
            i += 2
            stack = []
            while expression[i] != ')':
                if expression[i] == ',':
                    i += 1
                    continue
                res, i = eval(i)
                stack.append(res)

            # 3. once we encounter ')', we simply evaluate &, | and ! by evaluating the operands stored in the stack.
            res = 0
            if op == '&':
                res = all(stack)
            elif op == '|':
                res = any(stack)
            elif op == '!':
                res = not stack[0]
            # 4. The one good pattern to follow is, once we finish evaluating a particular expression,
            # we also return the index i+1, to the caller, so that the high level caller can continue evaluating
            # other expressions from this returned index.
            return res, i+1
        return eval(0)[0]


print(Solution().parseBoolExpr(expression="!(f)"))
print(Solution().parseBoolExpr(expression="|(f,t)"))
print(Solution().parseBoolExpr(expression="&(t,f)"))
print(Solution().parseBoolExpr(expression="|(&(t,f,t),!(t))"))
