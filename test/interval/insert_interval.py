import unittest

from leetcode.interval.insert_interval import Solution, Interval


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()

    def test_insert_interval_1(self):
        intervals = [Interval(1,3),Interval(6,9)]
        newInterval = Interval(2,5)
        expected = [Interval(1,5),Interval(6,9)]
        output = self.solution.insert(intervals, newInterval)
        self.assertEqual(output, expected)

    def test_insert_interval_2(self):
        intervals = [Interval(1,2),Interval(3,5),Interval(6,7),Interval(8,10),Interval(12,16)]
        newInterval = Interval(4,8)
        expected = [Interval(1,2),Interval(3,10),Interval(12,16)]
        output = self.solution.insert(intervals, newInterval)
        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()
