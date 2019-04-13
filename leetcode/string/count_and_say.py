class Solution(object):
    def countAndSay(self, n):
        """
        :type n: int
        :rtype: str
        """
        input = "1"
        output = []
        for i in range(1, n):
            prev = ""
            cnt = 0
            for c in input:
                if c != prev:
                    if prev != "":
                        output.append(str(cnt))
                        output.append(prev)
                    cnt = 1
                else:
                    cnt += 1
                prev = c
            # count and say the remaining part
            output.append(str(cnt) + prev)
            # current round's output as next round's input
            input = "".join(output)
            # print(input)
            output = []
        return input
