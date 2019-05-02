import collections

class Solution(object):
    def openLock(self, deadends, target):
        """
        :type deadends: List[str]
        :type target: str
        :rtype: int
        """
        def successors(node):
            res = []
            for i, c in enumerate(node):
                num = int(c)
                for j in [-1, 1]:
                    # roll ahead (0->9) or roll behind (0->1)
                    # node[0~(i-1)] + 'rolled_num' + node[(i+1)~(n-1)]
                    res.append(node[:i] + str((num + j) % 10) + node[(i+1):])
            return res

        q = collections.deque(['0000'])
        visited = set(deadends)
        levels = -1
        while q:
            levels += 1  # we need depth by depth scan/enqueue/dequeue, thus count queue size
            for _ in range(len(q)):
                node = q.popleft()
                if node == target:
                    return levels
                if node not in visited:
                    visited.add(node)
                    # list all possible rolls in coming step
                    q.extend(successors(node))
        return -1

