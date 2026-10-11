# Thread-Safe Durable Event Writer — Cheat Sheet

**Problem:** Thousands of threads share one `DataWriter`. Each `push(bytes)` appends an opaque record ≤1 KB to one local file.

**Core promise:** Successful `push()` means its complete record survives a process crash or power loss, assuming storage honors `fsync()`.

**Memory hook:** **Contract → Frame → Queue → Batch → Sync → Ack → Recover**

| Checkpoint | What to say |
|---|---|
| Clarify | Durability on return? Ordering? Recovery readers? Blocking allowed? Error policy? Shutdown/rotation? Permanent disk loss is outside this local-file design. |
| Naive correct baseline | Mutex around writing one complete framed record and syncing it. Correct, but one sync per record limits throughput. |
| Record format | `[length][payload][checksum]`. Binary bytes; fixed field sizes and byte order. Checksum covers length + payload. |
| Efficient architecture | Many producers enqueue; one background writer writes and syncs groups. Protect shared state with a mutex; perform disk I/O outside it. |
| Batch triggers | Size threshold OR deadline, whichever comes first. Start deadline at the first record; don’t reset it on later arrivals. |
| Acknowledgment | Assign sequence and enqueue under the same lock. After successful sync, publish the group’s last sequence as `durable_seq`. |
| Waiting | Condition variable: wait while `my_seq > durable_seq` and no failure. `wait()` releases the mutex; notification means “recheck,” not “success.” |
| Backpressure | Bound outstanding framed bytes: queued + active batch. Block admission when full; release capacity after sync. |
| Failure | Save the error, permanently fail this instance, leave the durable watermark unchanged, wake everyone. Unconfirmed and future calls raise. |
| Recovery | Scan and validate frames. Truncate an incomplete tail and sync before appending. Report corruption conservatively. |
| Shutdown | Reject new records, drain accepted records, sync, stop worker, close. Never hold the shared mutex while joining the worker. |

## Persistence ladder

```text
Python buffer ──flush()──▶ OS cache ──fsync(fd)──▶ persistent storage
```

- `file.fileno()` gives the OS file descriptor.
- `flush()` and `close()` alone don’t establish power-loss durability.
- With `os.write()`, there is no Python buffer to flush.
- Handle short writes: loop until all bytes are written.
- For a newly created file, sync its parent directory too.

## The concurrency invariant

**`durable_seq = N` means every record through N is confirmed durable.**

```text
Caller: wait for capacity → assign seq + enqueue → wait for durability
Writer: take group → write fully → fsync → publish group_end → notify
```

Syncing 1–100 while 101 arrives → publish 100. Callers 1–100 may return; 101 waits.

## Five traps

1. Mutex ≠ durability. It prevents concurrent interference.
2. Deque removal ≠ persistence. The active batch still counts as outstanding.
3. Notification ≠ acknowledgment. Recheck the predicate in a loop.
4. Failure ≠ absence. A failed or interrupted call may have persisted; retry can duplicate it.
5. Checksum ≠ durability. It detects corruption probabilistically; `fsync()` establishes persistence.

## Closing interview answer

“I’d use a bounded producer queue and one writer performing group commit. Each caller waits on a sequence-based durable watermark. Size and time limits control batching; framing supports recovery; a permanent failure state wakes all waiters.”

**Validation:** Concurrent unique records, low-traffic deadlines, overload, short writes, write/sync failures, shutdown races, and crash recovery. Killing a process does not simulate power loss—the OS cache remains alive.
