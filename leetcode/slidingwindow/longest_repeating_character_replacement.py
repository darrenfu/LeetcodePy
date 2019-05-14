class Solution(object):
    def characterReplacement(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """
        from collections import Counter
        table = Counter()
        # initialize the hash map here

        # two pointers, one point to tail and one head
        # max_len is the length of substring
        # max_char_cnt is the maximum count of repeating char in a sliding window
        begin, end, max_len, max_char_cnt = 0, 0, 0, 0

        while end < len(s):
            end_c = s[end]
            table[end_c] += 1
            # time complexity for `Counter.most_common(k)` is: O(nlogk)
            # table.most_common(1) returns a key-value pair list whose size is 1, here we need the value of
            # the most freq repeating char
            max_char_cnt = table.most_common(1)[0][1]
            # print("end", table.most_common(1)[0], begin, end)
            end += 1

            while end - begin > max_char_cnt + k:  # condition:
                # this sliding window must contain max_char_cnt repeated char + at most k other chars,
                # otherwise, start to move begin pointer

                # Case 1. update min_len here if finding minimum
                # update minimum should be inside the inner while loop

                begin_c = s[begin]
                table[begin_c] -= 1
                max_char_cnt = table.most_common(1)[0][1]
                # print("begin", table.most_common(1)[0], begin, end)
                # increase begin to make it invalid/valid again
                begin += 1

            # Case 2. update max_len here if finding maximum
            # update maximum should be after the inner while loop to guarantee that the substring is valid
            max_len = max(max_len, end - begin)
        print(max_len)
        return max_len


Solution().characterReplacement("ABAB", 2)
Solution().characterReplacement("AABABBA", 1)
