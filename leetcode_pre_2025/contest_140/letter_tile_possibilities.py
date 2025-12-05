from collections import Counter
import copy


class Solution:
    def numTilePossibilities(self, tiles: str) -> int:
        L = len(tiles)
        counter = Counter(tiles)
        mem = set()

        def dp(counter, L, idx, res):
            if idx == L:
                s = "".join(res)
                if s not in mem:
                    mem.add(s)
                return
            for k in counter.keys():
                if counter[k] <= 0: continue
                res.append(k)
                counter[k] -= 1
                dp(counter, L, idx+1, res)
                counter[k] += 1
                res.pop()

        for i in range(L):
            c = copy.deepcopy(counter)
            res = []
            dp(c, i+1, 0, res)
        return len(mem)


tiles = "AAABBC"
Solution().numTilePossibilities(tiles)
