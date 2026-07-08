#!/usr/bin/env python3
"""Post-analysis of fig2_data.json:
  - compare Unmit / PEC / NEPEC absolute bias vs the ideal (1.0)
  - generate a matplotlib PNG mirroring Fig. 2 of arXiv:2108.02237
  - emit a short verdict summary as verdict.json / verdict.txt
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

evidence = Path(__file__).resolve().parent.parent / "report" / "evidence"
data = json.loads((evidence / "fig2_data.json").read_text())
rows = data["rows"]
ideal = data["ideal_expectation_value"]
p_est = data["p_est_for_PEC"]

p = np.array([r["p_actual"] for r in rows])
un = np.array([r["unmitigated"] for r in rows])
pec = np.array([r["pec"] for r in rows])
pec_err = np.array([r["pec_std"] for r in rows])
nep = np.array([r["nepec"] for r in rows])
nep_err = np.array([r["nepec_std"] for r in rows])

# ----- reproduce the Fig. 2 plot -----
fig, ax = plt.subplots(figsize=(6.5, 4.5))
ax.axhline(ideal, color="black", linestyle="-", label=f"Ideal value ({ideal:.2f})")
ax.axvline(p_est, color="gray", linestyle=":", alpha=0.6, label=f"Estimated noise (p={p_est})")
ax.plot(p, un, color="tab:blue", marker="o", label="Unmitigated")
ax.errorbar(p, pec, yerr=pec_err, color="tab:red", marker="s",
            capsize=3, label=f"PEC (assuming p={p_est})")
ax.errorbar(p, nep, yerr=nep_err, color="tab:green", marker="^",
            capsize=3, label="NEPEC (noise-agnostic, S={1,51})")
ax.set_xlabel("Actual noise level p_actual")
ax.set_ylabel("Expectation value  <|0><0|>")
ax.set_ylim(0.7, 1.3)
ax.set_title("Independent replication — Fig. 2 of arXiv:2108.02237\n"
             f"(depth-14 single-qubit RB circuit, {data['num_samples_per_point']} PEC samples/point)")
ax.legend(loc="lower left", fontsize=9)
ax.grid(True, alpha=0.3)
fig.tight_layout()
outpng = evidence / "fig2_replication.png"
fig.savefig(outpng, dpi=140)
print(f"[info] wrote {outpng}")

# ----- quantitative comparison -----
abs_bias_un = np.abs(un - ideal)
abs_bias_pec = np.abs(pec - ideal)
abs_bias_nep = np.abs(nep - ideal)

# Metrics defined pairwise against the paper's qualitative claims:
#   Q1: Unmitigated <A> decreases monotonically with p_actual.
#   Q2: PEC(p_est=0.01) hits <A>=1 (within its shot-noise CI) at p_actual=0.01
#       and is biased on both sides.
#   Q3: NEPEC noise-agnostic S={1,51} is closer to 1 than Unmit across the full
#       noise range on average.

q1_monotone = bool(np.all(np.diff(un) <= 1e-3))  # allow tiny numerical noise

idx_match = np.argmin(np.abs(p - p_est))
pec_at_match_close_to_1 = bool(abs(pec[idx_match] - ideal) <= 2 * pec_err[idx_match] + 0.05)
# PEC bias should be *larger* at the edges than at the match point (mismatch penalty)
pec_max_edge_bias = max(abs_bias_pec[0], abs_bias_pec[-1])
pec_match_bias = abs_bias_pec[idx_match]
pec_mismatch_hurts = bool(pec_max_edge_bias > pec_match_bias)

# NEPEC should on average be closer to 1 than Unmit across the sweep.
mean_bias_un = float(abs_bias_un.mean())
mean_bias_pec = float(abs_bias_pec.mean())
mean_bias_nep = float(abs_bias_nep.mean())
nepec_beats_unmit_on_avg = bool(mean_bias_nep < mean_bias_un)

# NEPEC should also be more robust than PEC when p_actual != p_est
mask_mismatch = np.abs(p - p_est) > 1e-4
mean_pec_mismatch = float(abs_bias_pec[mask_mismatch].mean())
mean_nep_mismatch = float(abs_bias_nep[mask_mismatch].mean())
nepec_beats_pec_on_mismatch = bool(mean_nep_mismatch < mean_pec_mismatch)

verdict = {
    "paper": data["paper"],
    "figure": data["figure"],
    "num_samples_per_point": data["num_samples_per_point"],
    "ideal_expectation_value": ideal,
    "p_est_for_PEC": p_est,
    "abs_bias_summary": {
        "unmitigated_per_p": [float(x) for x in abs_bias_un],
        "pec_per_p": [float(x) for x in abs_bias_pec],
        "nepec_per_p": [float(x) for x in abs_bias_nep],
        "mean_unmitigated": mean_bias_un,
        "mean_pec": mean_bias_pec,
        "mean_nepec": mean_bias_nep,
        "mean_pec_when_p_mismatch": mean_pec_mismatch,
        "mean_nepec_when_p_mismatch": mean_nep_mismatch,
    },
    "qualitative_checks": {
        "Q1_unmit_monotone_decreasing": q1_monotone,
        "Q2_PEC_hits_ideal_at_matched_noise": pec_at_match_close_to_1,
        "Q2b_PEC_mismatch_bias_grows_at_edges": pec_mismatch_hurts,
        "Q3_NEPEC_better_than_unmit_on_average": nepec_beats_unmit_on_avg,
        "Q4_NEPEC_beats_PEC_on_noise_mismatch": nepec_beats_pec_on_mismatch,
    },
}
(evidence / "verdict.json").write_text(json.dumps(verdict, indent=2))

lines = [
    "Quantitative replication summary (arXiv:2108.02237 Fig. 2):",
    f"  N samples per point = {data['num_samples_per_point']}, ideal = {ideal:.4f}",
    f"  mean |bias|  Unmit = {mean_bias_un:.4f}   PEC = {mean_bias_pec:.4f}   NEPEC = {mean_bias_nep:.4f}",
    f"  on p mismatch:  PEC = {mean_pec_mismatch:.4f}   NEPEC = {mean_nep_mismatch:.4f}",
    "",
    "Qualitative claims:",
    f"  Q1 Unmit monotonically decreases with p_actual                 : {q1_monotone}",
    f"  Q2 PEC hits ideal (within CI) at p_actual == p_est             : {pec_at_match_close_to_1}",
    f"  Q2b PEC mismatch bias larger at edges than at match            : {pec_mismatch_hurts}",
    f"  Q3 NEPEC on average closer to ideal than Unmit                 : {nepec_beats_unmit_on_avg}",
    f"  Q4 NEPEC beats PEC when p_actual != p_est (robustness claim)   : {nepec_beats_pec_on_mismatch}",
]
(evidence / "verdict.txt").write_text("\n".join(lines) + "\n")
print("\n" + "\n".join(lines))
