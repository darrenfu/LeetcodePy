class Solution:

    """
    Runtime: 68 ms, faster than 26.27%
    """
    def isPalindrome(self, s: str) -> bool:
        L = len(s)
        if L <= 1: return True
        p1, p2 = 0, L-1

        def isAlphaOrIsNumeric(c: str) -> bool:
            return 'a' <= c <= 'z' or 'A' <= c <= 'Z' or '0' <= c <= '9'

        while p1 < p2:
            if not isAlphaOrIsNumeric(s[p1]):
                p1 += 1
                continue
            if not isAlphaOrIsNumeric(s[p2]):
                p2 -= 1
                continue
            if s[p1].lower() == s[p2].lower():
                p1 += 1
                p2 -= 1
            else: return False
        return True


print(Solution().isPalindrome(s="A man, a plan, a canal: Panama"))
print(Solution().isPalindrome(s="race a car"))
print(Solution().isPalindrome(s="0P"))
print(Solution().isPalindrome(s="a."))
