# LUCID100 slot 80 (Wave 5) — Fast Neutron / Lymphocyte / Dose-Rate γ-H2AX

**Paper:** Nair S, Engelbrecht M, Miles X, Ndimba R, Fisher R, du Plessis P, Bolcaen J,
Nieto-Camero J, de Kock E, Vandevoorde C. (2019).
*The Impact of Dose Rate on DNA Double-Strand Break Formation and Repair in Human
Lymphocytes Exposed to Fast Neutron Irradiation.*
**Int. J. Mol. Sci.** 20(21): 5350. [doi:10.3390/ijms20215350](https://doi.org/10.3390/ijms20215350)
PMID 31661782 • PMCID PMC6862539 • OA (CC-BY 4.0)

## TL;DR

- **First pass: PASS-low** (3/3 smoke checks reproduced from digitized tables).
- **No supplements, no deposited code/data** (`hasSuppl: N` in EPMC; authors used
  Excel 2013 + GraphPad Prism v5).
- **Worktype retag recommended:** master TSV labels this `simulation/model replication`,
  but it is actually a **wet-lab radiobiology assay** (γ-H2AX immunofluorescence on
  human lymphocytes irradiated with p(66)/Be(40) fast neutrons at iThemba LABS) with
  a **reduced table/curve replication** path (2nd-order polynomial induction fit +
  single-exponential repair half-life).
- **No author contact, no paid endpoints, no heavy compute used or required.**

## What the paper does

1. Whole blood from 4 healthy donors irradiated with p(66)/Be(40) fast neutrons at two
   dose rates: HDR = 0.400 Gy/min, LDR = 0.015 Gy/min.
2. **Induction:** γ-H2AX foci per cell measured 30 min post-IR at 5 doses
   (0.125–2 Gy). Result: HDR yields ~40 % more foci than LDR across doses (Table 1,
   ratios in Table 2). Dose response well fit by a 2nd-order polynomial.
3. **Repair kinetics:** foci followed over 0.5–24 h post 1 Gy. Peak at ~2 h, then
   decay. Repair half-life HDR ≈ 8.6 h, LDR ≈ 12 h (Discussion, p.10). Residual at
   24 h: LDR 1.65 ± 0.46, HDR 1.29 ± 0.45 foci/cell.

## Artifacts harvested

See [`artifacts/MANIFEST.md`](artifacts/MANIFEST.md). Key files:

- `artifacts/paper.pdf` — full OA PDF via Europe PMC (`?pdf=render`), 1.2 MB, 13 pp
- `artifacts/paper_fulltext.xml` — JATS XML full text
- `artifacts/paper.txt` — `pdftotext -layout` extraction
- `data/table1_induction.csv` — 5 doses × HDR/LDR mean/SD foci
- `data/table2_hdr_ldr_ratio.csv` — published per-dose ratios
- `data/table3_repair_kinetics.csv` — 6 time points × HDR/LDR mean/SD foci at 1 Gy
- `data/paper_key_numbers.json` — abstract-level claims for the smoke harness

## Reproducing the smoke check

```bash
cd lucid100-fast-neutron-lymphocyte-dsbs-doserate
python3 scripts/smoke_replicate.py
```

Requires only `numpy` (plus optional `matplotlib` for the figure). Runs in <1 s on
CherryRd. No heavy compute — full work is well within laptop CPU.

Outputs: `scripts/smoke_outputs/smoke_results.json` + `smoke_plots.png`.

## What is NOT covered by the smoke check

- Per-donor variability or the underlying foci-count distributions (paper reports
  only mean ± SD across 4 donors; per-cell data not deposited).
- Statistical p-values (paper used GraphPad Prism v5, methods state ANOVA via
  total sum-of-squares; raw per-cell counts not available to replicate p-values).
- Image-analysis (Metafer / MetaCyte automated foci scoring) — out of scope without
  raw images.
- Dosimetry / neutron physics — separate Monte Carlo enterprise, not the assay
  table replication targeted here.

## Possible next passes (if upgraded from PASS-low → PASS-medium)

1. Email corresponding author (Charlot Vandevoorde, iThemba LABS / now HZDR) for
   per-cell foci CSVs to allow proper non-linear fits + ANOVA — **explicitly
   blocked by task: no author contact.**
2. Build a Monte Carlo damage simulation (MCDS) or PARTRAC mechanistic model of
   p(66)/Be(40) DSB induction vs dose rate, predict the HDR/LDR ratio from first
   principles, and compare to Table 2 — this would be the true "simulation/model"
   workpath the master TSV intended.
3. Rasterize Figures 1–4 with WebPlotDigitizer and compare digitized curve to
   our poly2 fit residuals.

## Status

See [`PROGRESS.md`](PROGRESS.md) and [`FIRST_PASS_REPORT.md`](FIRST_PASS_REPORT.md).
