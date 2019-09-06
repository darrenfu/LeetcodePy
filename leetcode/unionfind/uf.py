from typing import List


class UF:
    def __init__(self, n: int, count: int = -1):
        # index must start from 0
        self.parents = [i for i in range(n)]
        self.count = n if count == -1 else count

    def find(self, i: int) -> int:
        if self.parents[i] != i:  # i is not root
            # path compression: point all non-root nodes in that chain to root node (flat tree)
            self.parents[i] = self.find(self.parents[i])
        return self.parents[i]

    def union(self, i: int, j: int) -> bool:
        a, b = self.find(i), self.find(j)
        ret = a != b
        if ret:  # optimization: to record how many unions if a and b don't have the same root
            self.count -= 1
            self.parents[a] = b
        return ret

    def maxUnion(self) -> int:
        """
        Get node # of the deepest tree, O(N)
        :return:
        """
        N, max_val = len(self.parents), 0
        counts = [0] * N
        for i in range(N):
            root = self.find(i)
            # if nodes are sharing the root node, count[root]++
            # thus, it will get the biggest tree among the forest
            counts[root] += 1
            # print(i, root, counts[root])
            max_val = max(max_val, counts[root])
        return max_val
