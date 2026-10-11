"""Single-file durable event writer for interview study (Linux/POSIX).

One instance must exclusively own the file. Successful push() means its framed
record is covered by a successful fsync(), assuming storage honors that call.
"""

import os
import struct
import threading
import zlib
from collections import deque


# Frame: [4-byte payload length][payload bytes][4-byte CRC32].
# >I is an unsigned 32-bit integer in big-endian byte order.
U32 = struct.Struct(">I")
MAX_PAYLOAD = 1024


def encode_record(data):
    # Explicit framing preserves boundaries between arbitrary byte payloads.
    header = U32.pack(len(data))
    # Protect both the encoded length and payload. CRC32 detects accidental
    # corruption probabilistically; it is not a cryptographic guarantee.
    checksum = zlib.crc32(header + data)
    return header + data + U32.pack(checksum)


def write_all(fd, data):
    # OS writes can be short. Advance through the buffer until all bytes have
    # been accepted. A memoryview avoids copying every remaining suffix.
    remaining = memoryview(data)
    while remaining:
        written = os.write(fd, remaining)
        if written == 0:
            raise OSError("Write made no progress")
        remaining = remaining[written:]
    # Accepted by the OS does not yet mean persistent: fsync is still needed.


def recover(fd):
    """Keep valid records and remove an incomplete final frame."""
    size = os.fstat(fd).st_size
    offset = 0  # End of the last fully validated record.

    while offset < size:
        # pread reads at an explicit offset without changing the file cursor.
        header = os.pread(fd, 4, offset)
        if len(header) < 4:
            break  # Incomplete final length field.

        length = U32.unpack(header)[0]
        if length > MAX_PAYLOAD:
            # Do not guess record boundaries after an invalid length.
            raise OSError(f"Invalid record length at offset {offset}")

        frame_size = 4 + length + 4
        body = os.pread(fd, length + 4, offset + 4)
        if len(body) < length + 4:
            break  # Incomplete final payload/checksum.

        payload = body[:length]
        expected = U32.unpack(body[length:])[0]
        actual = zlib.crc32(header + payload)
        if actual != expected:
            # Conservatively report complete-frame corruption. Even at the
            # tail, silently deleting it could discard an acknowledged record.
            raise OSError(f"Checksum mismatch at offset {offset}")

        offset += frame_size

    if offset != size:
        # Remove the incomplete suffix before allowing any new appends.
        os.ftruncate(fd, offset)
    os.fsync(fd)  # Persist recovery changes before accepting records.


class DataWriter:
    def __init__(
        self,
        path,
        max_pending_bytes=4 * 1024 * 1024,
        max_batch_bytes=256 * 1024,
    ):
        # Each limit must accommodate one maximum-size frame (payload + 8).
        if max_pending_bytes < MAX_PAYLOAD + 8:
            raise ValueError("Queue must hold at least one maximum-size record")
        if max_batch_bytes < MAX_PAYLOAD + 8:
            raise ValueError("Batch must hold at least one maximum-size record")

        # Condition includes a mutex. All shared state is protected by it.
        # wait releases the mutex while sleeping and reacquires before return.
        self._condition = threading.Condition()
        self._queue = deque()
        self._next_seq = 0
        self._durable_seq = 0  # All records through this sequence are durable.
        self._pending_bytes = 0  # Queued frames PLUS the active unsynced batch.
        self._max_pending_bytes = max_pending_bytes
        self._max_batch_bytes = max_batch_bytes
        self._closing = False
        self._failure = None  # Permanent failure for this instance.

        # Recovery needs reads; O_APPEND places each write at the file end.
        # This does not provide cross-process coordination or ownership.
        self._fd = os.open(path, os.O_CREAT | os.O_RDWR | os.O_APPEND, 0o600)
        try:
            recover(self._fd)

            # A new filename also needs its directory entry persisted.
            parent = os.path.dirname(os.path.abspath(path))
            directory_fd = os.open(parent, os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        except BaseException:
            os.close(self._fd)
            raise

        # One worker owns disk writes. It is non-daemon: close explicitly.
        self._worker = threading.Thread(target=self._run, name="data-writer")
        try:
            self._worker.start()
        except BaseException:
            os.close(self._fd)
            raise

    def push(self, data: bytes) -> None:
        # Immutable bytes avoid payload mutation while a record is queued.
        if not isinstance(data, bytes):
            raise TypeError("data must be bytes")
        if len(data) > MAX_PAYLOAD:
            raise ValueError("Record exceeds 1 KB")
        frame = encode_record(data)

        with self._condition:
            # Backpressure occurs before accepting the record. The byte limit
            # bounds accepted outstanding frames, not blocked caller memory.
            while (
                self._pending_bytes + len(frame) > self._max_pending_bytes
                and self._failure is None
                and not self._closing
            ):
                self._condition.wait()

            if self._failure is not None:
                raise OSError("Writer has failed") from self._failure
            if self._closing:
                raise RuntimeError("Writer is closing or closed")

            # Atomic sequence assignment + enqueue keeps queue order aligned
            # with sequence order. Each push has its own sequence, not thread.
            self._next_seq += 1
            my_seq = self._next_seq
            self._queue.append((my_seq, frame))
            self._pending_bytes += len(frame)
            self._condition.notify_all()  # Wake the worker if idle.

            # Notifications are only prompts to recheck. Loop handles unrelated
            # notifications and spurious wakeups. Failure also ends the wait.
            while self._durable_seq < my_seq and self._failure is None:
                self._condition.wait()

            if self._durable_seq < my_seq:
                # Failure does not imply absence; retry can create duplicates.
                raise OSError(
                    "Write failed; record persistence is uncertain"
                ) from self._failure
            # Returning None is the successful durability acknowledgment.

    def _run(self):
        try:
            while True:
                with self._condition:
                    while not self._queue and not self._closing:
                        self._condition.wait()
                    if not self._queue:
                        return  # Closing, and accepted records are drained.

                    batch = []
                    batch_bytes = 0
                    group_end = 0
                    # Drain available work without deliberately waiting to fill
                    # a batch. A lone record is therefore synced promptly.
                    while self._queue:
                        seq, frame = self._queue[0]
                        if batch_bytes + len(frame) > self._max_batch_bytes:
                            break
                        self._queue.popleft()
                        batch.append(frame)
                        batch_bytes += len(frame)
                        group_end = seq

                # Disk I/O runs OUTSIDE the mutex so callers can still enqueue.
                # os.write bypasses Python buffering: no file.flush needed.
                write_all(self._fd, b"".join(batch))
                os.fsync(self._fd)  # One sync covers every frame in this group.

                with self._condition:
                    # Publish the synced group's end, not the latest enqueued
                    # sequence. Later arrivals are not covered by this sync.
                    self._durable_seq = group_end
                    self._pending_bytes -= batch_bytes
                    self._condition.notify_all()  # Durability + capacity waits.

        except Exception as error:
            with self._condition:
                self._failure = error
                # Do not advance the durable watermark for the failed group.
                self._queue.clear()
                self._pending_bytes = 0
                self._condition.notify_all()  # Ensure no waiter sleeps forever.
        finally:
            try:
                os.close(self._fd)
            except OSError as error:
                with self._condition:
                    if self._failure is None:
                        self._failure = error
                    self._condition.notify_all()

    def close(self) -> None:
        with self._condition:
            self._closing = True  # Stop admission; accepted records still drain.
            self._condition.notify_all()

        # Joining while holding the mutex would prevent the worker finishing.
        self._worker.join()
        with self._condition:
            if self._failure is not None:
                raise OSError("Writer failed") from self._failure

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
