"""
Core GraphBLAS operations — generalized over arbitrary semirings.

Implements all operations from Kepner et al., Section 2:
  mxm, mxv, vxm, eWiseAdd, eWiseMult, extract, assign,
  apply, reduce, transpose, Kronecker product.

All operations support optional masking and accumulation.
"""

from __future__ import annotations
from typing import Any, Callable, Optional, Set, List, Dict, Tuple

from .algebra import (
    SparseMatrix, SparseVector, Semiring, Monoid, _NOVAL
)


# ══════════════════════════════════════════════════════════════════════════════
# Masking and Accumulation Helpers
# ══════════════════════════════════════════════════════════════════════════════

def _apply_mask(result_entries: dict, mask, complement: bool = False):
    """
    Filter entries by a structural mask.
    - mask: SparseMatrix or SparseVector (or None)
    - complement: if True, keep entries where mask does NOT have a stored value
    """
    if mask is None:
        return result_entries
    mask_struct = mask.structure()
    if complement:
        return {k: v for k, v in result_entries.items() if k not in mask_struct}
    else:
        return {k: v for k, v in result_entries.items() if k in mask_struct}


def _accumulate(existing, new_entries, accum_op: Optional[Callable] = None):
    """
    Merge new_entries into existing using accumulator.
    If accum_op is None, new entries simply overwrite.
    """
    if accum_op is None:
        result = dict(existing.entries)
        result.update(new_entries)
        return result
    result = dict(existing.entries)
    for k, v in new_entries.items():
        if k in result:
            result[k] = accum_op(result[k], v)
        else:
            result[k] = v
    return result


# ══════════════════════════════════════════════════════════════════════════════
# Core Operations
# ══════════════════════════════════════════════════════════════════════════════

def mxm(A: SparseMatrix, B: SparseMatrix, semiring: Semiring,
        mask: Optional[SparseMatrix] = None, complement_mask: bool = False,
        accum: Optional[Callable] = None,
        C: Optional[SparseMatrix] = None) -> SparseMatrix:
    """
    Generalized matrix-matrix multiply: C = A ⊕.⊗ B
    
    C(i,j) = ⊕_k [A(i,k) ⊗ B(k,j)]
    where ⊕ is the additive monoid and ⊗ is the multiplicative operator.
    """
    assert A.ncols == B.nrows, f"Dimension mismatch: A is {A.nrows}×{A.ncols}, B is {B.nrows}×{B.ncols}"

    # Build column-indexed structure of B for efficiency
    B_by_col: Dict[int, Dict[int, Any]] = {}
    for (r, c), v in B.entries.items():
        if c not in B_by_col:
            B_by_col[c] = {}
        B_by_col[c][r] = v

    entries = {}
    # Group A entries by row
    A_by_row: Dict[int, Dict[int, Any]] = {}
    for (r, c), v in A.entries.items():
        if r not in A_by_row:
            A_by_row[r] = {}
        A_by_row[r][c] = v

    for i, a_row in A_by_row.items():
        for j, b_col in B_by_col.items():
            # Compute semiring dot product over shared k indices
            products = []
            for k, a_val in a_row.items():
                if k in b_col:
                    products.append(semiring.mul(a_val, b_col[k]))
            if products:
                val = semiring.add.reduce(products)
                entries[(i, j)] = val

    # Apply mask
    entries = _apply_mask(entries, mask, complement_mask)

    # Handle accumulation with existing C
    if C is not None:
        entries = _accumulate(C, entries, accum)
        return SparseMatrix(C.nrows, C.ncols, entries)

    return SparseMatrix(A.nrows, B.ncols, entries)


def mxv(A: SparseMatrix, v: SparseVector, semiring: Semiring,
        mask: Optional[SparseVector] = None,
        complement_mask: bool = False) -> SparseVector:
    """Matrix-vector multiply: w = A ⊕.⊗ v"""
    assert A.ncols == v.n
    entries = {}
    
    # Group A by row
    A_by_row: Dict[int, Dict[int, Any]] = {}
    for (r, c), val in A.entries.items():
        if r not in A_by_row:
            A_by_row[r] = {}
        A_by_row[r][c] = val

    for i, row in A_by_row.items():
        products = []
        for k, a_val in row.items():
            v_val = v[k]
            if v_val is not _NOVAL:
                products.append(semiring.mul(a_val, v_val))
        if products:
            entries[i] = semiring.add.reduce(products)

    entries = _apply_mask(entries, mask, complement_mask)
    return SparseVector(A.nrows, entries)


def vxm(v: SparseVector, A: SparseMatrix, semiring: Semiring,
        mask: Optional[SparseVector] = None,
        complement_mask: bool = False) -> SparseVector:
    """Vector-matrix multiply: w = v ⊕.⊗ A (row vector × matrix)"""
    assert v.n == A.nrows
    entries = {}

    # Group A by column
    A_by_col: Dict[int, Dict[int, Any]] = {}
    for (r, c), val in A.entries.items():
        if c not in A_by_col:
            A_by_col[c] = {}
        A_by_col[c][r] = val

    for j, col in A_by_col.items():
        products = []
        for k, a_val in col.items():
            v_val = v[k]
            if v_val is not _NOVAL:
                products.append(semiring.mul(v_val, a_val))
        if products:
            entries[j] = semiring.add.reduce(products)

    entries = _apply_mask(entries, mask, complement_mask)
    return SparseVector(A.ncols, entries)


def eWiseAdd(A: SparseMatrix, B: SparseMatrix, op: Callable,
             identity: Any = None,
             mask: Optional[SparseMatrix] = None,
             complement_mask: bool = False) -> SparseMatrix:
    """
    Element-wise addition (union semantics).
    Operates on the UNION of structures of A and B.
    For positions only in A: use A's value; only in B: use B's value;
    in both: apply op(a, b).
    """
    assert A.nrows == B.nrows and A.ncols == B.ncols
    entries = {}
    all_keys = A.structure() | B.structure()
    for key in all_keys:
        a_val = A[key]
        b_val = B[key]
        if a_val is not _NOVAL and b_val is not _NOVAL:
            entries[key] = op(a_val, b_val)
        elif a_val is not _NOVAL:
            entries[key] = a_val
        else:
            entries[key] = b_val

    entries = _apply_mask(entries, mask, complement_mask)
    return SparseMatrix(A.nrows, A.ncols, entries)


def eWiseMult(A: SparseMatrix, B: SparseMatrix, op: Callable,
              mask: Optional[SparseMatrix] = None,
              complement_mask: bool = False) -> SparseMatrix:
    """
    Element-wise multiplication (intersection semantics).
    Operates only on positions present in BOTH A and B.
    """
    assert A.nrows == B.nrows and A.ncols == B.ncols
    entries = {}
    common_keys = A.structure() & B.structure()
    for key in common_keys:
        entries[key] = op(A.entries[key], B.entries[key])

    entries = _apply_mask(entries, mask, complement_mask)
    return SparseMatrix(A.nrows, A.ncols, entries)


def extract_matrix(A: SparseMatrix, row_indices: List[int],
                   col_indices: List[int]) -> SparseMatrix:
    """Extract sub-matrix A[row_indices, col_indices]."""
    entries = {}
    row_set = set(row_indices)
    col_set = set(col_indices)
    row_map = {r: i for i, r in enumerate(row_indices)}
    col_map = {c: j for j, c in enumerate(col_indices)}
    for (r, c), v in A.entries.items():
        if r in row_set and c in col_set:
            entries[(row_map[r], col_map[c])] = v
    return SparseMatrix(len(row_indices), len(col_indices), entries)


def extract_vector(v: SparseVector, indices: List[int]) -> SparseVector:
    """Extract sub-vector v[indices]."""
    entries = {}
    for new_i, old_i in enumerate(indices):
        val = v[old_i]
        if val is not _NOVAL:
            entries[new_i] = val
    return SparseVector(len(indices), entries)


def assign_matrix(C: SparseMatrix, A: SparseMatrix,
                  row_indices: List[int], col_indices: List[int],
                  accum: Optional[Callable] = None) -> SparseMatrix:
    """Assign A into C at positions [row_indices, col_indices]."""
    result = C.copy()
    for (i, j), v in A.entries.items():
        ri = row_indices[i]
        cj = col_indices[j]
        if accum and (ri, cj) in result.entries:
            result.entries[(ri, cj)] = accum(result.entries[(ri, cj)], v)
        else:
            result.entries[(ri, cj)] = v
    return result


def assign_vector(w: SparseVector, v: SparseVector,
                  indices: List[int],
                  accum: Optional[Callable] = None) -> SparseVector:
    """Assign v into w at positions [indices]."""
    result = w.copy()
    for i, val in v.entries.items():
        idx = indices[i]
        if accum and idx in result.entries:
            result.entries[idx] = accum(result.entries[idx], val)
        else:
            result.entries[idx] = val
    return result


def apply_op(A, func: Callable):
    """Apply a unary function to every stored entry of a matrix or vector."""
    if isinstance(A, SparseMatrix):
        entries = {k: func(v) for k, v in A.entries.items()}
        return SparseMatrix(A.nrows, A.ncols, entries)
    elif isinstance(A, SparseVector):
        entries = {k: func(v) for k, v in A.entries.items()}
        return SparseVector(A.n, entries)
    raise TypeError(f"Expected SparseMatrix or SparseVector, got {type(A)}")


def reduce_matrix_to_vector(A: SparseMatrix, monoid: Monoid,
                            axis: str = 'row') -> SparseVector:
    """
    Reduce matrix to vector using a monoid.
    axis='row': reduce across columns (one result per row)
    axis='col': reduce across rows (one result per column)
    """
    entries: Dict[int, Any] = {}
    if axis == 'row':
        for (r, c), v in A.entries.items():
            if r in entries:
                entries[r] = monoid(entries[r], v)
            else:
                entries[r] = v
        return SparseVector(A.nrows, entries)
    else:  # col
        for (r, c), v in A.entries.items():
            if c in entries:
                entries[c] = monoid(entries[c], v)
            else:
                entries[c] = v
        return SparseVector(A.ncols, entries)


def reduce_vector_to_scalar(v: SparseVector, monoid: Monoid) -> Any:
    """Reduce vector to scalar using a monoid."""
    if not v.entries:
        return monoid.identity
    return monoid.reduce(v.entries.values())


def transpose(A: SparseMatrix) -> SparseMatrix:
    """Transpose a matrix."""
    return A.transpose()


def kronecker(A: SparseMatrix, B: SparseMatrix,
              semiring: Semiring) -> SparseMatrix:
    """
    Kronecker product: C = A ⊗_kron B
    C((i*B.nrows + k), (j*B.ncols + l)) = A(i,j) ⊗ B(k,l)
    """
    entries = {}
    for (i, j), a_val in A.entries.items():
        for (k, l), b_val in B.entries.items():
            row = i * B.nrows + k
            col = j * B.ncols + l
            entries[(row, col)] = semiring.mul(a_val, b_val)
    return SparseMatrix(A.nrows * B.nrows, A.ncols * B.ncols, entries)
