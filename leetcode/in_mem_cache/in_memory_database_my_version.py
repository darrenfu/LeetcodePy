import json
import os
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Callable

RowType = Dict[str, Any]

@dataclass
class Row:
    data: RowType
    create_at: float = field(default_factory=time.time)
    ttl: float | None = None

    def is_expired(self, now: float | None = None) -> bool:
        if self.ttl is None:
            return False
        now = now or time.time()
        return now - self.create_at >= self.ttl

    def serialize(self) -> Dict[str, Any]:
        return {
            "data": self.data,
            "create_at": self.create_at,
            "ttl": self.ttl
        }

    @classmethod
    def deserialize(cls, obj: Dict[str, Any]) -> "Row":
        return cls(data=obj["data"], create_at=obj["create_at"], ttl=obj["ttl"])

class Table:
    def __init__(self, name: str, rows: Dict[int, Row] | None = None, next_row_id: int = 0):
        self.name = name
        self.rows = rows or {}
        self._next_row_id = next_row_id

    def _materialize(self, row_id: int, row: Row) -> RowType:
        return {"row_id": row_id, **row.serialize()}

    def insert(self, row: RowType, ttl: float | None = None) -> int:
        row_id = self._next_row_id
        self.rows[row_id] = Row(data=row, ttl=ttl)
        self._next_row_id += 1
        return row_id

    def get(self, row_id: int) -> RowType | None:
        self._purge_expired()
        row = self.rows.get(row_id)
        if not row:
            return None
        return self._materialize(row_id, row)

    def update(self, row_id: int, row: RowType, ttl: float | None = None) -> bool:
        self._purge_expired()
        if row_id not in self.rows:
            return False
        self.rows[row_id] = Row(data=row, ttl=ttl)
        return True

    def delete(self, row_id: int) -> bool:
        self._purge_expired()
        if row_id not in self.rows:
            return False
        del self.rows[row_id]
        return True

    def scan(self) -> List[RowType]:
        self._purge_expired()
        return [
            self._materialize(row_id, row)
            for row_id, row in sorted(self.rows.items())
        ]

    def where(self, predicate: Callable[[RowType], bool]) -> List[RowType]:
        self._purge_expired()
        results = []
        for row_id, row in self.rows.items():
            row_as_dict = self._materialize(row_id, row)
            if predicate(row_as_dict["data"]):
                results.append(row_as_dict)
        return results

    def _purge_expired(self) -> None:
        now = time.time()
        expired_keys = [row_id for row_id, row in self.rows.items() if row.is_expired(now)]
        for expired_key in expired_keys:
            del self.rows[expired_key]

    def serialize(self):
        self._purge_expired()
        return {
            "rows": [{"row_id": row_id, **row.serialize()} for row_id, row in self.rows.items()],
            "name": self.name,
            "next_row_id": self._next_row_id
        }

    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> "Table":
        deserialized_rows = {
            int(row["row_id"]): Row.deserialize(row)
            for row in data["rows"]
        }
        return cls(name=data["name"], rows=deserialized_rows, next_row_id=data["next_row_id"])

class InMemDb:
    def __init__(self):
        self.tables: Dict[str, Table] = {}
        self.backup_file_path = "my_db_backup.json"
        self.restore()

    def create_table(self, name: str) -> Table:
        if name in self.tables:
            print(f"Table name {name} already exists")
            return self.tables[name]
        tbl = Table(name=name)
        self.tables[name] = tbl
        return tbl

    def drop_table(self, name: str) -> None:
        if name not in self.tables:
            raise ValueError(f"Table name {name} doesn't exist")
        del self.tables[name]

    def get_table(self, name: str) -> Table | None:
        return self.tables.get(name)

    def backup(self):
        backup_data = {"tables": [tbl.serialize() for _, tbl in self.tables.items()]}
        with open(self.backup_file_path, "w") as f:
            json.dump(backup_data, f, indent=2)

    def restore(self):
        if not os.path.isfile(self.backup_file_path):
            print("Restore file not found")
            return
        with open(self.backup_file_path, "r") as f:
            backup_data = json.load(f)
            for tbl_obj in backup_data["tables"]:
                tbl = Table.deserialize(tbl_obj)
                self.tables[tbl.name] = tbl

if __name__ == "__main__":
    db = InMemDb()
    tbl = db.create_table("users")
    alice_id = tbl.insert({"name": "Alice", "age": 30}, ttl=1.5)
    bob_id = tbl.insert({"name": "Bob", "age": 25})

    print("Initial scan:", tbl.scan())
    print("Bob via get:", tbl.get(bob_id))

    # time.sleep(2)
    print("After TTL:", tbl.scan())
    print("Filter age>20:", tbl.where(lambda row: row["age"] > 20))
    tbl.update(bob_id, {"name": "Bobby", "age": 26})
    print("After update:", tbl.get(bob_id))
    tbl.delete(bob_id)
    db.backup()
    print("After delete:", tbl.scan())

    # Test backup/restore functionality
    print("\n--- Testing Backup/Restore ---")
    db2 = InMemDb()
    tbl2 = db2.create_table("products")
    p1 = tbl2.insert({"name": "Laptop", "price": 999})
    p2 = tbl2.insert({"name": "Mouse", "price": 29})
    print("Before backup:", tbl2.scan())

    # Backup to file
    db2.backup()
    print("Database backed up to my_db_backup.json")

    # Create new database and restore
    db3 = InMemDb()
    db3.restore()
    tbl3 = db3.get_table("products")
    print("After restore:", tbl3.scan())
    print("Verify data integrity:", tbl3.get(p1))
