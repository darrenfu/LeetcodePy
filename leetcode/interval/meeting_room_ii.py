class Solution(object):

    def minMeetingRooms(self, intervals):
        """
        :type intervals: List[Interval]
        :rtype: int
        """
        import heapq
        arr = sorted(intervals, key=lambda x: x.start)
        min_heap = [float("inf")]
        heapq.heapify(min_heap)
        for i in range(len(arr)):
            cur = arr[i]
            # get min(end) from previous intervals
            # print(cur.start, "vs", min_heap[0])
            if cur.start < min_heap[0]:
                heapq.heappush(min_heap, cur.end)
            else:
                heapq.heapreplace(min_heap, cur.end)
        return len(min_heap) - 1
