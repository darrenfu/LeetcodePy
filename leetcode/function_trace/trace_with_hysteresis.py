from typing import List

from function_trace.trace import Sample, Event, FrameState

# We are given a stream of sampled call stacks over time, and we want to
# reconstruct the logical start/end events of each function.
# The key idea is that from one sample to the next, only the suffix of the
# call stack may change — the ancestral prefix must remain valid
# if the stack is consistent.

# Step 1: Compute the Longest Common Prefix (LCP)
# For each pair of consecutive samples, I compare the previous logical stack and
# the new raw stack from the top (the root function) down.
# The longest prefix where names still match represents the portion of the
# call stack that is guaranteed to still be active.
# I reset any missing counters on those frames.
# Step 2: Detect structural changes at depth i
# If at depth i the names differ — for example the previous stack has A but the new sample shows B —
# that cannot be a sampling glitch, because sampling errors can truncate the stack but they don’t mutate a function name.
# I immediately end every frame from index i to the top, and then start the new frames from the raw stack starting at i.
# No hysteresis applies in this branch.
# Step 3: Handle prefix truncation (possible sampling noise)
# If the new raw stack is a strict prefix of the logical stack — meaning all names match but the raw stack is shorter —
# this could be a sampling artifact. Samplers sometimes drop the deepest frames.
# So for the truncated suffix, I increment a missing_count for each frame.
# Only when a frame has been missing for N consecutive samples do I emit an actual end event and pop it from the logical stack.
# This is the hysteresis mechanism that filters out one-off sampling noise.
# Step 4: Handle stack growth
# If the new stack is longer than the logical one and all names matched up to the old length,
# then the program simply called into new deeper functions.
# I emit start events for the additional frames and append them to the logical stack.

def convert_with_hysteresis(samples: List[Sample], N: int = 5) -> List[Event]:
    events: List[Event] = []
    logical_stack: List[FrameState] = []

    for sample in samples:
        ts = sample.ts
        raw = sample.stack
        longest_common_size = min(len(logical_stack), len(raw))
        i = 0
        while i < longest_common_size and logical_stack[i].name == raw[i]:
            logical_stack[i].missing_count = 0
            i += 1

        if i < len(logical_stack) and i < len(raw):
            # Case 1: At depth i, found name difference
            # E.g. ["main","A"] → ["main","B"]

            # Generate end events from callstack top
            for j in range(len(logical_stack)-1, i-1, -1):
                frame = logical_stack.pop()
                events.append(Event("end", ts, frame.name))

            # Generate start events from callstack bottom
            for j in range(i, len(raw)):
                events.append(Event("start", ts, raw[j]))
                logical_stack.append(FrameState(name=raw[j], missing_count=0))
        else:
            # Case 2: no name inconsistency between uncommon prefixes
            if len(raw) < len(logical_stack):
                # raw has the common prefix of logical.
                # can be a noisy sample, apply N denoise algo
                for j in range(len(raw), len(logical_stack)):
                    logical_stack[j].missing_count += 1

                # Pop end events whose missing_count >= N
                while logical_stack and logical_stack[-1].missing_count >= N:
                    frame = logical_stack.pop()
                    events.append(Event("end", ts, frame.name))

            elif len(raw) > len(logical_stack):
                # Found new names in the new stack, fire start events
                for j in range(len(logical_stack), len(raw)):
                    events.append(Event("start", ts, raw[j]))
                    logical_stack.append(FrameState(name=raw[j], missing_count=0))
            else:
                # Exactly the same
                pass

    return events


