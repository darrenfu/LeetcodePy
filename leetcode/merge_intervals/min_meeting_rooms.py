# Given a list of closed intervals representing meeting times, return the minimum number of meeting rooms required so that no meetings overlap in the same room. Intervals are inclusive on both ends.
# Input:
# * intervals: List of [start, end], with 0 ≤ start ≤ end ≤ 10^9
# * n = number of intervals, 1 ≤ n ≤ 2e5
# Output:
# * Integer: minimum rooms needed.
# Example:
# * Input: [[0, 30], [5, 10], [15, 20]]
# * Output: 2
# Notes:
# * Adjacent intervals like [10,10] and [10,10] overlap since endpoints are inclusive.
from typing import List
import heapq

class Solution:
    def min_meeting_rooms(self, intervals: List[List[int]]) -> int:
        if not intervals:
            return 0

        intervals = sorted(intervals, key=lambda itv: (itv[0], itv[1]))
        min_heap = []
        max_rooms = 0
        for s, e in intervals:
            # no overlap with previous interval, keep releasing meeting rooms
            while min_heap and min_heap[0] < s:
                heapq.heappop(min_heap)
            # Allocate a room for current meeting (or reuse a freed one)
            heapq.heappush(min_heap, e)
            max_rooms = max(max_rooms, len(min_heap))
        return max_rooms

print(Solution().min_meeting_rooms([[0, 30], [5, 10], [15, 20]])) # 2
print(Solution().min_meeting_rooms([[0, 30], [5, 20], [15, 20]])) # 3
print(Solution().min_meeting_rooms([[0, 1], [0, 2], [1, 1], [2, 3]])) # 3
