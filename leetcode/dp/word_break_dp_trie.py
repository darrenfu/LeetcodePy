from typing import List


class Solution:
    """
    Runtime: 152 ms, faster than 5.94%
    https://leetcode.com/problems/word-break/discuss/306561/A-Simple-Solution-Using-Tries
    """
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        t = Trie()
        for w in wordDict:
            t.addWord(w)

        L = len(s)
        dp = [True]
        for i in range(1, (L+1)):
            dp += any(dp[j] and t.checkWord(s[j:i]) for j in range(i)),
        return dp[-1]


class TrieNode:
    def __init__(self, letter):
        self.nodes = {}
        self.val = letter
        self.term = False

    def markTerm(self, stat):
        self.term = stat

    def isTerm(self):
        return self.term

    def addKid(self, kid):
        if kid not in self.nodes:
            self.nodes[kid] = TrieNode(kid)
        return self.nodes[kid]

    def getKid(self, kid):
        return self.nodes.get(kid)

    def hasKid(self, kid):
        return True if kid in self.nodes else False


class Trie:
    def __init__(self):
        self.root = TrieNode('Root')

    def addWord(self, word):
        p = self.root
        for w in word:
            p = p.addKid(w)
        p.markTerm(True)

    def checkWord(self, word):
        p = self.root
        for w in word:
            p = p.getKid(w)
            if p is None:
                return False
        return True if p.isTerm() else False


print(Solution().wordBreak(s="catsandog", wordDict=["cat", "san", "dog", "cats", "an", "og", "and"]))
