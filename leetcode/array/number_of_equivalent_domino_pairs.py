from typing import List
from collections import Counter


class Solution:
    def numEquivDominoPairs(self, dominoes: List[List[int]]) -> int:
        pairs = Counter()
        for i, n in enumerate(dominoes):
            a, b = sorted(n)
            if (a,b) not in pairs:
                pairs[(a,b)] = 1
            else:
                pairs[(a,b)] += 1

        res = 0
        for k in pairs.keys():
            n = pairs[k]
            res += n * (n - 1) // 2  # (n-1)+(n-2)+...+1=n*(n-1)//2
        return res


assert Solution().numEquivDominoPairs(dominoes=[[1,2],[2,1],[3,4],[5,6]]) == 1
assert Solution().numEquivDominoPairs(dominoes=[[2,1],[1,2],[1,2],[1,2],[2,1],[1,1],[1,2],[2,2]]) == 15
