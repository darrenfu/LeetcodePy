from typing import List
from typing import Deque


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        if not nums or not k: return nums

        def reorg_queue(new_idx: int, nums: List[int], queue: Deque) -> None:
            """
             keep a stack of indexes of top max values, stack bottom: max value's index; stack top: coming value's index
            :param new_idx:
            :param nums:
            :param queue:
            :return:
            """
            while len(queue):
                if nums[new_idx] > nums[queue[-1]]:
                    queue.pop()
                else:
                    break
            queue.append(new_idx)

        import collections
        queue = collections.deque()

        for i in range(k):
            reorg_queue(i, nums, queue)

        res = []
        for i in range(k, len(nums)):
            max_idx = queue[0]
            res.append(nums[max_idx])

            if max_idx < i - k + 1:  # Check if left most is still in the range of k
                queue.popleft()  # remove max idx (aka. bottom of stack)

            reorg_queue(i, nums, queue)

        # Appending i at the end of the deque
        res.append(nums[queue[0]])
        print(res)
        return res


Solution().maxSlidingWindow([1,3,-1,-3,5,3,6,7], 3)
