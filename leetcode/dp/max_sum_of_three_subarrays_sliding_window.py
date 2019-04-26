class Solution(object):
    def maxSumOfThreeSubarrays(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """
        seq_sum, seq_two_sum, seq_three_sum = sum(nums[:k]), sum(nums[k:2 * k]), sum(nums[2 * k:3 * k])
        best_seq, best_two_seq, best_three_seq = [0], [0, k], [0, k, 2 * k]
        # sums of combined best windows
        best_seq_sum, best_two_sum, best_three_sum = seq_sum, seq_sum + seq_two_sum, seq_sum + seq_two_sum + seq_three_sum
        # Update first window start position
        for i in range(1, len(nums) - k * 3 + 1):
            seq_index = i
            two_seq_index = i + k
            three_seq_index = i + k * 2
            # Update the three sliding windows
            seq_sum, seq_two_sum, seq_three_sum = seq_sum - nums[seq_index - 1] + nums[seq_index + k - 1], \
                                                  seq_two_sum - nums[two_seq_index - 1] + nums[two_seq_index + k - 1], \
                                                  seq_three_sum - nums[three_seq_index - 1] + nums[three_seq_index + k - 1]
            # Update best single windows
            if seq_sum > best_seq_sum:
                best_seq_sum, best_seq = seq_sum, [seq_index]
            # Update best two windows
            if best_seq_sum + seq_two_sum > best_two_sum:
                best_two_sum, best_two_seq = best_seq_sum + seq_two_sum, best_seq + [two_seq_index]
            # Update best three windows
            if best_two_sum + seq_three_sum > best_three_sum:
                best_three_sum, best_three_seq = best_two_sum + seq_three_sum, best_two_seq + [three_seq_index]
        return best_three_seq
