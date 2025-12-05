# Resumable Iterators
# 📌 Part 4 — Higher-Dimensional Resumable Iterators (2D + 3D) (LC251)
# You must generalize your iterator to handle multi-dimensional structures:
# 1. 2D Resumable List Iterator
# Given a list of lists:
# [
#   [1,2,3],
#   [4,5],
#   [6]
# ]
# Implement a resumable 2D iterator that:
# 	•	preserves the interface from Part 1
# 	•	emits all values in row-major order
# 	•	stores both row and column indices in state
# 	•	resumes correctly across row boundaries
# 	•	handles nested empty lists
# Important:
# next() may require recursive handling depending on your design.
#
# 2. 3D Resumable Iterator
# Extend your 2D iterator to 3D:
# [
#   [
#     [1,2],
#     [3]
#   ],
#   [
#     [],
#     [4,5]
#   ]
# ]
# Requirements:
# 	•	store full 3-dimensional indices in state
# 	•	handle all corner cases: empty inner lists, last element of a dimension, etc.
# 	•	write tests for all boundary behavior

from typing import Any, Dict

from resumable_iterator.iterator_1 import IteratorInterface

def iter_nd_values(data, ndim, depth=0):
    if depth == ndim - 1:
        # last dimension: data is a list of leaf values
        print("ndim - depth = 1")
        for x in data:
            yield x
    else:
        print("ndim - depth > 1")
        for sub in data:
            yield from iter_nd_values(sub, ndim, depth + 1)

class GeneratorBasedNDIterator(IteratorInterface):
    def __init__(self, data: Any, ndim: int):
        self._data = data
        self._ndim = ndim
        self._gen = iter_nd_values(data, ndim)
        print("init")
        self._count = 0   # how many elements have been yielded

    def __next__(self) -> Any:
        val = next(self._gen)
        self._count += 1
        return val

    def get_state(self) -> Dict[str, Any]:
        # Only save how many items we have yielded
        return {"count": self._count}

    def set_state(self, state: Dict[str, Any]) -> None:
        # Rebuild generator from scratch and skip 'count' items
        if "count" not in state:
            raise ValueError("missing 'count' in state")
        count = state["count"]
        self._gen = iter_nd_values(self._data, self._ndim)
        for _ in range(count):
            next(self._gen)
        self._count = count

if __name__ == "__main__":
    iter = GeneratorBasedNDIterator([[1,2,3], [4, 5], [6]], 2)
    for item in iter:
        print(item)
    print(iter.get_state())

    iter.set_state({'count': 3})
    for item in iter:
        print(item)
