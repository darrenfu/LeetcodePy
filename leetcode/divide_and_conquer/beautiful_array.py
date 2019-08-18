from typing import List


class Solution:
    """
    Apply addition or multiplication to a beautiful array, it will yield another beautiful array
    Runtime: 44 ms, faster than 70.83%
    https://leetcode.com/problems/beautiful-array/discuss/186679/Odd-%2B-Even-Pattern-O(N)
    """
    def beautifulArray(self, N: int) -> List[int]:
        res = [1]
        while len(res) < N:
            # A1 = A * 2 - 1 is beautiful with only odds from 1 to N * 2 -1
            # A2 = A * 2 is beautiful with only even from 2 to N * 2
            # B = A1 + A2 beautiful array with length N * 2
            res = [n*2-1 for n in res] + [n*2 for n in res]
        return [n for n in res if n <= N]

        # bin(i) returns the binary code str of the integer, e.g. 3='0b11'
        # [start:stop:step] is Python's extended slices, [:1:-1] means reversing the str till the first digit except '0b'
        # 1. we divide range(N+1) into two groups: evens and odd. Which would also be realized by sorting the last char in the numbers' binary representation.
        # 2. For each group, divide the number i (i+1 if odd) by 2, which equals i>>2, then repeat the process.
        # Since in every group, the last char (aka. first char when reversed) in bin(i) is the same (1 if odd else 0). So the key in second sorting pass is bin(i)[-2].
        # Runtime: 48 ms, faster than 31.25%
        # https://leetcode.com/problems/beautiful-array/discuss/186680
        # return sorted(range(1, N + 1), key=lambda x: bin(x)[:1:-1])


print(Solution().beautifulArray(5))
