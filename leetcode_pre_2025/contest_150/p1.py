from typing import List
from collections import Counter

class Solution:
    def countCharacters(self, words: List[str], chars: str) -> int:
        cnt = Counter()
        for c in chars:
            cnt[c] += 1

        res = 0
        for w in words:
            newCnt = cnt.copy()
            notmatch = False
            for c in w:
                newCnt[c] -= 1
                if newCnt[c] < 0:
                    notmatch = True
                    break
            if not notmatch:
                res += len(w)
        return res


print(Solution().countCharacters(words = ["cat","bt","hat","tree"], chars = "atach"))
print(Solution().countCharacters(words = ["hello","world","leetcode"], chars = "welldonehoneyr"))
