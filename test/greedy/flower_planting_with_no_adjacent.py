import unittest

from leetcode.greedy.flower_planting_with_no_adjacent import Solution


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()

    def test_gardenNoAdj_1(self):
        N = 3
        paths = [[1,2],[2,3],[3,1]]
        expected = [1,2,3]
        output = self.solution.gardenNoAdj(N, paths)
        self.assertEqual(output, expected)

    def test_gardenNoAdj_2(self):
        N = 4
        paths = [[1,2],[3,4]]
        expected = [1, 2, 1, 2]
        output = self.solution.gardenNoAdj(N, paths)
        self.assertEqual(output, expected)

    def test_gardenNoAdj_3(self):
        N = 4
        paths = [[1,2],[2,3],[3,4],[4,1],[1,3],[2,4]]
        expected = [1,2,3,4]
        output = self.solution.gardenNoAdj(N, paths)
        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()
