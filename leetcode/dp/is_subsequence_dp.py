class Solution:
    """
    Runtime: 140 ms, faster than 58.37%
    """
    def isSubsequence(self, s: str, t: str) -> bool:
        if not s:
            return True

        def dp(ss: str, tt: str) -> bool:
            l = len(ss)
            if l == 1:
                for i, ch in enumerate(tt):
                    if ch == ss:
                        return True
            elif l >= 2:
                cstart, cend = ss[0], ss[-1]
                istart = iend = 0
                for i, ch in enumerate(tt):
                    if ch == cstart:
                        istart = i
                        break
                for i in range(len(tt)-1, -1, -1):
                    if tt[i] == cend:
                        iend = i
                        break
                if istart < iend:
                    if l == 2:
                        return True
                    return dp(ss[1:-1], tt[istart+1:iend])
            return False
        return dp(s, t)


print(Solution().isSubsequence(s="", t="ahbgdc"))
print(Solution().isSubsequence(s="abc", t="ahbgdc"))
print(Solution().isSubsequence(s="abc", t="bbbbahbgdc"))
print(Solution().isSubsequence(s="axc", t="ahbgdc"))
