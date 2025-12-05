from typing import Iterable

from spark.shuffle.common import Record
from spark.shuffle.driver import mini_shuffle_hash_join


def demo_shuffle_hash_join() -> None:
    # Example: join users with events on user_id

    left_shards = [
        [("u1", "Alice"), ("u2", "Bob")],
        [("u3", "Carol")],
    ]

    right_shards = [
        [("u1", "click"), ("u1", "purchase")],
        [("u2", "view"), ("u4", "click")],
    ]

    def left_map_fn(raw) -> Iterable[Record]:
        user_id, user_name = raw
        yield user_id, user_name

    def right_map_fn(raw) -> Iterable[Record]:
        user_id, event = raw
        yield user_id, event

    joined = mini_shuffle_hash_join(
        left_shards=left_shards,
        left_map_fn=left_map_fn,
        right_shards=right_shards,
        right_map_fn=right_map_fn,
        num_partitions=4,
    )

    print(joined)
    # Example:
    # [
    #   ('u1', 'Alice', 'click'),
    #   ('u1', 'Alice', 'purchase'),
    #   ('u2', 'Bob', 'view')
    # ]

if __name__ == "__main__":
    demo_shuffle_hash_join()