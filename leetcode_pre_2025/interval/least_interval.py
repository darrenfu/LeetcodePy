class Solution(object):
    def leastInterval(self, tasks, n):
        """
        :type tasks: List[str]
        :type n: int
        :rtype: int
        """
        LETTER_NUM = 26
        freqs = [0] * LETTER_NUM
        for c in tasks:
            freqs[ord(c) - ord('A')] += 1
        freqs.sort()  # in-place sort

        ret = 0
        while freqs[-1] > 0:
            i = 0
            while i <= n:
                if freqs[-1] == 0:
                    break
                # use most frequently appeared letter by turn
                if i < LETTER_NUM and freqs[LETTER_NUM - i - 1] > 0:
                    freqs[LETTER_NUM - i - 1] -= 1
                ret += 1
                i += 1
            freqs.sort()
        return ret
