import unittest

from leetcode.stack.basic_calculator import Solution


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()

    def test_calculate_1(self):
        input = "1 + 1"
        expected = 2
        output = self.solution.calculate(input)
        self.assertEqual(output, expected)

    def test_calculate_1(self):
        input = " 2-1 + 2 "
        expected = 3
        output = self.solution.calculate(input)
        self.assertEqual(output, expected)

    def test_calculate_3(self):
        input = "(1+(4+5+2)-3)+(6+8)"
        expected = 23
        output = self.solution.calculate(input)
        self.assertEqual(output, expected)

    def test_calculate_4(self):
        input = "2147483647"
        expected = 2147483647
        output = self.solution.calculate(input)
        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()
