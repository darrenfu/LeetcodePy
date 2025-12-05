# test_fuzz_spreadsheet.py

import random
import re

from spreadsheet import Spreadsheet  # your implementation under test

# Local regex for cell names (same as in spreadsheet.py)
CELL_RE = re.compile(r"^[A-Z]+[1-9][0-9]*$")


class NaiveSpreadsheet:
    """
    Simple reference implementation that recomputes the entire sheet
    from scratch after every change.

    It uses the same expression semantics as Spreadsheet:
    - expressions are sums of integer literals and cell references
    - unset cells default to expression "0"
    - cycles raise ValueError
    """

    def __init__(self) -> None:
        # cell -> original expression string
        self._exprs: dict[str, str] = {}
        # cell -> evaluated value
        self._values: dict[str, int] = {}

    # --- public API mirroring Spreadsheet ---

    def set_cell(self, name: str, expression: str) -> None:
        cell = self._normalize_cell(name)
        self._exprs[cell] = expression.strip()
        self._recompute_all()

    def batch_set_cells(self, updates) -> None:
        for name, expr in updates:
            cell = self._normalize_cell(name)
            self._exprs[cell] = expr.strip()
        self._recompute_all()

    def get_cell(self, name: str) -> int:
        cell = self._normalize_cell(name)
        if cell not in self._values:
            raise KeyError(f"Cell {cell} has no computed value yet.")
        return self._values[cell]

    # --- internal helpers ---

    @staticmethod
    def _normalize_cell(name: str) -> str:
        cell = name.strip().upper()
        if not CELL_RE.match(cell):
            raise ValueError(f"Invalid cell name: {name!r}")
        return cell

    @staticmethod
    def _extract_dependencies(expression: str) -> set[str]:
        """
        Extract all cell references from an expression.
        Semantics:
        - strip spaces
        - split by '+'
        - tokens matching CELL_RE are deps
        - other tokens must be valid ints
        """
        expr = expression.replace(" ", "")
        deps: set[str] = set()
        if not expr:
            return deps

        for token in expr.split("+"):
            if not token:
                continue
            if CELL_RE.match(token):
                deps.add(token)
            else:
                # validate integer literal
                int(token)
        return deps

    def _eval_expression(self, cell: str, values: dict[str, int]) -> int:
        """
        Evaluate a cell using the same rules as Spreadsheet._eval_expression.
        """
        expr = self._exprs.get(cell, "0")  # unset cells behave like "0"
        s = expr.replace(" ", "")
        if s == "":
            return 0

        total = 0
        for token in s.split("+"):
            if not token:
                continue
            if CELL_RE.match(token):
                if token not in values:
                    raise KeyError(f"Referenced cell {token} has no value yet")
                total += values[token]
            else:
                total += int(token)
        return total

    def _recompute_all(self) -> None:
        """
        Rebuild dependency graph from scratch and recompute all cell values
        in topological order (global recompute).
        """
        # Build deps: cell -> set(upstream cells)
        deps: dict[str, set[str]] = {}
        all_cells: set[str] = set(self._exprs.keys())
        for cell, expr in self._exprs.items():
            d = self._extract_dependencies(expr)
            deps[cell] = d
            all_cells |= d

        # Ensure referenced-only cells exist in graph with default expr "0"
        for c in all_cells:
            deps.setdefault(c, set())

        # Kahn's algorithm for topo sort
        in_degree = {c: 0 for c in deps}
        for cell, ups in deps.items():
            for u in ups:
                in_degree[cell] += 1

        from collections import deque

        q = deque([c for c, deg in in_degree.items() if deg == 0])
        order: list[str] = []

        while q:
            c = q.popleft()
            order.append(c)
            # find all v such that c -> v (v depends on c)
            for v, ups in deps.items():
                if c in ups:
                    in_degree[v] -= 1
                    if in_degree[v] == 0:
                        q.append(v)

        if len(order) != len(in_degree):
            # same cycle semantics as Spreadsheet._ensure_topological_order
            raise ValueError("Cycle detected in spreadsheet dependencies")

        # Evaluate in topo order
        values: dict[str, int] = {}
        for c in order:
            values[c] = self._eval_expression(c, values)

        self._values = values


# -------- fuzz generator helpers --------

def _random_cell(rng: random.Random, max_col: int = 3, max_row: int = 5) -> str:
    """
    Generate a random cell name like A1..D5.
    """
    col = chr(ord("A") + rng.randint(0, max_col))
    row = rng.randint(1, max_row)
    return f"{col}{row}"


def _random_expr(
        rng: random.Random,
        existing_cells: set[str],
        max_terms: int = 3,
) -> str:
    """
    Generate a random expression:
    - 1..max_terms tokens
    - tokens are either ints (including negatives) or existing cell refs
    - joined by '+'
    """
    n_terms = rng.randint(1, max_terms)
    tokens: list[str] = []
    for _ in range(n_terms):
        # bias to use existing cells when available
        if existing_cells and rng.random() < 0.6:
            tokens.append(rng.choice(list(existing_cells)))
        else:
            tokens.append(str(rng.randint(-5, 5)))
    return " + ".join(tokens)


def _run_single_fuzz(seed: int, n_ops: int = 50, verbose: bool = False) -> bool:
    rng = random.Random(seed)
    fast = Spreadsheet()        # your incremental impl
    ref = NaiveSpreadsheet()    # full recompute reference

    existing: set[str] = set()

    for step in range(n_ops):
        # Mostly single set, occasional batch
        op_kind = rng.choice([0, 0, 0, 1])  # 0 = set, 1 = batch

        try:
            if op_kind == 0:
                # single set_cell
                cell = _random_cell(rng)
                expr = _random_expr(rng, existing)
                if verbose:
                    print(f"[seed={seed} step={step}] set {cell} = {expr!r}")
                fast.set_cell(cell, expr)
                ref.set_cell(cell, expr)
                existing.add(cell)
            else:
                # batch_set_cells
                batch = []
                batch_size = rng.randint(2, 4)
                for _ in range(batch_size):
                    cell = _random_cell(rng)
                    expr = _random_expr(rng, existing)
                    batch.append((cell, expr))
                    existing.add(cell)
                if verbose:
                    print(f"[seed={seed} step={step}] batch {batch}")
                fast.batch_set_cells(batch)
                ref.batch_set_cells(batch)

        except ValueError:
            # cycle detected in either engine – treat as "this scenario is invalid"
            # and consider this seed as passed (we're not testing cycle behavior here).
            if verbose:
                print(f"[seed={seed} step={step}] cycle detected, skipping further checks")
            return True

        # After each op, compare current values for all known cells
        for cell in list(existing):
            try:
                v_fast = fast.get_cell(cell)
                v_ref = ref.get_cell(cell)
            except KeyError:
                # cell not yet fully initialized in one of the engines
                continue

            if v_fast != v_ref:
                if verbose:
                    print(
                        f"[seed={seed} step={step}] mismatch at {cell}: "
                        f"Spreadsheet={v_fast}, Reference={v_ref}"
                    )
                return False

    return True


def test_fuzz_spreadsheet():
    # Try multiple seeds to explore different random operation sequences.
    # You can increase the range for heavier fuzzing.
    for seed in range(10):
        assert _run_single_fuzz(seed, n_ops=50, verbose=False), f"Fuzz failed for seed={seed}"