class Solution(object):
    def longestOnes(self, A, k):
        """
        easy edition of longest_repeating_character_replacement
        :type A: List[int]
        :type k: int
        :rtype: int
        """
        # two pointers, one point to tail and one head
        # max_len is the length of substring
        # max_one_cnt is the maximum count of repeating ones in a sliding window
        begin, end, max_len, max_one_cnt = 0, 0, 0, 0

        while end < len(A):
            end_i = A[end]
            if end_i == 1: max_one_cnt += 1
            end += 1

            while end - begin > max_one_cnt + k:  # condition:
                # this sliding window must contain max_one_cnt repeated ones + at most k other ones,
                # otherwise, start to move begin pointer

                # Case 1. update min_len here if finding minimum
                # update minimum should be inside the inner while loop

                begin_i = A[begin]
                if begin_i == 1: max_one_cnt -= 1
                # increase begin to make it invalid/valid again
                begin += 1

            # Case 2. update max_len here if finding maximum
            # update maximum should be after the inner while loop to guarantee that the substring is valid
            max_len = max(max_len, end - begin)
        print(max_len)
        return max_len


Solution().longestOnes([1,1,1,0,0,0,1,1,1,1,0], 2)
Solution().longestOnes([0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], 3)
