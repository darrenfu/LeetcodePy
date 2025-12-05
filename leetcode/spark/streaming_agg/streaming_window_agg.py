from heapq import heappush, heappop
from typing import Dict, List, Tuple


class StreamingWindowAggregator:
    """
    Streaming window aggregator with watermark and optional sliding windows.

    - Events: (key, ts, value)
    - Windows: time-based, aligned at multiples of `slide` starting from 0.
      Window = [window_start, window_start + window_size)
    - If slide == window_size → tumbling windows.
    - Aggregation: sum of `value` for each (key, window).

    API:
      process_event(key, ts, value)          # ingest one event
      advance_watermark(watermark_ts) -> []  # emit finalized windows
    """

    def __init__(self, window_size: int, slide: int = None, allowed_lateness: int = 0):
        self.window_size = window_size
        self.slide = slide or window_size  # default (tumbling window): slide == window_size
        self.allowed_lateness = allowed_lateness

        # Track max event time to do a simple allowed-lateness filter
        self.max_event_time = float("-inf")

        # Per-key, per-window_start aggregate state:
        # state[key][window_start] = aggregate_value
        self.state: Dict[str, Dict[int, float]] = {}

        # Global min-heap of (window_end, key, window_start)
        # Used to efficiently find windows that have ended before watermark
        self.heap: List[Tuple[int, str, int]] = []

    # ---------- window indexing ----------

    def _iter_windows_for_event(self, ts: int):
        """
        Yield all window_start values of windows that contain timestamp `ts`.

        We assume windows start at multiples of `slide`, and each window covers
        [start, start + window_size).

        For sliding windows, a single event may belong to multiple windows.
        For tumbling windows, slide == window_size, so there is exactly one.
        """
        size = self.window_size
        slide = self.slide

        # Find the last window_start s.t. s <= ts
        last_start = (ts // slide) * slide

        start = last_start
        # Move left while `ts` is still inside [start, start+size)
        while start + size > ts and start >= 0:
            yield start
            start -= slide

    # ---------- ingestion ----------

    def process_event(self, key: str, ts: int, value: float) -> None:
        """
        Ingest one event into the aggregator.

        Late data handling:
        - If ts < max_event_time - allowed_lateness, we treat it as "too late"
          and ignore it. (Alternative policy: route to a "late events" side output.)
        """
        # Filter out events that are too late beyond allowed_lateness
        if ts < self.max_event_time - self.allowed_lateness:
            # Too-late event; choose to drop it
            return

        # Update max_event_time
        if ts > self.max_event_time:
            self.max_event_time = ts

        # Initialize per-key state if needed
        if key not in self.state:
            self.state[key] = {}
        window_map = self.state[key]

        # For each window the event belongs to, update the aggregate
        for ws in self._iter_windows_for_event(ts):
            if ws < 0:
                continue
            if ws not in window_map:
                # First time we see this window → initialize and put in heap
                window_map[ws] = 0.0
                we = ws + self.window_size
                heappush(self.heap, (we, key, ws))
            # Simple aggregation: sum of values
            window_map[ws] += value

    # ---------- watermark advancing & emission ----------

    def advance_watermark(self, watermark_ts: int):
        """
        Advance the watermark and emit finalized windows.

        A window is finalized when `window_end <= watermark_ts`.
        Once finalized, its state is removed.

        Returns:
            List of (key, window_start, window_end, aggregate_value).
        """
        results = []

        # Pop from heap while the earliest window_end is before watermark
        while self.heap and self.heap[0][0] <= watermark_ts:
            window_end, key, window_start = heappop(self.heap)

            # Guard: this window may already have been emitted/cleaned
            per_key = self.state.get(key)
            if per_key is None:
                continue
            if window_start not in per_key:
                continue

            agg_value = per_key.pop(window_start)

            # Cleanup empty per-key map
            if not per_key:
                self.state.pop(key, None)

            results.append((key, window_start, window_end, agg_value))

        return results

def demo_tumbling_window(window_size: int) -> None:
    print("Tumbling window")
    agg = StreamingWindowAggregator(window_size=window_size)
    events = [
        ("a", 1,  1),
        ("a", 5,  1),
        ("a", 12, 1),
        ("a", 19, 1),
    ]

    for e in events:
        agg.process_event(*e)

    print("emit at wm=10:", agg.advance_watermark(10))
    # → [('a', 0, 10, 2)]  # [0,10) 窗口内两条

    print("emit at wm=20:", agg.advance_watermark(20))
    # → [('a', 10, 20, 2)] # [10,20) 窗口内两条

def demo_sliding_window(window_size: int, slide: int) -> None:
    print("Sliding window")
    agg = StreamingWindowAggregator(window_size=window_size, slide=slide)

    for ts in [1, 5, 7, 11, 13]:
        agg.process_event("a", ts, 1)

    print("emit at wm=10:", agg.advance_watermark(10))
    # [0,10): ts=1,5,7 → sum=3
    # → [('a', 0, 10, 3)]

    print("emit at wm=20:", agg.advance_watermark(20))
    # [5,15): ts=5,7,11,13 → 4
    # [10,20): ts=11,13 → 2
    # → [('a', 5, 15, 4), ('a', 10, 20, 2)]

if __name__ == "__main__":
    demo_tumbling_window(10)
    demo_sliding_window(10, 5)