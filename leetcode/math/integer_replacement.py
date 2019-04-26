class Solution(object):
    def integerReplacement(self, n):
        """
        :type n: int
        :rtype: int
        """
        memo = {1:0}

        def find_next(input, memo):
            """
            :type input: int
            :type memo: dict
            :rtype: int steps
            """
            if input in memo:
                return memo[input]
            ret = 0
            if input % 2:
                ret = 1 + min(find_next(input-1, memo), find_next(input+1, memo))
            else:
                ret = 1 + find_next(int(input/2), memo)
            memo[input] = ret
            return memo[input]

        ret = find_next(n, memo)
        #print(memo)
        return ret
