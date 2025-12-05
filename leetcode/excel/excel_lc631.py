import re
from collections import deque
from typing import List, Tuple

from excel.spreadsheet import Spreadsheet


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
        print(expr)
        self.spreadsheet.set_cell(dest_cell, expr)
        return self.spreadsheet.get_cell(dest_cell)

    def _coord(self, row: int, column: str) -> str:
        return f"{column}{row}"

    def _coord_index(self, cell: str) -> Tuple[int, int]:
        col = ''.join([ch for ch in cell if ch.isalpha()])
        row = cell.removeprefix(col)

        col_idx = 0
        for ch in col:
            col_idx = col_idx * 26 + ord(ch) - ord('A')
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
        
        r_lo, r_hi = sorted((r_start, r_end))
        c_lo, c_hi = sorted((c_start, c_end))

        cells = []
        for r in range(r_lo, r_hi + 1):
            for c in range(c_lo, c_hi + 1):
                cells.append(self._to_cell_name(r, c))
        return cells

s = Excel(10, 'C')
# print(s._expand_cells("Y2", "AB10"))
# for col in range(0, 5):
#     for row in range(1, 5):
#         s.set(row, s._to_col(col), row * 10)
s.set(1, 'A', 2)
print(s.sum(5, "G", ["A1", "A1:B2"]))