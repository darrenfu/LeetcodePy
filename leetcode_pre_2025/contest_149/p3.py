class Solution:
    def maxRepOpt1(self, text: str) -> int:
        L = len(text)
        max_cnt = 0
        for i in range(L-1):
            char = text[i]
            cnt = 1
            exception = False
            for j in range(i+1, L):
                if text[j] == char:
                    cnt += 1
                elif not exception:
                    exception = True
                else:
                    break
            existsOtherChar = char in text[:i] or char in text[j+1:]
            max_cnt = max(max_cnt, cnt+1 if existsOtherChar else cnt)
        return max_cnt


print(Solution().maxRepOpt1("ababa"))
print(Solution().maxRepOpt1("aaabaaa"))
print(Solution().maxRepOpt1("aaabbaaa"))
print(Solution().maxRepOpt1("aaaaa"))
print(Solution().maxRepOpt1("abcdef"))
