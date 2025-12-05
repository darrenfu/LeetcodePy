from typing import List, Dict
from leetcode.unionfind.uf import UF


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        N = len(nums)
        uf = UF(N)
        hashmap: Dict[int, int] = dict()
        directions = [1, -1]
        for i, num in enumerate(nums):
            # edge case - dedupe duplicate elements
            if num in hashmap:
                continue
            hashmap[num] = i
            # if consecutive number is also in hashmap, union as an edge
            for direction in directions:
                if num + direction in hashmap:
                    uf.union(i, hashmap[num + direction])
        res = uf.maxUnion()
        print(res)
        return res


nums = [100, 4, 200, 1, 3, 2]
Solution().longestConsecutive(nums)
nums = [1,2,0,1]
Solution().longestConsecutive(nums)
