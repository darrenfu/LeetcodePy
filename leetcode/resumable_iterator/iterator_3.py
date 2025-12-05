# Resumable Iterators
# 📌 Part 3 — Async Version: Efficient Async Resumable File Iterator
#
# Convert your file-based iterators into async versions:
# 	•	async def __anext__(self)
# 	•	async def get_state(self)
# 	•	async def set_state(self, state)
#
# Requirements:
# 	1.	Must support efficient async I/O.
# 	2.	Must not block the event loop (avoid slow synchronous file reads).
# 	3.	Must maintain the correctness of save/restore semantics.
# 	4.	Write tests using Python’s async test framework.
import asyncio
import os
from concurrent.futures import ProcessPoolExecutor
from functools import partial

import json
from typing import List, Any, Dict, AsyncIterator, Protocol


class AsyncResumableIterator(AsyncIterator[Any]):
    """Abstract resumable iterator interface."""

    def __aiter__(self) -> "AsyncResumableIterator":
        return self

    async def __anext__(self) -> Any:
        raise NotImplementedError

    async def get_state(self) -> Dict[str, Any]:
        """Return a JSON-serializable state object."""
        raise NotImplementedError

    async def set_state(self, state: Dict[str, Any]) -> None:
        """Restore state from a JSON object."""
        raise NotImplementedError

@DeprecationWarning
async def async_open(path, mode="r", *args, **kwargs):
    loop = asyncio.get_running_loop()
    # run sync open() in a thread so it doesn't block the event loop
    return await loop.run_in_executor(
        None,
        partial(open, path, mode, *args, **kwargs)
    )

async def async_read(path: str, mode='r'):
    loop = asyncio.get_running_loop()
    def read():
        with open(path, mode) as f:
            return f.read()
    # When executor=None, Python uses the default ThreadPoolExecutor, NOT a ProcessPoolExecutor.
    return await loop.run_in_executor(None, read)

class ResumableFileIterator(AsyncResumableIterator):
    def __init__(self, file_path: str) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)
        self._file_path = file_path
        self._data: List[Any] | None = None
        self._index = 0

    async def _ensure_loaded(self) -> None:
        if self._data is not None:
            return

        def _sync_load() -> List[Any]:
            with open(self._file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    return []
            if data is None:
                return []
            if not isinstance(data, list):
                raise ValueError("JSON file must contain a top-level array")
            return data

        # runs in a thread; no event-loop blocking
        # equivalent to async_open() above
        self._data = await asyncio.to_thread(_sync_load)
        # If it is CPU bound, use ProcessPoolExecutor:
        # process_pool = ProcessPoolExecutor()
        # loop = asyncio.get_running_loop()
        # self._data = await loop.run_in_executor(process_pool, _sync_load)

    def __aiter__(self) -> "AsyncResumableFileIterator":
        return self

    async def __anext__(self) -> Any:
        await self._ensure_loaded()
        assert self._data is not None

        if self._index >= len(self._data):
            raise StopAsyncIteration

        value = self._data[self._index]
        self._index += 1
        return value

    async def get_state(self) -> Dict[str, Any]:
        # We allow index == len(_data) to represent "finished"
        return {"index": self._index}

    async def set_state(self, state: Dict[str, Any]) -> None:
        if "index" not in state:
            raise ValueError("state missing 'index'")

        idx = state["index"]
        if not isinstance(idx, int):
            raise ValueError("'index' must be an int")

        # Make sure data is loaded to validate bounds
        await self._ensure_loaded()
        assert self._data is not None

        if not (0 <= idx <= len(self._data)):
            raise ValueError(f"'index' out of range: {idx}")

        self._index = idx

class MultipleResumableFileIterator(AsyncResumableIterator):
    """
     Async iterator across multiple JSON files in sequence.

     State format:
       {
         "file_index": <int>,   # index into self._file_paths
         "inner_index": <int>   # index inside that file's array
       }

     When file_index == len(file_paths), the iterator is fully exhausted.
    """
    def __init__(self, json_fps: List[str]) -> None:
        self._file_paths = json_fps
        self._file_index = 0
        self._iter : ResumableFileIterator | None = None

    def __aiter__(self) -> "MultipleResumableFileIterator":
        return self

    async def _ensure_inner(self):
        """Create an inner iterator for current file if needed."""
        if self._iter is None and self._file_index < len(self._file_paths):
            path = self._file_paths[self._file_index]
            self._iter = ResumableFileIterator(path)

    async def __anext__(self) -> Any:
        while self._file_index < len(self._file_paths):
            await self._ensure_inner()
            assert self._iter is not None
            try:
                return await anext(self._iter)
            except StopIteration:
                self._file_index += 1
                self._iter = None
        raise StopIteration

    async def get_state(self) -> Dict[str, Any]:
        # Exhausted case
        if self._file_index >= len(self._file_paths):
            return {"file_index": len(self._file_paths), "inner_index": 0}

        # If inner not yet created, inner_index is 0
        if self._iter is None:
            inner_index = 0
        else:
            inner_state = await self._iter.get_state()
            inner_index = int(inner_state.get("index", 0))

        return {
            "file_index": self._file_index,
            "inner_index": inner_index,
        }

    async def set_state(self, state: Dict[str, Any]) -> None:
        if not isinstance(state, dict):
            raise ValueError("state must be a dict")

        if "file_index" not in state or "inner_index" not in state:
            raise ValueError("state must contain 'file_index' and 'inner_index'")

        fi = state["file_index"]
        ii = state["inner_index"]

        if not isinstance(fi, int) or not isinstance(ii, int):
            raise ValueError("'file_index' and 'inner_index' must be ints")

        if not (0 <= fi <= len(self._file_paths)):
            raise ValueError("'file_index' out of range")

        self._file_index = fi
        self._iter = None

        # Fully exhausted
        if self._file_index == len(self._file_paths):
            return

        # Recreate inner iterator at correct offset
        path = self._file_paths[self._file_index]
        self._iter = ResumableFileIterator(path)
        await self._iter.set_state({"index": ii})


async def main():
    it = MultipleResumableFileIterator(
        ["json/basic1.json", "json/basic2.json", "json/basic3.json", "json/basic4.json", "json/basic5.json"]
    )

    # Consume a few items
    async for item in it:
        print("item:", item)
        state = await it.get_state()
        print("state:", state)
        break  # pretend we stop early and need to resume later

    # Resume later from saved state
    resume_state = state
    it2 = MultipleResumableFileIterator(
        ["json/basic1.json", "json/basic2.json", "json/basic3.json", "json/basic4.json", "json/basic5.json"]
    )
    await it2.set_state(resume_state)

    async for item in it2:
        print("resumed:", item)

    print()
    iter = ResumableFileIterator('json/basic1.json')
    async for item in iter:
        print(item)
    print(await iter.get_state())

if __name__ == "__main__":
    asyncio.run(main())