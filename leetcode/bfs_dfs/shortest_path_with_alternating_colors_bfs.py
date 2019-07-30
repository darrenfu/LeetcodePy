from typing import List
from collections import defaultdict
from collections import deque
import math


class Solution:
    """
    https://leetcode.com/problems/shortest-path-with-alternating-colors/discuss/339965/Python-BFS
    """
    def shortestAlternatingPaths(self, n: int, red_edges: List[List[int]], blue_edges: List[List[int]]) -> List[int]:
        graph = defaultdict(lambda: defaultdict(set))
        # + color dimension: red as 0, blue as 1
        for s, e in red_edges:
            graph[s][0].add(e)
        for s, e in blue_edges:
            graph[s][1].add(e)
        visited = [set(), set()]
        res = [math.inf] * n
        q = deque([(0, 0), (0, 1)])  # starting node is not one but two: 0 with red, 0 with blue
        lvl = -1
        while q:
            lvl += 1
            for _ in range(len(q)):
                node, color = q.popleft()
                visited[color].add(node)
                res[node] = min(res[node], lvl)  # shortest path
                nextColor = color ^ 1  # 0xor1=1, 1xor1=0 -> red->blue; blue->red. Or: nextColor=1-color
                neighborSet = graph[node][nextColor]
                for neighbor in list(neighborSet):  # convert to list to avoid 'Set changed size during iteration' error
                    # neighborSet.remove(neighbor)  # mark as visited
                    if neighbor not in visited[nextColor]:
                        q.append((neighbor, nextColor))
        return [r if r != math.inf else -1 for r in res]  # inf means no available path between 0 and that node


assert Solution().shortestAlternatingPaths(n = 3, red_edges = [[0,1],[1,2]], blue_edges = []) == [0,1,-1]
assert Solution().shortestAlternatingPaths(n = 3, red_edges = [[0,1]], blue_edges = [[2,1]]) == [0,1,-1]
assert Solution().shortestAlternatingPaths(n = 3, red_edges = [[1,0]], blue_edges = [[2,1]]) == [0,-1,-1]
assert Solution().shortestAlternatingPaths(n = 3, red_edges = [[0,1]], blue_edges = [[1,2]]) == [0,1,2]
assert Solution().shortestAlternatingPaths(n = 3, red_edges = [[0,1],[0,2]], blue_edges = [[1,0]]) == [0,1,1]
