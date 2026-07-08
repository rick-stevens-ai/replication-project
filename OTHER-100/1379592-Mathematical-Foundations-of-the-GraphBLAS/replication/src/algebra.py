"""
GraphBLAS algebraic foundations: Monoids, Semirings, and Sparse containers.

Implements the mathematical structures from Kepner et al., 
"Mathematical Foundations of the GraphBLAS" (2016).
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import Any, Callable, Optional, Dict, Tuple, List, Set

# Sentinel for "no value" (structural zero — distinct from semiring identity)
_NOVAL = object()


# ══════════════════════════════════════════════════════════════════════════════
# Algebraic Structures
# ══════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class Monoid:
    """A monoid: an associative binary operator with an identity element."""
    op: Callable[[Any, Any], Any]
    identity: Any
    name: str = ""

    def __call__(self, a, b):
        return self.op(a, b)

    def reduce(self, values):
        """Reduce an iterable using the monoid."""
        result = self.identity
        for v in values:
            result = self.op(result, v)
        return result


@dataclass(frozen=True)
class Semiring:
    """
    A semiring (⊕, ⊗, 0, 1):
    - additive monoid (⊕, 0)
    - multiplicative monoid (⊗, 1)
    - ⊗ distributes over ⊕
    - 0 is the annihilator of ⊗: a ⊗ 0 = 0 ⊗ a = 0
    """
    add: Monoid       # (⊕, 0)
    mul: Monoid       # (⊗, 1)
    name: str = ""

    @property
    def zero(self):
        return self.add.identity

    @property
    def one(self):
        return self.mul.identity


# ── Built-in semirings ───────────────────────────────────────────────────────

# Arithmetic semiring: (ℝ, +, ×, 0, 1)
PLUS = Monoid(op=lambda a, b: a + b, identity=0, name="PLUS")
TIMES = Monoid(op=lambda a, b: a * b, identity=1, name="TIMES")
ARITHMETIC = Semiring(add=PLUS, mul=TIMES, name="Arithmetic(+,×)")

# Tropical (min-plus) semiring: (ℝ∪{∞}, min, +, ∞, 0)
INF = float('inf')
MIN = Monoid(op=lambda a, b: min(a, b), identity=INF, name="MIN")
PLUS_TROP = Monoid(op=lambda a, b: a + b, identity=0, name="PLUS")
TROPICAL = Semiring(add=MIN, mul=PLUS_TROP, name="Tropical(min,+)")

# Boolean semiring: ({T,F}, OR, AND, False, True)
OR = Monoid(op=lambda a, b: a or b, identity=False, name="OR")
AND = Monoid(op=lambda a, b: a and b, identity=True, name="AND")
BOOLEAN = Semiring(add=OR, mul=AND, name="Boolean(∨,∧)")

# Max-plus semiring: (ℝ∪{-∞}, max, +, -∞, 0)
NEGINF = float('-inf')
MAX = Monoid(op=lambda a, b: max(a, b), identity=NEGINF, name="MAX")
MAXPLUS = Semiring(add=MAX, mul=PLUS_TROP, name="MaxPlus(max,+)")

# Min-times semiring: (ℝ∪{∞}, min, ×, ∞, 1)
MINTIMES = Semiring(add=MIN, mul=TIMES, name="MinTimes(min,×)")

# Max-min semiring: (ℝ∪{-∞}, max, min, -∞, ∞)
MIN_OP = Monoid(op=lambda a, b: min(a, b), identity=INF, name="MIN")
MAXMIN = Semiring(add=MAX, mul=MIN_OP, name="MaxMin(max,min)")

# Or-and semiring (same as Boolean but explicit)
OR_AND = BOOLEAN

# Plus-min semiring (path counting in min-width networks)
PLUSMIN = Semiring(add=PLUS, mul=MIN_OP, name="PlusMin(+,min)")


# ══════════════════════════════════════════════════════════════════════════════
# Sparse Matrix and Vector
# ══════════════════════════════════════════════════════════════════════════════

class SparseVector:
    """Sparse vector over a semiring. Only stored entries participate in operations."""

    def __init__(self, n: int, entries: Optional[Dict[int, Any]] = None):
        self.n = n
        self.entries: Dict[int, Any] = dict(entries) if entries else {}

    def __getitem__(self, i: int):
        return self.entries.get(i, _NOVAL)

    def __setitem__(self, i: int, val):
        if val is _NOVAL:
            self.entries.pop(i, None)
        else:
            self.entries[i] = val

    def nnz(self) -> int:
        return len(self.entries)

    def __repr__(self):
        return f"SparseVector(n={self.n}, nnz={self.nnz()}, {self.entries})"

    def to_dense(self, zero=0):
        """Return dense list, filling missing entries with `zero`."""
        return [self.entries.get(i, zero) for i in range(self.n)]

    @classmethod
    def from_dense(cls, values, zero=0) -> 'SparseVector':
        n = len(values)
        entries = {i: v for i, v in enumerate(values) if v != zero}
        return cls(n, entries)

    def copy(self) -> 'SparseVector':
        return SparseVector(self.n, dict(self.entries))

    def structure(self) -> Set[int]:
        """Return set of indices with stored entries."""
        return set(self.entries.keys())


class SparseMatrix:
    """
    Sparse matrix over a semiring. 
    Stored as dict of (row, col) → value.
    """

    def __init__(self, nrows: int, ncols: int,
                 entries: Optional[Dict[Tuple[int, int], Any]] = None):
        self.nrows = nrows
        self.ncols = ncols
        self.entries: Dict[Tuple[int, int], Any] = dict(entries) if entries else {}

    def __getitem__(self, key: Tuple[int, int]):
        return self.entries.get(key, _NOVAL)

    def __setitem__(self, key: Tuple[int, int], val):
        if val is _NOVAL:
            self.entries.pop(key, None)
        else:
            self.entries[key] = val

    def nnz(self) -> int:
        return len(self.entries)

    def __repr__(self):
        return f"SparseMatrix({self.nrows}×{self.ncols}, nnz={self.nnz()})"

    def to_dense(self, zero=0) -> List[List[Any]]:
        """Return dense 2D list."""
        return [[self.entries.get((i, j), zero)
                 for j in range(self.ncols)]
                for i in range(self.nrows)]

    @classmethod
    def from_dense(cls, rows: List[List[Any]], zero=0) -> 'SparseMatrix':
        nrows = len(rows)
        ncols = len(rows[0]) if rows else 0
        entries = {}
        for i, row in enumerate(rows):
            for j, v in enumerate(row):
                if v != zero:
                    entries[(i, j)] = v
        return cls(nrows, ncols, entries)

    @classmethod
    def from_lists(cls, nrows: int, ncols: int,
                   rows: List[int], cols: List[int], vals: List[Any]) -> 'SparseMatrix':
        entries = {(r, c): v for r, c, v in zip(rows, cols, vals)}
        return cls(nrows, ncols, entries)

    def copy(self) -> 'SparseMatrix':
        return SparseMatrix(self.nrows, self.ncols, dict(self.entries))

    def row_indices(self, i: int) -> Dict[int, Any]:
        """Return {col: val} for row i."""
        return {c: v for (r, c), v in self.entries.items() if r == i}

    def col_indices(self, j: int) -> Dict[int, Any]:
        """Return {row: val} for column j."""
        return {r: v for (r, c), v in self.entries.items() if c == j}

    def structure(self) -> Set[Tuple[int, int]]:
        """Return set of (row, col) with stored entries."""
        return set(self.entries.keys())

    def transpose(self) -> 'SparseMatrix':
        """Return transposed matrix."""
        entries = {(c, r): v for (r, c), v in self.entries.items()}
        return SparseMatrix(self.ncols, self.nrows, entries)
