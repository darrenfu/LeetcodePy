import heapq
from typing import Any


class ListNode:
    def __init__(self, val: int, next: "Optional[ListNode]" = None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode({self.val})"

def extract_key(value: ListNode) -> int:
    return value.val


def merge_k_streams(streams):
    """
    streams: list of iterators, each yielding sorted items.
    Yields a globally sorted sequence.
    """
    heap = []  # entries: (key, stream_id, value)

    # Initialize: read first element from each stream
    for i, it in enumerate(streams):
        try:
            val = next(it)
            key = extract_key(val)  # maybe val itself, or val.timestamp
            heapq.heappush(heap, (key, i, val))
        except StopIteration:
            # this stream is empty; skip
            pass

    while heap:
        key, i, val = heapq.heappop(heap)
        # Yield the smallest element
        yield val

        # Advance that stream
        it = streams[i]
        try:
            next_val = next(it)
            next_key = extract_key(next_val)
            heapq.heappush(heap, (next_key, i, next_val))
        except StopIteration:
            # stream i exhausted; nothing to push
            pass