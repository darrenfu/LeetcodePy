from bisect import bisect_right
import math


class SnapshotArray:

    def __init__(self, length: int):
        self.arr = [[(0, 0)] for _ in range(length)]
        self.snaps = 0

    def set(self, index: int, val: int) -> None:
        self.arr[index].append((self.snaps, val))

    def snap(self) -> int:
        res = self.snaps
        self.snaps += 1
        return res

    def get(self, index: int, snap_id: int) -> int:
        idx = bisect_right(self.arr[index], (snap_id, math.inf))  # (snap_id, inf) is bigger than any (snap_id, int)
        # which is right next to we expect to fetch, so idx-1 is the location to get
        return self.arr[index][idx-1][1]

# Your SnapshotArray object will be instantiated and called as such:
# obj = SnapshotArray(length)
# obj.set(index,val)
# param_2 = obj.snap()
# param_3 = obj.get(index,snap_id)
