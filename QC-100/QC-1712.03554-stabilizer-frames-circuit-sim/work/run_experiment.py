"""Reproduce the stabilizer-frames headline for arXiv:1712.03554.

For n in {6, 8, 10} and t in {0, 1, 2, 3, 4}:
    * build a Clifford baseline (t=0) or a near-Clifford circuit with t
      inserted T-gates
    * simulate with our stabilizer-frame simulator (frame doubles per T)
    * ground-truth statevector from Qiskit (Clifford + T native)
    * for t=0, also cross-check the Clifford baseline with Stim's tableau
      simulator statevector
    * record frame size, wallclock, max amplitude error, L2 error
"""
import json
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from stabilizer_frame import (
    build_clifford_baseline,
    inject_t_gates,
    run_frame_on_ops,
    exact_qiskit_statevector,
    stim_clifford_statevector,
)


def max_abs_amp_error(a: np.ndarray, b: np.ndarray) -> float:
    """max_i | |a_i| - |b_i| |  --  phase-insensitive amplitude comparison
    to be robust to global phase differences between simulators.
    Also compute complex diff after removing the best global phase."""
    # remove global phase using the largest-magnitude amplitude of b
    idx = int(np.argmax(np.abs(b)))
    if abs(b[idx]) < 1e-15 or abs(a[idx]) < 1e-15:
        phase = 1.0
    else:
        phase = (b[idx] / a[idx])
        phase = phase / abs(phase)
    a_aligned = a * phase
    return float(np.max(np.abs(a_aligned - b)))


def l2_error(a: np.ndarray, b: np.ndarray) -> float:
    idx = int(np.argmax(np.abs(b)))
    if abs(b[idx]) < 1e-15 or abs(a[idx]) < 1e-15:
        phase = 1.0
    else:
        phase = (b[idx] / a[idx])
        phase = phase / abs(phase)
    a_aligned = a * phase
    return float(np.linalg.norm(a_aligned - b))


def main():
    results = []
    for n in [6, 8, 10]:
        base = build_clifford_baseline(n, seed=100 + n)

        # ----- t = 0 : pure Clifford baseline, cross-check Stim vs Qiskit vs Frame
        psi_frame, chi, dt_frame = run_frame_on_ops(base, n)
        t0 = time.perf_counter()
        psi_qiskit = exact_qiskit_statevector(base, n)
        dt_qk = time.perf_counter() - t0
        t0 = time.perf_counter()
        psi_stim = stim_clifford_statevector(base, n)
        dt_stim = time.perf_counter() - t0
        err_frame_vs_qk = max_abs_amp_error(psi_frame, psi_qiskit)
        err_stim_vs_qk  = max_abs_amp_error(psi_stim,  psi_qiskit)
        l2_frame_vs_qk  = l2_error(psi_frame, psi_qiskit)
        results.append({
            "n": n, "t": 0, "frame_size": chi,
            "frame_time_s": dt_frame,
            "qiskit_time_s": dt_qk,
            "stim_time_s": dt_stim,
            "max_amp_err_frame_vs_qiskit": err_frame_vs_qk,
            "max_amp_err_stim_vs_qiskit":  err_stim_vs_qk,
            "l2_err_frame_vs_qiskit": l2_frame_vs_qk,
            "n_ops": len(base),
        })
        print(f"[n={n} t=0] chi={chi} frame_dt={dt_frame*1000:.2f}ms "
              f"qk_dt={dt_qk*1000:.2f}ms stim_dt={dt_stim*1000:.2f}ms "
              f"err_frame_vs_qk={err_frame_vs_qk:.2e} "
              f"err_stim_vs_qk={err_stim_vs_qk:.2e}")

        # ----- t in {1, 2, 3, 4} : inject T-gates
        for t in [1, 2, 3, 4]:
            ops = inject_t_gates(base, n, t, seed=200 + n * 10 + t)
            psi_frame, chi, dt_frame = run_frame_on_ops(ops, n)
            t0 = time.perf_counter()
            psi_qk = exact_qiskit_statevector(ops, n)
            dt_qk = time.perf_counter() - t0
            err = max_abs_amp_error(psi_frame, psi_qk)
            l2 = l2_error(psi_frame, psi_qk)
            results.append({
                "n": n, "t": t, "frame_size": chi,
                "frame_time_s": dt_frame,
                "qiskit_time_s": dt_qk,
                "max_amp_err_frame_vs_qiskit": err,
                "l2_err_frame_vs_qiskit": l2,
                "n_ops": len(ops),
            })
            print(f"[n={n} t={t}] chi={chi} (expected 2^t={2**t}) "
                  f"frame_dt={dt_frame*1000:.2f}ms qk_dt={dt_qk*1000:.2f}ms "
                  f"max_amp_err={err:.2e} l2={l2:.2e}")

    # Also probe scaling in t at fixed n=6 for t=5..8 (chi=32..256)
    print("\n--- scaling probe n=6, t=5..8 ---")
    base6 = build_clifford_baseline(6, seed=106)
    for t in [5, 6, 7, 8]:
        ops = inject_t_gates(base6, 6, t, seed=300 + t)
        psi_frame, chi, dt_frame = run_frame_on_ops(ops, 6)
        psi_qk = exact_qiskit_statevector(ops, 6)
        err = max_abs_amp_error(psi_frame, psi_qk)
        l2 = l2_error(psi_frame, psi_qk)
        results.append({
            "n": 6, "t": t, "frame_size": chi,
            "frame_time_s": dt_frame,
            "max_amp_err_frame_vs_qiskit": err,
            "l2_err_frame_vs_qiskit": l2,
            "n_ops": len(ops),
            "note": "scaling_probe",
        })
        print(f"[n=6 t={t}] chi={chi} frame_dt={dt_frame*1000:.2f}ms "
              f"max_amp_err={err:.2e} l2={l2:.2e}")

    out = {
        "results": results,
        "tolerance_amp": 1e-10,
        "tolerance_l2":  1e-9,
    }
    print(json.dumps(out, indent=2))
    with open(os.path.join(os.path.dirname(__file__), "..", "report", "evidence", "results.json"), "w") as f:
        json.dump(out, f, indent=2)


if __name__ == "__main__":
    main()
