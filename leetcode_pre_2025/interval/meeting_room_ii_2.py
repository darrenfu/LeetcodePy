class Solution(object):

    def minMeetingRooms(self, intervals):
        """
        :type intervals: List[Interval]
        :rtype: int
        """
        # from collections import Counter
        from collections import Counter
        dict = Counter()
        for itv in intervals:
            dict[itv.start] += 1
            dict[itv.end] -= 1
        cur_rooms = 0
        max_rooms = 0
        # sort by offset (key)
        for _, freq in sorted(list(dict.items()), key=lambda x: x[0]):
            # at current offset, how many rooms required
            cur_rooms += freq
            # pick the peak room count required
            max_rooms = max(max_rooms, cur_rooms)
        return max_rooms


