import unittest

from leetcode.math import integer_replacement
from leetcode.math import integer_replacement_bit


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.solution = integer_replacement.Solution()
        self.solution_2 = integer_replacement_bit.Solution()

    def test_integer_replacement_1(self):
        input = 8
        expected = 3
        output_1 = self.solution.integerReplacement(input)
        output_2 = self.solution_2.integerReplacement(input)
        self.assertEqual(output_1, expected)
        self.assertEqual(output_2, expected)

    def test_integer_replacement_2(self):
        input = 65535
        expected = 17
        output_1 = self.solution.integerReplacement(input)
        output_2 = self.solution_2.integerReplacement(input)
        self.assertEqual(output_1, expected)
        self.assertEqual(output_2, expected)


if __name__ == '__main__':
    unittest.main()
