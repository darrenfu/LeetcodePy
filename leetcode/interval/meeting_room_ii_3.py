class Solution(object):

    def minMeetingRooms(self, intervals):
        """
        :type intervals: List[Interval]
        :rtype: int
        """
        starts = sorted(i.start for i in intervals)
        ends = sorted(i.end for i in intervals)
        used_rooms = 0
        # The start pointer simply iterates over all the meetings
        # The end pointer helps us track if a meeting has ended and if we can reuse a room
        e_ptr = 0
        for s_ptr in range(len(starts)):
            if starts[s_ptr] >= ends[e_ptr]:
                e_ptr += 1
            else:
                used_rooms += 1
        return used_rooms
