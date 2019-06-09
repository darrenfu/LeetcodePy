from typing import List

class Solution:
    def addNegabinary(self, arr1: List[int], arr2: List[int]) -> List[int]:
        """
        ref: https://en.wikipedia.org/wiki/Negative_base#Addition
            Carry:          1 −1  0 −1  1 −1  0  0  0
            First addend:         1  0  1  0  1  0  1
            Second addend:        1  1  1  0  1  0  0 + addition
                            --------------------------
            Number:         1 −1  2  0  3 −1  2  0  1 when we come with a number, lookup from the hashtable
            -----------------------------------------
            Bit (result):   1  1  0  0  1  1  0  0  1
            Carry:          0  1 −1  0 −1  1 −1  0  0 <- each number will be moved to the carry on the top in the next bit
        :param arr1:
        :param arr2:
        :return:
        """
        lookup = {
            # key: Number
            # value: (Bit(Result), Carry)
            # -2: (0, 1),  # useless because −2 occurs only during subtraction
            -1: (1, 1),
            0: (0, 0),
            1: (1, 0),
            2: (0, -1),
            3: (1, -1),
        }
        carry = 0
        result = []
        while len(arr1) > 0 or len(arr2) > 0:
            a, b = (arr1 or [0]).pop(), (arr2 or [0]).pop()
            tmp_res = a + b + carry
            res, carry = lookup[tmp_res]
            result.insert(0, res)
        # if there is still a carry
        while carry != 0:
            res, carry = lookup[carry]
            result.insert(0, res)
        # remove leading zeros
        while len(result) > 1 and result[0] == 0:
            result.pop(0)
        # reverse array
        # ret = result[::-1]
        # print(result)
        return result


arr1, arr2 = [1, 1, 1, 1, 1], [1, 0, 1]
Solution().addNegabinary(arr1, arr2)
arr1, arr2 = [1], [1]
Solution().addNegabinary(arr1, arr2)
arr1, arr2 = [1], [1,1]
Solution().addNegabinary(arr1, arr2)
arr1, arr2 = [1], [1,0,1]
Solution().addNegabinary(arr1, arr2)
