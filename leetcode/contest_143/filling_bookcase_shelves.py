from typing import List
import math


class Solution:
    def minHeightShelves(self, books: List[List[int]], shelf_width: int) -> int:
        L = len(books)
        widths = [0] * L
        heights = [0] * L
        for i, b in enumerate(books):
            w, h = b[0], b[1]
            widths[i] = w
            heights[i] = h

        def dp(start: int) -> int:
            if start >= L:
                return 0
            if start in cache:
                return cache[start]
            end, cur_w, max_h, min_max_h = 0, 0, 0, math.inf
            for k in range(start, L):
                if cur_w + widths[k] > shelf_width:
                    break
                cur_w += widths[k]
                max_h = max(max_h, heights[k])
                min_max_h = min(min_max_h, max_h + dp(k + 1))
            cache[start] = min_max_h
            return cache[start]

        cache = {}
        return dp(0)


print(Solution().minHeightShelves(books=[[1, 1], [2, 3], [2, 3], [1, 1], [1, 1], [1, 1], [1, 2]], shelf_width=4))
