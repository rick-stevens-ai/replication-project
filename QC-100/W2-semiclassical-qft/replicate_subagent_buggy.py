"""
Replication: Griffiths & Niu (1996), "Semiclassical Fourier Transform for Quantum
Computation" — applied to k-bit phase estimation of a 1-qubit phase gate.

Two equivalent implementations on an exact numpy statevector:

  (A) Standard QFT-based phase estimation: k ancillas + inverse QFT (with
      controlled-phase 2-qubit gates) + measurement of the k ancillas.
  (B) Semiclassical (Griffiths–Niu) phase estimation: ancillas measured one at
      a time (most-significant first); the next ancilla's pre-Hadamard gate is
      a *classical* Z-phase computed from previously-measured bits.  No 2-qubit
      gates among ancillas.  This is the textbook MSB-first version of
      Fig. 2 / eqs. (10)–(11) of the paper, specialized to phase estimation:
      the inverse-QFT-with-controlled-rotations is collapsed into measure +
      classically-conditioned single-qubit rotation, exactly as Griffiths–Niu
      collapse Fig. 1 → Fig. 2.

Verification: for a 1-qubit eigenstate |1> of U = diag(1, e^{2πiφ}), both methods
produce identical readout-integer distributions (up to machine precision) and
identical phase estimates.  This is the algorithm-equivalence claim of the
paper.

Run: `python replicate.py`  →  writes results.json next to this file.
"""

from __future__ import annotations

import json
import math
import os
import time
from collections import Counter
from typing import Dict, List, Tuple

import numpy as np

# ---------------------------------------------------------------------------
# Single-qubit + statevector helpers (little-endian: qubit 0 = LSB of index).
# ---------------------------------------------------------------------------

I2 = np.eye(2, dtype=complex)
H = (1.0 / math.sqrt(2.0)) * np.array([[1, 1], [1, -1]], dtype=complex)


def kron_list(ops: List[np.ndarray]) -> np.ndarray:
    out = ops[0]
    for op in ops[1:]:
        out = np.kron(out, op)
    return out


def apply_1q(state: np.ndarray, gate: np.ndarray, qubit: int, n: int) -> np.ndarray:
    """Apply a single-qubit gate to `qubit` of an n-qubit state (qubit 0 = LSB)."""
    ops = [I2] * n
    ops[n - 1 - qubit] = gate
    return kron_list(ops) @ state


def apply_controlled_phase(state: np.ndarray, control: int, target: int,
                            phase: float, n: int) -> np.ndarray:
    """Diagonal controlled-phase gate: |1>_c |1>_t picks up e^{i*phase}."""
    dim = 1 << n
    diag = np.ones(dim, dtype=complex)
    cbit = 1 << control
    tbit = 1 << target
    ph = np.exp(1j * phase)
    for k in range(dim):
        if (k & cbit) and (k & tbit):
            diag[k] = ph
    return diag * state


def swap_qubits(state: np.ndarray, a: int, b: int, n: int) -> np.ndarray:
    if a == b:
        return state
    dim = 1 << n
    new = np.empty_like(state)
    abit = 1 << a
    bbit = 1 << b
    for idx in range(dim):
        ai = (idx >> a) & 1
        bi = (idx >> b) & 1
        if ai == bi:
            new[idx] = state[idx]
        else:
            new[idx] = state[idx ^ abit ^ bbit]
    return new


def measure_qubit(state: np.ndarray, qubit: int, n: int,
                   rng: np.random.Generator) -> Tuple[int, np.ndarray]:
    """Sample a Z-basis measurement of `qubit`; return (bit, collapsed state)."""
    dim = 1 << n
    qbit = 1 << qubit
    p1 = 0.0
    for k in range(dim):
        if k & qbit:
            p1 += (state[k].conjugate() * state[k]).real
    bit = 1 if rng.random() < p1 else 0
    new = state.copy()
    for k in range(dim):
        has = bool(k & qbit)
        keep = (has and bit == 1) or ((not has) and bit == 0)
        if not keep:
            new[k] = 0.0
    norm = np.linalg.norm(new)
    if norm == 0.0:
        raise RuntimeError("zero-norm post-measurement state")
    new /= norm
    return bit, new


def _qubit_marginal(state: np.ndarray, qubit: int, n: int, outcome: int) -> float:
    dim = 1 << n
    qbit = 1 << qubit
    p = 0.0
    for k in range(dim):
        has = bool(k & qbit)
        if (has and outcome == 1) or ((not has) and outcome == 0):
            p += (state[k].conjugate() * state[k]).real
    return p


def _collapse(state: np.ndarray, qubit: int, n: int, outcome: int,
              p: float) -> np.ndarray:
    dim = 1 << n
    qbit = 1 << qubit
    new = state.copy()
    for k in range(dim):
        has = bool(k & qbit)
        keep = (has and outcome == 1) or ((not has) and outcome == 0)
        if not keep:
            new[k] = 0.0
    new /= math.sqrt(p)
    return new


# ---------------------------------------------------------------------------
# Phase estimation building blocks.
#
# Layout (n = k + 1 qubits):
#   qubits 0..k-1 = ancillas;  controlled-U^{2^j} applied with ancilla j as
#   control and the eigenstate register as target.
#   qubit k = work (eigenstate) qubit prepared in |1> ↔ eigenvalue e^{2πiφ}.
#
# Readout integer convention (matches Nielsen & Chuang for both methods):
#   y = sum_{j=0..k-1} y_j * 2^j   where y_j is the measured bit on ancilla j.
#   The phase estimate is φ_est = y / 2^k.
# ---------------------------------------------------------------------------


def prepare_initial_state(k: int) -> np.ndarray:
    """k ancillas in |0>, work qubit (index k) in |1>; Hadamard all ancillas."""
    n = k + 1
    dim = 1 << n
    state = np.zeros(dim, dtype=complex)
    state[1 << k] = 1.0  # work qubit = 1, all ancillas = 0
    for q in range(k):
        state = apply_1q(state, H, q, n)
    return state


def apply_controlled_U_powers(state: np.ndarray, k: int, phi: float) -> np.ndarray:
    """Apply controlled-U^{2^j} for j=0..k-1 (ancilla j = control, work = target).
    Because work qubit is in |1> eigenstate of U, this is diagonal in the basis:
    basis states with ancilla_j = 1 AND work = 1 pick up e^{2πiφ·2^j}.
    """
    n = k + 1
    dim = 1 << n
    wbit = 1 << k
    diag = np.ones(dim, dtype=complex)
    for j in range(k):
        abit = 1 << j
        ph = np.exp(1j * 2.0 * math.pi * phi * (1 << j))
        for idx in range(dim):
            if (idx & abit) and (idx & wbit):
                diag[idx] *= ph
    return diag * state


# ---------------------------------------------------------------------------
# (A) Standard inverse-QFT phase estimation.
# Inverse QFT (Nielsen & Chuang eq. 5.4 inverted) on ancillas 0..k-1, with the
# convention that after the QFT/iQFT the bit value of qubit j is y_j (the
# j-th bit of the readout integer y = sum y_j 2^j).
#
# Implementation: apply the dagger of the standard QFT circuit:
#   1. SWAP layer (qubit i ↔ qubit k-1-i) — same as forward QFT.
#   2. For j = k-1, k-2, ..., 0:
#        for m = k-1, ..., j+1:
#            controlled-phase(control = qubit m, target = qubit j),
#                phase = -π / 2^(m-j)
#        H on qubit j.
# (This is the dagger of: H on qubit j, then CR_2..CR_{k-j} from above qubits.)
# ---------------------------------------------------------------------------


def apply_inverse_qft(state: np.ndarray, n: int, k: int) -> np.ndarray:
    # 1) swap layer
    for i in range(k // 2):
        state = swap_qubits(state, i, k - 1 - i, n)
    # 2) gate layer (dagger of forward QFT)
    for j in range(k - 1, -1, -1):
        for m in range(k - 1, j, -1):
            phase = -math.pi / (1 << (m - j))
            state = apply_controlled_phase(state, m, j, phase, n)
        state = apply_1q(state, H, j, n)
    return state


def run_qft_phase_estimation(phi: float, k: int, shots: int,
                              rng: np.random.Generator) -> Dict:
    n = k + 1
    state = prepare_initial_state(k)
    state = apply_controlled_U_powers(state, k, phi)
    state = apply_inverse_qft(state, n, k)

    # Marginal probability over ancilla bit-pattern (sum over work qubit).
    dim = 1 << n
    wbit = 1 << k
    y_probs = np.zeros(1 << k, dtype=float)
    for idx in range(dim):
        anc = idx & (wbit - 1)  # low k bits hold the ancillas (little-endian)
        y_probs[anc] += (state[idx].conjugate() * state[idx]).real
    y_probs /= y_probs.sum()

    counts: Counter = Counter()
    for _ in range(shots):
        y = int(rng.choice(1 << k, p=y_probs))
        counts[y] += 1

    mode_y = int(np.argmax(y_probs))
    return {
        "exact_y_probs": y_probs.tolist(),
        "shot_counts": dict(counts),
        "mode_y": mode_y,
        "phi_estimate_mode": mode_y / (1 << k),
    }


# ---------------------------------------------------------------------------
# (B) Semiclassical (Griffiths–Niu) phase estimation.
#
# MSB-first measurement order: t = 0..k-1 measures ancilla j = k-1-t.
# Before measuring ancilla j we apply
#    R_z(theta_j)   then   H
# where theta_j is the classical phase fed forward from already-measured bits:
#
#    theta_j = - 2*pi * sum_{l=j+1}^{k-1}  b_l / 2^(l - j + 1)
#
# This is precisely the conjugate of the controlled-phase corrections inside
# the inverse QFT: between ancillas l and j (l>j), the iQFT applies a
# controlled-phase with angle -2π / 2^(l-j+1) when control = 1; once b_l is
# measured the unitary collapses to a classical Z-phase on ancilla j of that
# angle, which is what the formula above accumulates.
#
# This is the MSB-first form of Griffiths–Niu's eq. (11) recursion
# φ' = φ/2 + c/4 applied iteratively along the ancilla line.  No 2-qubit
# gate on ancillas is ever applied; only single-qubit gates on the ancillas
# (the controlled-U^{2^j} acts only between an ancilla and the eigenstate
# register, and is the same in both methods).
# ---------------------------------------------------------------------------


def Rz(angle: float) -> np.ndarray:
    """diag(1, e^{i*angle}) — applies the phase to the |1> component."""
    return np.array([[1.0, 0.0], [0.0, np.exp(1j * angle)]], dtype=complex)


def _feed_forward_theta(j: int, bits_by_j: Dict[int, int], k: int) -> float:
    theta = 0.0
    for l in range(j + 1, k):
        if bits_by_j.get(l, 0):
            theta += -2.0 * math.pi / (1 << (l - j + 1))
    return theta


def run_semiclassical_phase_estimation(phi: float, k: int, shots: int,
                                        rng: np.random.Generator) -> Dict:
    n = k + 1
    base = prepare_initial_state(k)
    base = apply_controlled_U_powers(base, k, phi)

    # Exact distribution over readout integer y = sum_j y_j * 2^j by
    # enumerating the measurement tree.
    exact_y_probs = np.zeros(1 << k, dtype=float)

    def recurse(state: np.ndarray, t: int, bits_by_j: Dict[int, int],
                prob_so_far: float) -> None:
        if t == k:
            y = 0
            for jj in range(k):
                y |= bits_by_j[jj] << jj
            exact_y_probs[y] += prob_so_far
            return
        j = k - 1 - t
        theta = _feed_forward_theta(j, bits_by_j, k)
        s = apply_1q(state, Rz(theta), j, n)
        s = apply_1q(s, H, j, n)
        for outcome in (0, 1):
            p = _qubit_marginal(s, j, n, outcome)
            if p < 1e-15:
                continue
            sc = _collapse(s, j, n, outcome, p)
            new_bits = dict(bits_by_j)
            new_bits[j] = outcome
            recurse(sc, t + 1, new_bits, prob_so_far * p)

    recurse(base, 0, {}, 1.0)

    # MC samples
    counts: Counter = Counter()
    for _ in range(shots):
        s = base.copy()
        bits_by_j: Dict[int, int] = {}
        for t in range(k):
            j = k - 1 - t
            theta = _feed_forward_theta(j, bits_by_j, k)
            s = apply_1q(s, Rz(theta), j, n)
            s = apply_1q(s, H, j, n)
            bit, s = measure_qubit(s, j, n, rng)
            bits_by_j[j] = bit
        y = 0
        for jj in range(k):
            y |= bits_by_j[jj] << jj
        counts[y] += 1

    mode_y = int(np.argmax(exact_y_probs))
    return {
        "exact_y_probs": exact_y_probs.tolist(),
        "shot_counts": dict(counts),
        "mode_y": mode_y,
        "phi_estimate_mode": mode_y / (1 << k),
    }


# ---------------------------------------------------------------------------
# Experiment harness.
# ---------------------------------------------------------------------------


def total_variation(p: np.ndarray, q: np.ndarray) -> float:
    return 0.5 * float(np.sum(np.abs(p - q)))


def _topk(p: np.ndarray, k: int) -> List[Tuple[int, float]]:
    idx = np.argsort(-p)[:k]
    return [(int(i), float(p[i])) for i in idx]


def run_experiment(phi: float, k: int, shots: int) -> Dict:
    seed = (int(1e7 * (phi % 1.0)) * 1000 + k) & 0xFFFFFFFF
    rng_a = np.random.default_rng(seed)
    rng_b = np.random.default_rng(seed + 1)
    t0 = time.time()
    a = run_qft_phase_estimation(phi, k, shots, rng_a)
    t1 = time.time()
    b = run_semiclassical_phase_estimation(phi, k, shots, rng_b)
    t2 = time.time()

    pa = np.array(a["exact_y_probs"]); pa /= pa.sum()
    pb = np.array(b["exact_y_probs"]); pb /= pb.sum()
    tv_exact = total_variation(pa, pb)
    max_abs = float(np.max(np.abs(pa - pb)))

    def counts_to_dist(c: Dict[int, int], dim: int) -> np.ndarray:
        d = np.zeros(dim, dtype=float)
        for ky, v in c.items():
            d[int(ky)] = v
        if d.sum() > 0:
            d /= d.sum()
        return d

    dim_y = 1 << k
    da = counts_to_dist(a["shot_counts"], dim_y)
    db = counts_to_dist(b["shot_counts"], dim_y)
    tv_emp = total_variation(da, db)

    return {
        "phi_true": phi,
        "k": k,
        "shots": shots,
        "qft": {
            "mode_y": a["mode_y"],
            "phi_estimate_mode": a["phi_estimate_mode"],
            "top3": _topk(pa, 3),
            "time_sec": round(t1 - t0, 4),
        },
        "semiclassical": {
            "mode_y": b["mode_y"],
            "phi_estimate_mode": b["phi_estimate_mode"],
            "top3": _topk(pb, 3),
            "time_sec": round(t2 - t1, 4),
        },
        "agreement": {
            "tv_exact_distributions": tv_exact,
            "max_abs_prob_diff_exact": max_abs,
            "tv_empirical_distributions": tv_emp,
            "mode_phi_match": (a["phi_estimate_mode"] == b["phi_estimate_mode"]),
            "abs_phi_error_qft": abs(a["phi_estimate_mode"] - phi),
            "abs_phi_error_semicl": abs(b["phi_estimate_mode"] - phi),
        },
    }


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(here, "results.json")

    experiments: List[Dict] = []

    # (i) Exactly representable phases (phi = y_true / 2^k).  Both methods must
    # give the SAME single-bin distribution centered on y_true with prob ≈ 1.
    cases_exact = [
        (3, 0.375),     # 3/8
        (4, 0.0625),    # 1/16
        (4, 0.8125),    # 13/16
        (5, 0.46875),   # 15/32
        (6, 0.703125),  # 45/64
    ]
    for k, phi in cases_exact:
        experiments.append(run_experiment(phi, k, shots=2000))

    # (ii) Non-representable phases.  PE produces a sinc²-like distribution
    # centered near the nearest y/2^k; both methods must give IDENTICAL exact
    # distributions (and statistically-equivalent empirical ones).
    cases_irr = [
        (3, 1.0 / 3.0),
        (4, math.sqrt(2.0) - 1.0),  # ≈ 0.4142
        (5, 1.0 / math.pi),         # ≈ 0.3183
        (6, math.e - 2.0),          # ≈ 0.7183
    ]
    for k, phi in cases_irr:
        experiments.append(run_experiment(phi, k, shots=4000))

    # Aggregate statistics
    tv_exact = [e["agreement"]["tv_exact_distributions"] for e in experiments]
    tv_emp = [e["agreement"]["tv_empirical_distributions"] for e in experiments]
    mode_matches = [e["agreement"]["mode_phi_match"] for e in experiments]

    summary = {
        "n_experiments": len(experiments),
        "max_tv_exact": max(tv_exact),
        "mean_tv_exact": sum(tv_exact) / len(tv_exact),
        "max_tv_empirical": max(tv_emp),
        "mean_tv_empirical": sum(tv_emp) / len(tv_emp),
        "mode_phi_match_all": all(mode_matches),
        "mode_phi_match_count": sum(mode_matches),
        "verdict_numeric": (
            "REPLICATED" if (max(tv_exact) < 1e-10 and all(mode_matches))
            else "DISAGREEMENT"
        ),
    }

    payload = {
        "paper": "Griffiths & Niu, Semiclassical Fourier Transform for Quantum Computation (1996)",
        "task": ("k-bit phase estimation of a 1-qubit phase gate; compare "
                 "standard inverse-QFT-based PE vs Griffiths–Niu semiclassical "
                 "(measure + classically-conditioned single-qubit rotation) PE."),
        "numpy_version": np.__version__,
        "rng_seed_note": "per-experiment seed = (1e7*phi*1000 + k); two independent draws per experiment.",
        "summary": summary,
        "experiments": experiments,
    }

    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"[ok] wrote {out_path}")
    print(f"[summary] verdict_numeric = {summary['verdict_numeric']}")
    print(f"[summary] max TV (exact distributions) over {len(experiments)} cases = {summary['max_tv_exact']:.3e}")
    print(f"[summary] mode-φ matches: {summary['mode_phi_match_count']}/{summary['n_experiments']}")


if __name__ == "__main__":
    main()
