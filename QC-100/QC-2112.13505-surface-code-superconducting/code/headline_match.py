#!/usr/bin/env python3
"""
Headline reproduction for Zhao et al. arXiv:2112.13505.

Paper headline (Fig 5 + text, lines 353/360/462):
  - d=3 rotated surface code, 11 error-correction cycles, on Zuchongzhi 2.1.
  - Uncorrected logical error rate  εL ≈ 0.32 (|0L>) / 0.33 (|-L>).
  - MWPM-corrected logical error rate εL ≈ 0.26 (both states).
  - "the logical errors εL of |0L> and |-L> are reduced by 19% and 21%"
    -> ~20% relative reduction from applying MWPM correction.

This script:
  1. Finds the Stim circuit-level depolarizing p that puts the d=3/11-round
     UNCORRECTED whole-experiment εL near the paper's ~0.32.
  2. At that operating point, reports the MWPM-CORRECTED whole-experiment εL
     and the relative reduction, to compare against the paper's ~20% (19-21%).
  3. Confirms sub-threshold distance suppression (d=3 -> d=5 at low p).

Everything is a real Stim + PyMatching (MWPM) Monte-Carlo simulation.
"""
import json
from pathlib import Path
import numpy as np
import stim
import pymatching


def sim(distance, rounds, p, shots, basis="Z", seed=0x2112):
    circ = stim.Circuit.generated(
        f"surface_code:rotated_memory_{basis.lower()}",
        distance=distance, rounds=rounds,
        after_clifford_depolarization=p,
        after_reset_flip_probability=p,
        before_measure_flip_probability=p,
        before_round_data_depolarization=p,
    )
    dem = circ.detector_error_model(decompose_errors=True)
    m = pymatching.Matching.from_detector_error_model(dem)
    det, obs = circ.compile_detector_sampler(seed=seed).sample(shots, separate_observables=True)
    pred = m.decode_batch(det)
    raw = float(np.mean(np.any(obs, axis=1)))          # uncorrected whole-experiment εL
    corr = float(np.mean(np.any(pred != obs, axis=1))) # MWPM-corrected whole-experiment εL
    return raw, corr


def main():
    out = {"paper": "arXiv:2112.13505", "tool": {
        "stim": stim.__version__, "pymatching": pymatching.__version__, "numpy": np.__version__}}

    # ---- Step 1: locate operating point where uncorrected whole-exp εL ~ 0.32 ----
    print("Step 1: locate p giving uncorrected d=3/11-round whole-experiment εL ~ 0.32")
    target = 0.32
    best = None
    for p in [0.015, 0.020, 0.025, 0.030, 0.035, 0.040]:
        raw, corr = sim(3, 11, p, shots=60000, basis="Z")
        red = (raw - corr) / raw if raw > 0 else 0.0
        print(f"  p={p:.3f}: uncorr εL(whole)={raw:.3f}  MWPM εL(whole)={corr:.3f}  reduction={red*100:.1f}%")
        if best is None or abs(raw - target) < abs(best[1] - target):
            best = (p, raw, corr, red)
    p_op, raw_op, corr_op, red_op = best
    print(f"  -> operating point p={p_op:.3f}: uncorr εL={raw_op:.3f}, MWPM εL={corr_op:.3f}, reduction={red_op*100:.1f}%")

    # ---- Step 2: high-statistics reduction at operating point, both bases ----
    print("Step 2: high-stat MWPM reduction at operating point (both logical states)")
    step2 = {}
    for basis, label in (("Z", "|0L>"), ("X", "|-L>")):
        raw, corr = sim(3, 11, p_op, shots=200000, basis=basis, seed=0xA0 if basis == "Z" else 0xB1)
        red = (raw - corr) / raw if raw > 0 else 0.0
        step2[label] = {"basis": basis, "uncorr_epsL_whole": raw, "mwpm_epsL_whole": corr, "reduction": red}
        print(f"  {label} (basis {basis}): uncorr εL={raw:.4f}  MWPM εL={corr:.4f}  reduction={red*100:.1f}%")

    # ---- Step 3: sub-threshold distance suppression ----
    print("Step 3: distance suppression d=3 -> d=5 (MWPM-corrected εL/round, low p)")
    step3 = []
    for p in [0.001, 0.002, 0.003, 0.005]:
        row = {"p": p}
        for d in (3, 5):
            _, corr = sim(d, d, p, shots=100000, basis="Z", seed=0xAA + d)
            # per-round corrected logical error
            pr = 0.5 * (1.0 - (1.0 - 2.0 * min(corr, 0.4999)) ** (1.0 / d))
            row[f"d{d}_mwpm_epsL_per_round"] = pr
        row["suppressed_d5_lt_d3"] = row["d5_mwpm_epsL_per_round"] < row["d3_mwpm_epsL_per_round"]
        step3.append(row)
        print(f"  p={p:.3f}: d3={row['d3_mwpm_epsL_per_round']:.5f}  d5={row['d5_mwpm_epsL_per_round']:.5f}  "
              f"suppressed={row['suppressed_d5_lt_d3']}")

    out["paper_reported"] = {
        "uncorr_epsL_0L": 0.32, "uncorr_epsL_mL": 0.33, "mwpm_epsL": 0.26,
        "reduction_0L": 0.19, "reduction_mL": 0.21, "reduction_abstract": 0.20,
    }
    out["operating_point"] = {"p": p_op, "uncorr_epsL_whole": raw_op, "mwpm_epsL_whole": corr_op, "reduction": red_op}
    out["step2_reduction_both_states"] = step2
    out["step3_distance_suppression"] = step3
    outp = Path(__file__).parent.parent / "report/evidence/headline_match.json"
    with open(outp, "w") as fh:
        json.dump(out, fh, indent=2)
    print(f"\nWrote {outp}")


if __name__ == "__main__":
    main()
