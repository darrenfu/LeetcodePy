from __future__ import annotations

import re
from collections import defaultdict, deque
from typing import Dict, Set, List, Iterable, Tuple


# support multi-letter columns (A, Z, AA, XFD, etc.)
CELL_RE = re.compile(r"^[A-Z]+[1-9][0-9]*$")

#  Complexity
# 	•	get = O(1) with cache
# 	•	set = O(#affected nodes)
# 	•	space = O(#cells + #dependencies)
# This class includes the following components:
# 1. cell name system
# 2. Expression parsing where tokens are either cell refs or integers, split by '+'.
# 3. Dependency tracking & incremental recompute
class Spreadsheet:
    """
    Simplified spreadsheet engine with:
    - cell formulas using '+' and cell references
    - dependency tracking
    - incremental recomputation using a cached topological order
    """

    def __init__(self) -> None:
        # central store of original expressions per cell
        self._exprs: Dict[str, str] = {}

        # Cached evaluated value per cell
        self._values: Dict[str, int] = {}

        # dependency graph: cell -> set of upstream cells it depends on
        self._deps: Dict[str, Set[str]] = defaultdict(set)

        # reverse dependency graph: cell -> set of downstream cells that depend on it
        self._rev_deps: Dict[str, Set[str]] = defaultdict(set)

        # cached global topological order of all known cells
        # self._topo_order: List[str] = []
        # node -> index in _topo_order to sort affected nodes quickly.
        self._topo_index: Dict[str, int] = {}
        self._topo_dirty: bool = True  # flip to True whenever deps graph changes

    # ------------- Public API -------------

    def set_cell(self, name: str, expression: str) -> None:
        """
        Set a single cell's expression (either integer or formula).
        Triggers incremental recompute of that cell and all downstream dependents.
        """
        cell = self._normalize_cell(name)
        expr = expression.strip()

        # extract upstream dependencies from the new expression
        new_deps = self._extract_dependencies(expr)

        # Store raw expression
        self._exprs[cell] = expr

        # keep _deps and _rev_deps in sync
        self._update_dependencies(cell, new_deps)

        # Topo order is now stale
        self._topo_dirty = True

        # collect affected cells: this cell + all downstream cells
        affected = self._collect_downstream_cells({cell})

        # recompute only affected cells, in topo order
        self._recompute_affected(affected)

    def batch_set_cells(self, updates: Iterable[Tuple[str, str]]) -> None:
        """
        Batch version of set_cell for better efficiency when many cells change at once.

        Steps:
        1. Parse all expressions and compute their dependencies.
        2. Apply all expression + dependency updates.
        3. Mark topo order dirty once.
        4. Collect the union of all affected cells (updated cells + downstream).
        5. Recompute them in a single pass in topo order.
        """
        normalized_updates: List[Tuple[str, str, Set[str]]] = []
        roots: Set[str] = set()

        # Normalize and pre-parse
        for name, expr in updates:
            cell = self._normalize_cell(name)
            expression = expr.strip()
            deps = self._extract_dependencies(expression)
            normalized_updates.append((cell, expression, deps))
            roots.add(cell)

        # Apply expressions & dependency graph updates
        for cell, expression, deps in normalized_updates:
            self._exprs[cell] = expression
            self._update_dependencies(cell, deps)

        # Invalidate topo order once for all graph changes
        self._topo_dirty = True

        # All cells that need recomputation: roots + their downstream
        affected = self._collect_downstream_cells(roots)

        # Single recomputation pass
        self._recompute_affected(affected)

    def get_cell(self, name: str) -> int:
        """
        Return cached value; assumes set_cell / batch_set_cells
        have already brought it up to date.
        """
        cell = self._normalize_cell(name)
        if cell not in self._values:
            raise KeyError(f"Cell {cell} has no computed value yet.")
        return self._values[cell]

    # ------------- Internal helpers -------------

    @staticmethod
    def _normalize_cell(name: str) -> str:
        """
        normalize + validate a cell name (supports AA10, etc.).
        """
        cell = name.strip().upper()
        if not CELL_RE.match(cell):
            raise ValueError(f"Invalid cell name: {name!r}")
        return cell

    def _extract_dependencies(self, expression: str) -> Set[str]:
        """
        Return the set of cell names referenced in this expression.
        Expression format is limited to tokens separated by '+'.
        """
        deps: Set[str] = set()
        # strip spaces once; split by '+'
        for token in expression.replace(" ", "").split("+"):
            if not token:
                continue

            if CELL_RE.match(token):
                # Cell reference like A1, AA10
                deps.add(token)
            else:
                # Should be an integer literal; fail early on garbage
                try:
                    int(token)
                except ValueError:
                    raise ValueError(
                        f"Unsupported token in expression {expression!r}: {token!r}"
                    )
        return deps

    def _update_dependencies(self, cell: str, new_deps: Set[str]) -> None:
        """
        Update graph edges for `cell` to match `new_deps`.
        Keeps both _deps and _rev_deps consistent.
        """
        # Remove old reverse edges
        old_deps = self._deps.get(cell, set())
        for upstream in old_deps:
            self._rev_deps[upstream].discard(cell)

        # Install new deps
        self._deps[cell] = set(new_deps)
        for upstream in new_deps:
            self._rev_deps[upstream].add(cell)

        # Ensure all referenced cells exist in the graph, even if they have no expression yet.
        for upstream in new_deps:
            self._deps.setdefault(upstream, set())

    def _collect_downstream_cells(self, roots: Set[str]) -> Set[str]:
        """
        From a set of starting cells, collect all cells that need recomputation:
        - the roots themselves
        - all (transitive) downstream dependents via _rev_deps
        """
        to_visit = deque(roots)
        seen: Set[str] = set()

        while to_visit:
            c = to_visit.popleft()
            if c in seen:
                continue
            seen.add(c)

            for child in self._rev_deps.get(c, ()):
                if child not in seen:
                    to_visit.append(child)

        return seen

    def _ensure_topological_order(self) -> None:
        """
        Build and cache a global topological order for all known cells if needed.
        Uses Kahn's algorithm over the dependency graph.
        """
        if not self._topo_dirty:
            return

        # compute in-degree from _deps (upstream dependencies)
        in_degree: Dict[str, int] = {c: 0 for c in self._deps}
        for cell, ups in self._deps.items():
            for upstream in ups:
                in_degree[cell] += 1
                # Ensure upstream also appears in in_degree
                in_degree.setdefault(upstream, 0)

        # Kahn's algorithm
        q = deque([c for c, deg in in_degree.items() if deg == 0])
        order: List[str] = []

        while q:
            c = q.popleft()
            order.append(c)
            for downstream in self._rev_deps.get(c, ()):
                in_degree[downstream] -= 1
                if in_degree[downstream] == 0:
                    q.append(downstream)

        if len(order) != len(in_degree):
            # cycle detection; real system might rollback instead of raising
            raise ValueError("Cycle detected in spreadsheet dependencies")

        # self._topo_order = order
        # maintain topo_index alongside topo_order
        self._topo_index = {cell: idx for idx, cell in enumerate(order)}

        self._topo_dirty = False

    def _recompute_affected(self, affected: Set[str]) -> None:
        """
        Re-evaluate all affected cells in topological order so that
        dependencies are always computed before dependents.
        """
        if not affected:
            return

        # Ensure topo order is fresh
        self._ensure_topological_order()

        # recompute only affected cells, in topo order.
        # Optimization: We use the precomputed _topo_index to sort only
        # the affected nodes. This reduces cost from O(#all_cells) to roughly
        # O(#affected * log #affected) (due to sort).
        affected_cells = sorted(
            (c for c in affected if c in self._topo_index),
            key=lambda c: self._topo_index[c],
        )

        # for cell in self._topo_order:
        #   if cell not in affected:
        #      continue
        for cell in affected_cells:
            expr = self._exprs.get(cell, "0")
            self._values[cell] = self._eval_expression(expr)

    def _eval_expression(self, expression: str) -> int:
        """
        Evaluate a single expression using current cached cell values.
        """
        expr = expression.replace(" ", "")
        if expr == "":
            return 0

        total = 0
        for token in expr.split("+"):
            if not token:
                continue

            if CELL_RE.match(token):
                # Cell reference
                if token not in self._values:
                    # raise KeyError(f"Referenced cell {token} has no value yet")
                    print(f"Referenced cell {token} has no value yet")
                    self._values[token] = 0
                total += self._values[token]
            else:
                # Integer literal
                total += int(token)

        return total


if __name__ == "__main__":
    # Basic test
    s = Spreadsheet()
    s.set_cell("A1", "1")
    s.set_cell("A2", "2")
    s.set_cell("A3", "A1 + A2")        # 3
    s.set_cell("A4", "A3 + A2")        # 5
    s.set_cell("A5", "A3 + A4")        # 8
    s.set_cell("B1", "A1 + A2 + A3 + A4 + A5")  # 1+2+3+5+8=19

    print("B1 =", s.get_cell("B1"))    # 19

    # Change A1 and see incremental recompute
    s.set_cell("A1", "100")
    print("A3 =", s.get_cell("A3"))    # 100 + 2 = 102
    print("A4 =", s.get_cell("A4"))    # 102 + 2 = 104
    print("A5 =", s.get_cell("A5"))    # 102 + 104 = 206
    print("B1 =", s.get_cell("B1"))    # 100 + 2 + 102 + 104 + 206 = 514

    # batch update example
    s.batch_set_cells(
        [
            ("C1", "10"),
            ("C2", "C1 + A1"),
            ("C3", "C2 + B1"),
        ]
    )
    print("C3 =", s.get_cell("C3"))