from leetcode.interval.interval import Interval


class Solution(object):

    def merge(self, intervals):
        """
        :type intervals: List[Interval]
        :rtype: List[Interval]
        """
        if len(intervals) <= 1:
            return intervals

        def overlap(l1, l2):
            """
            :type l1: Interval
            :type l2: Interval
            """
            return l2.start <= l1.end

        def merge_one(l1, l2):
            """
            :type l1: Interval
            :type l2: Interval
            """
            return Interval(l1.start, max(l1.end, l2.end))

        def eq(l1, l2):
            """
            :type l1: Interval
            :type l2: Interval
            """
            return l1.start == l2.start and l1.end == l2.end

        ret = []
        # Greedy: Earliest start time
        sorted_itvs = sorted(intervals, key=lambda x: x.start)
        merged_itv = sorted_itvs[0]
        for i in range(1, len(sorted_itvs)):
            itv = sorted_itvs[i]
            if overlap(merged_itv, itv):
                merged_itv = merge_one(merged_itv, itv)
            else:
                ret.append(merged_itv)
                merged_itv = itv
        if not ret or not eq(ret[-1], merged_itv):
            ret.append(merged_itv)
        return ret
