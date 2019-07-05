from typing import List


class Solution:
    def distributeCandies(self, candies: int, num_people: int) -> List[int]:
        c, i = candies, 0
        res = [0] * num_people
        while c > 0:  # remaining candies
            for p in range(1, num_people+1):
                if c <= 0: break
                i += 1
                cur_candies = c if c < i else i
                c -= cur_candies
                res[p-1] += cur_candies
        return res


print(Solution().distributeCandies(candies=10**8, num_people=100))
print(Solution().distributeCandies(candies=10, num_people=3))



