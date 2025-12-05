from copy import deepcopy
from typing import List, Tuple
from itertools import chain

class PuzzleSlider:

    def __init__(self, grid: List[List[int]]):
        self.grid = grid
        self.R, self.C = len(grid), len(grid[0])
        self.pos = self.getZeroPos(self.grid)

    def getZeroPos(self, grid: List[List[int]]):
        for i in range(self.R):
            for j in range(self.C):
                if grid[i][j] == 0:
                    return (i, j)
        return (-1,-1)

    def move(self, h_direction: int, v_direction: int):
        # h_direction: -1: left, 0: no_move, 1: right
        # v_direction: -1: down, 0: no_move, 1: up
        # return next state of the grid
        i, j = self.pos  # current zero position
        x, y = i + v_direction, j + h_direction
        if 0<=x<self.R and 0<=y<self.C:
            self.grid[i][j], self.grid[x][y] = self.grid[x][y], self.grid[i][j]

    def is_solvable(self, dest: List[List[int]]) -> bool:
        start = self.to1d(self.grid)
        q = [self.grid]
        visited = set(start)
        dest1d = self.to1d(dest)
        while q:
            cur_state = q.pop(0)
            cur1d = self.to1d(cur_state)
            self.pos = self.getZeroPos(cur_state)
            if cur1d == dest1d:
                print(cur_state, self.pos)
                return True
            cur = deepcopy(cur_state)
            for deltax, deltay in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                reset = deepcopy(cur)
                self.grid = reset
                self.move(deltax, deltay)
                tup = self.to1d(self.grid)
                if tup not in visited:
                    visited.add(tup)
                    q.append(self.grid)
                self.grid = reset
        return False

    def to1d(self, grid: List[List[int]]) -> Tuple[int]:
        return tuple(chain(*grid))


ps = PuzzleSlider(grid=[
    # [1,2,3],
    # [8,0,5],
    # [4,7,6]
    # [3,1,2],
    # [0,4,5],
    # [6,7,8]
    [8,1,2],
    [0,4,3],
    [7,6,5]
])

print(ps.is_solvable(dest=[
    [1,2,3],
    [4,5,6],
    [7,8,0]
]))

#ps.move(-1,0) # left move
# left, right, up, down
# init = deepcopy(ps.grid)
# for deltax, deltay in ((-1, 0), (1, 0), (0, -1), (0, 1)):
#     reset = deepcopy(init)
#     ps.move(deltax, deltay)
#     print(ps.grid)
#     ps.grid = reset


