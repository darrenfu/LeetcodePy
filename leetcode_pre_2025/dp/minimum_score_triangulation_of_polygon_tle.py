class Solution(object):
    def minScoreTriangulation(self, A):
        """
        :type A: List[int]
        :rtype: int
        """
        from functools import reduce

        def product(arr):
            return reduce((lambda x, y: x * y), arr)

        dct = {}

        def triple(arr):
            res = sorted(arr)
            return res[0], res[1], res[2]

        def dp(A):
            if len(A) == 3:
                triplet = triple(A)
                if triplet not in dct:
                    dct[triplet] = product(A)
                return dct[triplet]

            min_score = float('inf')
            for i in range(len(A) - 1):
                for j in range(len(A)):
                    if j == i or j == i + 1 or j == i - 1:
                        pass
                    else:
                        triangle = dp(A[i:i+2] + [A[j]])
                        if j == i + 2:
                            remaining_polygon = dp(A[:i+1] + A[i+2:])
                            min_score = min(min_score, remaining_polygon + triangle)
                        else:
                            left_polygon = dp(A[:i] + A[i+1:])
                            right_polygon = dp(A[:i+1] + A[i+2:])
                            # print(i,i+1,j, A[i],A[i+1],A[j], left_polygon, triangle, right_polygon)
                            min_score = min(min_score, left_polygon + triangle + right_polygon)
            return min_score
        score = dp(A)
        # print(score)
        return score
