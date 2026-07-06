# Artifact Manifest — LUCID100 Wave 1, Slot 9

**Paper:** Wang, Li, Qiu, Chen, Wu, Zhang, Li.
*Modelling of Cellular Survival Following Radiation-Induced DNA Double-Strand Breaks.*
Scientific Reports **8**:16202 (2018). DOI: 10.1038/s41598-018-34159-3.

**Harvest date:** 2026-06-09 (CDT). **Harvester:** subagent slot 9.

## Primary artifacts (locally held)

| Path | Kind | SHA-256 | Source | Notes |
| --- | --- | --- | --- | --- |
| `artifacts/paper.pdf` | PDF | `429bf7d8bc5b767b9d39da63031a281f3c6994d11414a60b99f604ebae43a92a` | Copied from `~/Dropbox/XFER/LUCID-replication-targets/1d5ad1b1274b89f661610a9863c4ff81784e0f1c.pdf` (LUCID curated drop) | Full main text, 12 pp + refs. CC-BY 4.0. |
| `code/wang2018_dsb_survival.py` | Python script | (generated, see file) | Original reimplementation by this slot | Self-contained Eqs. 1-20, Table 1 best-fit params. |
| `smoke_test.json` | JSON | (regenerated each run) | `python3 code/wang2018_dsb_survival.py --out-dir .` | Numerical outputs of smoke test. |
| `figures/sf_HSG.png` | PNG | (regenerated) | smoke test | Qualitative survival curves, HSG, X-ray / C-12 50 / C-12 200 keV/um. |
| `figures/sf_V79.png` | PNG | (regenerated) | smoke test | Qualitative survival curves, V79, same conditions. |
| `figures/alpha_beta_vs_LET.png` | PNG | (regenerated) | smoke test | alpha/beta vs LET (qualitative Fig. 6 shape). |
| `figures/rbe10_vs_LET.png` | PNG | (regenerated) | smoke test | RBE_10% vs LET (qualitative Fig. 5 shape). |

## External dependencies needed for STRICT replication (not bundled)

| Resource | Used for | Access |
| --- | --- | --- |
| **MCDS** (Monte Carlo Damage Simulation), Stewart et al. 2008, 2011 (refs 33-34) | Computes Y(LET, particle) and lambda(LET, particle), the two physical inputs of Eqs. (5)-(6). | Free academic source from Robert Stewart group, University of Washington (https://faculty.washington.edu/trawets/mcds/). Requires download form, no payment. |
| **PIDE database** v3.2+, Friedrich et al. 2013 / 2021 (ref. 37) | Source of all experimental (alpha, beta, D10, SF) data used as fitting and validation targets. | Free academic access on request from GSI: https://www.gsi.de/work/forschung/biophysik/forschungsfelder/radiobiological_modelling/pide_project — registration form, no payment. |
| **Furusawa 2000** (ref. 38) | Primary fit dataset: 54 HSG + 52 V79 cell-survival curves for X-ray, He-3, C-12, Ne-20 ions. Most data are already in PIDE. | Paywalled at Radiat. Res. 154:485 (2000). Subset available via PIDE. |
| **Supporting per-experiment papers** refs 39-57 | Validation only: V79 SF curves for protons, He, N, O, Fe ions at additional LETs (Fig. 3c-d, Fig. 5). | All available via PIDE; primary papers paywalled. |

## What is NOT available

- **No code repository** — the paper has no GitHub / Zenodo / supplementary code link. Only descriptive equations.
- **No supplementary material** — Scientific Reports record shows the article only; no SI tables or extra data files. Confirmed by inspection of the PDF (no "Supplementary" section).
- **No deposited data** — neither model fits nor MCDS outputs nor digitized SF points are deposited. They must be regenerated from MCDS + PIDE.

## Table 1 (paper) — verbatim best-fit parameters

| Parameter | HSG | V79 |
| --- | --- | --- |
| mu_x | 0.9817 +/- 0.0056 | 0.9568 +/- 0.0236 |
| mu_y | 0.0891 +/- 0.0068 | 0.0300 +/- 0.0177 |
| zeta | 0.1025 +/- 0.0065 | 0.0412 +/- 0.0209 |
| xi   | 0.0572 +/- 0.0027 | 0.0608 +/- 0.0381 |
| eta(lambda_p -> 1)   | (7.26 +/- 0.04) x 10^-4 | (9.78 +/- 0.10) x 10^-4 |
| eta(lambda_p -> inf) | 0.0022 +/- 0.0001 | 0.0065 +/- 0.0001 |

Encoded as constants in `code/wang2018_dsb_survival.py` (`HSG` and `V79` instances of `CellParams`).

## Equations implemented

All equations 1-20 of the paper are coded literally in `code/wang2018_dsb_survival.py`:

- Eq. (1) `N = Y * D`
- Eq. (2) `n = pi * R^2 * D * rho / (LET * 1.602e-19) * 1e-18` — `n_particles_per_nucleus`
- Eqs. (5),(6) `np`, `lambda_p` — `np_and_lambda_p`
- Eq. (8) eta(lambda_p) ramp — `eta_of_lambda_p`
- Eqs. (7),(9),(10),(11),(13) — `n_death`
- Eqs. (14),(15) S = exp(-Ndeath) — `survival`
- Eqs. (18),(19) LQ-form alpha, beta — `alpha_beta_LQ`
- Eq. (20) alpha/beta via Eqs. 18/19 (computed in summary table).

## Figures and tables in the paper (for digitization plan)

| Item | What it shows | Replication accessibility |
| --- | --- | --- |
| Fig. 1 | Y, lambda, lambda_p vs LET, human nucleus, proton/He-3/C-12/Ne-20 | Needs MCDS run. |
| Table 1 | Best-fit parameters for HSG and V79 | **Already verbatim above.** |
| Fig. 2a-f | Observed vs modelled alpha, beta, and X-ray SF curves, HSG and V79 | Needs PIDE + Furusawa 2000 alpha/beta. |
| Fig. 3a-d | SF curves for HSG, V79 vs C-12 at several LETs and V79 vs H-1, He-4, N-14, Fe-56 | Needs PIDE for experimental points; MCDS for Y(LET); model curves regenerable here. |
| Fig. 4a-h | Observed vs modelled D10 and RBE at 10%, 50%, 5% survival, HSG and V79 | PIDE + MCDS. |
| Fig. 5    | V79 RBE_10 vs LET across many particle species | PIDE + MCDS. |
| Fig. 6    | alpha/beta vs LET for HSG and V79 | PIDE + MCDS. |
| Fig. 7a-d | HSG vs V79 D10, RBE_10, P_track and P_contribution under C-12 | MCDS + this code. |

See `FIRST_PASS_REPORT.md` for the strict replication plan.
