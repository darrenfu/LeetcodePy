class Solution:
    # identical to #316
    def smallestSubsequence(self, text: str) -> str:
        # list all unique chars in text
        for c in sorted(set(text)):
            suffix = text[text.index(c):]
            # check whether there is missing char in suffix comparing to text
            # e.g. ecbacba, 'e' is missing in suffix 'acba'
            if set(suffix) == set(text):
                # prepend this char to result
                # recursively calculate the rest text, i.e. suffix without c
                return c + self.smallestSubsequence(suffix.replace(c, ''))
        return ''


text = "ecbacba"
res = Solution().smallestSubsequence(text)
print(res)
