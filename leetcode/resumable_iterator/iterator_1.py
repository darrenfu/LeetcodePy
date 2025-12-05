# Resumable Iterators
# You are asked to design and implement a family of resumable iterators that
# support saving and restoring execution state via getState() and setState(state).
# A resumable iterator behaves like a normal iterator, but can be paused,
# serialized, deserialized, and resumed later—even across process boundaries.
import json
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Any, Iterator, Dict


# Part 1: Implement the Basic Interface + List Resumable Iterator
# class IteratorInterface:
#     def __init__(self): pass
#     def __iter__(self): pass
#     def __next__(self): pass
#     def get_state(self): pass
#     def set_state(self, state): pass
# Implement a resumable list iterator over a Python list (e.g. [1,2,3,4]):
# 	•	next -> 1
# 	•	next -> 2
# 	•	getState -> { "index": 2 }
# 	•	resume from that state:
# 	•	next -> 3, then next -> 4, etc.
# get_state() must return a dedicated state object/class, not just a raw number.
# set_state() must correctly resume iteration from the saved point.
# Your implementation must handle:
# 	•	stopping correctly
# 	•	state validation
# 	•	edge cases (empty list, restoring bad state)
# 	Write runnable unit tests to verify:
# 	•	correctness of iteration
# 	•	correctness of state save/restore
# 	•	stopping conditions
#
@dataclass(frozen=True)
class IteratorState:
    index: int

class IteratorInterface(Iterator):
    """Abstract resumable iterator interface."""

    def __iter__(self) -> "IteratorInterface":
        return self

    def __next__(self) -> Any:
        raise NotImplementedError

    def get_state(self) -> Dict[str, Any]:
        """Return a JSON-serializable state object."""
        raise NotImplementedError

    def set_state(self, state: Dict[str, Any]) -> None:
        """Restore state from a JSON object."""
        raise NotImplementedError

class ListResumableIterator(IteratorInterface):
    def __init__(self, data: List[Any]) -> None:
        self._data = data
        self._index = 0

    def __next__(self) -> Any:
        if self._index >= len(self._data):
            raise StopIteration
        value = self._data[self._index]
        self._index += 1
        return value

    def get_state(self) -> Dict[str, Any]:
        """
        Return a JSON-serializable state object.
        Always return a copy so the caller cannot mutate internal state.
        """
        return {"index": self._index}

    def set_state(self, state: Dict[str, Any]) -> None:
        """
        Validate and restore state. The expected shape is:
            { "index": <int> }
        """
        if "index" not in state:
            raise ValueError("State missing required key: 'index'")

        index = state["index"]
        if not isinstance(index, int):
            raise ValueError("'index' must be an integer")

        # allow index == len(self._data) so a completed iterator can be resumed
        if not (0 <= index <= len(self._data)):
            raise ValueError(f"'index' out of range: {index}")

        # copy to internal storage
        self._index = index

if __name__ == "__main__":
    iter = ListResumableIterator([1,2,3])
    print(next(iter))
    print(next(iter))
    print(next(iter))
    print(iter.get_state())
    iter.set_state({'index': 2})
    print(next(iter))
    try:
        next(iter)
    except StopIteration as e:
        print("StopIteration")
    iter.set_state({'index': 3})
