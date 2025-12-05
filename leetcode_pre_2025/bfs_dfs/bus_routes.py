import collections
#
# @lc app=leetcode id=815 lang=python
#
# [815] Bus Routes
#
class Solution(object):
    def numBusesToDestination(self, routes, S, T):
        """
        :type routes: List[List[int]]
        :type S: int
        :type T: int
        :rtype: int
        """
        q = collections.deque([S])
        # q = ([S, 0])
        visited = set([S])
        neighbors = collections.defaultdict(set)  # use `list` will cause TLE for last test case
        for i, _ in enumerate(routes):
            for j in routes[i]:
                neighbors[j].add(i)  # add bus index

        level = -1
        while q:
            level += 1
            for _ in range(len(q)):
                cur = q.popleft()
                if cur == T: return level
                for idx in neighbors[cur]:
                    for stop in routes[idx]:
                        if stop not in visited:
                            visited.add(stop)
                            q.append(stop)
        return -1

if __name__ == "__main__":
    Solution().numBusesToDestination([[1,2,7], [3,6,7]], 1, 6)

