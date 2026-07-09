# LUCID100 slot 47 (Wave 5) — Low-Dose Fractionated Radiation in HNSCC patient fibroblasts

**Paper:** Winiarska G, Rutkowski T, Gądek A, Fidyk W, Głowala-Kosińska M, Kacorzyk U, Składowski K, Słonina D.
*Radiobiological Effects of Low-Dose Radiation in Normal Fibroblasts of Patients with Head and Neck Cancer Treated with Induction Chemotherapy Combined with Low-Dose Fractionated Radiation.*
*International Journal of Molecular Sciences* 27(6):2525, 2026.
**DOI:** [10.3390/ijms27062525](https://doi.org/10.3390/ijms27062525) · **PMCID:** PMC13027110 · OA cc-by-4.0

**Master row:** `LUCID100_SOLID_MASTER_QA.tsv` row 101 (rank 78, Wave 5, tier A).

## TL;DR (verdict)

**FEASIBLE & PASS** for a partial computational replication. The paper exposes:

- **Table 1** — 40-patient × 9-dose clonogenic survival matrix (raw means + SEMs).
- **Table 2** — published nonlinear-LS fit parameters (induced-repair + LQ) with 95% CIs for 6 HRS+ patients.
- **Table 3** — 40-patient × 8-condition chemopotentiation matrix (LDFR vs single 2 Gy, ± carboplatin, ± paclitaxel).

We refit both **LQ** (Eq. 1) and **induced-repair / IR** (Eq. 2; Joiner 1996) by SEM-weighted nonlinear least-squares (scipy `curve_fit`, trust region) to Table 1 and compare to the paper's Table 2 parameter CIs. We also reproduce the paper's central narrative claims from Table 3 with Mann-Whitney U and paired Wilcoxon.

| Smoke | Result |
|---|---|
| `scripts/lq_ir_smoke.py` — refit LQ + IR vs Table 2 | **PASS** — 27/36 (75%) parameters inside 95% CI; every HRS+ patient ≥ 3/6 in CI |
| `scripts/table3_stats_smoke.py` — narrative claims | **PASS** — paired Wilcoxon SF(4×0.5 Gy) vs SF(2 Gy): p = 0.65 (paper: "similar"); all four ER-by-HRS Mann-Whitney tests p > 0.05 (paper: HRS independent) |
| `scripts/plot_fig1_replication.py` — replot Fig. 1 | **PASS** — `artifacts/fig1_replication.png` |

All runs complete in well under 5 s on CherryRd (Python 3.13 + numpy + scipy + matplotlib). **No heavy compute required, no job plan needed.**

## Worktype retag — IMPORTANT

Master TSV row 101 worktype is `simulation/model replication`. This is **partly correct, partly wrong**:

- The paper is **primarily wet-lab** (skin biopsy → primary fibroblast cultures → 6 MV X-ray clonogenic survival flow-cytometry assay → immunofluorescence pATM and γH2AX foci scoring).
- The **only** computational/modeling content is the LQ + IR nonlinear-LS fitting in §4.5 used to classify HRS+ vs HRS− patients (Table 2, Figure 1).
- There is **no Monte Carlo / track-structure / cell-by-cell simulation** of the kind implied by the master TSV theme `computational model / simulation`.

**Recommended retag:** `simulation/model replication` → **`wet-lab clonogenic + LQ/IR model-fit replication`**. Keep tier A — the in-paper data tables are dense enough to support a real model-fit replication, which we have already done.

## Repository layout

```
lucid100-lowdose-fractionated-hnc-fibroblasts/
├── README.md                         this file
├── PROGRESS.md                       chronological log
├── FIRST_PASS_REPORT.md              verdict + evidence
├── ARTIFACT_MANIFEST.tsv             every artifact with sha256
├── artifacts/
│   ├── crossref.json                 DOI metadata
│   ├── europepmc_search.json         OA confirmation
│   ├── europepmc_fullText.xml        JATS source
│   ├── europepmc_PMC13027110.pdf     5-p cover PDF (MDPI source PDF Cloudflare-blocked)
│   ├── europepmc_supplementaryFiles.zip   wraps the MDPI s001 supplement
│   ├── supp_unzipped/
│   │   ├── ijms-27-02525-s001.zip
│   │   └── ijms-4167211-supplementary.pptx   Figs S1, S2 (per-patient kinetics)
│   ├── paper_abstract.txt
│   ├── paper_full_body.txt           Methods/Results/Discussion/Statistical Analysis
│   ├── paper_tables.md               Tables 1–3 as markdown
│   ├── paper_figs.md                 Figures 1–8 captions
│   ├── table1_singledose_SF.csv      360-row tidy CSV (40 patients × 9 doses)
│   ├── table3_chemopotentiation.csv  320-row tidy CSV (40 patients × 8 conditions)
│   ├── fig1_replication.png          replotted Figure 1
│   ├── lq_ir_smoke_output.txt        canonical smoke output
│   └── table3_stats_smoke_output.txt canonical smoke output
└── scripts/
    ├── extract_table1.py
    ├── extract_table3.py
    ├── lq_ir_smoke.py                ← main quantitative smoke (LQ + IR)
    ├── table3_stats_smoke.py         ← Table 3 narrative smoke
    └── plot_fig1_replication.py
```

## How to reproduce

```bash
cd lucid100-lowdose-fractionated-hnc-fibroblasts
python3 scripts/extract_table1.py      # writes artifacts/table1_singledose_SF.csv
python3 scripts/extract_table3.py      # writes artifacts/table3_chemopotentiation.csv
python3 scripts/lq_ir_smoke.py         # PASS: 27/36 params inside paper 95% CI
python3 scripts/table3_stats_smoke.py  # PASS: paired Wilcoxon + MW-U match paper claims
python3 scripts/plot_fig1_replication.py
```

Required Python packages: `numpy`, `scipy`, `matplotlib` (all in the standard CherryRd scientific Python env).

## Data availability per the paper

- Funded by Polish National Science Center grant 2020/39/O/NZ5/02625.
- Ethics approval: KB/430-106/19 (19 Nov 2019), MSC National Research Institute of Oncology, Gliwice.
- Data Availability Statement: *"All data generated and analyzed during this study are included in this article."* No GEO/SRA/figshare/Zenodo/Dryad deposits. Per-patient raw DPM, foci counts per nucleus, and per-fraction time-course data are **not** released; aggregated means±SEM are available in Tables 1 and 3 and the per-patient kinetic plots are in Supplementary Figure S1 (as embedded WMF — not directly digitizable).
- **No author contact attempted** (per task rule). No paid endpoints used.

## What would extend this replication

| Effort | Cost | Value |
|---|---|---|
| WebPlotDigitizer of Figs 5–8 to get per-patient pATM/γH2AX foci max + residual values | ~2–4 h | Allows reproducing the foci-vs-survival correlations and the per-patient HRS vs foci scatter |
| WebPlotDigitizer of Supp Fig S1 (per-patient kinetics) | ~1 d (36 patients × 4 conditions) | Enables a DSB repair-kinetic two-exponential refit |
| Wet-lab re-run | months, IACUC + clinical-trial scope | Out of scope |
| Author contact for per-nucleus foci CSVs | excluded by task rule | — |
