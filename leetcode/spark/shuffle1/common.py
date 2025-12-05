from collections import defaultdict
from typing import Any, Tuple, Callable, Dict, List, Iterable

Key = Any
Value = Any
# Like UnsafeRow
Record = Tuple[Key, Value]
# Like shuffle spill files
# partition_id -> list of (key, value)
MapperBuckets = Dict[int, List[Record]]
# map-side combine (combineByKey, pre-reduce).
# partition_id -> key -> [values...]
CombinerBuckets = Dict[int, Dict[Key, List[Value]]]

class Partitioner:
    def __init__(self, num_partitions: int):
        self.num_partitions = num_partitions

    def get_partition_id(self, key: Key) -> int:
        return hash(key) % self.num_partitions

class Mapper:
    def __init__(self,
                 shard: Iterable[Any],
                 map_fn: Callable[[Any], Iterable[Record]],
                 partitioner: Partitioner,
                 combine_fn: Callable[[Key, Iterable[Value]], Value] | None = None):
        self._shard = shard
        self._map_fn = map_fn
        self._partitioner = partitioner
        self._combine_fn = combine_fn

    def run(self) -> MapperBuckets:
        num_parts: int = self._partitioner.num_partitions
        if self._combine_fn is None:
            buckets: MapperBuckets = {p: [] for p in range(num_parts)}
            for raw in self._shard:
                for k, v in self._map_fn(raw):
                    pid = self._partitioner.get_partition_id(k)
                    buckets[pid].append((k, v))
            return buckets

        combinerBuckets: CombinerBuckets = {p: defaultdict(list) for p in range(num_parts)}
        for raw in self._shard:
            for k, v in self._map_fn(raw):
                pid = self._partitioner.get_partition_id(k)
                combinerBuckets[pid][k].append(v)

        buckets: MapperBuckets = {p: [] for p in range(num_parts)}
        for pid, key_to_values in combinerBuckets.items():
            for k, values in key_to_values.items():
                partialAggValue = self._combine_fn(k, values)
                buckets[pid].append((k, partialAggValue))
        return buckets

class ShuffleManager:
    def __init__(self, shuffle_matrix: List[MapperBuckets], num_partitions: int):
        # MapperBuckets = one mapper’s output, partitioned by partition_id.
        # One mapper = one ShuffleMapTask.
        # shuffle_matrix = a list (per mapper) of partition→records buckets.
        self.shuffle_matrix = shuffle_matrix
        self._num_partitions = num_partitions

    @property
    def num_partitions(self) -> int:
        return self._num_partitions

    def get_partition_data(self, partition_id: int) -> Iterable[Record]:
        for buckets in self.shuffle_matrix:
            for pid, records in buckets.items():
                if partition_id == pid:
                    for record in buckets[pid]:
                        yield record

class Reducer:
    def __init__(self, partition_id: int, shuffle_manager: ShuffleManager, reduce_fn: Callable[[Key, Iterable[Value]], Value]):
        self.partition_id = partition_id
        self.shuffle_manager = shuffle_manager
        self.reduce_fn = reduce_fn

    def run(self) -> Dict[Key, Value]:
        grouped: Dict[Key, List[Value]] = defaultdict(list)
        for k, v in self.shuffle_manager.get_partition_data(self.partition_id):
            grouped[k].append(v)

        res: Dict[Key, Value] = {}
        for k, values in grouped.items():
            res[k] = self.reduce_fn(k, values)
        return res

class Driver:
    def shuffle(self,
                shards: List[Iterable[Any]],
                map_fn: Callable[[Any], Iterable[Record]],
                num_partitions: int,
                combine_fn: Callable[[Key, Iterable[Value]], Value] | None = None,
                ) -> ShuffleManager:
        partitioner = Partitioner(num_partitions)
        shuffle_matrix: List[MapperBuckets] = []
        for shard in shards:
            mapper = Mapper(shard, map_fn, partitioner, combine_fn)
            mapper_buckets = mapper.run()
            shuffle_matrix.append(mapper_buckets)
        return ShuffleManager(shuffle_matrix, num_partitions)

    def reduce_by_key(self,
                      shards: List[Iterable[Any]],
                      map_fn: Callable[[Any], Iterable[Record]],
                      combine_fn: Callable[[Key, Iterable[Value]], Value],
                      reduce_fn: Callable[[Key, Iterable[Value]], Value],
                      num_partitions: int,
                      ) -> Dict[Key, Value]:
        # Stage 1 (ShuffleMapStage)
        #      map → combine → write shuffle files
        #         ↓ SHUFFLE BARRIER
        # When Driver.shuffle(...) returns a ShuffleManager, you’ve crossed the shuffle barrier.
        # All mapper outputs are “materialized” into shuffle_matrix; from now on reducers only read from it.
        shuffle_manager = self.shuffle(shards, map_fn, num_partitions, combine_fn)
        # Stage 2 (ShuffleReduceStage)
        #      shuffle-read → group-by-key → reduce
        final_agg_results: Dict[Key, Value] = {}
        for pid in range(num_partitions):
            reducer = Reducer(pid, shuffle_manager, reduce_fn)
            partitioned_agg_result = reducer.run()
            final_agg_results.update(partitioned_agg_result)
        return final_agg_results

def demo_shuffle_reduce_by_key() -> None:
    # Example: word count using the mini shuffle

    shard1 = ["hello world", "hello spark"]
    shard2 = ["spark shuffle", "hello anthropic"]

    def map_words(line: str) -> Iterable[Record]:
        for word in line.split():
            yield word, 1

    def sum_values(key: Key, values: Iterable[int]) -> int:
        return sum(values)

    result = Driver().reduce_by_key(
        shards=[shard1, shard2],
        map_fn=map_words,
        combine_fn=sum_values,
        reduce_fn=sum_values,
        num_partitions=4,
    )

    print(result)
    # Possible output (order not guaranteed):
    # {'hello': 3, 'world': 1, 'spark': 2, 'shuffle': 1, 'anthropic': 1}

if __name__ == "__main__":
    demo_shuffle_reduce_by_key()

