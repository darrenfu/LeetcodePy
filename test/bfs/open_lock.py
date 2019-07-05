import unittest

from leetcode.bfs_dfs.open_lock import Solution


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()

    def test_openLock_1(self):
        deadends = ["0201","0101","0102","1212","2002"]
        target = "0202"
        expected = 6
        output = self.solution.openLock(deadends, target)
        self.assertEqual(output, expected)

    def test_openLock_2(self):
        deadends = ["8888"]
        target = "0009"
        expected = 1
        output = self.solution.openLock(deadends, target)
        self.assertEqual(output, expected)

    def test_openLock_3(self):
        deadends = ["8887","8889","8878","8898","8788","8988","7888","9888"]
        target = "8888"
        expected = -1
        output = self.solution.openLock(deadends, target)
        self.assertEqual(output, expected)

    def test_openLock_4(self):
        deadends = ["0000"]
        target = "8888"
        expected = -1
        output = self.solution.openLock(deadends, target)
        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()
