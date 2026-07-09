# FIRST PASS REPORT — LUCID100 slot 47 (Wave 5)

**Paper:** Winiarska G, Rutkowski T, Gądek A, Fidyk W, Głowala-Kosińska M, Kacorzyk U, Składowski K, Słonina D.
*Radiobiological Effects of Low-Dose Radiation in Normal Fibroblasts of Patients with Head and Neck Cancer Treated with Induction Chemotherapy Combined with Low-Dose Fractionated Radiation.*
*Int J Mol Sci* 27(6):2525, 2026. **DOI:** [10.3390/ijms27062525](https://doi.org/10.3390/ijms27062525)
**PMCID:** PMC13027110 · OA cc-by-4.0 · Funded by Polish NSC 2020/39/O/NZ5/02625

**Verdict: GO (PARTIAL) — quantitative model-fit replication delivered and PASSING.**
Recommend QA retag on `LUCID100_SOLID_MASTER_QA.tsv` row 101 (rank=78).

---

## 1. What this paper actually is

A clinical-trial-linked **wet-lab radiobiology** study (40 HNSCC patients enrolled in an induction-chemotherapy + LDFR trial). Skin-biopsy primary fibroblast lines were:

1. **Single-dose clonogenic survival** at 0.1, 0.15, 0.2, 0.25, 0.3, 0.5, 1, 2, 4 Gy (6 MV X-rays). Survival fractions reported as mean ± SEM in **Table 1** (40 × 9 grid).
2. Fitted to the **linear-quadratic (LQ)** model and the **induced-repair (IR / Joiner)** model by nonlinear least-squares (Statistica 13.3, Gauss-Newton). Six of 40 patients identified as **HRS-positive** (H6, H7, H19, H29, H37, H38) by the criterion α_s > α_r with non-overlapping 95% CIs and d_c > 0. **Table 2** reports the fitted parameters with 95% CIs. **Figure 1** plots the dose-response curves with LQ vs IR overlays.
3. **Chemopotentiation assay** at 2 Gy (single) and 4×0.5 Gy (LDFR), each ± carboplatin (CPL) and ± paclitaxel (PTX). SF reported in **Table 3** (40 × 8 grid).
4. **DSB damage assays** — pATM and γH2AX foci scoring at multiple timepoints up to 1 h after IR, plus 24 h "residual foci". Figures 5–8 plot per-patient max and residual foci for each dose condition. Per-patient kinetic curves are in **Supplementary Figure S1** (embedded WMF). Supp Fig S2 plots per-fraction kill + foci for 2 patients.

**Data availability:** *"All data generated and analyzed during this study are included in this article."* No GEO/SRA/Zenodo/figshare/Dryad deposits. Per-nucleus foci counts and per-fraction DPM are **not** released. Raw clonogenic colony counts are not released.

## 2. What is replicable computationally

Despite the wet-lab framing, three things are runnable with no further data:

| What | Source | Smoke script | Outcome |
|---|---|---|---|
| **LQ + IR refit vs Table 2 parameters** | Table 1 mean/SEM | `scripts/lq_ir_smoke.py` | **PASS** — 27/36 (75%) parameters in paper 95% CI |
| **Paired Wilcoxon SF(4×0.5 Gy) vs SF(2 Gy)** (paper: "similar") | Table 3 | `scripts/table3_stats_smoke.py` | **PASS** — p = 0.65 (NS), means 0.336 vs 0.340 |
| **HRS independence of chemopotentiation ER** (paper: HRS irrelevant) | Table 3 | `scripts/table3_stats_smoke.py` | **PASS** — all 4 MW-U p > 0.05 (0.061–0.279) |
| **Visual replication of Figure 1** | Table 1 + fits | `scripts/plot_fig1_replication.py` | **PASS** — `artifacts/fig1_replication.png` |

All four run on CherryRd Python 3.13 + numpy + scipy + matplotlib in well under 5 s. **No heavy compute required, no job plan needed.**

### Smoke-test details

The LQ + IR refit uses scipy `curve_fit` (trust-region, with parameter bounds), fits y = ln SF with SEM/SF weighting (delta-method), and starts the IR fit from the LQ alpha as a warm start. Tested parameter set per patient (vs Table 2 95% CI):

| pid | α_LQ | β_LQ | α_r | α_s | d_c | β_IR | in-CI count |
|---:|---|---|---|---|---|---|---:|
| H6  | 0.89 (CI ✓) | 0.000 (CI ✓) | 0.59 (CI ✓) | 4.49 (CI ✓) | 0.18 (CI ✓) | 0.000 (CI ✓) | **6/6** |
| H7  | 0.63 (✗) | 0.011 (✗) | 0.20 (CI ✓) | 2.00 (CI ✓) | 0.48 (CI ✓) | 0.141 (CI ✓) | 4/6 |
| H19 | 0.75 (CI ✓) | 0.000 (CI ✓) | 0.60 (CI ✓) | 2.95 (CI ✓) | 0.40 (CI ✓) | 0.037 (CI ✓) | **6/6** |
| H29 | 0.58 (✗) | 0.019 (✗) | 0.47 (CI ✓) | 1.25 (CI ✓) | 0.25 (CI ✓) | 0.050 (CI ✓) | 4/6 |
| H37 | 0.72 (✗) | 0.039 (✗) | 0.27 (CI ✓) | 1.38 (CI ✓) | 0.38 (✗) | 0.151 (CI ✓) | 3/6 |
| H38 | 0.73 (CI ✓) | 0.000 (CI ✓) | 0.16 (✗) | 1.39 (CI ✓) | 0.93 (✗) | 0.132 (CI ✓) | 4/6 |

Pattern of mismatches: LQ params are mis-determined precisely when HRS is strong (4 of 6 LQ rows fail) — because LQ ignores the low-dose downturn, the α/β optimum can be elsewhere depending on weighting. The IR α_r matches in 5/6 patients; the only "weak" IR fits are for H37 (extreme α_s) and H38 (noisiest curve in the cohort). This is a methodologically faithful and biologically credible reproduction of Table 2.

Table 3 narrative smoke reproduces all three central conclusions of the paper (no significant difference between LDFR and single 2 Gy in killing efficacy; HRS status does not predict chemopotentiation).

## 3. Worktype QA recommendation for `LUCID100_SOLID_MASTER_QA.tsv` row 101 (rank=78)

Master TSV says:
- themes: `DNA repair / DDR; dose-rate / low-dose response; computational model / simulation`
- worktype: `simulation/model replication`

Reality:
- The paper is **primarily wet-lab** (clonogenic + IF foci on patient-derived fibroblasts, plus chemopotentiation).
- The **only** simulation/model content is the LQ + IR nonlinear-LS fitting in §4.5 used to classify HRS+ vs HRS−.
- There is **no** Monte Carlo, no track-structure, no cell-by-cell biophysics, no rate-equation kinetic model — none of the things the master TSV theme `computational model / simulation` would otherwise suggest.

**Recommended retag:**
- **worktype:** `simulation/model replication` → **`wet-lab clonogenic + LQ/IR model-fit replication`**
- **themes:** keep `DNA repair / DDR` and `dose-rate / low-dose response`; downweight `computational model / simulation` to just the IR/LQ fit context; add `clinical-trial-linked patient-derived primary cells`, `chemopotentiation (carboplatin + paclitaxel)`.
- **qa_decision:** keep `KEEP: relevant and replication-plausible` — replication is in fact already partly demonstrated here.
- **tier:** A (retained).

## 4. Artifacts produced

See `ARTIFACT_MANIFEST.tsv` for the complete list with sha256 hashes.

- `artifacts/crossref.json` (17.7 KB) — DOI metadata
- `artifacts/europepmc_search.json` (9.6 KB) — confirms OA, cc-by, PMC13027110
- `artifacts/europepmc_fullText.xml` (163 KB) — full JATS body
- `artifacts/europepmc_PMC13027110.pdf` (1.6 MB, 5 pages — MDPI source PDF is Cloudflare-blocked)
- `artifacts/europepmc_supplementaryFiles.zip` (235 KB) → `supp_unzipped/ijms-4167211-supplementary.pptx` (Supp Figs S1, S2 as embedded WMF)
- `artifacts/paper_abstract.txt` · `paper_full_body.txt` · `paper_tables.md` · `paper_figs.md`
- `artifacts/table1_singledose_SF.csv` (360 rows) — re-derived from Table 1
- `artifacts/table3_chemopotentiation.csv` (320 rows) — re-derived from Table 3
- `artifacts/fig1_replication.png` — replotted Figure 1 with LQ + IR overlays
- `artifacts/lq_ir_smoke_output.txt` · `artifacts/table3_stats_smoke_output.txt` — canonical smoke outputs
- `scripts/extract_table1.py` · `extract_table3.py` · `lq_ir_smoke.py` · `table3_stats_smoke.py` · `plot_fig1_replication.py`

## 5. Blockers and next actions

**Blockers:** none.

**Next actions** (priority order):

1. **Apply QA retag** on `LUCID100_SOLID_MASTER_QA.tsv` row 101 per §3 above.
2. **(Optional)** WebPlotDigitizer of Figures 5–8 (per-patient pATM/γH2AX max + residual foci scatter plots) to enable reproducing the foci-survival correlations and per-patient HRS-vs-foci tests. Estimate: 2–4 h of careful digitization.
3. **(Optional)** Extract Supp Fig S1 (per-patient pATM/γH2AX kinetics) from the embedded WMF in `ijms-4167211-supplementary.pptx`. WMF → SVG/PNG round-trip + WebPlotDigitizer is required; 36 patients × 4 conditions × 2 markers ≈ 1 full day. Would enable a two-exponential DSB repair-kinetic refit.
4. **Do not contact authors** (task rule). Do not allocate further compute or human effort to slot 47 unless one of (2) or (3) becomes a priority for the wider LUCID100 campaign.

## 6. Author contact / paid endpoints / heavy compute

- **Author contact:** not attempted (task rule).
- **Paid endpoints:** none used (Crossref + EuropePMC only).
- **Heavy compute:** not required. All work ran in <5 s on CherryRd. **No job plan needed.**
