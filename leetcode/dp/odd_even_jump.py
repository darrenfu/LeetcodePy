from typing import List


class Solution:
    """
    Runtime: 308 ms, faster than 84.62%
    https://leetcode.com/problems/odd-even-jump/discuss/217974/Java-solution-DP-%2B-TreeMap
    https://leetcode.com/problems/odd-even-jump/discuss/240594/Python-Solution-Annotated
    """
    def oddEvenJumps(self, A: List[int]) -> int:
        L = len(A)

        # Monotonic Stack
        def makeStack(sortedIdxes: List[int]) -> List[int]:
            res = [0] * L
            stack = []
            for i in sortedIdxes:
                while stack and stack[-1] < i:
                    res[stack.pop()] = i
                stack.append(i)
            return res

        sortedIdxes = sorted(range(L), key=lambda k:A[k])  # sort indexes by values
        nextHigher = makeStack(sortedIdxes)  # In Java, TreeMap.ceilingKey/higherKey returns the least key >= the given key

        sortedIdxes = sorted(range(L), key=lambda k:A[k], reverse=True)
        nextLower = makeStack(sortedIdxes)  # In Java, TreeMap.floorKey/lowerKey returns the greatest key <= the given key

        # initialize odd and even lists where the end can be reached from the respective index
        higher, lower = [False] * L, [False] * L
        higher[-1] = lower[-1] = True

        for i in range(L-2, -1, -1):
            higher[i] = lower[nextHigher[i]]  # odd step, next step is even
            lower[i] = higher[nextLower[i]]  # even step, next step is odd

        # return the number of spots marked True in odd.
        # we always start with an odd jump, so odd will contain the number of valid jumps to reach the end
        return sum(higher)


print(Solution().oddEvenJumps(A=[10,13,12,14,15]))
print(Solution().oddEvenJumps(A=[2,3,1,1,4]))

