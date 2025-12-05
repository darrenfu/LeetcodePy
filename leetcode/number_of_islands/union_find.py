from enum import Enum
from typing import List, Any

from scipy.cluster.hierarchy import DisjointSet

class Heuristic(Enum):
    NONE = 0
    RANK = 1
    SIZE = 2

# Required components
# •	Parent map ✔️
# •	Path compression ✔️
# •	Subset count ✔️
class DisjointSet:
    # The element must be a hashable object
    def __init__(self, elements: List[Any], heuristic: Heuristic = Heuristic.SIZE):
        # Initially, every node is a root, and root must point to themselves
        self._parents = {i:i for i in elements}
        self.n_subsets = len(self._parents)

        # Optional optimizations: union-by-rank (or size), prevents the tree from becoming tall.
        self.heuristic = heuristic
        if heuristic == Heuristic.RANK:
            self._rank = {e: 0 for e in elements}
        elif heuristic == Heuristic.SIZE:
            self._size = {e:1 for e in elements}

    def find(self, x: Any) -> Any:
        if x not in self._parents:
            raise KeyError(f"Key {x} not found in DisjointSet")
        if self._parents[x] != x: # x is not a root
            # path compression
            self._parents[x] = self.find(self._parents[x])
        return self._parents[x]

    def add(self, x: Any) -> None:
        if x not in self._parents:
            self._parents[x] = x
            self.n_subsets += 1
            if self.heuristic == Heuristic.RANK:
                self._rank[x] = 0
            elif self.heuristic == Heuristic.SIZE:
                self._size[x] = 1

    def connected(self, a: Any, b: Any) -> bool:
        return self.find(a) == self.find(b)

    def merge(self, e1: Any, e2: Any) -> bool:
        p1, p2 = self.find(e1), self.find(e2)
        # They already share a common root
        if p1 == p2:
            return False
        # Do not share a common root, connecting the two roots, and root_number --
        if self.heuristic == Heuristic.NONE:
            # Naive solution: always stack p1 on top of p2
            self._parents[p1] = p2
        # Optimization space:
        # Always attach p1 under p2. In worst cases this can create tall trees (though path compression helps a lot).
        elif self.heuristic == Heuristic.RANK:
            # Union-by-rank idea: Always attach the smaller rank (shallow tree) under the larger rank (deeper tree).
            # Ensure p1 is the root with higher (or equal) rank
            if self._rank[p1] < self._rank[p2]:
                p1, p2 = p2, p1

            # Now p1 always has >= rank, aka. deeper tree
            self._parents[p2] = p1

            # If equal rank, increase rank of the new root
            if self._rank[p1] == self._rank[p2]:
                self._rank[p1] += 1
        elif self.heuristic == Heuristic.SIZE:
            # Union-by-size: Always attach the smaller set under the larger set.
            if self._size[p1] < self._size[p2]:
                p1, p2 = p2, p1

            # Now p1 has the larger (or equal) size
            self._parents[p2] = p1
            self._size[p1] += self._size[p2]

        self.n_subsets -= 1
        return True

# This problem is essentially about counting connected components among cells that contain ‘1’.
# Why DSU fits this problem
#   Union-Find efficiently tracks which elements belong to the same connected component.
#   Every time two adjacent land cells are neighbors, we union their sets.
#   Then the number of islands is simply the number of distinct roots among all land cells.
# Pattern: dynamic connectivity

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid or not grid[0]:
            return 0
        R, C = len(grid), len(grid[0])
        land_indices = [(r, c)
                        for r in range(R)
                        for c in range(C)
                        if grid[r][c] == '1']
        if not land_indices:
            return 0

        dset = DisjointSet(land_indices)
        directions = ((0, 1), (1, 0))

        # Traversal logic:
        # For each land cell, I check its neighbors (usually right and down to avoid duplicates).
        # When two neighbors are both land, I call union on their ids (here it's coordinates).
        # This merges all connected land cells into the same component.
        for r in range(R):
            for c in range(C):
                if grid[r][c] == '1':
                    # Go right or go down
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if nr < R and nc < C and grid[nr][nc] == '1':
                            dset.merge((r, c), (nr, nc))

        number_of_islands = dset.n_subsets
        print(number_of_islands)
        return number_of_islands

Solution().numIslands([["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]])

