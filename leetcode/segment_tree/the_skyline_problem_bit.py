from typing import List


class BinaryIndexTree(object):

    def __init__(self, buildings: List[List[int]]):
        self.points, self.ends = [], {}
        for i, b in enumerate(buildings):
            self.points += ((b[0], -1, -b[2]), (b[1], 1, -b[2]))
            self.ends[self.points[-2]] = self.points[-1]  # ends[L] = R

        self.N = len(self.points)
        self.bits = [0] * (self.N + 1)

        self.points.sort()
        self.idx = {self.points[i]: i for i in range(self.N)}  # store sorted idx

    def getSkeleton(self):
        ret = []
        for i, p in enumerate(self.points):
            if p[1] == -1:  # L
                R, H = self.ends[p], -p[2]
                self.set(self.idx[R], H)
            h = self.get(i + 1)
            if not ret or ret[-1][1] != h:
                L = p[0]
                if ret and ret[-1][0] == L:
                    ret[-1][1] = h
                else:
                    ret.append([L, h])
        return ret

    def set(self, p: int, h: int) -> None:
        while p > 0:  # scope of h is towards left
            self.bits[p] = max(self.bits[p], h)
            p -= BinaryIndexTree._lowbit(p)  # go to parent node

    def get(self, p: int) -> int:
        ret = 0
        while p <= self.N + 1:  # check any points to the right that has a higher value
            ret = max(ret, self.bits[p])
            p += BinaryIndexTree._lowbit(p)  # go to child node
        return ret

    @staticmethod
    def _lowbit(x: int):
        return x & (-x)


class Solution:
    """
    Runtime: 184 ms, faster than 23.00%
    Note: TOO HARD to understand
    """
    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
        bit = BinaryIndexTree(buildings)
        return bit.getSkeleton()


print(Solution().getSkyline(buildings=[[2, 9, 10], [3, 7, 15], [5, 12, 12], [15, 20, 10], [19, 24, 8]]))
