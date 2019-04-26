import unittest
import numpy

from leetcode.dp.knight_probability_dp import Solution
from leetcode.dp.knight_probability_dp2 import Solution


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()
        self.solution2 = Solution()

    def test_knight_probability_1(self):
        N, K, r, c = 3, 2, 0, 0
        expected = 0.0625
        output = self.solution.knightProbability(N, K, r, c)
        output2 = self.solution2.knightProbability(N, K, r, c)
        numpy.testing.assert_almost_equal(output, expected, decimal=5)
        numpy.testing.assert_almost_equal(output2, expected, decimal=5)

    def test_knight_probability_2(self):
        N, K, r, c = 8, 30, 6, 4
        expected = 0.00019
        output = self.solution.knightProbability(N, K, r, c)
        output2 = self.solution2.knightProbability(N, K, r, c)
        numpy.testing.assert_almost_equal(output, expected, decimal=5)
        numpy.testing.assert_almost_equal(output2, expected, decimal=5)

    def test_knight_probability_3(self):
        N, K, r, c = 8, 3, 4, 4
        expected = 0.62109375
        output = self.solution.knightProbability(N, K, r, c)
        output2 = self.solution2.knightProbability(N, K, r, c)
        numpy.testing.assert_almost_equal(output, expected, decimal=5)
        numpy.testing.assert_almost_equal(output2, expected, decimal=5)


if __name__ == '__main__':
    unittest.main()
