from typing import List, Dict
from src.main.python import UF


class Solution:
    """
    737. Sentence Similarity II
    Tags: DFS, UnionFind
    Given two sentences words1, words2 (each represented as an array of strings), and a list of similar word pairs pairs, determine if two sentences are similar.
    For example, words1 = ["great", "acting", "skills"] and words2 = ["fine", "drama", "talent"] are similar, if the similar word pairs are pairs = [["great", "good"], ["fine", "good"], ["acting","drama"], ["skills","talent"]].
    Note that the similarity relation is transitive. For example, if "great" and "good" are similar, and "fine" and "good" are similar, then "great" and "fine" are similar.
    Similarity is also symmetric. For example, "great" and "fine" being similar is the same as "fine" and "great" being similar.
    Also, a word is always similar with itself. For example, the sentences words1 = ["great"], words2 = ["great"], pairs = [] are similar, even though there are no specified similar word pairs.
    Finally, sentences can only be similar if they have the same number of words. So a sentence like words1 = ["great"] can never be similar to words2 = ["doubleplus","good"].
    Note:
    - The length of words1 and words2 will not exceed 1000.
    - The length of pairs will not exceed 2000.
    - The length of each pairs[i] will be 2.
    - The length of each words[i] and pairs[i][j] will be in the range [1, 20].
    """

    def areSentencesSimilarTwo(self, words1: List[str], words2: List[str], pairs: List[List[str]]) -> bool:
        global_incr = 0

        def getWordIdx(word: str, dictionary: Dict[str, int], create: bool = False) -> int:
            nonlocal global_incr
            if word in dictionary:
                return dictionary[word]
            elif create:
                dictionary[word] = global_incr
                global_incr += 1
                return dictionary[word]
            return -1

        if len(words1) != len(words2):
            return False
        N = len(pairs) * 2
        uf = UF(N)
        # use a word-to-index map to map all words to UnionFind's int data structure (starting from 0!)
        hashmap = dict()
        # build union-find forest from all similar pairs, similar words will compose a cycle inside
        for edge in pairs:
            u = getWordIdx(edge[0], hashmap, True)
            v = getWordIdx(edge[1], hashmap, True)
            uf.union(u, v)
        # compare each word in words1 and words2 to see whether they are similar
        for i, w1 in enumerate(words1):
            w2 = words2[i]
            if w1 == w2: continue
            u, v = getWordIdx(w1, hashmap), getWordIdx(w2, hashmap)
            if u < 0 or v < 0: return False
            if uf.find(u) != uf.find(v): return False
        return True


words1 = ["great", "acting", "skills"]
words2 = ["fine", "drama", "talent"]
pairs = [["great", "good"], ["fine", "good"], ["acting", "drama"], ["skills", "talent"]]
ret = Solution().areSentencesSimilarTwo(words1, words2, pairs)
print(ret)
pairs = [["great", "good"],["skills", "talent"]]
ret = Solution().areSentencesSimilarTwo(words1, words2, pairs)
print(ret)
