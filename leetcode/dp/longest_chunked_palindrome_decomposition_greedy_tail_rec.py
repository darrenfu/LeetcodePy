class Solution:
    """
    https://leetcode.com/problems/longest-chunked-palindrome-decomposition/discuss/350560/JavaC%2B%2BPython-Easy-Greedy-with-Prove
    Runtime: 36 ms, faster than 83.64%
    """
    def longestDecomposition(self, text: str, res: int = 0) -> int:
        n = len(text)
        for l in range(1, n // 2 + 1):  # why for loop?
            # compare head and tail char word by word
            if text[0] == text[n - l] and text[l - 1] == text[n - 1]:
                if text[:l] == text[n - l:]:  # if matches, compare the whole word
                    # if matches, dig into the substring, tail recursion
                    # why res + 2? Because two words counted (head and tail)
                    return self.longestDecomposition(text[l:n - l], res + 2)
        # If there are no two words matched (e.g. merchant), res + 1
        return res + 1 if text else res


assert Solution().longestDecomposition(text="ghiabcdefhelloadamhelloabcdefghi") == 7
assert Solution().longestDecomposition(text="merchant") == 1
assert Solution().longestDecomposition(text="antaprezatepzapreanta") == 11
assert Solution().longestDecomposition(text="aaa") == 3
