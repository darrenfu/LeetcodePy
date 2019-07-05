import unittest

from leetcode.bfs_dfs.matrix_01 import Solution


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()

    def test_updateMatrix_1(self):
        matrix = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
        expected = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
        output = self.solution.updateMatrix(matrix)
        self.assertEqual(output, expected)

    def test_updateMatrix_2(self):
        matrix = [[0, 0, 0], [0, 1, 0], [1, 1, 1]]
        expected = [[0, 0, 0], [0, 1, 0], [1, 2, 1]]
        output = self.solution.updateMatrix(matrix)
        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()
