class Solution(object):
    def leastInterval(self, tasks, n):
        """
        :type tasks: List[str]
        :type n: int
        :rtype: int
        """
        from collections import Counter
        freqs = Counter(tasks).values()
        queue = map(lambda x: -x, freqs)
        import heapq
        heapq.heapify(queue)  # in-place converted to a max heap

        ret = 0
        while queue:
            i = 0
            tmp = []
            while i <= n:
                if queue:
                    print("#", i, "pop:", -queue[0])
                    if -queue[0] > 1:
                        tmp.append(-heapq.heappop(queue) - 1)
                    else:
                        heapq.heappop(queue)
                ret += 1
                if not queue and not tmp:
                    break
                i += 1
            for l in tmp:
                print("push:", l)
                heapq.heappush(queue, -l)
        return ret
