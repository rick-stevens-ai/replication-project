# Modelling of Cellular Survival Following Radiation-Induced DNA Double-Strand Breaks

## LUCID100 curated Wave 1 — Slot 9 replication

- **Rank:** 40 (Wave 1, Tier A, priority score 20)
- **DOI:** [10.1038/s41598-018-34159-3](https://doi.org/10.1038/s41598-018-34159-3)
- **Year / venue:** 2018 / *Scientific Reports* **8**:16202
- **Authors:** Wang, Li, Qiu, Chen, Wu, Zhang, Li (Tsinghua / Nuctech)
- **Themes:** DNA repair / DDR; radiation quality / RBE; computational model / simulation
- **Worktype:** simulation/model replication
- **QA decision:** KEEP — relevant and replication-plausible
- **First-pass verdict (2026-06-09):** **GREEN — replicable, partial reimplementation already runs.** See `FIRST_PASS_REPORT.md`.

## Quick start

```bash
python3 code/wang2018_dsb_survival.py --out-dir .
```

This regenerates `smoke_test.json` and the four qualitative figures in `figures/`. Pure-Python; needs only NumPy and Matplotlib.

## Layout

```
artifacts/paper.pdf            local source PDF (CC-BY 4.0)
code/wang2018_dsb_survival.py  reimplementation of Eqs. 1-20 + smoke test
data/                          (empty; will hold MCDS / PIDE inputs)
figures/                       smoke-test PNGs (SF, alpha/beta, RBE)
smoke_test.json                numerical smoke-test outputs
ARTIFACT_MANIFEST.md           full file inventory + external deps
FIRST_PASS_REPORT.md           verdict + scope + acceptance criteria + plan
PROGRESS.md                    chronological progress log
README.md                      this file
```

## What's in scope

A mechanistic DSB-survival model with **2 physical inputs** (`n_p`, `lambda_p` from MCDS) and **6 biological fit parameters** per cell type. The paper supplies the fit values (Table 1) for HSG and V79 cells; this folder reimplements the equations literally and demonstrates that they reproduce the paper's qualitative behaviour.

| Quantity | Where it comes from |
| --- | --- |
| `Y(LET, particle)` DSBs/cell/Gy | MCDS (Stewart 2008/2011) - free academic code |
| `lambda(LET, particle)` DSBs/track | MCDS |
| `mu_x, mu_y, zeta, xi, eta(1), eta(inf)` | Table 1 of Wang 2018 - HSG and V79 |
| Experimental SF, alpha, beta | PIDE database (free, GSI registration) |

## Artifact harvest checklist

- [x] Source PDF saved locally (`artifacts/paper.pdf`, sha256 `429bf7d8...43a92a`)
- [x] Full text extracted and reviewed
- [x] Supplementary files searched (none exist - confirmed)
- [x] Code repository searched (none exists - confirmed)
- [x] External dependencies identified (MCDS + PIDE, both free)
- [x] Environment plan written (`FIRST_PASS_REPORT.md` section 7)
- [x] Acceptance metrics defined (`FIRST_PASS_REPORT.md` section 8)
- [x] Blockers listed explicitly (`FIRST_PASS_REPORT.md` section 6)

## Execution checklist

- [x] Smoke test / minimal calculation (`code/wang2018_dsb_survival.py`)
- [ ] Pull PIDE subset for HSG / V79 (requires GSI registration)
- [ ] Pull MCDS Y / lambda tables (Stewart 2011 supplement or run MCDS)
- [ ] Staged re-fit `fit_table1.py` to verify Table 1
- [ ] Regenerate Figs. 2, 3, 5, 6 with real inputs
- [ ] Logs, hashes, environment, provenance captured (partial)
- [ ] Final `REPORT.md` written

## Key claim (one line)

A six-parameter analytic NHEJ-based DSB model recovers the LQ form at low LET, predicts cell survival vs dose for HSG and V79 cells across photon, He-3, C-12, Ne-20 (and validated against H-1, He-4, N-14, O-16, Fe-56) ions over LET 0.3-1000 keV/um, and reproduces the rising-then-falling RBE_10 vs LET with a peak near 100-200 keV/um.

## Smoke-test result

Run on CherryRd 2026-06-09. From the model + Table 1 verbatim:

- Eq. 15 -> Eq. 17 LQ form within ~1% at proton 2 keV/um (consistency check passes).
- HSG / V79 X-ray alpha/beta ratios 3.8 / 4.3 Gy (right order of magnitude).
- RBE_10% (V79) peaks at 100 keV/um with RBE = 4.6 (matches Fig. 5 shape).
- All four qualitative figures reproduced (`figures/`).

Full numerical strict replication will follow once PIDE and MCDS inputs are loaded; effort estimate ~1-2 days, no heavy compute (do not run on uicgpu/Aurora/Sparks - single-CPU job).

## Initial abstract / notes

A mechanistic model of cellular survival following radiation-induced DNA double-strand breaks (DSBs). DSBs are the initial lesions; NHEJ is the dominant repair pathway. Two physical inputs (avg primary particles causing DSB, avg DSBs per such primary) and six biological fit parameters describe the irradiated cell. Calibrated to HSG and V79 survival curves, the model predicts survival for arbitrary particle/LET combinations and RBE at any survival level. See `FIRST_PASS_REPORT.md` for the full first-pass analysis and replication plan.
