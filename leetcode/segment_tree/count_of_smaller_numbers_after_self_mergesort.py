from typing import List


class Solution:
    """
    Runtime: 148 ms, faster than 57.91%
    """
    def countSmaller(self, nums: List[int]) -> List[int]:
        def mergesort(enum: List[int]):
            mid = len(enum) // 2
            if mid:
                left, right = mergesort(enum[:mid]), mergesort(enum[mid:])
                for i in range(-1, -len(enum)-1, -1):
                    # compare last element of each half
                    if not right or left and left[-1][1] > right[-1][1]:
                        # add tracking of those right-to-left jumps, aka. smaller numbers
                        smaller[left[-1][0]] += len(right)
                        # place larger element from bottom of origin array
                        enum[i] = left.pop()  # remove last element
                    else:
                        enum[i] = right.pop()
            return enum

        smaller = [0] * len(nums)
        mergesort(list(enumerate(nums)))
        return smaller


print(Solution().countSmaller(nums=[5, 2, 6, 1]))
