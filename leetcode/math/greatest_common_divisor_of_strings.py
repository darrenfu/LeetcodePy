class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        l1, l2 = len(str1), len(str2)
        lstr = str1 if l1 > l2 else str2
        sstr = str2 if l1 > l2 else str1
        while sstr != '':
            for i, s in enumerate(sstr):
                if lstr[i] != s:
                    return ""
            newstr1 = sstr
            newstr2 = lstr[len(sstr):]
            l1, l2 = len(newstr1), len(newstr2)
            lstr = newstr1 if l1 > l2 else newstr2
            sstr = newstr2 if l1 > l2 else newstr1
        print(lstr)
        return lstr


str1, str2 = 'TUAXLDDFDSU', 'TUAXLDDFDSUTUAXLDDFDSUTUAXLDDFDSUTUAXLDDFDSUTUAXLDDFDSUTUAXLDDFDSU'
Solution().gcdOfStrings(str1, str2)
str1, str2 = 'ABCABC', 'ABC'
Solution().gcdOfStrings(str1, str2)
str1, str2 = 'ABABAB', 'ABAB'
Solution().gcdOfStrings(str1, str2)
str1, str2 = 'LEET', 'CODE'
Solution().gcdOfStrings(str1, str2)
