import unittest

# from leetcode.interval.meeting_room_ii import Solution, Interval
from leetcode.interval import meeting_room_ii
from leetcode.interval import meeting_room_ii_2
from leetcode.interval import meeting_room_ii_3
from leetcode.interval.interval import Interval

class TestSolution(unittest.TestCase):
    def setUp(self):
        self.solution1 = meeting_room_ii.Solution()
        self.solution2 = meeting_room_ii_2.Solution()
        self.solution3 = meeting_room_ii_3.Solution()

    def test_min_meeting_rooms_1(self):
        intervals = [Interval(30, 75), Interval(0, 50), Interval(60, 150)]
        expected = 2
        output1 = self.solution1.minMeetingRooms(intervals)
        output2 = self.solution2.minMeetingRooms(intervals)
        output3 = self.solution3.minMeetingRooms(intervals)
        self.assertEqual(output1, expected)
        self.assertEqual(output2, expected)
        self.assertEqual(output3, expected)

    def test_min_meeting_rooms_2(self):
        intervals = [Interval(7, 10), Interval(2,4)]
        expected = 1
        output1 = self.solution1.minMeetingRooms(intervals)
        output2 = self.solution2.minMeetingRooms(intervals)
        output3 = self.solution3.minMeetingRooms(intervals)
        self.assertEqual(output1, expected)
        self.assertEqual(output2, expected)
        self.assertEqual(output3, expected)

    def test_min_meeting_rooms_3(self):
        intervals = [Interval(1, 5), Interval(8,9),Interval(8,9)]
        expected = 2
        output1 = self.solution1.minMeetingRooms(intervals)
        output2 = self.solution2.minMeetingRooms(intervals)
        output3 = self.solution3.minMeetingRooms(intervals)
        self.assertEqual(output1, expected)
        self.assertEqual(output2, expected)
        self.assertEqual(output3, expected)


if __name__ == '__main__':
    unittest.main()
