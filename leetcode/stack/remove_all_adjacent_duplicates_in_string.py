class Solution:
    def removeDuplicates(self, S: str) -> str:
        res = []
        for c in S:
            if res and res[-1] == c:
                res.pop()
            else:
                res.append(c)
        res = "".join(res)
        print(res)
        return res

Solution().removeDuplicates("abbaca")
Solution().removeDuplicates("aaaaaaaaa")
