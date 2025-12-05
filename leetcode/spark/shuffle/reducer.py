from collections import defaultdict
from typing import Callable, Iterable, List, Dict

from spark.shuffle.common import Key, Value
from spark.shuffle.shuffle_manager import ShuffleManager


class Reducer:
    """
    Consumes data for one partition:
    - groups by key
    - aggregates values with reduce_fn(key, values)
    """

    def __init__(
            self,
            partition_id: int,
            shuffle_manager: ShuffleManager,
            reduce_fn: Callable[[Key, Iterable[Value]], Value],
    ) -> None:
        self._partition_id = partition_id
        self._shuffle_manager = shuffle_manager
        self._reduce_fn = reduce_fn

    def run(self) -> Dict[Key, Value]:
        grouped: Dict[Key, List[Value]] = defaultdict(list)

        # 1. Shuffle read:
        # Read all data for this partition from all mappers
        for key, value in self._shuffle_manager.get_partition_data(self._partition_id):
            # 2. group by key
            grouped[key].append(value)

        # Aggregate per key
        result: Dict[Key, Value] = {}
        for key, values in grouped.items():
            # 3. reduce
            result[key] = self._reduce_fn(key, values)

        return result