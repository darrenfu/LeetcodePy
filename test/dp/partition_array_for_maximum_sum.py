import unittest

from leetcode.dp.partition_array_for_maximum_sum import Solution


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()

    def test_maxSumAfterPartitioning_1(self):
        A = [1,15,7,9,2,5,10]
        K = 3
        expected = 84
        output = self.solution.maxSumAfterPartitioning(A, K)
        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()
