# Replication design — Plodowska 2025 (U2OS VLDR gamma DDR)

## What is replicable on a single workstation

| Endpoint | Replication path | Feasible without PDF? | Feasible with PDF? |
| --- | --- | --- | --- |
| 53BP1 foci kinetics (AD-only, CD-only, AD+CD; ± KU-55933) | Two-component induction+repair model (`code/foci_kinetics.py`), parameters from Fig 1/2 digitisation, residuals & RMSE table. | **No** (need digitised data points). | **Yes** — partial. |
| Cell-cycle G2 block (± KU-55933) | Reproduce stacked-bar G1/S/G2 fractions vs condition; chi-squared on condition × phase contingency. | No | Yes — partial; can re-express published bars; no raw FCS. |
| Gene-expression panel | Re-tabulate Δ vs control with author-supplied table (likely `mmc1.xlsx`); reproduce any heatmap with row z-score. | No | Yes — partial; signature replication contingent on table format. |
| Wet-lab reproduction | Out of scope — needs gamma source @ 31/55 µGy/h, U2OS, KU-55933, IF facility. | No | No (this replication folder). |

## Why a computational scaffold is worth seeding now

LUCID100 prior art established the same kinetic backbone used here:

- `lucid-autofoci-detection` (rank 2) — Lengert/Mirsch 2018 foci-counting/modelling.
- `lucid-mariotti-split-dose-gamma-h2ax` — γH2AX split-dose model fit (REPLICATED with 7/10 coverage); confirms the induction + first-order resolution form is sufficient at the per-cell-mean level.
- `lucid-dna-repair-kinetics-doserate-rbe` — dose-rate dependence of repair kinetics.

The 53BP1 chronic model used here is:
- During VLDR exposure of length T:  N(t) = (R/k) (1 − exp(−k t)).
- Post-exposure:                     N(t>T) = N(T) exp(−k (t−T)).
- Acute CD impulse:                  N(t≥t0) = Y_acute exp(−k (t−t0)).

For the Plodowska doses (5.9 mGy @ 31 µGy/h → T ≈ 190 h; 10.5 mGy @ 55 µGy/h → T ≈ 191 h), with literature defaults (Y=35 foci/Gy, k=0.45/h), steady-state mean 53BP1 foci during AD is ~0.0024 and ~0.0043 per cell respectively — i.e. *the AD alone produces sub-foci-per-cell mean levels*, which is consistent with the paper's claim that the response is weak yet measurable, and with the well-known result that VLDR exposures sit at the noise floor of the foci assay. The CD impulse contributes ~35 foci/cell peak, dwarfing the AD baseline — so the AD+CD vs CD comparison is what carries the scientific weight in the paper.

## KU-55933 modelling handle

The paper's two non-trivial qualitative results are:

1. **KU does not block AD-only foci induction** → ATM is not the kinase responsible at VLDR; some other PIKK (DNA-PKcs or ATR) is paying the bill. Modeled as `AD_yield_factor ≈ 1.0` in the scaffold.
2. **KU partly blocks CD-only induction** → expected ATM-dependent component for acute 1 Gy. Modeled as `CD_yield_factor ≈ 0.3-0.5` (placeholder 0.40 in scaffold; refit from digitised Fig).
3. **KU potentiates G2 block in AD+CD** → captured outside the foci model; reproduced from the bar chart once digitised.

## Next-pass minimal deliverables (after PDF acquisition)

- `data/paper.pdf`
- `supplementary/mmc*.{docx,xlsx,pdf}`
- `data/digitized_fig1.csv` … `data/digitized_fig3.csv` (WebPlotDigitizer; one row per (condition, time_h, foci_mean, foci_sd)).
- `code/fit_kinetics.py` (wires `scipy.optimize.curve_fit` over `chronic_N`, `acute_N`, `ad_then_cd_curve`).
- `results/kinetic_fits.csv` (per-condition fitted Y, k, RMSE).
- `figures/fig1_replication.png`, `figures/fig2_replication.png`, `figures/fig3_replication.png`.
- `REPORT.md` — verdict (REPLICATED / PARTIAL / NO-GO) with coverage/agreement scores in the LUCID house format (out of 10).

## Compute envelope

All work fits on CherryRd (≪1 CPU·min per fit). No HPC plan needed.
