class Solution:
    def longestDecomposition(self, text: str) -> int:
        memo = {}

        def helper(a: str, b: str) -> int:
            if (a, b) not in memo:
                ans = 1  # if a and b do not match, take a as the only palindrome, e.g. merchant
                n = len(a)
                for i in range(1, n):
                    # head pointer scan from left to right
                    # while tail pointer jumps to n-1-i, then scan from n-1-i to n-1 (reversed word by word)
                    if a[:i] == b[:i][::-1]:
                        new = helper(a[i:], b[i:])
                        ans = max(ans, new + 1)  # largest possible k in substring
                memo[(a,b)] = ans
            return memo[(a,b)]
        # two pointers - head and tail
        return helper(text, text[::-1])


assert Solution().longestDecomposition(text="ghiabcdefhelloadamhelloabcdefghi") == 7
assert Solution().longestDecomposition(text="merchant") == 1
assert Solution().longestDecomposition(text="antaprezatepzapreanta") == 11
assert Solution().longestDecomposition(text="aaa") == 3
