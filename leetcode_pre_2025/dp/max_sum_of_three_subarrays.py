class Solution(object):
    def maxSumOfThreeSubarrays(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """
        # nums.length will be between 1 and 20000.
        # nums[i] will be between 1 and 65535.
        # k will be between 1 and floor(nums.length / 3).
        sum_len = len(nums) - k + 1
        dp = [0] * sum_len
        for i in range(sum_len):
            for j in range(k):
                dp[i] += nums[i+j]
        #print(dp)

        max_num = 0
        ii, jj, oo = 0, 0, 0
        for i in range(len(nums) - 3*k + 1):
            for j in range(i + k, len(nums) - 2*k + 1):
                for o in range(j + k, sum_len):
                    local_sum = dp[i] + dp[j] + dp[o]
                    if local_sum > max_num:
                        max_num = local_sum
                        ii, jj, oo = i, j, o
        return [ii, jj, oo]
