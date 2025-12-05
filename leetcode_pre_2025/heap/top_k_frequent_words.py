from typing import List
from collections import Counter
from functools import cmp_to_key


class Solution:
    def topKFrequent(self, words: List[str], k: int) -> List[str]:
        cnt = Counter(words)
        freq2wordlist = {}
        for w, c in cnt.items():
            if c not in freq2wordlist:
                freq2wordlist[c] = []
            freq2wordlist[c].append(w)
        word2cnt = []
        L, i = len(words), 0
        for c in range(L, 0, -1):
            if c in freq2wordlist:
                for w in freq2wordlist[c]:
                    word2cnt.append((w, c))
                    i += 1
            if i >= k:
                break

        def mycmp(x: (str, int), y: (str, int)) -> int:
            """
            negative number for less-than
            positive number for great-than
            :param x:
            :param y:
            :return:
            """
            if x[1] != y[1]:
                return y[1] - x[1]  # x first (with higher freq)
            return -1 if x[0] < y[0] else 1  # x first (with lower lex order)

        word2cnt.sort(key=cmp_to_key(mycmp))
        return [itm[0] for itm in word2cnt[:k]]


print(Solution().topKFrequent(words=["i", "love", "leetcode", "i", "love", "coding"], k = 2))
print(Solution().topKFrequent(words=["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"], k = 4))
