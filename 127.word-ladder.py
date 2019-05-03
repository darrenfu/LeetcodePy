import collections
#
# @lc app=leetcode id=127 lang=python
#
# [127] Word Ladder
#
class Solution(object):
    def ladderLength(self, beginWord, endWord, wordList):
        """
        :type beginWord: str
        :type endWord: str
        :type wordList: List[str]
        :rtype: int
        """
        dct = collections.defaultdict(list)
        q = collections.deque([beginWord])
        visited = set()
        levels = 0

        def get_word_with_one_star(w, i):
            return w[:i] + "*" + w[i+1:]

        for w in wordList:
            for i in range(len(w)):
                dct[get_word_with_one_star(w, i)].append(w)

        while q:
            levels += 1
            for _ in range(len(q)):
                w = q.popleft()
                if w == endWord:
                    return levels
                for i in range(len(w)):
                    neighbors = dct[get_word_with_one_star(w, i)]
                    for w2 in neighbors:
                        if w2 not in visited:
                            visited.add(w2)
                            q.append(w2)
        return 0
