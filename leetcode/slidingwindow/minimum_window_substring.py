class Solution(object):
    def minWindow(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: str
        """
        from collections import Counter
        table = Counter()
        for c in t:
            table[c] += 1
        counter = len(table)

        begin, end, s_len = 0, 0, len(s) + 1
        ans = ""

        while end < len(s):
            end_c = s[end]
            if end_c in table:
                table[end_c] -= 1
                if table[end_c] == 0:
                    counter -= 1
            end += 1
            # print("end++", begin, end, s[begin:end], counter)

            while counter == 0:
                if end - begin < s_len:
                    s_len = end - begin
                    ans = s[begin:end]
                    # print(begin, end, ans)

                begin_c = s[begin]
                if begin_c in table:
                    table[begin_c] += 1
                    if table[begin_c] > 0: counter += 1
                # print("begin++", begin, end, s[begin:end], counter)
                begin += 1
        return ans

Solution().minWindow("ADOBECODEBANC", "ABC")
