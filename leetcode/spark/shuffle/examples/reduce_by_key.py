from typing import Iterable

from spark.shuffle.driver import mini_shuffle_reduce_by_key
from spark.shuffle.common import Key, Record

def demo_shuffle_reduce_by_key() -> None:
    # Example: word count using the mini shuffle

    shard1 = ["hello world", "hello spark"]
    shard2 = ["spark shuffle", "hello anthropic"]

    def map_words(line: str) -> Iterable[Record]:
        for word in line.split():
            yield word, 1

    def sum_values(key: Key, values: Iterable[int]) -> int:
        return sum(values)

    result = mini_shuffle_reduce_by_key(
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

