class Solution(object):
    def subarraysWithKDistinct(self, A, K):
        """
        :type A: List[int]
        :type K: int
        :rtype: int
        """

        def atMostK(A, K):
            from collections import Counter
            table = Counter()
            # initialize the hash map here

            # two pointers, one point to tail and one head
            begin, end, counter, res = 0, 0, 0, 0

            while end < len(A):
                end_c = A[end]
                if not table[end_c]:
                    counter += 1
                table[end_c] += 1
                end += 1

                while counter > K:  # condition

                    # Case 1. update min_len here if finding minimum
                    # update minimum should be inside the inner while loop

                    begin_c = A[begin]
                    table[begin_c] -= 1
                    if not table[begin_c]:
                        counter -= 1
                    # increase begin to make it invalid/valid again
                    begin += 1

                # Case 2. update max_len here if finding maximum
                # update maximum should be after the inner while loop to guarantee that the substring is valid

                # Smart:
                # end-begin+1 equal to the total number of subarrays ending at end contains at most K distinct integers
                res += end - begin + 1
            return res

        # Smart:
        # exactly K result = at most K result - at most K-1 result
        ans = atMostK(A, K) - atMostK(A, K - 1)
        return ans


Solution().subarraysWithKDistinct([1,2,1,2,3], 2)
Solution().subarraysWithKDistinct([1,2,1,3,4], 3)
