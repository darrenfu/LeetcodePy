class Solution(object):
    def knightProbability(self, N, K, r, c):
        """
        :type N: int
        :type K: int
        :type r: int
        :type c: int
        :rtype: float
        """

        possible_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                          (2, -1), (2, 1), (1, -2), (1, 2)]
        dp = [[[0.0] * (K+1) for _ in range(N)] for _ in range(N)]

        def next_move(i, lr, lc):
            if is_off_board(N, lr, lc):
                return 0.0
            if i == K:
                return 1.0
            if dp[lr][lc][i] != 0:
                return dp[lr][lc][i]
            prob = 0.0
            for mr, mc in possible_moves:
                prob += 0.125 * next_move(i + 1, lr + mr, lc + mc)
            # memorization
            dp[lr][lc][i] = prob
            return prob

        def is_off_board(lN, lr, lc):
            return lr < 0 or lr >= lN or lc < 0 or lc >= lN

        return next_move(0, r, c)
