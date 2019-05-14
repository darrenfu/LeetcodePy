class Solution(object):
    def lengthOfLongestSubstringKDistinct(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """
        from collections import Counter
        table = Counter()
        # initialize the hash map here

        counter = 0  # check whether the substring is valid
        # two pointers, one point to tail and one head
        # max_len is the length of substring
        begin, end, max_len = 0, 0, 0

        while end < len(s):
            end_c = s[end]
            table[end_c] += 1
            if len(table) > k:
                counter += 1
            end += 1

            while counter > 0:  # counter condition
                # print(begin, end, counter)

                # Case 1. update min_len here if finding minimum
                # update minimum should be inside the inner while loop

                begin_c = s[begin]
                table[begin_c] -= 1
                if not table[begin_c]:
                    del table[begin_c]
                if len(table) <= k:
                    counter -= 1
                # increase begin to make it invalid/valid again
                begin += 1

            # Case 2. update max_len here if finding maximum
            # update maximum should be after the inner while loop to guarantee that the substring is valid
            max_len = max(max_len, end - begin)
        print(max_len)
        return max_len


Solution().lengthOfLongestSubstringKDistinct("eceba", 2)
Solution().lengthOfLongestSubstringKDistinct("aa", 1)
