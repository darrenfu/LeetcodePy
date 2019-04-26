import unittest

from leetcode.queue.queue_with_fixed_size_of_arrays import QueueWithFixedSizeOfArrays


class TestSolution(unittest.TestCase):
    def setUp(self):
        pass

    def test_queue_dequeue(self):
        self.queue = QueueWithFixedSizeOfArrays(5)
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        output = self.queue.dequeue()
        self.assertEqual(output, 1)
        self.assertEqual(len(self.queue), 1)

    def test_queue_dequeue_2(self):
        self.queue = QueueWithFixedSizeOfArrays(5)
        for i in range(1, 7):
            self.queue.enqueue(i)
        output = self.queue.dequeue()
        self.assertEqual(output, 1)
        self.assertEqual(len(self.queue), 5)

    def test_queue_dequeue_3(self):
        self.queue = QueueWithFixedSizeOfArrays(5)
        for i in range(1, 12):
            self.queue.enqueue(i)
        self.assertEqual(len(self.queue), 11)
        for _ in range(1, 12):
            self.queue.dequeue()
        self.assertEqual(len(self.queue), 0)
        self.queue.dequeue()
        self.assertEqual(len(self.queue), 0)


if __name__ == '__main__':
    unittest.main()
