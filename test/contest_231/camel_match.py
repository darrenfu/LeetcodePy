import unittest

from leetcode.contest_231.camel_match import Solution


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()

    def test_camelMatch_1(self):
        queries = ["FooBar", "FooBarTest", "FootBall", "FrameBuffer", "ForceFeedBack"]
        pattern = "FB"
        expected = [True, False, True, True, False]
        output = self.solution.camelMatch(queries, pattern)
        self.assertEqual(output, expected)

    def test_camelMatch_2(self):
        queries = ["FooBar", "FooBarTest", "FootBall", "FrameBuffer", "ForceFeedBack"]
        pattern = "FB"
        expected = [True, False, True, True, False]
        output = self.solution.camelMatch(queries, pattern)
        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()
