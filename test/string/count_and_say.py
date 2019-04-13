import unittest

from leetcode.string.count_and_say import Solution


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()

    def test_count_and_say_1(self):
        input = 1
        expected = "1"
        output = self.solution.countAndSay(input)
        self.assertEqual(output, expected)

    def test_count_and_say_2(self):
        input = 4
        expected = "1211"
        output = self.solution.countAndSay(input)
        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()
