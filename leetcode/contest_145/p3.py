from typing import List


class Solution(object):
    """
    https://leetcode.com/problems/longest-well-performing-interval/discuss/334565/JavaC%2B%2BPython-O(N)-Solution-Life-needs-996-and-669
    Or from @badgergo - Rank 2 - https://leetcode.com/contest/weekly-contest-145/ranking/1/
    """
    def longestWPI(self, hours: List[int]) -> int:
        hours = [1 if h > 8 else -1 for h in hours]
        sum, ans = 0, 0
        memo = {0: -1}
        for i, v in enumerate(hours):
            sum += v
            if sum > 0:
                ans = i + 1
            if sum not in memo:
                memo[sum] = i
            if (sum - 1) in memo:
                # Hard to understand!
                ans = max(ans, i - memo[sum - 1])
        return ans


print(Solution().longestWPI(hours=[9, 9, 6, 0, 6, 6, 9]))
