import os
import pickle
import tempfile
from typing import Any, Dict, List, Tuple, Iterator

Key = Any
Value = Any
Record = Tuple[Key, Value]
JoinedRecord = Tuple[Key, Value, Value]  # (key, left_value, right_value)

# partition_id -> list of (key, value)
MapperBuckets = Dict[int, List[Record]]
# partition_id -> key -> [values...]
CombinerBuckets = Dict[int, Dict[Key, List[Value]]]

# One MapperBuckets per mapper
ShuffleMatrix = List[MapperBuckets]


class Partitioner:
    """Deterministic partitioner. Maps a key into [0, num_partitions)."""

    def __init__(self, num_partitions: int) -> None:
        if num_partitions <= 0:
            raise ValueError("num_partitions must be positive")
        self.num_partitions = num_partitions

    def get_partition(self, key: Key) -> int:
        # Simple deterministic hash partitioner
        return hash(key) % self.num_partitions


class Bucket:
    """
    Abstract bucket that can store records either in memory or on disk.
    For simplicity we pickled records when spilling.
    """

    def __init__(self, spill_to_disk: bool = False) -> None:
        self._spill_to_disk = spill_to_disk
        self._in_memory: List[Record] = []

        self._file_path: str | None = None
        self._file_handle = None  # type: ignore

        if spill_to_disk:
            fd, path = tempfile.mkstemp(prefix="bucket_", suffix=".bin")
            os.close(fd)  # We'll reopen with normal file object
            self._file_path = path
            self._file_handle = open(path, "ab")  # append-binary

    def add(self, record: Record) -> None:
        if not self._spill_to_disk:
            self._in_memory.append(record)
        else:
            # Append a pickled record to file
            pickle.dump(record, self._file_handle)

    def iter_records(self) -> Iterator[Record]:
        if not self._spill_to_disk:
            yield from self._in_memory
        else:
            # Flush and reopen file for read
            self._file_handle.close()
            with open(self._file_path, "rb") as f:
                try:
                    while True:
                        yield pickle.load(f)
                except EOFError:
                    pass

    def cleanup(self) -> None:
        if self._file_handle and not self._file_handle.closed:
            self._file_handle.close()
        if self._file_path and os.path.exists(self._file_path):
            os.remove(self._file_path)