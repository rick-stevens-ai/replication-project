#!/usr/bin/env python3
"""
Per-cycle εL match to Zhao et al. arXiv:2112.13505.

The paper's εL is a PER-CYCLE logical error rate extracted from an exponential
fit of logical-state fidelity vs number of cycles (Fig 5), NOT the whole-11-round
flip probability (which saturates at 0.5). Reported (d=3, Zuchongzhi 2.1):
    uncorrected  εL ≈ 0.32 (|0L>) / 0.33 (|-L>)
    MWPM-corrected εL ≈ 0.26   -> ~20% (19%/21%) relative reduction.

We reproduce a real Stim+PyMatching (MWPM) surface code at d=3, sweep the
circuit-level depolarizing p, convert whole-experiment logical error to a
per-cycle εL via  (1-2 eps)^rounds = 1-2 p_L, and locate the p where the
UNCORRECTED per-cycle εL matches the paper's ~0.32, then report the
MWPM-corrected per-cycle εL and the relative reduction at that point.
"""
import json
from pathlib import Path
import numpy as np
import stim
import pymatching

ROUNDS = 11


def per_round(pL):
    pL = min(pL, 0.49999)
    return 0.5 * (1.0 - (1.0 - 2.0 * pL) ** (1.0 / ROUNDS))


def sim(p, shots, basis="Z", seed=0x2112):
    circ = stim.Circuit.generated(
        f"surface_code:rotated_memory_{basis.lower()}",
        distance=3, rounds=ROUNDS,
        after_clifford_depolarization=p,
        after_reset_flip_probability=p,
        before_measure_flip_probability=p,
        before_round_data_depolarization=p,
    )
    dem = circ.detector_error_model(decompose_errors=True)
    m = pymatching.Matching.from_detector_error_model(dem)
    det, obs = circ.compile_detector_sampler(seed=seed).sample(shots, separate_observables=True)
    pred = m.decode_batch(det)
    raw = float(np.mean(np.any(obs, axis=1)))
    corr = float(np.mean(np.any(pred != obs, axis=1)))
    return per_round(raw), per_round(corr)


def main():
    print("Per-cycle εL sweep (d=3, 11 rounds); target uncorrected per-cycle εL ~ 0.32")
    rows = []
    target = 0.32
    best = None
    for p in [0.008, 0.010, 0.012, 0.014, 0.016, 0.018, 0.020]:
        raw, corr = sim(p, shots=100000, basis="Z")
        red = (raw - corr) / raw if raw > 0 else 0.0
        rows.append({"p": p, "uncorr_epsL_percycle": raw, "mwpm_epsL_percycle": corr, "reduction": red})
        print(f"  p={p:.3f}: uncorr εL/cyc={raw:.3f}  MWPM εL/cyc={corr:.3f}  reduction={red*100:.1f}%")
        if best is None or abs(raw - target) < abs(best["uncorr_epsL_percycle"] - target):
            best = rows[-1]

    print(f"\nBest match to paper uncorrected εL≈0.32:")
    print(f"  p={best['p']:.3f}: uncorr εL/cyc={best['uncorr_epsL_percycle']:.3f} "
          f"(paper 0.32), MWPM εL/cyc={best['mwpm_epsL_percycle']:.3f} (paper 0.26), "
          f"reduction={best['reduction']*100:.1f}% (paper ~20% / 19-21%)")

    out = {
        "paper": "arXiv:2112.13505",
        "rounds": ROUNDS,
        "tool": {"stim": stim.__version__, "pymatching": pymatching.__version__, "numpy": np.__version__},
        "paper_reported": {"uncorr_epsL_percycle_0L": 0.32, "uncorr_epsL_percycle_mL": 0.33,
                           "mwpm_epsL_percycle": 0.26, "reduction_19to21pct": [0.19, 0.21]},
        "sweep": rows,
        "best_match": best,
    }
    outp = Path(__file__).parent.parent / "report/evidence/percycle_match.json"
    with open(outp, "w") as fh:
        json.dump(out, fh, indent=2)
    print(f"Wrote {outp}")


if __name__ == "__main__":
    main()
