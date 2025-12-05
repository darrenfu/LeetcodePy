class Solution(object):
    def lengthOfLongestSubstringTwoDistinct(self, s):
        """
        :type s: str
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
            if end_c not in table:
                table[end_c] = 0
            table[end_c] += 1
            if table[end_c] == 1:
                counter += 1
            end += 1

            while counter > 2:  # counter condition
                # print(begin, end, counter)

                # Case 1. update min_len here if finding minimum
                # update minimum should be inside the inner while loop

                begin_c = s[begin]
                if begin_c in table:
                    table[begin_c] -= 1
                    if table[begin_c] == 0:
                        # modify counter here
                        counter -= 1
                # increase begin to make it invalid/valid again
                begin += 1

            # Case 2. update max_len here if finding maximum
            # update maximum should be after the inner while loop to guarantee that the substring is valid
            max_len = max(max_len, end - begin)
        # print(max_len)
        return max_len


Solution().lengthOfLongestSubstringTwoDistinct("eceba")
Solution().lengthOfLongestSubstringTwoDistinct("ccaabbb")
