from typing import List
import itertools

class Solution:
    def permute(self, S: str) -> List[str]:
        stack = []
        char_lists = []
        for c in S:
            if c == '{':
                stack.append(c)
            elif c == '}':
                char_lists.append(sorted(stack[1:]))
                stack.clear()
            elif c == ',':
                pass
            else:
                stack.append(c)
                if len(stack) == 1 and stack[0] != '{':
                    char_lists.append(sorted(stack))
                    stack.clear()

        print(char_lists)
        res = list(map(''.join, itertools.chain(itertools.product(*char_lists))))
        return res


# S = "{a,b}c{d,e}f"
S = 'abcd'
Solution().permute(S)
