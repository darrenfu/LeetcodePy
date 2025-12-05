class Solution(object):
    def knightProbability(self, N, K, r, c):
        """
        :type N: int
        :type K: int
        :type r: int
        :type c: int
        :rtype: float
        """

        dp = {}

        def next_move(i, r, c):
            if is_off_board(N, r, c):
                return 0.0
            if i == 0:
                return 1.0
            if (i, r, c) not in dp:
                dp[i, r, c] = .125 * sum(
                    next_move(i - 1, r + m, c + n) + next_move(i - 1, r + n, c + m)
                    for m in (-1, 1) for n in (-2, 2)
                )
            return dp[i, r, c]

        def is_off_board(lN, lr, lc):
            return not (0 <= lr < lN and 0 <= lc < lN)

        return next_move(K, r, c)
