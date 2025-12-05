from typing import List
from collections import defaultdict
import bisect


class Solution:
    def highFive(self, items: List[List[int]]) -> List[List[int]]:
        hashmap = defaultdict(list)

        for item in items:
            bisect.insort(hashmap[item[0]], item[1])

        def avgTopFive(entry: [int, List[int]]) -> [int, int]:
            top_lst = entry[1][-5:]
            L = len(top_lst)
            res = sum(top_lst) // L
            return [entry[0], res]

        return list(map(avgTopFive, hashmap.items()))


items = [[1,91],[1,92],[2,93],[2,97],[1,60],[2,77],[1,65],[1,87],[1,100],[2,100],[2,76]]
print(Solution().highFive(items))
