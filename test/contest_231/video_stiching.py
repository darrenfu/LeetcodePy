import unittest

from leetcode.contest_231.video_stitching import Solution


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()

    def test_videoStitching_1(self):
        clips = [[0,2],[4,6],[8,10],[1,9],[1,5],[5,9]]
        T = 10
        expected = 3
        output = self.solution.videoStitching(clips, T)
        self.assertEqual(output, expected)

    def test_videoStitching_2(self):
        clips = [[0,1],[1,2]]
        T = 5
        expected = -1
        output = self.solution.videoStitching(clips, T)
        self.assertEqual(output, expected)

    def test_videoStitching_3(self):
        clips = [[0,1],[6,8],[0,2],[5,6],[0,4],[0,3],[6,7],[1,3],[4,7],[1,4],[2,5],[2,6],[3,4],[4,5],[5,7],[6,9]]
        T = 9
        expected = 3
        output = self.solution.videoStitching(clips, T)
        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()
