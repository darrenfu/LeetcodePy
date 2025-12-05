from typing import List
from collections import Counter
import heapq


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        cnt = Counter(nums)
        return list(map(lambda x: x[0], cnt.most_common(k)))
        # Solution 2:
        heapq.heappush()
        # return heapq.nlargest(k, cnt.keys(), key=cnt.get)


print(Solution().topKFrequent(nums = [1,1,1,2,2,3], k = 2))
print(Solution().topKFrequent(nums = [1], k = 1))
