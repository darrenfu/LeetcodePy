"""GPU credit system implementation.

This file turns the problem description into a runnable, well-documented
implementation. The goal is to process grants, spends, and queries **in logical
time order**, honoring the following constraints described in the original
problem statement:

* Credits can be granted with an expiry time. Expired credits cannot be used.
* Spends can exceed the current balance, creating a debt that future grants
  must first repay.
* Multiple operations may share the same timestamp. In that case, **spends are
  processed before grants**, and queries observe the post-grant state at that
  timestamp.
* Requests may arrive in any order but must be applied strictly in timestamp
  order.

The implementation below provides a reusable ``GPUCreditSystem`` class plus a
simple ``main`` demonstration. It intentionally uses clear data structures and
commentary so that the processing rules are easy to follow.
"""

from __future__ import annotations

import dataclasses
import enum
import heapq
from collections import defaultdict
from typing import DefaultDict, Iterable, List, Optional, Tuple


class EventType(enum.IntEnum):
    """Logical ordering for events that share a timestamp.

    Lower values run earlier when sorting. Spend must run before grant, and
    query observes the state after both spend and grant, so their sort order is:
    ``SPEND < GRANT < QUERY``.
    """

    SPEND = 0
    GRANT = 1
    QUERY = 2


@dataclasses.dataclass(order=True)
class Event:
    """Represents a single operation in the system."""

    sort_index: Tuple[int, EventType] = dataclasses.field(init=False, repr=False)
    timestamp: int
    kind: EventType
    user: str
    amount: int = 0
    expiry: Optional[int] = None

    def __post_init__(self) -> None:
        # sort_index makes ``sorted(events)`` honor the required time ordering.
        self.sort_index = (self.timestamp, self.kind)


@dataclasses.dataclass
class UserState:
    """Tracks a user's current credit lots and debt."""

    debt: int = 0
    # Min-heap of (expiry, amount_remaining)
    active_credits: List[Tuple[int, int]] = dataclasses.field(default_factory=list)

    def expire_credits(self, now: int) -> None:
        """Drop any credit lots that are expired at the current timestamp."""

        while self.active_credits and self.active_credits[0][0] <= now:
            heapq.heappop(self.active_credits)

    def total_active(self) -> int:
        """Compute the total unexpired credit remaining."""

        return sum(amount for _, amount in self.active_credits)


class GPUCreditSystem:
    """Core GPU credit logic with timestamp-aware processing."""

    def __init__(self) -> None:
        self.users: DefaultDict[str, UserState] = defaultdict(UserState)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def process_events(self, events: Iterable[Event]) -> List[int]:
        """Process a batch of events in logical order.

        Args:
            events: Iterable of ``Event`` objects. Arrival order does not
                matter—the method sorts them by timestamp and event type.

        Returns:
            A list of query results in the order the queries were processed.
        """

        sorted_events = sorted(events)
        query_results: List[int] = []

        for event in sorted_events:
            state = self.users[event.user]
            state.expire_credits(event.timestamp)

            if event.kind is EventType.SPEND:
                self._apply_spend(state, event.amount)
            elif event.kind is EventType.GRANT:
                self._apply_grant(state, event.amount, event.expiry, event.timestamp)
            else:  # EventType.QUERY
                query_results.append(self._apply_query(state))

        return query_results

    def grant(self, user: str, amount: int, expiry: int, timestamp: int) -> None:
        """Convenience wrapper for granting a single credit lot."""

        self.process_events([
            Event(timestamp=timestamp, kind=EventType.GRANT, user=user, amount=amount, expiry=expiry)
        ])

    def spend(self, user: str, amount: int, timestamp: int) -> None:
        """Convenience wrapper for spending credits."""

        self.process_events([
            Event(timestamp=timestamp, kind=EventType.SPEND, user=user, amount=amount)
        ])

    def query(self, user: str, timestamp: int) -> int:
        """Convenience wrapper for querying the balance at a time."""

        results = self.process_events([
            Event(timestamp=timestamp, kind=EventType.QUERY, user=user)
        ])
        return results[0]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _apply_spend(self, state: UserState, amount: int) -> None:
        """Consume credits, increasing debt if necessary."""

        remaining = amount

        # Spend from the earliest-expiring lots first (heap is ordered by expiry).
        while remaining > 0 and state.active_credits:
            expiry, lot_amount = heapq.heappop(state.active_credits)
            if lot_amount > remaining:
                # Partially consume this lot and push the remainder back.
                lot_amount -= remaining
                heapq.heappush(state.active_credits, (expiry, lot_amount))
                remaining = 0
            else:
                # Consume the entire lot.
                remaining -= lot_amount

        if remaining > 0:
            # Not enough credits—record the deficit as debt.
            state.debt += remaining

    def _apply_grant(self, state: UserState, amount: int, expiry: Optional[int], now: int) -> None:
        """Add credits, repaying debt before increasing usable balance."""

        if expiry is None or expiry <= now:
            # Grant is already expired; ignore.
            return

        # First, repay any outstanding debt.
        debt_payment = min(state.debt, amount)
        state.debt -= debt_payment
        remaining = amount - debt_payment

        if remaining > 0:
            heapq.heappush(state.active_credits, (expiry, remaining))

    def _apply_query(self, state: UserState) -> int:
        """Return the current balance (active credits minus debt)."""

        return state.total_active() - state.debt


def example_usage() -> None:
    """Small demonstration showing the processing order rules."""

    system = GPUCreditSystem()
    events = [
        Event(timestamp=1, kind=EventType.SPEND, user="alice", amount=50),
        Event(timestamp=1, kind=EventType.GRANT, user="alice", amount=100, expiry=5),
        Event(timestamp=2, kind=EventType.QUERY, user="alice"),
        Event(timestamp=3, kind=EventType.SPEND, user="alice", amount=60),
        Event(timestamp=4, kind=EventType.QUERY, user="alice"),
        Event(timestamp=5, kind=EventType.QUERY, user="alice"),
    ]

    print("Query results:", system.process_events(events))


if __name__ == "__main__":
    example_usage()
