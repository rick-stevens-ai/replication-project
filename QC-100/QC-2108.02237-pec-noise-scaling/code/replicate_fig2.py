#!/usr/bin/env python3
"""
Independent replication of Fig. 2 of arXiv:2108.02237
Mari, Shammah, Zeng — "Extending quantum probabilistic error cancellation by noise scaling"

Fig. 2: single-qubit randomized benchmarking circuit of depth 14, observable A = |0><0|,
ideal <A> = 1. Compare three methods on a density-matrix simulation (infinite-shot limit)
under a depolarizing channel of actual strength p_actual varied in [0, 0.02]:
  (Unmit) raw noisy expectation
  (PEC)   PEC with quasi-prob representation built assuming a fixed p_est = 0.01
  (NEPEC) noise-agnostic PEC via gate extrapolation with scale factors S = {1, 51}

We reproduce the qualitative claims of Fig. 2:
  - Unmitigated <A> drops roughly linearly with p_actual.
  - PEC hits <A> ~ 1 exactly at p_actual = p_est = 0.01, and is biased on either side.
  - NEPEC (extended by noise scaling) is more robust across the whole p_actual range —
    stays much closer to 1 than either Unmit or PEC when p_actual != p_est.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import cirq

from mitiq import Observable, PauliString
from mitiq.pec import execute_with_pec, OperationRepresentation, NoisyOperation
from mitiq.pec.representations.depolarizing import (
    represent_operation_with_local_depolarizing_noise,
)
from mitiq.zne.scaling import fold_gates_at_random

# ------------------------------------------------------------------------------
# 1. Build the depth-14 single-qubit RB-like circuit.
#    We use a fixed pseudo-random Clifford sequence and append its inverse so
#    the ideal action is the identity (<0|C^-1 C |0> = 1). This matches the
#    randomized-benchmarking setup used in the paper (their Fig. 2 says
#    "single-qubit randomized benchmarking circuit of depth 14 such that
#    <A>_ideal = 1", A = |0><0|).
# ------------------------------------------------------------------------------

def build_rb_circuit(depth: int = 14, seed: int = 20260703) -> cirq.Circuit:
    """Single-qubit Clifford RB circuit: (depth-1) random 1q Cliffords + inverse."""
    rng = np.random.default_rng(seed)
    q = cirq.LineQubit(0)
    # 1-qubit Clifford gate pool as unitaries. We stick to a small set of gates
    # that survive Mitiq's PEC representation & folding paths cleanly.
    pool = [
        cirq.X, cirq.Y, cirq.Z, cirq.H, cirq.S, cirq.S**-1,
        cirq.X**0.5, cirq.X**-0.5, cirq.Y**0.5, cirq.Y**-0.5,
    ]
    ops = []
    for _ in range(depth - 1):
        g = pool[rng.integers(len(pool))]
        ops.append(g.on(q))
    circ = cirq.Circuit(ops)
    # Compute the exact inverse unitary and append it as a single Cirq gate so
    # the ideal circuit is the identity.
    U = cirq.unitary(circ)
    U_inv = U.conj().T
    inv_gate = cirq.MatrixGate(U_inv).on(q)
    circ = circ + cirq.Circuit(inv_gate)
    return circ


# ------------------------------------------------------------------------------
# 2. Density-matrix executor with per-gate depolarizing noise.
#    All noisy expectation values are computed from the exact density matrix
#    (no shot noise) — the paper explicitly says Fig. 2 uses simulated density
#    matrices (infinite-shot limit).
# ------------------------------------------------------------------------------

def _apply_depolarizing_after_each_op(circ: cirq.Circuit, p: float) -> cirq.Circuit:
    q = cirq.LineQubit(0)
    noisy_ops = []
    for op in circ.all_operations():
        noisy_ops.append(op)
        if p > 0:
            noisy_ops.append(cirq.depolarize(p).on(q))
    return cirq.Circuit(noisy_ops)


def make_executor(p_actual: float):
    """Return a Mitiq-compatible executor: circuit -> <A> = <|0><0|> via density-matrix sim."""
    q = cirq.LineQubit(0)
    sim = cirq.DensityMatrixSimulator()
    proj0 = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)

    def executor(circuit: cirq.Circuit) -> float:
        noisy = _apply_depolarizing_after_each_op(circuit, p_actual)
        result = sim.simulate(noisy)
        rho = result.final_density_matrix
        return float(np.real(np.trace(proj0 @ rho)))

    # Explicitly declare the return annotation so Mitiq's Executor accepts float outputs.
    executor.__annotations__ = {"circuit": cirq.Circuit, "return": float}
    return executor


# ------------------------------------------------------------------------------
# 3. Standard PEC representations assuming a *fixed estimated* noise level p_est.
# ------------------------------------------------------------------------------

def pec_representations(circuit: cirq.Circuit, p_est: float):
    reps = []
    seen = set()
    for op in circuit.all_operations():
        key = str(op)
        if key in seen:
            continue
        seen.add(key)
        rep = represent_operation_with_local_depolarizing_noise(
            cirq.Circuit(op), noise_level=p_est
        )
        reps.append(rep)
    return reps


# ------------------------------------------------------------------------------
# 4. NEPEC "noise-agnostic" gate extrapolation representation (Eq. 30/31 of the paper).
#    For each ideal gate G we build:
#         G  ~  sum_lambda  eta_lambda * G^(lambda)
#    where G^(lambda) is the *noisy* gate at scale lambda (implemented via unitary
#    folding of the single-op circuit), and the coefficients are the Richardson
#    coefficients eta_lambda = prod_{lambda' != lambda} lambda' / (lambda' - lambda).
#    We use S = {1, 51} exactly as in the paper's Fig. 2 caption.
# ------------------------------------------------------------------------------

def richardson_coeffs(scale_factors):
    S = list(scale_factors)
    etas = []
    for i, l in enumerate(S):
        prod = 1.0
        for j, lp in enumerate(S):
            if i == j:
                continue
            prod *= lp / (lp - l)
        etas.append(prod)
    return etas


def fold_op_at_scale(op: cirq.Operation, scale: int) -> cirq.Circuit:
    """Apply local unitary folding of a single-op sub-circuit: G -> G (G^dag G)^k."""
    # scale must be an odd positive integer; for scale=1 it's just [op].
    assert scale >= 1 and int(scale) == scale and scale % 2 == 1, scale
    k = (scale - 1) // 2
    q = cirq.LineQubit(0)
    ops = [op]
    for _ in range(k):
        # Inverse of a Cirq op / MatrixGate: use unitary.
        U = cirq.unitary(op.gate)
        U_dag = U.conj().T
        ops.append(cirq.MatrixGate(U_dag).on(q))
        ops.append(op)
    return cirq.Circuit(ops)


def nepec_representations(circuit: cirq.Circuit, scale_factors=(1, 51)):
    """Build a Mitiq OperationRepresentation for each unique ideal gate using
    the noise-agnostic gate-extrapolation formula (Eqs. 30-31 of the paper)."""
    etas = richardson_coeffs(scale_factors)
    reps = []
    seen = set()
    for op in circuit.all_operations():
        key = str(op)
        if key in seen:
            continue
        seen.add(key)
        # Ideal single-op circuit that this representation is FOR.
        ideal_circ = cirq.Circuit(op)
        # Noisy implementable circuits at each lambda (folded).
        noisy_circs = [fold_op_at_scale(op, s) for s in scale_factors]
        noisy_ops = [NoisyOperation(circuit=c) for c in noisy_circs]
        rep = OperationRepresentation(
            ideal=ideal_circ,
            noisy_operations=noisy_ops,
            coeffs=list(etas),
            is_qubit_dependent=False,
        )
        reps.append(rep)
    return reps


# ------------------------------------------------------------------------------
# 5. Sweep p_actual and compute Unmit / PEC / NEPEC expectation values.
# ------------------------------------------------------------------------------

def main():
    outdir = Path(__file__).resolve().parent.parent / "report" / "evidence"
    outdir.mkdir(parents=True, exist_ok=True)

    depth = 14
    circuit = build_rb_circuit(depth=depth, seed=20260703)
    ideal_exec = make_executor(p_actual=0.0)
    ideal_val = ideal_exec(circuit)
    print(f"[info] built RB circuit, {len(list(circuit.all_operations()))} ops, "
          f"ideal <A>|p=0 = {ideal_val:.6f}")

    import os, sys
    p_est = 0.01
    p_actuals = [0.0, 0.0025, 0.005, 0.0075, 0.01, 0.0125, 0.015, 0.0175, 0.02]
    # 5000 samples * 5 p * (14*51 ops per NEPEC sample) is heavy on the CPU. Use
    # NUM_SAMPLES env override; default 800 for a fast-but-honest reproduction.
    num_samples = int(os.environ.get("NUM_SAMPLES", "800"))
    scale_factors = (1, 51)
    # Force line-buffered stdout so we see per-p progress in the tee log.
    sys.stdout = os.fdopen(sys.stdout.fileno(), "w", buffering=1)

    pec_reps = pec_representations(circuit, p_est=p_est)
    nepec_reps = nepec_representations(circuit, scale_factors=scale_factors)

    print(f"[info] built {len(pec_reps)} PEC reps (p_est={p_est}) and "
          f"{len(nepec_reps)} NEPEC reps (S={scale_factors})")

    rows = []
    t0 = time.time()
    for p in p_actuals:
        exec_p = make_executor(p_actual=p)

        # Unmitigated
        unmit = exec_p(circuit)

        # PEC
        pec_val, pec_info = execute_with_pec(
            circuit=circuit,
            executor=exec_p,
            representations=pec_reps,
            num_samples=num_samples,
            random_state=int(1000 * p * 1000) + 1,
            full_output=True,
        )

        # NEPEC (noise-agnostic gate extrapolation)
        nepec_val, nepec_info = execute_with_pec(
            circuit=circuit,
            executor=exec_p,
            representations=nepec_reps,
            num_samples=num_samples,
            random_state=int(1000 * p * 1000) + 2,
            full_output=True,
        )

        row = {
            "p_actual": p,
            "unmitigated": unmit,
            "pec": pec_val,
            "pec_std": pec_info.get("pec_error"),
            "nepec": nepec_val,
            "nepec_std": nepec_info.get("pec_error"),
        }
        rows.append(row)
        print(f"  p={p:.4f}  unmit={unmit:.4f}  PEC={pec_val:.4f}"
              f" (+-{row['pec_std']:.4f})  NEPEC={nepec_val:.4f}"
              f" (+-{row['nepec_std']:.4f})   [elapsed {time.time()-t0:5.1f}s]")

    out = {
        "paper": "arXiv:2108.02237",
        "figure": "Fig. 2",
        "circuit_depth": depth,
        "n_ops": len(list(circuit.all_operations())),
        "ideal_expectation_value": ideal_val,
        "p_est_for_PEC": p_est,
        "nepec_scale_factors": list(scale_factors),
        "richardson_coeffs": richardson_coeffs(scale_factors),
        "num_samples_per_point": num_samples,
        "rows": rows,
    }
    (outdir / "fig2_data.json").write_text(json.dumps(out, indent=2))
    print(f"\n[info] wrote {outdir / 'fig2_data.json'}")

    # Also write a compact CSV
    csv_path = outdir / "fig2_data.csv"
    with open(csv_path, "w") as f:
        f.write("p_actual,unmitigated,pec,pec_std,nepec,nepec_std\n")
        for r in rows:
            f.write(
                f"{r['p_actual']},{r['unmitigated']},{r['pec']},{r['pec_std']},"
                f"{r['nepec']},{r['nepec_std']}\n"
            )
    print(f"[info] wrote {csv_path}")


if __name__ == "__main__":
    main()
