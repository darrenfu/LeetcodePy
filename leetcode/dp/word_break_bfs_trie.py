from typing import List


class Solution:
    """
    https://leetcode.com/problems/word-break/discuss/274536/python-trie-%2B-bfs-solution.-O(N)-on-english-dictionary
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


class Trie:
    def __init__(self):
        self.arr = [None] * 26
        self.word = False

    def add_chr(self, c):
        if self.arr[ord(c) - ord('a')] is None:
            self.arr[ord(c) - ord('a')] = Trie()
        return self.arr[ord(c) - ord('a')]

    def get_chr(self, c):
        return self.arr[ord(c) - ord('a')]

    def is_word(self):
        return self.word

    def make_word(self):
        self.word = True

    def add_word(self, word):
        node = self
        for c in word:
            node = node.add_chr(c)
        node.make_word()


print(Solution().wordBreak(s="catsandog", wordDict=["cat", "san", "dog", "cats", "an", "og", "and"]))
