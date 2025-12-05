class Solution(object):
    def maxSumOfThreeSubarrays(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """
        # Greedy algo
        best_seq, best_two_seq, best_three_seq = [0], [0,k], [k, 2*k]
        seq_sum, two_sum, three_sum = sum(nums[:k]), sum(nums[k:2*k]), sum(nums[2*k:3*k])
        best_seq_sum, best_two_sum, best_three_sum = seq_sum, seq_sum + two_sum, seq_sum + two_sum + three_sum

        def slide(sum, idx):
            return sum - nums[idx-1] + nums[idx+k-1]

        def compare_best_sum(prev_best_sum, cur_win_sum, cur_win_best_sum, prev_best_seq, cur_win_seq_idx, cur_win_best_seq):
            # e.g. compare (best two sums + current sum of third window) with best three sums
            if prev_best_sum + cur_win_sum > cur_win_best_sum:
                return prev_best_sum + cur_win_sum, prev_best_seq + [cur_win_seq_idx]
            return cur_win_best_sum, cur_win_best_seq

        for i in range(1, len(nums) - 3*k + 1):
            seq_idx = i
            seq_two_idx = i + k
            seq_three_idx = i + 2*k
            seq_sum = slide(seq_sum, seq_idx)
            two_sum = slide(two_sum, seq_two_idx)
            three_sum = slide(three_sum, seq_three_idx)

            best_seq_sum, best_seq = compare_best_sum(0, seq_sum, best_seq_sum, [], seq_idx, best_seq)
            best_two_sum, best_two_seq = compare_best_sum(best_seq_sum, two_sum, best_two_sum, best_seq, seq_two_idx, best_two_seq)
            best_three_sum, best_three_seq = compare_best_sum(best_two_sum, three_sum, best_three_sum, best_two_seq, seq_three_idx, best_three_seq)
        return best_three_seq
