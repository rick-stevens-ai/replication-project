#!/usr/bin/env python3
"""Find the Stim noise level that reproduces the paper's uncorrected εL ≈ 0.32
and MWPM-corrected εL ≈ 0.26 for the d=3, 11-round Zuchongzhi 2.1 experiment.
"""
import json
from pathlib import Path
import numpy as np
import stim
import pymatching


def simulate(p: float, shots: int = 40000, seed: int = 0xBEEF) -> tuple[float, float]:
    circuit = stim.Circuit.generated(
        "surface_code:rotated_memory_z",
        distance=3,
        rounds=11,
        after_clifford_depolarization=p,
        after_reset_flip_probability=p,
        before_measure_flip_probability=p,
        before_round_data_depolarization=p,
    )
    dem = circuit.detector_error_model(decompose_errors=True)
    matcher = pymatching.Matching.from_detector_error_model(dem)
    sampler = circuit.compile_detector_sampler(seed=seed)
    det, obs = sampler.sample(shots, separate_observables=True)
    pred = matcher.decode_batch(det)
    raw = np.mean(np.any(obs, axis=1))
    corr = np.mean(np.any(pred != obs, axis=1))

    def per_round(pL):
        if pL >= 0.5:
            return 0.5
        return 0.5 * (1.0 - (1.0 - 2.0 * pL) ** (1.0 / 11))

    return per_round(float(raw)), per_round(float(corr))


def main() -> None:
    print("Sweeping p to match paper: uncorrected εL ≈ 0.32, corrected εL ≈ 0.26 (d=3, 11 rounds)")
    ps = [0.030, 0.040, 0.050, 0.060, 0.075, 0.090, 0.110]
    rows = []
    for p in ps:
        raw, corr = simulate(p, shots=40000)
        rows.append({"p": p, "raw_eps": raw, "corr_eps": corr, "reduction": (raw - corr) / raw if raw > 0 else 0})
        print(f"  p={p:.3f}: raw εL/round = {raw:.3f}  corr εL/round = {corr:.3f}  reduction = {(raw-corr)/raw*100:.1f}%")
    out = Path(__file__).parent.parent / "report/evidence/match_paper_sweep.json"
    with open(out, "w") as fh:
        json.dump(rows, fh, indent=2)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
