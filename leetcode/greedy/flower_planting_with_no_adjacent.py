class Solution(object):
    def gardenNoAdj(self, N, paths):
        """
        :type N: int
        :type paths: List[List[int]]
        :rtype: List[int]
        """
        # intuition
        # Greedily paint nodes one by one.
        # Because there is no node that has more than 3 neighbors,
        # always one possible color to choose.
        import collections
        G = collections.defaultdict(list)
        for edge in paths:
            gx, gy = edge
            G[gx-1].append(gy-1)
            G[gy-1].append(gx-1)
        res = [0] * N
        for i in range(N):
            res[i] = ({1,2,3,4} - {res[j] for j in G[i]}).pop()
        return res
