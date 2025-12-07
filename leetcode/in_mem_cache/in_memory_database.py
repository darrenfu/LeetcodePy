"""Simple in-memory database supporting CRUD, filtering, and per-row TTL.

The design mirrors the caching examples in this package but adds a minimal
relational feel with tables, rows, and predicates for filtering.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, List, Optional


@dataclass
class Row:
    data: Dict[str, Any]
    created_at: float = field(default_factory=time.time)
    ttl: Optional[float] = None

    def is_expired(self, now: Optional[float] = None) -> bool:
        if self.ttl is None:
            return False
        now = now or time.time()
        return now - self.created_at >= self.ttl


class Table:
    def __init__(self, name: str):
        self.name = name
        self.rows: Dict[int, Row] = {}
        self._next_id = 1

    @staticmethod
    def _materialize(row_id: int, row: Row) -> Dict[str, Any]:
        """Return a dict including the synthetic id alongside row data."""
        return {"id": row_id, **row.data}

    def insert(self, data: Dict[str, Any], ttl: Optional[float] = None) -> int:
        row_id = self._next_id
        self.rows[row_id] = Row(data=data, ttl=ttl)
        self._next_id += 1
        return row_id

    def get(self, row_id: int) -> Optional[Dict[str, Any]]:
        self._purge_expired()
        row = self.rows.get(row_id)
        if not row:
            return None
        return self._materialize(row_id, row)

    def update(self, row_id: int, data: Dict[str, Any], ttl: Optional[float] = None) -> bool:
        self._purge_expired()
        if row_id not in self.rows:
            return False
        self.rows[row_id] = Row(data=data, ttl=ttl)
        return True

    def delete(self, row_id: int) -> bool:
        self._purge_expired()
        if row_id in self.rows:
            del self.rows[row_id]
            return True
        return False

    def scan(self) -> List[Dict[str, Any]]:
        self._purge_expired()
        return [
            self._materialize(row_id, row)
            for row_id, row in sorted(self.rows.items())
        ]

    def where(self, predicate: Callable[[Dict[str, Any]], bool]) -> List[Dict[str, Any]]:
        """Return rows matching the predicate after purging expired entries."""
        self._purge_expired()
        results: List[Dict[str, Any]] = []
        for row_id, row in self.rows.items():
            row_dict = self._materialize(row_id, row)
            if predicate(row_dict):
                results.append(row_dict)
        return results

    def _purge_expired(self) -> None:
        now = time.time()
        expired_keys = [row_id for row_id, row in self.rows.items() if row.is_expired(now)]
        for row_id in expired_keys:
            del self.rows[row_id]


class InMemoryDatabase:
    """A minimal in-memory database with tables, CRUD, filtering, and row TTL."""

    def __init__(self):
        self.tables: Dict[str, Table] = {}

    def create_table(self, name: str) -> None:
        if name in self.tables:
            raise ValueError(f"Table {name} already exists")
        self.tables[name] = Table(name)

    def drop_table(self, name: str) -> None:
        self.tables.pop(name, None)

    def insert(self, table: str, data: Dict[str, Any], ttl: Optional[float] = None) -> int:
        tbl = self._get_table(table)
        return tbl.insert(data=data, ttl=ttl)

    def get(self, table: str, row_id: int) -> Optional[Dict[str, Any]]:
        tbl = self._get_table(table)
        return tbl.get(row_id)

    def update(self, table: str, row_id: int, data: Dict[str, Any], ttl: Optional[float] = None) -> bool:
        tbl = self._get_table(table)
        return tbl.update(row_id, data=data, ttl=ttl)

    def delete(self, table: str, row_id: int) -> bool:
        tbl = self._get_table(table)
        return tbl.delete(row_id)

    def scan(self, table: str) -> List[Dict[str, Any]]:
        tbl = self._get_table(table)
        return tbl.scan()

    def where(self, table: str, predicate: Callable[[Dict[str, Any]], bool]) -> List[Dict[str, Any]]:
        tbl = self._get_table(table)
        return tbl.where(predicate)

    def _get_table(self, name: str) -> Table:
        if name not in self.tables:
            raise KeyError(f"Table {name} not found")
        return self.tables[name]


if __name__ == "__main__":
    db = InMemoryDatabase()
    db.create_table("users")
    alice_id = db.insert("users", {"name": "Alice", "age": 30}, ttl=1.5)
    bob_id = db.insert("users", {"name": "Bob", "age": 25})

    print("Initial scan:", db.scan("users"))
    print("Bob via get:", db.get("users", bob_id))

    time.sleep(2)
    print("After TTL:", db.scan("users"))
    print("Filter age>20:", db.where("users", lambda row: row["age"] > 20))
    db.update("users", bob_id, {"name": "Bobby", "age": 26})
    print("After update:", db.get("users", bob_id))
    db.delete("users", bob_id)
    print("After delete:", db.scan("users"))
