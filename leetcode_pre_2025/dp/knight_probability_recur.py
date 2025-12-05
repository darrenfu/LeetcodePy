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

        def next_move(lN, i, lK, lr, lc):
            if is_off_board(lN, lr, lc):
                return 0.0
            if i == lK:
                return 1.0
            prob = 0.0
            for mr, mc in possible_moves:
                prob += 0.125 * next_move(lN, i + 1, lK, lr + mr, lc + mc)
            print(i, prob)
            return prob

        def is_off_board(lN, lr, lc):
            return lr < 0 or lr >= lN or lc < 0 or lc >= lN

        return next_move(N, 0, K, r, c)
