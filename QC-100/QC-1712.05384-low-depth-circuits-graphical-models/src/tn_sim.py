"""
Replication of Boixo et al. 2017 (arXiv:1712.05384):
  "Simulation of low-depth quantum circuits as complex undirected graphical models"

Core claim replicated: A shallow quantum circuit on a 2D lattice of n qubits with
gate depth d can be mapped to a tensor network / undirected graphical model. The
cost of exact contraction is exponential in the *contraction width* (an upper
bound on the treewidth of the model's line graph), which in turn is bounded by
min(O(d * ell), O(n)) where ell is the minimum lateral dimension.

We:
  1. Build small random shallow circuits (Hadamards + T/sqrt(X)/sqrt(Y) singles
     + CZ nearest-neighbor two-qubit gates) on an ell x m 2D grid.
  2. Explicitly construct the tensor network of a single output amplitude
     <0...0|U|0...0>.
  3. Ask opt_einsum for a contraction path (greedy heuristic, similar in spirit
     to QuickBB used by the paper) and read off:
       - contraction_width  = log2(largest intermediate tensor size)
       - contraction_flops  = total FLOPs
     These are the tensor-network analogs of treewidth-based cost.
  4. Cross-check numerical value against a direct Schrodinger statevector
     simulation. They must match to ~1e-6.
  5. Sweep n and d, tabulate: statevector cost (2**n) vs TN contraction cost.

This is a real numeric simulation, not a mock.
"""

from __future__ import annotations

import json
import math
import time
from dataclasses import dataclass, field, asdict
from typing import List, Tuple

import numpy as np
import opt_einsum as oe


# ---------- Gate definitions ----------

H = (1.0 / math.sqrt(2.0)) * np.array([[1, 1], [1, -1]], dtype=np.complex128)
T = np.array([[1, 0], [0, np.exp(1j * math.pi / 4)]], dtype=np.complex128)
SX = 0.5 * np.array([[1 + 1j, 1 - 1j], [1 - 1j, 1 + 1j]], dtype=np.complex128)  # sqrt(X)
SY = 0.5 * np.array([[1 + 1j, -1 - 1j], [1 + 1j, 1 + 1j]], dtype=np.complex128)  # sqrt(Y)
I2 = np.eye(2, dtype=np.complex128)

# Controlled-Z as a rank-4 tensor. Convention (in1_a, in1_b, out1_a, out1_b)
# where the state amplitude convention below uses indices as
# tensor[in_a, in_b, out_a, out_b].
def cz_tensor() -> np.ndarray:
    t = np.zeros((2, 2, 2, 2), dtype=np.complex128)
    for a in range(2):
        for b in range(2):
            # CZ acts diagonally: flips sign if a==b==1
            phase = -1.0 if (a == 1 and b == 1) else 1.0
            t[a, b, a, b] = phase
    return t

CZ = cz_tensor()

# Single-qubit gate as rank-2 tensor gate[in, out].
SINGLE_GATES = {"T": T, "SX": SX, "SY": SY, "H": H}


# ---------- Circuit generation ----------

@dataclass
class Gate:
    """A gate in the circuit. Either single-qubit at (layer, qubit) or two-qubit
    CZ between two qubits at (layer, q1, q2)."""
    kind: str  # 'H', 'T', 'SX', 'SY', 'CZ'
    qubits: Tuple[int, ...]
    layer: int


def make_random_shallow_circuit(
    ell: int, m: int, depth: int, seed: int = 0
) -> Tuple[List[Gate], int]:
    """Build a random shallow circuit on an ell x m 2D grid, similar in
    structure to Boixo et al. 2017 (Google supremacy-style):
      - Layer 0: Hadamard on every qubit.
      - Layers 1..depth: alternate between:
          * random non-diagonal single-qubit gate from {T, SX, SY} on qubits
            that received a two-qubit gate in the previous layer;
          * a set of CZ gates on a chosen bond pattern (horizontal / vertical
            / two diagonals) that rotates each layer, chosen so no qubit is in
            two CZs of the same layer (planarity guaranteed by construction).
    We keep it structurally faithful to the paper (shallow 2D nearest-neighbor
    with CZs) but simplified for tractable small-instance simulation.

    Returns (gate_list, n_qubits).
    """
    rng = np.random.default_rng(seed)
    n = ell * m
    def qidx(r: int, c: int) -> int:
        return r * m + c

    gates: List[Gate] = []
    for q in range(n):
        gates.append(Gate("H", (q,), 0))

    # 4 bond patterns for CZs (h-even, h-odd, v-even, v-odd).
    def bonds_horiz(parity: int) -> List[Tuple[int, int]]:
        bs = []
        for r in range(ell):
            for c in range(parity, m - 1, 2):
                bs.append((qidx(r, c), qidx(r, c + 1)))
        return bs

    def bonds_vert(parity: int) -> List[Tuple[int, int]]:
        bs = []
        for c in range(m):
            for r in range(parity, ell - 1, 2):
                bs.append((qidx(r, c), qidx(r + 1, c)))
        return bs

    patterns = [bonds_horiz(0), bonds_horiz(1), bonds_vert(0), bonds_vert(1)]

    # Track which qubits got a two-qubit gate in the previous layer so we can
    # put a random single-qubit gate there next layer.
    prev_two = set(range(n))  # after Hadamards, apply single-qubit randoms next

    single_choices = ["T", "SX", "SY"]

    for L in range(1, depth + 1):
        # random single-qubit gate on qubits that had a CZ (or Hadamard) prev
        for q in sorted(prev_two):
            kind = single_choices[int(rng.integers(0, 3))]
            gates.append(Gate(kind, (q,), L))
        # CZ pattern for this layer
        pattern = patterns[(L - 1) % 4]
        touched = set()
        for (a, b) in pattern:
            gates.append(Gate("CZ", (a, b), L))
            touched.add(a); touched.add(b)
        prev_two = touched

    return gates, n


# ---------- Statevector simulation (ground truth) ----------

def statevector_amp_zero(gates: List[Gate], n: int) -> complex:
    """Apply full circuit to |0...0> and return <0...0| U |0...0>.
    Cost: O(2**n) memory, O(#gates * 2**n) time."""
    if n > 22:
        raise ValueError("Refusing statevector simulation for n > 22 (memory).")
    state = np.zeros(2 ** n, dtype=np.complex128)
    state[0] = 1.0

    def apply_single(state: np.ndarray, U: np.ndarray, q: int) -> np.ndarray:
        # Reshape state as (2,)*n, tensordot with U on axis q, then flatten.
        shape = (2,) * n
        s = state.reshape(shape)
        s = np.tensordot(U, s, axes=([1], [q]))
        # tensordot puts the new axis at position 0; move it back to q.
        s = np.moveaxis(s, 0, q)
        return s.reshape(2 ** n)

    def apply_cz(state: np.ndarray, q1: int, q2: int) -> np.ndarray:
        shape = (2,) * n
        s = state.reshape(shape).copy()
        # Diagonal in computational basis: flip sign iff both qubits are 1.
        # Use einsum-style indexing via explicit masking.
        idx = [slice(None)] * n
        idx[q1] = 1
        idx[q2] = 1
        s[tuple(idx)] *= -1.0
        return s.reshape(2 ** n)

    for g in gates:
        if g.kind == "CZ":
            state = apply_cz(state, g.qubits[0], g.qubits[1])
        else:
            state = apply_single(state, SINGLE_GATES[g.kind], g.qubits[0])
    return complex(state[0])


# ---------- Tensor network representation ----------

def build_tn_amp_zero(gates: List[Gate], n: int):
    """Build the tensor network for <0...0| U |0...0>. Return (tensors,
    index_lists, output_indices=[]). Each qubit's worldline is a chain of
    indices; each gate is a tensor connecting incoming/outgoing indices; the
    boundary tensors on both ends inject the |0> state.

    Convention:
      - We maintain, for each qubit q, its current 'wire index' name (a string).
      - Initial wire index for q is 'q{q}_0'.
      - For a single-qubit gate we create a new wire index 'q{q}_{k+1}' and add
        a rank-2 tensor with legs (old_wire, new_wire).
      - For a CZ we do the same for both qubits and add a rank-4 tensor with
        legs (old_q1, old_q2, new_q1, new_q2).
      - <0| on left is injected by a rank-1 tensor [1, 0] on the initial wire.
      - |0> on right is injected by a rank-1 tensor [1, 0] on the final wire.
    """
    wire = {q: f"q{q}_0" for q in range(n)}
    counter = {q: 0 for q in range(n)}
    tensors: List[np.ndarray] = []
    idx_lists: List[List[str]] = []

    # <0| on each qubit's initial wire.
    zero = np.array([1.0, 0.0], dtype=np.complex128)
    for q in range(n):
        tensors.append(zero)
        idx_lists.append([wire[q]])

    for g in gates:
        if g.kind == "CZ":
            q1, q2 = g.qubits
            counter[q1] += 1
            counter[q2] += 1
            new1 = f"q{q1}_{counter[q1]}"
            new2 = f"q{q2}_{counter[q2]}"
            tensors.append(CZ)
            # CZ tensor legs: (in_q1, in_q2, out_q1, out_q2)
            idx_lists.append([wire[q1], wire[q2], new1, new2])
            wire[q1] = new1
            wire[q2] = new2
        else:
            q = g.qubits[0]
            counter[q] += 1
            new = f"q{q}_{counter[q]}"
            # Standard numpy matrix U has shape [out, in]. To express the
            # tensor with legs (in_wire, out_wire) we store U.T so that
            # T[in, out] = U[out, in].
            tensors.append(SINGLE_GATES[g.kind].T.copy())
            idx_lists.append([wire[q], new])
            wire[q] = new

    # |0> on each qubit's final wire.
    for q in range(n):
        tensors.append(zero)
        idx_lists.append([wire[q]])

    return tensors, idx_lists


def tn_contract_amp_zero(tensors, idx_lists):
    """Contract the network to a scalar. Returns (value, path_info).
    Maps each string wire-index to a unique unicode symbol via
    opt_einsum.get_symbol so we can use the string-subscript einsum syntax
    (which supports arbitrarily many indices via unicode)."""
    name_to_sym = {}
    def sym(name: str) -> str:
        if name not in name_to_sym:
            name_to_sym[name] = oe.get_symbol(len(name_to_sym))
        return name_to_sym[name]

    subs = []
    for idx in idx_lists:
        subs.append("".join(sym(x) for x in idx))
    einsum_str = ",".join(subs) + "->"
    path, info = oe.contract_path(einsum_str, *tensors, optimize="greedy")
    val = oe.contract(einsum_str, *tensors, optimize=path)
    return complex(val), info, path


# ---------- Cost analysis ----------

def contraction_stats(info) -> dict:
    """Extract width/flops from an opt_einsum PathInfo."""
    # info.largest_intermediate is the size (element count) of the biggest
    # intermediate tensor across the whole path. Its log2 is the "contraction
    # width" (a well-known upper bound on the treewidth of the line graph of
    # the tensor network).
    lg = int(info.largest_intermediate)
    width = math.log2(lg) if lg > 0 else 0.0
    # Total FLOPs
    flops = float(info.opt_cost)
    return {
        "largest_intermediate": lg,
        "contraction_width_log2": width,
        "opt_cost_flops": flops,
    }


# ---------- Sweep ----------

@dataclass
class SweepPoint:
    ell: int
    m: int
    n: int
    depth: int
    seed: int
    tn_amp_real: float
    tn_amp_imag: float
    sv_amp_real: float
    sv_amp_imag: float
    max_abs_diff: float
    largest_intermediate: int
    contraction_width_log2: float
    opt_cost_flops: float
    n_tensors: int
    n_gates: int
    statevector_cost_2n: int
    tn_amp_time_s: float
    sv_amp_time_s: float


def run_point(ell: int, m: int, depth: int, seed: int = 0) -> SweepPoint:
    n = ell * m
    gates, n_check = make_random_shallow_circuit(ell, m, depth, seed=seed)
    assert n == n_check
    tensors, idx_lists = build_tn_amp_zero(gates, n)

    t0 = time.perf_counter()
    tn_val, info, path = tn_contract_amp_zero(tensors, idx_lists)
    tn_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    sv_val = statevector_amp_zero(gates, n)
    sv_time = time.perf_counter() - t0

    stats = contraction_stats(info)
    diff = abs(tn_val - sv_val)
    return SweepPoint(
        ell=ell, m=m, n=n, depth=depth, seed=seed,
        tn_amp_real=tn_val.real, tn_amp_imag=tn_val.imag,
        sv_amp_real=sv_val.real, sv_amp_imag=sv_val.imag,
        max_abs_diff=diff,
        largest_intermediate=stats["largest_intermediate"],
        contraction_width_log2=stats["contraction_width_log2"],
        opt_cost_flops=stats["opt_cost_flops"],
        n_tensors=len(tensors),
        n_gates=len(gates),
        statevector_cost_2n=2 ** n,
        tn_amp_time_s=tn_time,
        sv_amp_time_s=sv_time,
    )


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--configs", default="", help="ell,m,depth,seed;... override")
    args = ap.parse_args()

    if args.configs:
        configs = []
        for tok in args.configs.split(";"):
            e, m, d, s = tok.split(",")
            configs.append((int(e), int(m), int(d), int(s)))
    else:
        # Default sweep:
        # 1D chain (ell=1): treewidth should stay small even at deep depth.
        # 2xm: treewidth bounded by O(depth * 2).
        # 3xm, 4x4: treewidth grows with depth.
        configs = []
        # 1D chains
        for m in [8, 10, 12, 14, 16]:
            for d in [2, 3, 4, 5, 6]:
                configs.append((1, m, d, 7))
        # 2xN ladders
        for m in [4, 5, 6, 7, 8]:
            for d in [2, 3, 4, 5, 6]:
                configs.append((2, m, d, 7))
        # 3xN
        for m in [3, 4, 5]:
            for d in [2, 3, 4, 5, 6]:
                configs.append((3, m, d, 7))
        # 4x4
        for d in [2, 3, 4, 5, 6]:
            configs.append((4, 4, d, 7))

    results = []
    for i, (e, m, d, s) in enumerate(configs):
        n = e * m
        if n > 20:
            print(f"[skip] ell={e} m={m} n={n} > 20", flush=True)
            continue
        try:
            pt = run_point(e, m, d, s)
        except Exception as ex:
            print(f"[err ] ell={e} m={m} d={d}: {ex}", flush=True)
            continue
        results.append(asdict(pt))
        print(
            f"[{i+1:2d}/{len(configs)}] ell={e} m={m} n={n} d={d} "
            f"width={pt.contraction_width_log2:.2f} "
            f"flops={pt.opt_cost_flops:.2e} "
            f"|tn-sv|={pt.max_abs_diff:.2e} "
            f"tn={pt.tn_amp_time_s*1000:.1f}ms sv={pt.sv_amp_time_s*1000:.1f}ms",
            flush=True,
        )

    with open(args.out, "w") as f:
        json.dump({"results": results}, f, indent=2)
    print(f"wrote {args.out} ({len(results)} points)")


if __name__ == "__main__":
    main()
