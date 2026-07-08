#!/usr/bin/env python3
"""
Sweep the number of sequences per length K for both (A) naive Pauli RB and
(B) character Pauli RB (irrep Z), and compare the recovered per-basis-gate
survival f and the fit uncertainty as a function of K.

The paper's central efficiency claim is that character RB recovers the same
quality parameter with a much sharper fit (smaller stderr) at the same or
smaller K, i.e. it needs fewer sequences to reach a given fit precision.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np

# reuse machinery
import sys
sys.path.insert(0, str(Path(__file__).parent))
from rb_character_pauli import (Params, make_noise, run_naive_pauli_rb,
                                 run_character_pauli_rb, fit_exponential)
from qiskit_aer import AerSimulator


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=float, default=0.01)
    ap.add_argument("--Ks", type=str, default="5,10,20,40,80")
    ap.add_argument("--shots", type=int, default=256)
    ap.add_argument("--seed", type=int, default=101)
    ap.add_argument("--lengths", type=str, default="1,2,4,8,16,32,64,96")
    ap.add_argument("--out", type=str, required=True)
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    lengths = [int(x) for x in args.lengths.split(",")]
    Ks = [int(x) for x in args.Ks.split(",")]

    noise = make_noise(args.p)
    sim = AerSimulator(noise_model=noise)

    # expected: depolarizing_error(p, 1) in qiskit gives Bloch shrinkage 1-p
    # per gate, so f_expected = 1 - p
    f_expected = 1.0 - args.p

    sweep = []
    for K in Ks:
        params = Params(
            p_gate_depol=args.p,
            seq_lengths=lengths,
            seqs_per_length=K,
            shots=args.shots,
            seed=args.seed + K,
            lambda_irrep="Z",
        )
        print(f"\n=== K={K} ===")
        t0 = time.time()
        res_A = run_naive_pauli_rb(params, sim)
        dt_A = time.time() - t0

        t0 = time.time()
        res_B = run_character_pauli_rb(params, sim)
        dt_B = time.time() - t0

        fit_A = fit_exponential(res_A["curve"], two_param=False)
        fit_B = fit_exponential(res_B["curve"], two_param=True)

        entry = {
            "K": K,
            "shots": args.shots,
            "total_shots_naive": K * len(lengths) * args.shots,
            "total_shots_char": K * len(lengths) * args.shots,
            "wall_naive_sec": dt_A,
            "wall_char_sec": dt_B,
            "naive": {"fit": fit_A,
                      "curve": [{"m": int(m), "y": float(y), "sem": float(s)}
                                for m, y, s in res_A["curve"]]},
            "character": {"fit": fit_B,
                          "curve": [{"m": int(m), "y": float(y), "sem": float(s)}
                                    for m, y, s in res_B["curve"]]},
        }
        sweep.append(entry)

        f_A = fit_A.get("f", float("nan"))
        f_B = fit_B.get("f", float("nan"))
        e_A = fit_A.get("f_stderr", float("nan"))
        e_B = fit_B.get("f_stderr", float("nan"))
        print(f"  K={K:>3d}  naive  f={f_A:.5f} +/- {e_A:.5f}   err={abs(f_A - f_expected):.5f}")
        print(f"  K={K:>3d}  charRB f={f_B:.5f} +/- {e_B:.5f}   err={abs(f_B - f_expected):.5f}")

    payload = {
        "p_gate_depol": args.p,
        "seq_lengths": lengths,
        "Ks": Ks,
        "shots": args.shots,
        "seed": args.seed,
        "f_expected": f_expected,
        "sweep": sweep,
    }
    (out_dir / "efficiency_sweep_result.json").write_text(
        json.dumps(payload, indent=2))
    print(f"\nSaved sweep to {out_dir}/efficiency_sweep_result.json")

    print("\nSummary:")
    print(f"{'K':>5} {'naive f':>10} {'naive stderr':>15} "
          f"{'char f':>10} {'char stderr':>15} {'stderr ratio':>14}")
    for s in sweep:
        fA = s["naive"]["fit"].get("f", float("nan"))
        eA = s["naive"]["fit"].get("f_stderr", float("nan"))
        fB = s["character"]["fit"].get("f", float("nan"))
        eB = s["character"]["fit"].get("f_stderr", float("nan"))
        ratio = (eA / eB) if eB > 0 else float("nan")
        print(f"{s['K']:>5d} {fA:>10.5f} {eA:>15.5f} {fB:>10.5f} "
              f"{eB:>15.5f} {ratio:>14.2f}")
    print(f"\nExpected f = {f_expected:.5f}")


if __name__ == "__main__":
    main()
