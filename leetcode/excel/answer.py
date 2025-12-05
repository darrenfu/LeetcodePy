import re
from collections import defaultdict, deque
from typing import Set, List
# !!! use re.compile(str).match() instead of re.match(PATTERN, str)
CELL_RE = re.compile(r"^[A-Z]+[1-9][0-9]*$")

# Practice version compared to spreadsheet.py
class Spreadsheet:
    def __init__(self):
        self.expr = {}
        self.deps = defaultdict(set)
        self.rev_deps = defaultdict(set)
        # self.topo_order = []
        self.topo_index = {}
        self.values = {}

    def set_cell(self, cell: str, expr: str):
        cell = self._normalize_cell(cell)
        # !!! Don't forget this
        self.expr[cell] = expr
        upstreams = self._extract_upstream_deps(expr)
        self._update_deps(cell, upstreams)
        downstreams = self._collect_downstream_cells([cell])
        self._recompute_cell_values(downstreams)

    def get_cell(self, cell: str) -> int:
        cell = self._normalize_cell(cell)
        if cell not in self.values:
            raise ValueError(f"Value unset in cell {cell}")
        return self.values[cell]

    def _normalize_cell(self, cell: str) -> str:
        cell = cell.strip().upper()
        if CELL_RE.match(cell):
            return cell
        raise ValueError(f"invalid cell name: {cell}")

    def _extract_upstream_deps(self, expr: str) -> Set[str]:
        tokens = expr.replace(' ', '').split('+')
        deps = set()
        for token in tokens:
            expr = token.upper()
            if CELL_RE.match(expr): # cell ref
                deps.add(expr)
            else: # constant literal
                try:
                    int(expr)
                except ValueError:
                    raise ValueError(f"{expr} is not an integer")
        return deps

    def _update_deps(self, cell: str, upstreams: Set[str]) -> None:
        # Remove old dependencies in bidirectional way
        old_upstreams = self.deps[cell]
        for upstream in old_upstreams:
            self.rev_deps[upstream].discard(cell)
        # Install new dependencies
        self.deps[cell] = upstreams
        for ups in upstreams:
            self.rev_deps[ups].add(cell)
            # Ensure all upstream nodes exist
            self.deps.setdefault(ups, set())

    def _collect_downstream_cells(self, roots: List[str]) -> Set[str]:
        # BFS
        q = deque(roots)
        # !!! Use visited set to track all downstream cells
        visited = set()
        while q:
            node = q.popleft()
            visited.add(node)
            # !!! Use rev_deps to traverse downstream nodes
            for downstream in self.rev_deps[node]:
                if downstream not in visited:
                    q.append(downstream)
        return visited

    def _ensure_topological_order(self):
        in_degree = {c: 0 for c in self.deps.keys()}
        for c, upstreams in self.deps.items():
            for ups in upstreams:
                in_degree[c] += 1
                # !!! tip: if certain upstream's value is not set, set its default value to 0
                in_degree.setdefault(ups, 0)

        # !!! Start nodes whose in_degree == 0
        q = deque([c for c, deg in in_degree.items() if deg == 0])
        topo_order = []
        while q:
            node = q.popleft()
            topo_order.append(node)
            for downstream in self.rev_deps[node]:
                # !!! Once you “consume” an upstream node, you effectively remove all edges from it.
                # -= 1 means one of the upstreams was handled
                in_degree[downstream] -= 1
                # !!! This is the core invariant that guarantees topological order:
                # any node appears in topo_order only after all nodes it depends on.
                if in_degree[downstream] == 0:
                    q.append(downstream)

        if len(in_degree) != len(topo_order):
            raise ValueError("Cycle detected")

        # self.topo_order = topo_order
        self.topo_index = {c: i for i, c in enumerate(topo_order)}

    def _recompute_cell_values(self, affected: Set[str]) -> None:
        if not affected:
            return
        self._ensure_topological_order()

        # for cell in self.topo_order:
        #     if cell not in affected:
        #         continue
        for cell in sorted(affected, key=lambda c: self.topo_index[c]):
            # !!! Safe fallback when a cell is referenced as a dependency but hasn’t been set yet.
            # Matches the “Excel-y” behavior: empty cells are often treated as 0 in arithmetic.
            expr = self.expr.get(cell, "0")
            self.values[cell] = self._eval_expr(expr)

    def _eval_expr(self, expr: str) -> int:
        tokens = expr.replace(' ', '').split('+')
        total_sum = 0
        for token in tokens:
            cell_ref = token.upper()
            local_value: int = 0
            if CELL_RE.match(cell_ref):
                if cell_ref not in self.values:
                    print(f"Value unset at cell: {cell_ref}, fallback to 0")
                    local_value = 0
                else:
                    local_value = self.values[cell_ref]
            else: # constant literal
                local_value = int(cell_ref)
            total_sum += local_value
        return total_sum


class Excel:

    def __init__(self, height: int, width: str):
        self.spreadsheet = Spreadsheet()
        self.R = height
        self.C = width

    def set(self, row: int, column: str, val: int) -> None:
        cell = self._coord(row, column)
        print("set ", cell, val)
        self.spreadsheet.set_cell(cell, str(val))

    def get(self, row: int, column: str) -> int:
        cell = self._coord(row, column)
        return self.spreadsheet.get_cell(cell)

    def sum(self, row: int, column: str, numbers: List[str]) -> int:
        dest_cell = self._coord(row, column)
        src_cells = []
        for spec in numbers:
            if ':' not in spec: # single cell
                src_cells.append(spec)
            else: # multi cells
                start, end = spec.split(':')
                multi_cells = self._expand_cells(start, end)
                src_cells.extend(multi_cells)

        expr = '+'.join(src_cells) if src_cells else "0"
        self.spreadsheet.set_cell(dest_cell, expr)
        return self.spreadsheet.get_cell(dest_cell)

    def _coord(self, row: int, column: str) -> str:
        return f"{column}{row}"

    def _coord_index(self, cell: str) -> Tuple[int, int]:
        col = ''.join([ch for ch in cell if ch.isalpha()])
        row = cell.removeprefix(col)

        col_idx = 0
        for ch in col:
            col_idx = col_idx * 26 + ord(ch) - ord('A') + 1
        row_idx = int(row)-1
        return row_idx, col_idx

    def _to_col(self, col_index: int) -> str:
        # 0->"A", 25->"Z", 26->"AA", etc.
        chars = deque()
        while True:
            col_index, remainder = divmod(col_index, 26)
            chars.appendleft(chr(ord('A') + remainder))
            if col_index == 0:
                break
            col_index -= 1
        return ''.join(chars)

    def _to_cell_name(self, r: int, c: int) -> str:
        return self._coord(r+1, self._to_col(c))

    def _expand_cells(self, start_cell: str, end_cell: str) -> List[str]:
        s = self.spreadsheet._normalize_cell(start_cell)
        e = self.spreadsheet._normalize_cell(end_cell)
        if s == e:
            return [s]

        r_start, c_start = self._coord_index(s)
        r_end, c_end = self._coord_index(e)
        if (c_start, r_start) > (c_end, r_end):
            c_start, r_start = c_end, r_end
        cells = []
        for i in range(r_start, r_end+1):
            for j in range(c_start, c_end+1):
                cells.append(self._to_cell_name(i, j))
        return cells
