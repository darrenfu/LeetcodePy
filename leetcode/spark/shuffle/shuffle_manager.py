from typing import Iterable

from spark.shuffle.common import ShuffleMatrix, Record


class ShuffleManager:
    """
    Holds the logical shuffle matrix:
    - matrix[mapper_id][partition_id] -> list of (key, value)
    """

    def __init__(self, shuffle_matrix: ShuffleMatrix, num_partitions: int) -> None:
        self._matrix = shuffle_matrix
        self._num_partitions = num_partitions

    @property
    def num_partitions(self) -> int:
        return self._num_partitions

    def get_partition_data(self, partition_id: int) -> Iterable[Record]:
        """
        Yield all (key, value) pairs for a given partition_id
        from all mappers.
        """
        if not (0 <= partition_id < self._num_partitions):
            raise IndexError("Invalid partition_id")

        for mapper_buckets in self._matrix:
            # mapper_buckets[partition_id] is a list of (key, value)
            for record in mapper_buckets[partition_id]:
                yield record