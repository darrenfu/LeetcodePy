from dataclasses import dataclass
from typing import List

@dataclass
class Sample:
    ts: float
    stack: List[str]   # ["root", ..., "top"]


@dataclass
class Event:
    kind: str          # "start" or "end"
    ts: float
    name: str

@dataclass
class FrameState:
    name: str
    missing_count: int = 0

def convert_base(samples: List[Sample]) -> List[Event]:
    events: List[Event] = []
    logical_stack: List[FrameState] = []

    for sample in samples:
        ts = sample.ts
        raw = sample.stack
        longest_common_size = min(len(logical_stack), len(raw))
        i = 0
        while i < longest_common_size and logical_stack[i].name == raw[i]:
            i += 1

        # Generate end events from callstack top
        for j in range(len(logical_stack)-1, i-1, -1):
            frame = logical_stack.pop()
            events.append(Event("end", ts, frame.name))

        # Generate start events from callstack bottom
        for j in range(i, len(raw)):
            events.append(Event("start", ts, raw[j]))
            logical_stack.append(FrameState(name=raw[j]))

    return events
