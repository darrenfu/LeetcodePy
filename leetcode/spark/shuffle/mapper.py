from collections import defaultdict
from typing import Dict, Iterable, Callable, Any
from spark.shuffle.common import Partitioner, Key, Value, Record, MapperBuckets, CombinerBuckets, Bucket

class Mapper:
    """
    Simulates a single map task:
    - consumes a shard of raw input records
    - applies map_fn to produce (key, value) pairs
    - optionally applies a map-side combiner per partition
    - partitions them into num_partitions buckets
    """

    def __init__(
            self,
            shard: Iterable[Any],
            map_fn: Callable[[Any], Iterable[Record]],
            partitioner: Partitioner,
            combine_fn: Callable[[Key, Iterable[Value]], Value] | None = None,
    ) -> None:
        self._shard = shard
        self._map_fn = map_fn
        self._partitioner = partitioner
        self._combine_fn = combine_fn

    def run(self) -> MapperBuckets:
        num_partitions = self._partitioner.num_partitions

        if self._combine_fn is None:
            # Simple case: no map-side combine, just append
            buckets: MapperBuckets = {p: [] for p in range(num_partitions)}
            for raw in self._shard:
                for key, value in self._map_fn(raw):
                    # Shuffle write
                    # Decide which reducer should receive this key
                    pid = self._partitioner.get_partition(key)
                    # materialization
                    buckets[pid].append((key, value))
            return buckets

        # With combiner: aggregate per key inside each partition
        tmp: CombinerBuckets = {
            p: defaultdict(list) for p in range(num_partitions)
        }

        for raw in self._shard:
            for key, value in self._map_fn(raw):
                pid = self._partitioner.get_partition(key)
                tmp[pid][key].append(value)

        # Apply combiner per key per partition
        buckets: MapperBuckets = {p: [] for p in range(num_partitions)}
        for pid, key_to_values in tmp.items():
            for key, values in key_to_values.items():
                combined = self._combine_fn(key, values)
                buckets[pid].append((key, combined))

        return buckets

class MapperWithSpill(Mapper):
    def __init__(
            self,
            shard: Iterable[Any],
            map_fn: Callable[[Any], Iterable[Record]],
            partitioner: Partitioner,
            combine_fn: Callable[[Key, Iterable[Value]], Value] | None = None,
            spill_to_disk: bool = False,
    ) -> None:
        super().__init__(shard, map_fn, partitioner, combine_fn)
        self._spill_to_disk = spill_to_disk

    def run(self) -> Dict[int, Bucket]:
        num_partitions = self._partitioner.num_partitions
        buckets: Dict[int, Bucket] = {
            p: Bucket(spill_to_disk=self._spill_to_disk) for p in range(num_partitions)
        }

        # For brevity, only the non-combiner path is shown; combiner version is analogous:
        for raw in self._shard:
            for key, value in self._map_fn(raw):
                pid = self._partitioner.get_partition(key)
                buckets[pid].add((key, value))

        return buckets