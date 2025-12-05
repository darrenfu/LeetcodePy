from typing import List

class Solution:
    def pathInZigZagTree(self, label: int) -> List[int]:
        depth = 0
        for exp in range(20, -1, -1):  # 2**20 is just larger than 10**6 while 2**19 is not
            if label < 2 ** exp:
                depth = exp
            else:
                break

        ancestor = label
        ancestors = [ancestor]
        while ancestor > 1:
            ancestor //= 2
            depth -= 1
            mid_times_2 = 2 ** depth + 2 ** (depth-1) - 1
            ancestor = mid_times_2 - ancestor
            ancestors.append(ancestor)
        return ancestors[::-1]


print(Solution().pathInZigZagTree(14))
print(Solution().pathInZigZagTree(26))
print(Solution().pathInZigZagTree(10**6))



