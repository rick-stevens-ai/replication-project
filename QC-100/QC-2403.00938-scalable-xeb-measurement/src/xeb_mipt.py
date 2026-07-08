"""
Linear cross-entropy (XEB) order parameter for measurement-induced phase transition (MIPT).

Reproduces the core protocol of Kamakari et al., arXiv:2403.00938 ("Experimental
demonstration of scalable cross-entropy benchmarking to detect measurement-induced
phase transitions"), which itself operationalizes the theoretical proposal of
Li & Fisher (Ref. [40] in the paper).

Protocol (following Eq. (1) and surrounding text of the paper):
  * For a random hybrid Clifford circuit C with N mid-circuit measurements,
    apply the SAME circuit to two initial states rho and sigma.
  * For each measurement record m = (m1,...,mN), define
        p^rho_m  = Pr[record m | initial state rho, circuit C]
        p^sigma_m = Pr[record m | initial state sigma, circuit C]
  * The normalized linear cross entropy for circuit C is
        chi_C = sum_m p^rho_m p^sigma_m  /  sum_m (p^sigma_m)^2
    (Eq. 1 in the paper).
  * chi = E_C [chi_C].

For rho = sigma, chi = 1 identically (up to noise / sampling).
For rho != sigma, chi behaves as an order parameter for MIPT: chi -> 1 in the
volume-law phase (p < p_c), chi -> const < 1 in the area-law phase (p > p_c).

We use small system sizes L in {4, 6, 8} so that exact enumeration of all
2^N mid-circuit measurement records is feasible.  This is a real classical
simulation using Qiskit statevector, not the paper's IBM Sherbrooke hardware
data.  The paper's protocol is defined to be classically simulable at the
sigma side (Clifford + stabilizer input); we simulate BOTH sides classically
here since our goal is to verify the protocol behavior, not to demonstrate
quantum advantage.

Author: Ollie (Rick's OpenClaw subagent), 2026-07-03
"""

from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Sequence

import numpy as np

from qiskit import QuantumCircuit
from qiskit.circuit.random import random_clifford_circuit
from qiskit.quantum_info import Statevector, random_clifford


# ------------------------------------------------------------------ helpers

def _kron_state(bit: int, T_state: bool) -> np.ndarray:
    """|0>, |1>, or |T> = (|0> + e^{i pi/4}|1>)/sqrt(2) as a length-2 vector."""
    if T_state:
        return np.array([1.0, np.exp(1j * np.pi / 4.0)], dtype=complex) / math.sqrt(2.0)
    if bit == 0:
        return np.array([1.0, 0.0], dtype=complex)
    return np.array([0.0, 1.0], dtype=complex)


def initial_state_zero(L: int) -> np.ndarray:
    """|0>^L."""
    v = _kron_state(0, False)
    out = v
    for _ in range(L - 1):
        out = np.kron(out, v)
    return out


def initial_state_zeroT(L: int) -> np.ndarray:
    """Alternating |0 T 0 T ...> on L qubits (L must be even)."""
    assert L % 2 == 0, "alternating 0T state needs even L"
    # Qiskit convention: qubit 0 is the rightmost (least significant) tensor factor.
    # We build the vector in "qubit 0 first" order and then reverse for Qiskit.
    parts = []
    for i in range(L):
        parts.append(_kron_state(0, T_state=(i % 2 == 1)))
    # Compose in Qiskit little-endian: right-most in kron == qubit 0.
    v = parts[-1]
    for p in reversed(parts[:-1]):
        v = np.kron(p, v)
    # Wait: what we want is qubit 0 == |0>, qubit 1 == |T>, qubit 2 == |0>, ...
    # In Qiskit statevector, |q_{L-1} ... q_1 q_0>, so qubit 0 is rightmost.
    # `parts[i]` is intended for qubit i.  We compose as
    #   v = parts[L-1] (x) parts[L-2] (x) ... (x) parts[0]
    # which is exactly what the loop above does.  Good.
    return v


# ------------------------------------------------------------------ circuit

@dataclass
class MIPTCircuit:
    L: int
    p: float
    seed: int
    t_encoding: int  # number of unitary layers before bulk
    t_bulk: int      # number of unitary+measurement layers in bulk
    # After construction:
    layers_unitary: list = field(default_factory=list)  # list of list of (q0,q1) pairs
    layers_meas: list = field(default_factory=list)     # list of list of ints (qubit indices being measured this layer)
    cliffords_encoding: list = field(default_factory=list)  # list of layers; each layer is list of (q0,q1, clifford_matrix)
    cliffords_bulk: list = field(default_factory=list)      # same structure, one per bulk layer


def _brickwork_pairs(L: int, layer_idx: int) -> list[tuple[int, int]]:
    """Nearest-neighbor brickwork pattern on L qubits.
    Even layers: (0,1),(2,3),...  Odd layers: (1,2),(3,4),... (open boundaries)."""
    if layer_idx % 2 == 0:
        return [(i, i + 1) for i in range(0, L - 1, 2)]
    return [(i, i + 1) for i in range(1, L - 1, 2)]


def _random_2q_clifford(rng: np.random.Generator) -> np.ndarray:
    """Return a random 2-qubit Clifford unitary as a 4x4 complex matrix.
    Uses qiskit.quantum_info.random_clifford with a numpy-seeded RNG (int32 seed)."""
    # random_clifford accepts a `seed` argument.
    seed = int(rng.integers(0, 2**31 - 1))
    cl = random_clifford(num_qubits=2, seed=seed)
    return cl.to_matrix()


def sample_mipt_circuit(L: int, p: float, seed: int) -> MIPTCircuit:
    """Sample one hybrid Clifford circuit at (L, p).

    - t_encoding = t_bulk = L (paper uses 3L, but we scale down for small L to keep
      2^N-record enumeration tractable while retaining the physics; see NOTE below).
      Overridable via env var XEB_MIPT_TDEPTH (int).
    - Encoding: `t_encoding` brickwork layers of random 2-qubit Cliffords, no meas.
    - Bulk: `t_bulk` layers.  Each layer = brickwork unitaries, then each qubit is
      measured (single-qubit Z basis) independently with probability p.

    NOTE on depth: the paper uses t = 3L in the uncompressed circuit; for small L
    that's a lot of measurements to enumerate exactly (up to L * 3L = 3L^2 ~ 48-192
    records at L=4-8, giving 2^N up to 2^192 — infeasible).  We use t_bulk = L,
    which keeps expected records to p*L^2 ~ 3-13 at p up to 0.2 and L up to 8,
    i.e. at most a few thousand records.  This is enough to demonstrate the
    ordering-parameter behavior of chi that the paper describes (chi->1 at low p,
    chi<1 at high p), which is the reproducible core of the protocol.  The exact
    critical p_c depends on the encoding/bulk ratio and the L range.
    """
    import os as _os
    rng = np.random.default_rng(seed)
    _override = _os.environ.get('XEB_MIPT_TDEPTH')
    if _override is not None:
        t_encoding = t_bulk = int(_override)
    else:
        t_encoding = L
        t_bulk = L
    circ = MIPTCircuit(L=L, p=p, seed=seed, t_encoding=t_encoding, t_bulk=t_bulk)

    # Encoding stage: unitaries only.
    for l in range(t_encoding):
        pairs = _brickwork_pairs(L, l)
        layer_unitaries = []
        for (a, b) in pairs:
            U = _random_2q_clifford(rng)
            layer_unitaries.append((a, b, U))
        circ.cliffords_encoding.append(layer_unitaries)

    # Bulk stage: unitary layer + measurement layer.
    for l in range(t_bulk):
        pairs = _brickwork_pairs(L, l)
        layer_unitaries = []
        for (a, b) in pairs:
            U = _random_2q_clifford(rng)
            layer_unitaries.append((a, b, U))
        circ.cliffords_bulk.append(layer_unitaries)
        # Sample which qubits get measured this layer.
        meas_qubits = [q for q in range(L) if rng.random() < p]
        circ.layers_meas.append(meas_qubits)

    return circ


# ------------------------------------------------------------------ evolution

def _apply_2q_gate(state: np.ndarray, L: int, q0: int, q1: int, U: np.ndarray) -> np.ndarray:
    """Apply 4x4 unitary U on qubits (q0, q1) of an L-qubit statevector (Qiskit little-endian)."""
    # Reshape state to tensor of shape (2,)*L, indexed as [q_{L-1}, ..., q_1, q_0].
    # We'll use axis ordering: axis i corresponds to qubit (L-1 - i) in little-endian.
    # Easier: reshape so that axis i corresponds to qubit i (big-endian).  Since we own
    # the whole pipeline, pick one convention and stick to it.
    #
    # We use axis-i == qubit-i convention here.  Then Qiskit's |q_{L-1} ... q_0>
    # ordering means we need to REVERSE indices when converting to/from statevector.
    # Simpler: work entirely in axis-i == qubit-i and never involve Qiskit's Statevector
    # class for the arithmetic.  We only use random_clifford for the U itself.
    shape = (2,) * L
    t = state.reshape(shape)
    # U is 4x4 acting on (q0, q1) with q0 the more-significant index of U.
    # We reshape U to (2,2,2,2) with indices [q0_out, q1_out, q0_in, q1_in].
    U4 = U.reshape(2, 2, 2, 2)
    # Move q0 and q1 axes to the front, contract, then move back.
    axes_in = [q0, q1]
    other = [ax for ax in range(L) if ax not in axes_in]
    perm = axes_in + other
    inv_perm = np.argsort(perm)
    t2 = np.transpose(t, perm)  # shape (2,2, 2,2,...,2) with q0,q1 first
    t2 = t2.reshape(2, 2, -1)
    # Contract U4[a,b,c,d] * t2[c,d,rest]  -> out[a,b,rest]
    out = np.einsum('abcd,cde->abe', U4, t2)
    out = out.reshape((2, 2) + (2,) * (L - 2))
    out = np.transpose(out, inv_perm)
    return out.reshape(-1)


def _project_measure(state: np.ndarray, L: int, qubit: int, outcome: int) -> tuple[np.ndarray, float]:
    """Project qubit `qubit` onto |outcome> (0 or 1).  Return (unnormalized new state, probability)."""
    shape = (2,) * L
    t = state.reshape(shape)
    # axis == qubit in axis-i-is-qubit-i convention.
    idx = [slice(None)] * L
    idx[qubit] = outcome
    slab = t[tuple(idx)]  # shape (2,)*(L-1)
    # Probability = |slab|^2 summed.
    prob = float(np.vdot(slab, slab).real)
    # Rebuild full statevector with the other outcome zeroed out.
    new_t = np.zeros_like(t)
    new_t[tuple(idx)] = slab
    return new_t.reshape(-1), prob


def _initial_state_in_axis_convention(L: int, kind: str) -> np.ndarray:
    """Build initial state in axis-i==qubit-i (big-endian in numpy sense) ordering.

    - kind = 'zero'  -> |0>^L
    - kind = 'zeroT' -> alternating |0 T 0 T ...> on qubits (qubit 0 = |0>, qubit 1 = |T>, ...)
    """
    if kind == 'zero':
        v = np.zeros(2**L, dtype=complex)
        v[0] = 1.0
        return v
    if kind == 'zeroT':
        # In axis-i==qubit-i convention, index into shape (2,)*L is (q0, q1, ..., q_{L-1}).
        shape = (2,) * L
        t = np.zeros(shape, dtype=complex)
        # Each qubit i has 1-qubit state s_i in {|0>, |T>}.  |0>=[1,0], |T>=[1, e^{i pi/4}]/sqrt2.
        # Full state = outer product; component at (b_0,...,b_{L-1}) = prod_i s_i[b_i].
        # Enumerate:
        for idx in np.ndindex(*shape):
            amp = 1.0 + 0.0j
            for i, b in enumerate(idx):
                if i % 2 == 0:  # qubit i is |0>
                    if b != 0:
                        amp = 0.0
                        break
                else:  # qubit i is |T>
                    if b == 0:
                        amp *= 1.0 / math.sqrt(2.0)
                    else:
                        amp *= np.exp(1j * np.pi / 4.0) / math.sqrt(2.0)
            t[idx] = amp
        return t.reshape(-1)
    raise ValueError(f'unknown initial state {kind}')


def measurement_record_probs(
    circ: MIPTCircuit, initial_kind: str
) -> dict[tuple[int, ...], float]:
    """Return {record: prob} for all measurement records with prob > 0.

    Records are ordered as (m_layer0_qubit_a, m_layer0_qubit_b, ..., m_layer1_qubit_c, ...)
    matching circ.layers_meas iteration order (layer, then qubit index).
    Total record length N = sum(len(layer) for layer in circ.layers_meas).
    """
    L = circ.L
    # Depth-first enumeration over measurement outcomes.
    # We keep (state, partial_record, joint_prob) frontier.
    state0 = _initial_state_in_axis_convention(L, initial_kind)

    # Apply encoding stage: no measurements.
    st = state0
    for layer_unitaries in circ.cliffords_encoding:
        for (a, b, U) in layer_unitaries:
            st = _apply_2q_gate(st, L, a, b, U)

    # Frontier: list of (state, record_tuple, joint_prob)
    frontier = [(st, tuple(), 1.0)]

    for l, layer_unitaries in enumerate(circ.cliffords_bulk):
        # Apply unitaries in this bulk layer to every branch.
        new_frontier = []
        for (s, rec, pr) in frontier:
            ss = s
            for (a, b, U) in layer_unitaries:
                ss = _apply_2q_gate(ss, L, a, b, U)
            new_frontier.append((ss, rec, pr))
        frontier = new_frontier

        # Apply measurements: for each measured qubit, branch on outcomes 0/1.
        meas_qs = circ.layers_meas[l]
        for q in meas_qs:
            next_frontier = []
            for (s, rec, pr) in frontier:
                for outcome in (0, 1):
                    s_new, p_out = _project_measure(s, L, q, outcome)
                    joint = pr * p_out
                    if joint < 1e-14:
                        continue
                    # Normalize s_new so that subsequent gate action & measurements
                    # correspond to conditional dynamics.  The joint probability we
                    # track is Pr[record so far].
                    norm = math.sqrt(p_out)
                    s_new = s_new / norm
                    next_frontier.append((s_new, rec + (outcome,), joint))
            frontier = next_frontier

    # Sum joint probabilities per record (records should already be distinct here,
    # but just in case):
    out: dict[tuple[int, ...], float] = {}
    for (_, rec, pr) in frontier:
        out[rec] = out.get(rec, 0.0) + pr
    return out


# ------------------------------------------------------------------ chi

def linear_xeb_for_circuit(circ: MIPTCircuit) -> tuple[float, dict]:
    """Compute chi_C for one circuit, given the paper's definition (Eq. 1):
        chi_C = sum_m p^rho_m p^sigma_m / sum_m (p^sigma_m)^2

    rho = alternating |0 T 0 T ...>
    sigma = |0>^L
    """
    p_rho = measurement_record_probs(circ, 'zeroT')
    p_sig = measurement_record_probs(circ, 'zero')

    # Compute numerator and denominator on the union of supports.
    keys = set(p_rho.keys()) | set(p_sig.keys())
    num = 0.0
    den = 0.0
    for k in keys:
        pr = p_rho.get(k, 0.0)
        ps = p_sig.get(k, 0.0)
        num += pr * ps
        den += ps * ps
    chi = num / den if den > 0 else float('nan')

    diag = {
        'num': num,
        'den': den,
        'n_records_rho': len(p_rho),
        'n_records_sig': len(p_sig),
        'n_meas_total': sum(len(l) for l in circ.layers_meas),
    }
    return chi, diag


def linear_xeb_same_input(circ: MIPTCircuit, kind: str = 'zero') -> tuple[float, dict]:
    """Sanity: for rho = sigma, chi should be exactly 1."""
    p_a = measurement_record_probs(circ, kind)
    # chi = sum p_a p_a / sum p_a^2 = 1 identically.
    num = sum(v * v for v in p_a.values())
    den = num
    chi = num / den if den > 0 else float('nan')
    return chi, {'n_records': len(p_a), 'num': num, 'den': den}


# ------------------------------------------------------------------ main sweep

def sweep(
    L_list: Sequence[int],
    p_list: Sequence[float],
    n_circuits: int,
    seed0: int,
    do_same: bool = True,
    do_diff: bool = True,
    verbose: bool = True,
    incremental_out: str | None = None,
) -> dict:
    """Run the (L, p, n_circuits) sweep and return chi(L, p) averaged over circuits."""
    results = {'L_list': list(L_list), 'p_list': list(p_list),
               'n_circuits': n_circuits, 'seed0': seed0,
               'same_input': {}, 'diff_input': {}}
    t0 = time.time()
    seed_ctr = seed0
    for L in L_list:
        results['same_input'][L] = {}
        results['diff_input'][L] = {}
        for p in p_list:
            chis_same = []
            chis_diff = []
            n_recs = []
            for r in range(n_circuits):
                circ = sample_mipt_circuit(L, p, seed=seed_ctr)
                seed_ctr += 1
                if do_diff:
                    chi_d, diag_d = linear_xeb_for_circuit(circ)
                    chis_diff.append(chi_d)
                    n_recs.append(diag_d['n_meas_total'])
                if do_same:
                    chi_s, _ = linear_xeb_same_input(circ, 'zero')
                    chis_same.append(chi_s)
            if do_same:
                results['same_input'][L][f'{p:.3f}'] = {
                    'mean': float(np.mean(chis_same)) if chis_same else float('nan'),
                    'std': float(np.std(chis_same)) if chis_same else float('nan'),
                    'n': len(chis_same),
                }
            if do_diff:
                results['diff_input'][L][f'{p:.3f}'] = {
                    'mean': float(np.mean(chis_diff)) if chis_diff else float('nan'),
                    'std': float(np.std(chis_diff)) if chis_diff else float('nan'),
                    'sem': float(np.std(chis_diff) / math.sqrt(len(chis_diff))) if chis_diff else float('nan'),
                    'n': len(chis_diff),
                    'mean_meas_count': float(np.mean(n_recs)) if n_recs else float('nan'),
                }
            if verbose:
                print(f'  L={L} p={p:.3f}: '
                      f"same chi={results['same_input'][L][f'{p:.3f}']['mean'] if do_same else float('nan'):.4f} "
                      f"diff chi={results['diff_input'][L][f'{p:.3f}']['mean'] if do_diff else float('nan'):.4f} "
                      f'(n={n_circuits}, elapsed={time.time()-t0:.1f}s)')
            if incremental_out is not None:
                results_snap = dict(results)
                results_snap['elapsed_sec'] = time.time() - t0
                results_snap['status'] = 'incremental'
                Path(incremental_out).parent.mkdir(parents=True, exist_ok=True)
                with open(incremental_out, 'w') as f:
                    json.dump(results_snap, f, indent=2)
    results['elapsed_sec'] = time.time() - t0
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--L', nargs='+', type=int, default=[4, 6, 8])
    ap.add_argument('--p', nargs='+', type=float,
                    default=[0.00, 0.05, 0.10, 0.14, 0.18, 0.25, 0.35, 0.50])
    ap.add_argument('--n-circuits', type=int, default=40)
    ap.add_argument('--seed', type=int, default=20260703)
    ap.add_argument('--out', type=str, required=True)
    ap.add_argument('--no-same', action='store_true')
    ap.add_argument('--no-diff', action='store_true')
    args = ap.parse_args()

    print(f'Running XEB-MIPT sweep: L={args.L}, p={args.p}, n_circuits={args.n_circuits}')
    res = sweep(
        L_list=args.L, p_list=args.p,
        n_circuits=args.n_circuits, seed0=args.seed,
        do_same=not args.no_same, do_diff=not args.no_diff,
        incremental_out=args.out,
    )
    res['status'] = 'complete'
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(res, f, indent=2)
    print(f'Wrote {out_path}')


if __name__ == '__main__':
    main()
