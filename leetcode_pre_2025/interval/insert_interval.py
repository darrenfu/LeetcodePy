class Solution(object):
    def insert(self, intervals, newInterval):
        """
        :type intervals: List[Interval]
        :type newInterval: Interval
        :rtype: List[Interval]
        """
        # Solution 1
        # s, e = newInterval.start, newInterval.end
        # left = [i for i in intervals if i.end < s]
        # right = [i for i in intervals if i.start > e]
        # if left + right != intervals:
        #     s = min(s, intervals[len(left)].start)
        #     # ~x means -x-1
        #     e = max(e, intervals[~len(right)].end)
        # return left + [Interval(s, e)] + right

        # Solution 2
        # s, e = newInterval.start, newInterval.end
        # parts = merge, left, right = [], [], []
        # for i in intervals:
        #     parts[(i.end < s) - (i.start > e)].append(i)
        #     print((i.end < s) - (i.start > e), i, parts)
        # if merge:
        #     s = min(s, merge[0].start)
        #     e = max(e, merge[-1].end)
        # return left + [Interval(s, e)] + right

        # Solution 3
        ret = []
        for i in intervals:
            if not newInterval or i.end < newInterval.start:
                ret.append(i)
            elif newInterval.end < i.start:
                ret.append(newInterval)
                ret.append(i)
                newInterval = None # next round will go to the first if
            else:
                newInterval.start = min(newInterval.start, i.start)
                newInterval.end = max(newInterval.end, i.end)
        if newInterval: # append last element
            ret.append(newInterval)
        return ret
