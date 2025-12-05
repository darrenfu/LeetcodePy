from typing import List
from leetcode.unionfind.uf import UF


class Solution:
    # def calcEquation(self, equations, values, queries):
    #     """
    #     :type equations: List[List[str]]
    #     :type values: List[float]
    #     :type queries: List[List[str]]
    #     :rtype: List[float]
    #
    #     Using Union+Find. Faster than DFS.
    #
    #     Time: O(E+Q) , Union is approx O(1) because it's using path compression during find.
    #     Space:  O(E)
    #     """
    #     parents = {}  # {Child:Parent}, eg {'a':'b'}
    #     weights = {}  # {Node: float}, eg{'a': 1.0}
    #     result = []
    #
    #     for (eq1, eq2), value in zip(equations, values):
    #         if eq1 not in parents:
    #             parents[eq1] = eq1
    #             weights[eq1] = 1.0
    #         if eq2 not in parents:
    #             parents[eq2] = eq2
    #             weights[eq2] = 1.0
    #         self.union(eq1, eq2, parents, weights, value)
    #     print(parents, weights)
    #
    #     for q1, q2 in queries:
    #         if q1 not in parents or q2 not in parents:
    #             result.append(-1.0)
    #         else:
    #             parent1 = self.find(q1, parents, weights)
    #             parent2 = self.find(q2, parents, weights)
    #             print(q1,q2,parent1,parent2)
    #             if parent1 != parent2:
    #                 result.append(-1.0)
    #             else:
    #                 print(weights[q1], weights[q2])
    #                 result.append(weights[q1] / weights[q2])
    #     print(result)
    #     return result
    #
    # def union(self, node1, node2, parents, weights, value):
    #     parent1 = self.find(node1, parents, weights)
    #     parent2 = self.find(node2, parents, weights)
    #     if parent1 != parent2:
    #         parents[parent1] = parent2
    #         weights[parent1] = value * (weights[node2] / weights[
    #             node1])  # IMPORTANT: Node1 may already be compressed: its weight could be the product of all weights up to parent1
    #
    # def find(self, node, parents, weights):
    #     # Find parent node of a given node, doing path compression while doing so (set the node's parent to its root and multiply all weights along the way.)
    #     if parents[node] != node:
    #         p = parents[node]
    #         parents[node] = self.find(parents[node], parents, weights)
    #         weights[node] = weights[node] * weights[p]
    #     return parents[node]
    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        char_dict = {}  # lowercase char to index mapping
        char_cnt = 0
        # to count n for UF
        for edge in equations:
            e1, e2 = edge[0], edge[1]
            if e1 not in char_dict:
                char_dict[e1] = char_cnt
                char_cnt += 1
            if e2 not in char_dict:
                char_dict[e2] = char_cnt
                char_cnt += 1

        n = len(char_dict.keys())
        uf = WeightedUF(n)
        print(len(uf.parents))
        parents = uf.parents
        weights = uf.weights
        for (edge1, edge2), w in zip(equations, values):
            e1, e2 = char_dict[edge1], char_dict[edge2]
            if parents[e1] == -1:
                parents[e1] = e1
                weights[e1] = 1.0
            if parents[e2] == -1:
                parents[e2] = e2
                weights[e2] = 1.0
            uf.union(e1, e2, w)
        print(parents, weights)

        res = []
        for query1, query2 in queries:
            if query1 not in char_dict or query2 not in char_dict:
                res.append(-1.0)
            else:
                q1, q2 = char_dict[query1], char_dict[query2]
                parent1, parent2 = uf.find(q1), uf.find(q2)
                if parent1 != parent2:
                    res.append(-1.0)
                else:
                    res.append(weights[q1]/weights[q2])
        print(res)
        return res


class WeightedUF(UF):
    def __init__(self, n: int):
        UF.__init__(self, n)
        self.parents = [-1] * n
        self.weights = [1.0] * n

    def find(self, i: int) -> int:
        if self.parents[i] != i:  # i is not root
            tmp = self.parents[i]
            self.parents[i] = self.find(self.parents[i])
            self.weights[i] *= self.weights[tmp]
        return self.parents[i]
        # return super().find(i)

    def union(self, i: int, j: int, weight: float) -> bool:
        a, b = self.find(i), self.find(j)
        ret = a != b
        if ret:
            self.weights[a] = weight * self.weights[b] / self.weights[a]
            # print(a, b, weight, self.weights[a], self.weights[b])
            self.parents[a] = b
        return ret


# equations = [ ["a", "b"], ["b", "c"] ]
# values = [2.0, 3.0]
# queries = [ ["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"], ["x", "x"] ]
# ret = Solution().calcEquation(equations, values, queries)
# equations = [["x1","x2"],["x2","x3"],["x3","x4"],["x4","x5"]]
# values = [3.0,4.0,5.0,6.0]
# queries = [["x1","x5"],["x5","x2"],["x2","x4"],["x2","x2"],["x2","x9"],["x9","x9"]]
# ret = Solution().calcEquation(equations, values, queries)
# [360.0,0.00833,20.0,1.0,-1.0,-1.0]
equations = [["a","b"],["e","f"],["b","e"]]
values = [3.4,1.4,2.3]
# queries = [["b","a"],["a","f"],["f","f"],["e","e"],["c","c"],["a","c"],["f","e"]]
queries = [["a","f"]]
ret = Solution().calcEquation(equations, values, queries)
# [0.29412,10.948,1.0,1.0,-1.0,-1.0,0.71429]
