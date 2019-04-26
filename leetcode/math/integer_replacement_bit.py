class Solution(object):
    def integerReplacement(self, n):
        """
        :type n: int
        :rtype: int
        """
        # https://leetcode.com/problems/integer-replacement/discuss/87920/A-couple-of-Java-solutions-with-explanations
        # we just need to remove as many 1's as possible, doing +1 in case of a tie.
        # Except the infamous n=3 (11 -> 10 -> 1)
        c = 0
        while n != 1:
            if not n & 1:
                n >>= 1
            elif n == 3 or not n >> 1 & 1:  # ends with 01 -> n--
                n -= 1
            else:  # ends with 11 -> n++
                n += 1
            c += 1
        return c
