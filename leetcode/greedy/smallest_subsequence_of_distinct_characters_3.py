class Solution:
    # identical to #316
    def smallestSubsequence(self, text: str) -> str:
        res = []
        while text:
            # find the minimum last index among unique chars
            i = min(map(text.rindex, set(text)))
            # every turn, get the smallest char from the prefix: 0 till minimum last index above
            c = min(text[:i+1])
            # add to result
            res.append(c)

            # recursively repeat the three steps
            # new text will be suffix starting from first index of c without c occurrence
            text = text[text.index(c):].replace(c, '')
        return ''.join(res)


text = "ecbacba"
res = Solution().smallestSubsequence(text)
print(res)
