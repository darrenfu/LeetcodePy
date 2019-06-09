from typing import List


class Solution:
    def findOcurrences(self, text: str, first: str, second: str) -> List[str]:
        words = text.split()
        L = len(words)
        res = []
        for i, w in enumerate(words):
            if w == first:
                if i+2 < L and words[i+1] == second:
                    res.append(words[i+2])
        return res


text = "alice is a good girl she is a good student"
first, second = "a", "good"
Solution().findOcurrences(text, first, second)

text = "we will we will rock you"
first, second = "we", "will"
Solution().findOcurrences(text, first, second)
