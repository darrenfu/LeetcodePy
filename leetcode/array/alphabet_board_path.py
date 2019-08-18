

class Solution:
    def alphabetBoardPath(self, target: str) -> str:
        def charToBoardPoint(ch: str) -> (int, int):
            diff = ord(ch) - ord('a')
            return diff // 5, diff % 5

        targetBoards = [charToBoardPoint(ch) for ch in target]
        # print(targetBoards)
        cur = (0,0)
        res = []
        for dest in targetBoards:
            rOffset, cOffset = dest[0]-cur[0], dest[1]-cur[1]
            moves = []
            if dest == cur:
                pass
            elif dest[0] == 5:  # dest is point z at Row 5
                yMoves = ['L'] * (-cOffset)
                xMoves = ['D'] * rOffset
                moves = yMoves + xMoves
            # elif cur[0] == 5:  # cur is point z
            #     xMoves = ['U'] * (-rOffset)
            #     yMoves = ['R'] * cOffset
            #     moves = xMoves + yMoves
            else:
                xMoves = ['D'] * rOffset if rOffset > 0 else ['U'] * (-rOffset)
                yMoves = ['R'] * cOffset if cOffset > 0 else ['L'] * (-cOffset)
                moves = xMoves + yMoves
            res += (moves + ['!'])
            cur = dest
        return ''.join(res)


assert Solution().alphabetBoardPath(target="leet") == 'DDR!UURRR!!DDD!'
assert Solution().alphabetBoardPath(target="code") == 'RR!DDRR!UUL!R!'
assert Solution().alphabetBoardPath(target="jzz") == 'DRRRR!LLLLDDDD!!'
assert Solution().alphabetBoardPath(target="cozez") == 'RR!DDRR!LLLLDDD!UUUUURRRR!LLLLDDDDD!'
