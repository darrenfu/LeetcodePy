from typing import List
from heapq import heappush, heappop
import math


class Solution:
    """
    Runtime: 60 ms, faster than 98.36%
    """
    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
        # uphill events + downhill events
        # sort by L, then H (-H means using max_heap)
        events = [(L, -H, R) for (L, R, H) in buildings] + [(R, 0, 0) for (_, R, _) in buildings]
        events.sort()

        res = [[0, 0]]  # x, height
        live = [(0, math.inf)]  # max_heap, [-heap, ending pos]
        for X, negH, R in events:
            # 1, pop buildings that are already ended
            while live[0][1] <= X:  # live[0][1] is max_height tuple's R
                heappop(live)
            # 2, if it's uphill event, make the building alive
            if negH:
                heappush(live, (negH, R))
            # 3, if previous keypoint height != current highest height, edit the result
            lastH, maxH = res[-1][1], -live[0][0]
            if lastH != maxH:  # res[-1][1] is result's latest height; live[0][0] is max_height in max_heap
                res += [[X, maxH]]
        return res[1:]


print(Solution().getSkyline(buildings=[[2, 9, 10], [3, 7, 15], [5, 12, 12], [15, 20, 10], [19, 24, 8]]))
