# Resumable Iterators
# Part 2: Resumable File Iterator + Multiple-File Resumable Iterator
# You are given an existing resumable file iterator that iterates through JSON files.
# Your tasks:
# 	1.	Implement a ResumableFileIterator that iterates JSON items inside a file.
# 	2.	Then implement MultipleResumableFileIterator, which:
# 	•	iterates across multiple JSON files in sequence
# 	•	uses one combined state object
# 	•	handles empty-file cases gracefully
# 	•	restores correctly using set_state()
# 	•	must deal with boundaries between files
# 	3.	Write comprehensive tests, including:
# 	•	save/restore across file boundaries
# 	•	handling empty files
# 	•	restoring at end-of-file
# 	•	restoring into the middle of a file
import json
from typing import List, Any, Dict

from resumable_iterator.iterator_1 import ListResumableIterator, \
    IteratorInterface


class ResumableFileIterator(ListResumableIterator):
    def __init__(self, json_fp: str) -> None:
        self._data = self._load_one_file(json_fp)
        self._index = 0

    def _load_one_file(self, fp: str) -> List[Any]:
        try:
            with open(fp) as f:
                data = json.load(f)
                if not isinstance(data, list):
                    print(f"json object is not an array from file: {fp}")
                    return []
                return data
        except (OSError, json.JSONDecodeError) as e:
            print("Error loading JSON", e)
        return []

class MultipleResumableFileIterator(ListResumableIterator):
    def __init__(self, json_fps: List[str]) -> None:
        self._file_paths = json_fps
        self._file_index = 0
        self._iter : ResumableFileIterator | None = None
        self._index = 0 # global index

    def __next__(self) -> Any:
        while self._file_index < len(self._file_paths):
            # Lazily create inner iterator for the current file
            if self._iter is None:
                self._iter = ResumableFileIterator(self._file_paths[self._file_index])
            try:
                # Try to yield from current file
                value = next(self._iter)
                self._index += 1
                return value
            except StopIteration:
                # Current file exhausted, move to next file
                self._file_index += 1
                self._iter = None
                # Loop continues to next file
        # No more files
        raise StopIteration

# Suboptimal solution: read all files at once in ctor
class MultipleResumableFileIterator1(ResumableFileIterator):
    def __init__(self, json_fps: List[str]) -> None:
        self._data = [self._load_one_file(fp) for fp in json_fps]
        self.sizes = [len(entries) for entries in self._data]
        self.total_size = sum(self.sizes)
        self._index = 0

    def __next__(self) -> Any:
        if self._index >= self.total_size:
            raise StopIteration
        cur_size = 0
        for i, size in enumerate(self.sizes):
            cur_size += size
            if self._index < cur_size:
                value = self._data[i][self._index + size - cur_size]
                self._index += 1
                return value

        raise StopIteration

if __name__ == "__main__":
    iter = ResumableFileIterator('json/basic1.json')
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

    print()
    iter = MultipleResumableFileIterator([
        'json/basic1.json', 'json/basic2.json', 'json/basic3.json', 'json/basic4.json', 'json/basic5.json'
    ])
    for i in range(8):
        print(i, next(iter))
    try:
        next(iter)
    except StopIteration as e:
        print("StopIteration")
    print(iter.get_state())
