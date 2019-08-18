from collections import defaultdict

class Solution:
    def lastSubstring(self, s: str) -> str:
        # the answer must be starting with the largest letter, ending at the end of string S
        # use 'suffix array'

        L = len(s)
        # store a location array for each char in S
        predecessors = defaultdict(list)
        for i, v in enumerate(s):
            predecessors[v].append(i)
        # for every c, ensure all its predecessors are smaller than itself
        largestChar = max(predecessors.keys())
        starts = {}
        for pos in predecessors[largestChar]:

        for i, c in enumerate(s[::-1]):
            # avg = avg / 26.0 + (ord(c) - offset)
            # predecessors[c] -= 1
            # if predecessors[c] == 0:
            #     del predecessors[c]
            # if all(c >= p for p in predecessors.keys()):
            #     # check adjcent predecessor, if equals, continue
            #     consecutive = False
            #     for ii, pp in enumerate(s[L-i-2:0:-1]):
            #         if not consecutive and pp == c:
            #             consecutive = True
            #         if consecutive and pp != c:
            #             return s[L-2-i-ii:]
            #     return s[L-1-i:]
        return s


print(Solution().lastSubstring(s="abab"))
print(Solution().lastSubstring(s="zrziy"))
print(Solution().lastSubstring(s="leetcode"))
print(Solution().lastSubstring(s="xbylisvborylklftlkcioajuxwdhahdgezvyjbgaznzayfwsaumeccpfwamfzmkinezzwobllyxktqeibfoupcpptncggrdqbkji"))
print(Solution().lastSubstring(s="xbylisvborylklftlkcioajuxwdhahdgezvyjbgaznzayfwsaumeccpfwamfzmkinezzzwobllyxktqeibfoupcpptncggrdqbkji"))
