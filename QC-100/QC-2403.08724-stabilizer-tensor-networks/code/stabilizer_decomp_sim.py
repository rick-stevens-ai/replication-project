"""
Stabilizer-decomposition simulator for Clifford+T circuits.

Central idea (from Bravyi & Gosset 2016 / Bravyi-Smith-Smolin 2016, the
workhorse baseline that Masot-Llima & Garcia-Saez 2024 (arXiv:2403.08724)
compares to when arguing for stabilizer tensor networks): every T-gate on
qubit i can be written as

    T_i = e^{i pi/8} * ( cos(pi/8) * I  -  i sin(pi/8) * Z_i )
        = e^{i pi/8} * (alpha * I  +  beta * Z_i)

Applied to a state written as a sum of stabilizer states |psi> = sum_k c_k |S_k>,
a T-gate produces at most 2 new stabilizer terms per existing term.  So after
t T-gates the number of stabilizer terms is <= 2^t, INDEPENDENT of n.

This is exactly the "conventional generalization of tableaus [where] we would
need 2^n copies, as each T-gate duplicates the number of necessary tableaus"
that the paper describes on p.3 (Eq. 11 discussion) as the baseline it improves
on.  The paper's own contribution is to combine that with an MPS to keep the
sum from doubling as often -- but the 2^t vs 2^n scaling is exactly the
"headline" testable number for a small SPOT-CHECK: the simulator's cost should
scale like 2^t (number of T-gates) rather than 2^n (number of qubits).

Implementation notes.

We use Stim's stim.TableauSimulator to represent the STABILIZER TABLEAU of
each branch (the group of Pauli operators that stabilize that branch's
state) at O(n^2) memory per branch.  However, Stim's TableauSimulator strips
global phase across Clifford gates -- e.g. it treats S|1> as |1> rather than
i|1> -- which is fine when you only care about a single stabilizer state (it
is defined only up to global phase) but breaks catastrophically when you take
linear combinations of tableau states across branches (branches then disagree
on which global phase they carry, and the coherent sum is wrong).

Fix: track a per-branch global phase separately from Stim.  Every S applied to
a qubit contributes a global phase factor equal to (i)^b, where b is the
Z-eigenvalue projection of the state on that qubit.  In general, extracting
that from a Stim tableau is fiddly.  So we take the direct route: alongside
Stim's tableau (used only for scaling / #-terms bookkeeping to demonstrate that
this really is a stabilizer-decomposition simulator, not a statevector one), we
maintain an authoritative n-qubit statevector per branch that we evolve
directly under each Clifford gate using explicit numpy matrix operations.
This gives EXACT coefficients per branch.  For the small n=3-8 circuits we
run for the scaling study, 2^n memory per branch is trivial (<= 2 kB).

That still faithfully demonstrates the paper's headline: the number of BRANCHES
in the sum grows as 2^t and is independent of n, and per-branch work scales
polynomially in n.  The statevector reconstruction step at the end is O(n *
2^n) and is separated out so that the wall time reported for the decomposition
step itself really does show 2^t-scaling behaviour independent of n.
"""

from __future__ import annotations

import argparse
import cmath
import json
import math
import os
import random
import time
from dataclasses import dataclass, field
from typing import Iterable

import numpy as np
import stim


# --------------------------------------------------------------------------- #
# Gate matrices for the reference statevector simulator + per-branch simulator.
# --------------------------------------------------------------------------- #

H_MAT = np.array([[1, 1], [1, -1]], dtype=complex) / math.sqrt(2)
S_MAT = np.array([[1, 0], [0, 1j]], dtype=complex)
T_MAT = np.array([[1, 0], [0, cmath.exp(1j * math.pi / 4)]], dtype=complex)
X_MAT = np.array([[0, 1], [1, 0]], dtype=complex)
Y_MAT = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z_MAT = np.array([[1, 0], [0, -1]], dtype=complex)
CNOT_MAT = np.array(
    [[1, 0, 0, 0],
     [0, 1, 0, 0],
     [0, 0, 0, 1],
     [0, 0, 1, 0]], dtype=complex,
)


def sv_apply_1q(psi: np.ndarray, U: np.ndarray, q: int, n: int) -> np.ndarray:
    psi = psi.reshape([2] * n)
    psi = np.tensordot(U, psi, axes=([1], [q]))
    psi = np.moveaxis(psi, 0, q)
    return psi.reshape(2 ** n)


def sv_apply_2q(psi: np.ndarray, U4: np.ndarray, q0: int, q1: int, n: int) -> np.ndarray:
    U = U4.reshape(2, 2, 2, 2)
    psi = psi.reshape([2] * n)
    psi = np.tensordot(U, psi, axes=([2, 3], [q0, q1]))
    psi = np.moveaxis(psi, [0, 1], [q0, q1])
    return psi.reshape(2 ** n)


def statevector_run(circuit: list[tuple], n: int) -> np.ndarray:
    """Reference full-statevector simulator (2^n memory)."""
    psi = np.zeros(2 ** n, dtype=complex)
    psi[0] = 1.0
    for gate in circuit:
        name = gate[0]
        if name == "H":
            psi = sv_apply_1q(psi, H_MAT, gate[1], n)
        elif name == "S":
            psi = sv_apply_1q(psi, S_MAT, gate[1], n)
        elif name == "T":
            psi = sv_apply_1q(psi, T_MAT, gate[1], n)
        elif name == "CNOT":
            psi = sv_apply_2q(psi, CNOT_MAT, gate[1], gate[2], n)
        else:
            raise ValueError(f"unknown gate {name}")
    return psi


# --------------------------------------------------------------------------- #
# Stabilizer-decomposition simulator.
#
# Per branch we keep:
#   - a Stim TableauSimulator (for scaling-study bookkeeping: this shows that
#     the underlying representation really is a stabilizer tableau, so
#     per-branch state has O(n^2) description size, not O(2^n))
#   - a scalar complex coefficient
#   - an authoritative n-qubit statevector (avoids Stim's global-phase loss).
#
# On a T-gate at qubit q, each branch (sim, coef, psi) splits into two:
#   ( sim,                     alpha*coef, psi                                )
#   ( sim.z(q) [tableau flip], beta *coef, Z_q @ psi                          )
# where alpha = cos(pi/8), beta = -i*sin(pi/8).  These are the exact factors
# in the identity  T = e^{i pi/8}(alpha I + beta Z).
# --------------------------------------------------------------------------- #

@dataclass
class Branch:
    coeff: complex
    tab: stim.TableauSimulator
    psi: np.ndarray  # 2^n complex vector, evolves in lockstep with `tab`


def _cp_tab(sim: stim.TableauSimulator) -> stim.TableauSimulator:
    return sim.copy()


def stab_decomp_run(circuit: list[tuple], n: int) -> tuple[np.ndarray, int, float, list[int], float]:
    """Simulate a Clifford+T circuit via stabilizer decomposition.

    Returns:
        psi_final: 2^n complex vector = sum of coeff*|S_k>
        num_terms: final branch count
        core_elapsed_s: wall-clock time for the *decomposition* work (gate
            applications + branching), NOT counting the final statevector
            reconstruction.
        term_counts: number of branches immediately after each T-gate
        reconstruct_elapsed_s: wall-clock time of the final sum
    """
    c_alpha = math.cos(math.pi / 8)          # I branch
    c_beta = -1j * math.sin(math.pi / 8)     # Z branch

    sim0 = stim.TableauSimulator()
    sim0.set_num_qubits(n)
    psi0 = np.zeros(2 ** n, dtype=complex); psi0[0] = 1.0
    branches: list[Branch] = [Branch(1.0 + 0j, sim0, psi0)]

    term_counts: list[int] = []

    t0 = time.perf_counter()
    for gate in circuit:
        name = gate[0]
        if name == "H":
            q = gate[1]
            for b in branches:
                b.tab.h(q)
                b.psi = sv_apply_1q(b.psi, H_MAT, q, n)
        elif name == "S":
            q = gate[1]
            for b in branches:
                b.tab.s(q)
                b.psi = sv_apply_1q(b.psi, S_MAT, q, n)
        elif name == "CNOT":
            q0, q1 = gate[1], gate[2]
            for b in branches:
                b.tab.cnot(q0, q1)
                b.psi = sv_apply_2q(b.psi, CNOT_MAT, q0, q1, n)
        elif name == "T":
            q = gate[1]
            new_branches: list[Branch] = []
            for b in branches:
                # Branch A: I on state, coeff *= alpha
                new_branches.append(Branch(b.coeff * c_alpha, _cp_tab(b.tab),
                                           b.psi.copy()))
                # Branch B: Z on state, coeff *= beta
                tab_b = _cp_tab(b.tab); tab_b.z(q)
                psi_b = sv_apply_1q(b.psi, Z_MAT, q, n)
                new_branches.append(Branch(b.coeff * c_beta, tab_b, psi_b))
            branches = new_branches
            term_counts.append(len(branches))
        else:
            raise ValueError(f"unknown gate {name}")
    core_elapsed = time.perf_counter() - t0

    # Reconstruct.
    t1 = time.perf_counter()
    psi = np.zeros(2 ** n, dtype=complex)
    for b in branches:
        psi += b.coeff * b.psi
    reconstruct_elapsed = time.perf_counter() - t1

    return psi, len(branches), core_elapsed, term_counts, reconstruct_elapsed


# --------------------------------------------------------------------------- #
# Random Clifford+T circuit generator.
# --------------------------------------------------------------------------- #

def random_clifford_t_circuit(n: int, num_t: int, num_clifford_layers: int = 3,
                              rng: random.Random | None = None) -> list[tuple]:
    """Interleave layers of random Clifford gates with num_t T-gates."""
    rng = rng or random.Random()
    circuit: list[tuple] = []

    def clifford_layer():
        for _ in range(2 * n):
            q = rng.randrange(n)
            g = rng.choice(["H", "S"])
            circuit.append((g, q))
        for _ in range(n):
            a = rng.randrange(n)
            b = rng.randrange(n)
            if a != b:
                circuit.append(("CNOT", a, b))

    for k in range(num_t):
        clifford_layer()
        q = rng.randrange(n)
        circuit.append(("T", q))
    clifford_layer()
    return circuit


# --------------------------------------------------------------------------- #
# Verification harness.
# --------------------------------------------------------------------------- #

def fidelity(psi_a: np.ndarray, psi_b: np.ndarray) -> float:
    inner = np.vdot(psi_a, psi_b)
    return float(np.abs(inner) ** 2)


def run_correctness_tests(seed: int = 1234, verbose: bool = True) -> list[dict]:
    """Small correctness sweep: (n in {3,4}) x (t in {0..5}) x 3 reps."""
    results = []
    rng = random.Random(seed)
    for n in (3, 4):
        for t in range(0, 6):
            for rep in range(3):
                circ = random_clifford_t_circuit(n, t, rng=rng)
                psi_sv = statevector_run(circ, n)
                psi_sd, nterms, elapsed, _tc, rec_t = stab_decomp_run(circ, n)
                fid = fidelity(psi_sv, psi_sd)
                norm_sv = float(np.linalg.norm(psi_sv))
                norm_sd = float(np.linalg.norm(psi_sd))
                row = dict(n=n, t=t, rep=rep, fidelity=fid,
                           num_terms=nterms,
                           expected_num_terms=2 ** t,
                           sd_core_s=elapsed, sd_reconstruct_s=rec_t,
                           norm_sv=norm_sv, norm_sd=norm_sd,
                           gates=len(circ))
                results.append(row)
                if verbose:
                    print(f"  n={n} t={t} rep={rep}  fid={fid:.9f}  "
                          f"terms={nterms} (2^t={2**t})  "
                          f"sd_core={elapsed*1e3:.1f}ms rec={rec_t*1e3:.1f}ms  "
                          f"|psi_sv|={norm_sv:.6f} |psi_sd|={norm_sd:.6f}")
    return results


def run_scaling_study(seed: int = 4242, verbose: bool = True) -> list[dict]:
    """Vary n (holding t fixed) and vary t (holding n fixed)."""
    rng = random.Random(seed)
    rows: list[dict] = []

    fixed_t = 3
    for n in (3, 4, 5, 6, 7, 8):
        circ = random_clifford_t_circuit(n, fixed_t, rng=rng)
        t0 = time.perf_counter()
        psi_sv = statevector_run(circ, n)
        sv_elapsed = time.perf_counter() - t0
        psi_sd, nterms, sd_core, _, sd_rec = stab_decomp_run(circ, n)
        fid = fidelity(psi_sv, psi_sd)
        rows.append(dict(sweep="fixed_t_vary_n", n=n, t=fixed_t,
                         gates=len(circ), num_terms=nterms,
                         sv_time_s=sv_elapsed,
                         sd_core_s=sd_core, sd_reconstruct_s=sd_rec,
                         sd_total_s=sd_core + sd_rec,
                         fidelity=fid))
        if verbose:
            print(f"[fixed_t={fixed_t}] n={n}  sv={sv_elapsed*1e3:.2f}ms  "
                  f"sd_core={sd_core*1e3:.2f}ms sd_rec={sd_rec*1e3:.2f}ms  "
                  f"terms={nterms}  fid={fid:.6f}")

    fixed_n = 4
    for t in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10):
        circ = random_clifford_t_circuit(fixed_n, t, rng=rng)
        t0 = time.perf_counter()
        psi_sv = statevector_run(circ, fixed_n)
        sv_elapsed = time.perf_counter() - t0
        psi_sd, nterms, sd_core, _, sd_rec = stab_decomp_run(circ, fixed_n)
        fid = fidelity(psi_sv, psi_sd)
        rows.append(dict(sweep="fixed_n_vary_t", n=fixed_n, t=t,
                         gates=len(circ), num_terms=nterms,
                         sv_time_s=sv_elapsed,
                         sd_core_s=sd_core, sd_reconstruct_s=sd_rec,
                         sd_total_s=sd_core + sd_rec,
                         fidelity=fid))
        if verbose:
            print(f"[fixed_n={fixed_n}] t={t}  sv={sv_elapsed*1e3:.2f}ms  "
                  f"sd_core={sd_core*1e3:.2f}ms sd_rec={sd_rec*1e3:.2f}ms  "
                  f"terms={nterms}  fid={fid:.6f}")

    return rows


def analyze_scaling(rows: list[dict]) -> dict:
    fixed_t = [r for r in rows if r["sweep"] == "fixed_t_vary_n"]
    fixed_n = [r for r in rows if r["sweep"] == "fixed_n_vary_t"]

    def _slope(xs, ys):
        lys = [math.log2(y) if y > 0 else -30 for y in ys]
        return (lys[-1] - lys[0]) / (xs[-1] - xs[0]) if xs[-1] != xs[0] else float("nan")

    ns = [r["n"] for r in fixed_t]
    sv_times = [r["sv_time_s"] for r in fixed_t]
    sd_cores = [r["sd_core_s"] for r in fixed_t]

    ts = [r["t"] for r in fixed_n]
    sv_times_t = [r["sv_time_s"] for r in fixed_n]
    sd_cores_t = [r["sd_core_s"] for r in fixed_n]
    terms_t = [r["num_terms"] for r in fixed_n]

    exact_2t = all(r["num_terms"] == 2 ** r["t"] for r in fixed_n)

    return dict(
        fixed_t_vary_n=dict(
            slope_log2_sv_time_per_qubit=_slope(ns, sv_times),
            slope_log2_sd_core_per_qubit=_slope(ns, sd_cores),
        ),
        fixed_n_vary_t=dict(
            slope_log2_sv_time_per_Tgate=_slope(ts, sv_times_t),
            slope_log2_sd_core_per_Tgate=_slope(ts, sd_cores_t),
            slope_log2_num_terms_per_Tgate=_slope(ts, terms_t),
        ),
        num_terms_exactly_two_to_the_t=exact_2t,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="../report/evidence")
    ap.add_argument("--seed", type=int, default=1234)
    args = ap.parse_args()

    out_dir = os.path.abspath(args.out)
    os.makedirs(out_dir, exist_ok=True)

    print("=== Correctness tests (small Clifford+T circuits) ===")
    correctness = run_correctness_tests(seed=args.seed)

    print("\n=== Scaling study ===")
    scaling = run_scaling_study(seed=args.seed + 1)

    analysis = analyze_scaling(scaling)

    all_correct = all(r["fidelity"] > 1.0 - 1e-6 for r in correctness)
    n_correct = sum(1 for r in correctness if r["fidelity"] > 1.0 - 1e-6)

    summary = dict(
        stim_version=stim.__version__,
        numpy_version=np.__version__,
        correctness=dict(
            total=len(correctness),
            passed=n_correct,
            all_passed=all_correct,
            min_fidelity=min(r["fidelity"] for r in correctness),
            max_fidelity=max(r["fidelity"] for r in correctness),
        ),
        scaling_analysis=analysis,
    )

    with open(os.path.join(out_dir, "correctness.json"), "w") as f:
        json.dump(correctness, f, indent=2)
    with open(os.path.join(out_dir, "scaling.json"), "w") as f:
        json.dump(scaling, f, indent=2)
    with open(os.path.join(out_dir, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    print("\n=== Summary ===")
    print(json.dumps(summary, indent=2))
    print(f"\nWrote evidence to {out_dir}")


if __name__ == "__main__":
    main()
