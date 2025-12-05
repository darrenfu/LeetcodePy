class Solution(object):
    def numMovesStonesII(self, stones):
        """
        :type stones: List[int]
        :rtype: List[int]
        """
        # https://leetcode.com/problems/moving-stones-until-consecutive-ii/discuss/286707/JavaC%2B%2BPython-Sliding-Window
        stones.sort()
        i, n, minsteps = 0, len(stones), len(stones)
        # max moves from leftmost:
        # move leftmost (A[0]) to the first empty slot after the 2nd node(A[1]),
        # e.g. [1,2,3,4,10] ->[2,3,4,5,10]->[3,4,5,6,10]
        # keep moving new leftmost (A[1]) to the first empty slot after the 2nd node till consecutive,
        # e.g. [6,7,8,9,10]
        move_from_left = stones[-1] - stones[1] + 1 - (n - 1)

        # max moves from rightmost:
        # e.g. [1,2,3,4,10] ->[1,2,3,4,5]
        # e.g. [1,2,3,4,5]
        move_from_right = stones[-2] - stones[0] + 1 - (n - 1)
        maxsteps = max(move_from_left, move_from_right)


        # min moves using sliding window:
        # Slide a window of size N, and find how many stones are already in this window.
        # We want moves other stones into this window. For each missing stone, we need at least one move.
        for j in range(n):
            while stones[j] - n >= stones[i]: i += 1
            if j - i + 1 == n - 1 and stones[j] - stones[i] + 1 == n - 1:
                # Special case: the inner N is consecutive, and only one is not consecutive, min_step = 2
                minsteps = min(minsteps, 2)
            else:
                minsteps = min(minsteps, n - (j - i + 1))
        return [minsteps, maxsteps]


if __name__ == '__main__':
    print(Solution().numMovesStonesII([100,101,104,102,103]))  # [0,0]
    print(Solution().numMovesStonesII([6,5,4,3,10]))  # [2,3]
    print(Solution().numMovesStonesII([7,4,9]))  # [1,2]

