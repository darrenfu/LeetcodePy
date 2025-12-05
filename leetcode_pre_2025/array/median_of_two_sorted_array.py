from typing import List


class Solution:
    # another solution TODO: https://leetcode.com/problems/median-of-two-sorted-arrays/discuss/2567/Python-O(log(min(mn))-solution
    def findMedianSortedArrays(self, A: List[int], B: List[int]) -> float:
        def kth(A: List[int], B: List[int], k: int) -> int:
            if not B:
                return A[k]
            if not A:
                return B[k]
            ia, ib = len(A) // 2, len(B) // 2
            ma, mb = A[ia], B[ib]

            # when k is larger than the sum of a and b's median indices
            if ia + ib < k:
                # if b's median is larger than a's, a's first half doesn't include k
                if ma < mb:
                    return kth(A[ia+1:], B, k-ia-1)
                else:
                    return kth(A, B[ib+1:], k-ib-1)
            else:
                # if b's median is larger than a's, b's second half doesn't include k
                if ma < mb:
                    return kth(A, B[:ib], k)
                else:
                    return kth(A[:ia], B, k)

        L = len(A) + len(B)
        if L % 2 == 1:
            return kth(A, B, L//2)
        return (kth(A, B, L//2-1) + kth(A, B, L//2)) / 2


A, B = [1,2,5,6], [3,4,7]
print(Solution().findMedianSortedArrays(A, B))
