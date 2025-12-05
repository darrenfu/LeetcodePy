from collections import defaultdict
from typing import List, Iterable, Callable, Any, Dict

from spark.shuffle.common import Key, Value, Record, JoinedRecord, \
    ShuffleMatrix, Partitioner
from spark.shuffle.mapper import Mapper
from spark.shuffle.shuffle_manager import ShuffleManager
from spark.shuffle.reducer import Reducer


def shuffle_side(
        shards: List[Iterable[Any]],
        map_fn: Callable[[Any], Iterable[Record]],
        num_partitions: int,
        combine_fn: Callable[[Key, Iterable[Value]], Value] | None = None,
) -> ShuffleManager:
    partitioner = Partitioner(num_partitions)

    shuffle_matrix: ShuffleMatrix = []
    for shard in shards:
        # NOTE: join does NOT use combiner
        # because join semantics are row-level, not aggregated
        mapper = Mapper(shard, map_fn, partitioner, combine_fn=combine_fn)
        shuffle_matrix.append(mapper.run())
    return ShuffleManager(shuffle_matrix, num_partitions)

def mini_shuffle_reduce_by_key(
        shards: List[Iterable[Any]],
        map_fn: Callable[[Any], Iterable[Record]],
        combine_fn: Callable[[Key, Iterable[Value]], Value],
        reduce_fn: Callable[[Key, Iterable[Value]], Value],
        num_partitions: int,
) -> Dict[Key, Value]:
    """
    Simulate a Spark-like shuffle for reduceByKey.

    shards: list of input shards (one per mapper)
    map_fn: raw -> iterable of (key, value)
    reduce_fn: aggregates all values for a key
    num_partitions: number of logical reducers (shuffle partitions)
    """
    # 1) Map phase: run mappers with combiner and build the shuffle matrix
    shuffle_manager = shuffle_side(shards, map_fn, num_partitions, combine_fn)

    # 2) Reduce phase: run a reducer per partition
    final_result: Dict[Key, Value] = {}
    for pid in range(num_partitions):
        reducer = Reducer(pid, shuffle_manager, reduce_fn)
        partition_result = reducer.run()
        # Merge per-partition maps
        final_result.update(partition_result)

    return final_result

def hash_join_partition(
        partition_id: int,
        left_shuffle: ShuffleManager,
        right_shuffle: ShuffleManager,
) -> List[JoinedRecord]:
    """
    Inner join for a single partition:
    - build hash map from left side
    - probe with right side
    """
    # 1) Build hash table from left side: key -> [left_values...]
    left_map: Dict[Key, List[Value]] = defaultdict(list)
    for key, value in left_shuffle.get_partition_data(partition_id):
        left_map[key].append(value)

    # 2) Probe using right side
    results: List[JoinedRecord] = []
    for key, right_value in right_shuffle.get_partition_data(partition_id):
        if key in left_map:
            # inner equi-join semantics
            # Input:
            # Left:  K: [L1, L2]
            # Right: K: [R1]
            # Output:
            # (K, L1, R1)
            # (K, L2, R1)
            for left_value in left_map[key]:
                results.append((key, left_value, right_value))

    return results


def mini_shuffle_hash_join(
        left_shards: List[Iterable[Any]],
        left_map_fn: Callable[[Any], Iterable[Record]],
        right_shards: List[Iterable[Any]],
        right_map_fn: Callable[[Any], Iterable[Record]],
        num_partitions: int,
) -> List[JoinedRecord]:
    """
    Mini hash-based inner join:
    - Shuffle left and right sides into the same partition space
    - For each partition, do a local hash join
    """
    # 1) Shuffle both sides
    left_shuffle = shuffle_side(left_shards, left_map_fn, num_partitions)
    right_shuffle = shuffle_side(right_shards, right_map_fn, num_partitions)

    # 2) Join per partition
    joined: List[JoinedRecord] = []
    for pid in range(num_partitions):
        partition_result = hash_join_partition(pid, left_shuffle, right_shuffle)
        joined.extend(partition_result)

    return joined
