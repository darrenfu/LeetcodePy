from collections import defaultdict, deque


class Solution:
    # identical to #316
    def smallestSubsequence(self, text: str) -> str:
        dct = defaultdict(deque)
        # record index list for each character
        for i, v in enumerate(text):
            dct[v].append(i)

        keys = sorted(dct.keys())
        LK = len(keys)
        res = []
        last_idx = -1

        # total result length should be smaller than district char number
        while len(res) < LK:
            # search the first smallest letter
            for i in range(len(keys)):
                # first index of char i is less than all last indexes of char j (j > i)
                # e.g. s = 'cdadabcc'
                # index['a'] = [2, 4]
                # index['b'] = [5]
                # index['c'] = [0, 6, 7]
                # index['d'] = [1, 3]
                # which will be the first letter in ans?
                # it will be letter 'a' because 2 < min(5, 7, 3), (5,7,3) is the last index of other letters
                if all(dct[keys[i]][0] < dct[keys[j]][-1] for j in range(i+1, len(keys))):
                    res.append(keys[i])
                    last_idx = dct[keys[i]][0]
                    keys.remove(keys[i])
                    break
            # remove all indexes less than last_idx
            for k in range(len(keys)):
                while dct[keys[k]] and dct[keys[k]][0] < last_idx:
                    dct[keys[k]].popleft()

        return ''.join(res)


text = "ecbacba"
Solution().smallestSubsequence(text)
