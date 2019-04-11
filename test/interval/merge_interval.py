import unittest

from leetcode.interval.merge_interval import Solution, Interval


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()

    def test_merge_interval_1(self):
        intervals = [Interval(1,4),Interval(4,5)]
        expected = [Interval(1,5)]
        output = self.solution.merge(intervals)
        self.assertEqual(output, expected)

    def test_merge_interval_2(self):
        intervals = [Interval(1,3),Interval(2,6),Interval(8,10),Interval(15,18)]
        expected = [Interval(1,6),Interval(8,10),Interval(15,18)]
        output = self.solution.merge(intervals)
        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()
