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
        neighbors = collections.defaultdict(set)  # use `list` will cause TLE for last test case
        q = {S}
        for i, _ in enumerate(routes):
            for j in routes[i]:
                neighbors[j].add(i)  # add bus index

        level = -1
        while q:
            level += 1
            if T in q: return level
            # neighbors.pop(node, []) means if neighbors contains key `node`, remove and pop its value; 
            # otherwise, return []
            # it will not introduce another `visited` set
            q = {next_stop for node in q for route_i in neighbors.pop(node, []) for next_stop in routes[route_i]}
        return -1

if __name__ == "__main__":
    Solution().numBusesToDestination([[1,2,7], [3,6,7]], 1, 6)

