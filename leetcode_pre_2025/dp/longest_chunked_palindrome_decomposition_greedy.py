class Solution:
    """
    https://leetcode.com/problems/longest-chunked-palindrome-decomposition/discuss/350560/JavaC%2B%2BPython-Easy-Greedy-with-Prove
    Runtime: 36 ms, faster than 83.64%
    """
    def longestDecomposition(self, text: str) -> int:
        cnt = 0
        sL, sR = "", ""
        for sStart, sEnd in zip(text, text[::-1]):
            sL += sStart
            sR = sEnd + sR  # important! reverse scan, but non-reverse concat
            if sL == sR:
                cnt += 1
                sL, sR = "", ""
        return cnt


assert Solution().longestDecomposition(text="ghiabcdefhelloadamhelloabcdefghi") == 7
assert Solution().longestDecomposition(text="merchant") == 1
assert Solution().longestDecomposition(text="antaprezatepzapreanta") == 11
assert Solution().longestDecomposition(text="aaa") == 3
