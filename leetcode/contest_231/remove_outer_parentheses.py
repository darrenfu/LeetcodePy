class Solution(object):
    def removeOuterParentheses(self, S):
        LEFT = '('
        RIGHT = ')'
        """
        :type S: str
        :rtype: str
        """
        from collections import deque
        stack = deque()
        cur_arr = []
        primitive = ""
        ret = []
        for c in S:
            if not stack: # reset
                cur_arr = []
                primitive = ""
            cur_arr.append(c)
            if c == LEFT:
                stack.append(c)
            else:
                stack.pop()
                if not stack: # empty
                    # print "".join(cur_arr)
                    cur_arr = cur_arr[1:-1] # remove outer parentheses
                    primitive = "".join(cur_arr)
                    ret.append(primitive)
        return "".join(ret)

if __name__ == '__main__':
    s = Solution()
    print(s.removeOuterParentheses("(()())(())(()(()))"))