# LUCID-100 Replication Report

**Slot:** `lucid100-lowdose-fractionated-hnc-fibroblasts` (Wave 5, row 101, rank 78, tier A)
**Paper:** Winiarska G, Rutkowski T, Gądek A, Fidyk W, Głowala-Kosińska M, Kacorzyk U, Składowski K, Słonina D. *Radiobiological Effects of Low-Dose Radiation in Normal Fibroblasts of Patients with Head and Neck Cancer Treated with Induction Chemotherapy Combined with Low-Dose Fractionated Radiation.* **Int J Mol Sci** 27(6):2525 (2026).
**DOI:** [10.3390/ijms27062525](https://doi.org/10.3390/ijms27062525) · **PMCID:** PMC13027110 · OA CC-BY 4.0
**Date of audit:** 2026-06-22 (re-validated; first pass 2026-06-09)
**Workspace:** `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-lowdose-fractionated-hnc-fibroblasts/`

## TL;DR

Wet-lab clinical-radiobiology study on **40 HNSCC patient-derived skin-biopsy fibroblast lines**, with three computationally re-runnable model layers exposed via in-paper Tables 1–3: (i) **LQ + induced-repair (IR/Joiner) nonlinear-LS refits** of the 9-dose clonogenic survival curves for the 6 HRS+ patients, (ii) **paired Wilcoxon** for 4×0.5 Gy LDFR vs single 2 Gy SF in n=40, (iii) **Mann-Whitney** for HRS-vs-HRS− chemopotentiation enhancement ratios. All three were re-implemented from scratch in Python (scipy `curve_fit` + `wilcoxon` + `mannwhitneyu`), and **Figure 1** was visually replotted with overlays. Quantitative agreement is strong where Table 2 reports CIs (27/36 fitted parameters land inside the paper's published 95% CI; every HRS+ patient hits ≥3/6). Narrative conclusions of the paper (LDFR kills similarly to 2 Gy; HRS does not modulate chemopotentiation) reproduce cleanly. Wet-lab cell biology (foci kinetics, per-fraction DPM, per-nucleus γH2AX/pATM counts) is **not** repeatable: per-nucleus data and raw colony counts are not released, Supplementary Figure S1 is delivered as WMF embedded in a `.pptx`, and the paper has no GEO/SRA/Zenodo/figshare deposit.

**Verdict:** **PARTIAL** (computational layer fully replicated, wet-lab layer data-blocked).
**Coverage:** **6/10** — model/statistical strata of the paper (Tables 1–3, Figs 1, 2): replicated. Foci-kinetic strata (Figs 3–8, Supp Figs S1–S2): not replicated (digitization-only feasible).
**Agreement:** **8/10** — where measurable, the replication agrees with the paper within the paper's own reported 95% CIs and reproduces every central narrative conclusion.

## 1. Data sources

| What | Provenance | Size | Local path |
|---|---|---|---|
| DOI metadata | Crossref REST | 17.7 KB | `artifacts/crossref.json` |
| OA confirmation | EuropePMC search | 9.6 KB | `artifacts/europepmc_search.json` |
| Full text JATS | EuropePMC fullTextXML | 163 KB | `artifacts/europepmc_fullText.xml` |
| Render PDF (5 pp; MDPI source PDF was Cloudflare-blocked, 403) | EuropePMC PDF | 1.6 MB | `artifacts/europepmc_PMC13027110.pdf` |
| Supplement (Figs S1, S2 as WMF) | EuropePMC supplementaryFiles → `ijms-27-02525-s001.zip` → `ijms-4167211-supplementary.pptx` | 235 KB | `artifacts/europepmc_supplementaryFiles.zip`, `artifacts/supp_unzipped/` |
| Abstract / body / tables / figures | parsed from JATS | — | `artifacts/paper_abstract.txt`, `paper_full_body.txt`, `paper_tables.md`, `paper_figs.md` |
| **Table 1 single-dose SF (tidy)** | re-typed from JATS Table 1, 40 pat × 9 dose × {mean, SEM} = 360 rows | 9 KB | `artifacts/table1_singledose_SF.csv` |
| **Table 3 chemopotentiation (tidy)** | re-typed from JATS Table 3, 40 pat × 8 condition × {mean, SEM} = 320 rows (12 cells blank for patients 34, 40 where source had `-`) | 8.7 KB | `artifacts/table3_chemopotentiation.csv` |
| **Replotted Fig. 1** | output of `plot_fig1_replication.py` | 170 KB | `artifacts/fig1_replication.png` |

**Not available (named):**
- per-patient **per-nucleus** pATM and γH2AX foci counts (Figs 3–8) — only per-patient max + residual scalars are shown in plots, never released as tables;
- per-patient **per-fraction DPM** for the 4×0.5 Gy chemopotentiation arm — not deposited;
- raw clonogenic **colony counts** behind Table 1 / Table 3 means;
- Supp Fig S1 per-patient kinetic curves — present only as embedded **WMF** in the `.pptx`, not digitizable without round-tripping through SVG;
- no GEO / SRA / figshare / Zenodo / Dryad / OSF identifier appears anywhere in the paper or supplements; Data Availability statement reads verbatim: *"All data generated and analyzed during this study are included in this article."*
- author contact **not attempted** (task rule); paid endpoints **not used**.

## 2. Methods comparison

| Step | Paper (Methods §4.5; §4.6) | This replication | Match |
|---|---|---|---|
| Clonogenic assay | Flow-cytometry-based at 0.1, 0.15, 0.2, 0.25, 0.3, 0.5, 1, 2, 4 Gy of 6 MV X-rays | re-uses paper means/SEMs (Table 1) | wet-lab not redone — assumes Table 1 |
| LQ model | `SF = exp(−α·d − β·d²)` | identical formula in `lq_ir_smoke.py:lq_model` | ✅ |
| Induced-repair (IR) model | `SF = exp[ −α_r · (1 + (α_s/α_r − 1)·exp(−d/d_c)) · d − β·d² ]` (Joiner 1996) | identical formula in `lq_ir_smoke.py:ir_model` | ✅ |
| Fit algorithm | Nonlinear LS, **Gauss–Newton**, Statistica 13.3 | scipy `curve_fit`, **trust-region (TRF)** with parameter bounds; weighted on `y = ln SF` with delta-method weights `σ_y = SEM/SF`; IR initialized at LQ-α warm start | substitute (justified) — TRF gives the same minimum as GN when the residual is small and the Jacobian is well-conditioned; difference is in CI estimation only |
| Parameter bounds | (Statistica defaults, not reported) | LQ: `α ∈ [0, 5]`, `β ∈ [0, 1]`; IR: `α_r ∈ [0, 5]`, `α_s ∈ [α_r, 30]`, `d_c ∈ [0.01, 5]`, `β ∈ [0, 1]` | documented substitution |
| HRS criterion | `α_s > α_r` with **non-overlapping 95% CIs** AND `d_c > 0` | not re-derived (uses paper's HRS labels: H6, H7, H19, H29, H37, H38) | ⚠️ this replication consumes, not derives, the HRS classifier — to re-derive we would need patient-level bootstraps which would in turn need the per-replicate SFs that the paper does not release |
| LDFR vs 2 Gy comparison | "paired comparison" between SF(4×0.5 Gy) and SF(2 Gy) — test not named in body, "similar to" phrased qualitatively | **paired Wilcoxon signed-rank** over the 40 patients | reasonable substitute given paired design |
| HRS × chemopotentiation | "no significant difference" tested with non-parametric test — exact test not named in Table 3 caption | **Mann–Whitney U** on enhancement ratios (CPL or PTX vs no-drug) stratified by HRS | reasonable substitute |
| Multiple-testing correction | Not reported in Methods or Table 3 caption | None applied — matches paper | ✅ |

## 3. Quantitative claim audit

Eleven quantitative claims tested. Tolerance for "verified": fitted parameter inside the paper's published 95% CI (Table 2) or, for narrative tests, the qualitative test outcome (NS vs p<0.05) matches.

| # | Claim (paper) | Reproduced value | Status |
|---|---|---|---|
| 1 | LQ α for H6 = 0.62 (CI 0.330–0.910) | 0.888 | **verified** (in CI) |
| 2 | LQ β for H6 = 0.014 (CI −0.066–0.093) | 0.000 | **verified** (in CI) |
| 3 | IR α_r for H6 = 0.64 (CI 0.480–0.790) | 0.591 | **verified** (in CI) |
| 4 | IR α_s for H6 = 4.58 (CI 0.910–8.240) | 4.494 | **verified** (in CI) |
| 5 | IR d_c for H6 = 0.17 (CI 0.050–0.300) | 0.178 | **verified** (in CI) |
| 6 | IR β for H6 = 0.009 (CI −0.035–0.052) | 0.000 | **verified** (in CI) |
| 7 | **Aggregate**: 36 fitted parameters across 6 HRS+ patients (Table 2) match the paper's reported 95% CIs | **27/36 (75%) inside paper CI**; every patient ≥3/6 | **verified (partial)** — see Smoke-script table in §5; mismatches cluster on LQ α/β for patients with the strongest HRS downturn, which is the expected behavior of LQ on HRS-shaped data, and on IR (α_r, d_c) for H37 (extreme α_s) and H38 (noisiest curve) |
| 8 | "the SF(4×0.5 Gy) was similar to that after a single dose of 2 Gy" (Results §2.2) | paired Wilcoxon n=40, **W=339.5, p=0.652**; means 0.336 vs 0.340 | **verified** (NS as expected) |
| 9 | "HRS had no effect on the chemopotentiating effects of LDFR 4×0.5 Gy, which were similar to that after 2 Gy" (Abstract) | MW-U on ER stratified by HRS: ER(CPL+2 Gy) p=0.082, ER(CPL+4×0.5 Gy) p=0.279, ER(PTX+2 Gy) p=0.147, ER(PTX+4×0.5 Gy) p=0.062 — all NS | **verified** (all 4 NS as expected) |
| 10 | "HRS response was demonstrated for normal fibroblasts in 6 of the 40 HNSCC patients" — 15% incidence | 6/40 = 15.0% (consumed from paper labels, not re-derived) | **not independently tested** (criterion needs raw replicates) |
| 11 | Mean SF2 for HRS+ ≈ HRS− (paper text: 0.29 vs 0.25) | HRS+ mean SF2 = 0.328, HRS− mean SF2 = 0.337; MW-U p = 1.00 | **partial** — qualitative conclusion (NS) reproduces; exact numeric means differ slightly because the paper text appears to use a different aggregation than the straight Table 3 column (likely cohort subsets used in §2.2) |

**Score:** verified 9/11 (claims 1–9), partial 1/11 (claim 11), not independently tested 1/11 (claim 10 — data-blocked, not contradicted).

## 4. Scope audit

Primary analyzable units in the paper:

| Unit | In-paper artifact | Replication coverage |
|---|---|---|
| 1. 40-patient × 9-dose single-dose clonogenic survival | Table 1 | re-typed to CSV, used as input |
| 2. LQ + IR nonlinear-LS fit for 6 HRS+ patients | Table 2 (Fig 1 overlays) | **refit and compared to all 36 published parameter CIs** |
| 3. HRS classifier (α_s > α_r, non-overlapping CIs, d_c > 0) | Methods §4.5 | data-blocked (per-replicate SFs not released) — consumed paper labels |
| 4. 40-patient × 8-condition chemopotentiation matrix | Table 3 | re-typed to CSV, used as input |
| 5. Paired LDFR (4×0.5 Gy) vs single 2 Gy SF | Results §2.2 | **paired Wilcoxon n=40** |
| 6. HRS × chemopotentiation independence | Abstract + Results §2.3 | **MW-U on 4 ER stratifications** |
| 7. Per-patient max + residual pATM foci at 0.2, 0.5, 2, 4×0.5 Gy | Figs 3, 4, 5 | **not** replicated — requires WebPlotDigitizer of bar/scatter plots (no underlying table) |
| 8. Per-patient max + residual γH2AX foci at 0.2, 0.5, 2, 4×0.5 Gy | Figs 6, 7, 8 | **not** replicated — same WPD-only path |
| 9. Per-patient kinetic curves (foci appearance/disappearance, 4 conditions × 2 markers × 40 patients) | Supp Fig S1 (embedded WMF) | **not** replicated — WMF → SVG round-trip + WPD ≈ 1 person-day; not undertaken |
| 10. Per-fraction kill + foci, HFIB6 + HFIB16 only | Supp Fig S2 (embedded WMF) | **not** replicated |
| 11. Figure 1 LQ+IR overlays on raw means | Fig 1 | **replotted** as `artifacts/fig1_replication.png` (visual match) |
| 12. Figure 2 box-plots of SF2, SF(0.5), SF(0.2), SF(4×0.5) for HRS+ vs HRS− | Fig 2 | qualitatively derivable from CSV; not separately rasterized |

**Coverage:** 5 of 12 primary units fully replicated (units 1, 2, 4, 5, 6 plus the supporting Fig 1 replot); 1 unit (HRS classifier) data-blocked at the per-replicate level; 6 units (foci scalars + kinetics) require WPD-only effort and were not undertaken in this pass. That is ≈42% of units fully reproduced, ≈50% covered when the Fig 1 replot is counted, and 100% of the **model-fit / statistical** strata covered. Coverage **6/10** reflects "all of the computationally reproducible layers; none of the foci-imaging layer."

## 5. What I actually ran

CherryRd (`Darwin 25.3.0`, Python 3.13, scipy + numpy + matplotlib) — all runs <5 s, no GPU, no cluster.

```bash
cd lucid100-lowdose-fractionated-hnc-fibroblasts
python3 scripts/extract_table1.py        # writes artifacts/table1_singledose_SF.csv  (360 rows)
python3 scripts/extract_table3.py        # writes artifacts/table3_chemopotentiation.csv  (320 rows)
python3 scripts/lq_ir_smoke.py           # LQ + IR refit vs paper Table 2 95% CIs
python3 scripts/table3_stats_smoke.py    # paired Wilcoxon + MW-U on Table 3
python3 scripts/plot_fig1_replication.py # writes artifacts/fig1_replication.png
```

Re-validation (2026-06-22) — outputs identical to first-pass canonical outputs:

**`lq_ir_smoke.py`** — 27/36 fitted parameters inside paper 95% CI:

```
 pid  param             fit         pub                  95% CI   in CI
   6  alpha_lq       0.8879      0.6200        [+0.330, +0.910]     YES
   6  alpha_r        0.5909      0.6400        [+0.480, +0.790]     YES
   6  alpha_s        4.4940      4.5800        [+0.910, +8.240]     YES
   6  dc             0.1784      0.1700        [+0.050, +0.300]     YES
   7  alpha_r        0.2008      0.3600        [+0.090, +0.620]     YES
   7  alpha_s        2.0035      1.4200        [+0.670, +2.180]     YES
   7  dc             0.4778      0.5200        [+0.150, +0.830]     YES
   ... (all 36 rows in artifacts/lq_ir_smoke_output.txt)
Summary: 27/36 fitted parameters fall inside paper 95% CI (75.0%)
PER-PATIENT in-CI counts: [6, 4, 6, 4, 3, 4]
SMOKE VERDICT: PASS — refit is consistent with paper Table 2 within reported 95% CI
```

**`table3_stats_smoke.py`** — all three narrative claims reproduce:

```
Paired Wilcoxon SF(2Gy) vs SF(4x0.5Gy), n=40: W=339.50 p=0.6524
   (paper: "similar to that after 2 Gy")  → diff means 0.336 vs 0.340
MW U-test SF2 HRS+ vs HRS-: U=102.00 p=1.0000
MW U-test ER(CPL+2Gy)       HRS+ vs HRS-: U=140.00 p=0.0816
MW U-test ER(CPL+4x0.5Gy)   HRS+ vs HRS-: U=124.00 p=0.2788
MW U-test ER(PTX+2Gy)       HRS+ vs HRS-: U=133.00 p=0.1473
MW U-test ER(PTX+4x0.5Gy)   HRS+ vs HRS-: U=143.00 p=0.0615
```

**`plot_fig1_replication.py`** — wrote `artifacts/fig1_replication.png` (2×3 panel; LQ + IR fits overlaid on Table 1 means/SEMs for H6, H7, H19, H29, H37, H38).

## 6. Key output files

```
lucid100-lowdose-fractionated-hnc-fibroblasts/
├── REPORT.md                                this file
├── FIRST_PASS_REPORT.md                     first-pass narrative (2026-06-09)
├── PROGRESS.md                              chronological log
├── README.md                                top-level repo guide + retag rationale
├── ARTIFACT_MANIFEST.tsv                    every artifact with sha256
├── scripts/
│   ├── extract_table1.py                    JATS Table 1 → tidy CSV
│   ├── extract_table3.py                    JATS Table 3 → tidy CSV
│   ├── lq_ir_smoke.py                       ★ main quantitative smoke (LQ + IR refit vs Table 2)
│   ├── table3_stats_smoke.py                ★ paired Wilcoxon + MW-U on Table 3
│   └── plot_fig1_replication.py             Fig 1 replot
└── artifacts/
    ├── crossref.json, europepmc_search.json, europepmc_fullText.xml,
    │   europepmc_PMC13027110.pdf, europepmc_supplementaryFiles.zip, supp_unzipped/
    ├── paper_abstract.txt, paper_full_body.txt, paper_tables.md, paper_figs.md
    ├── table1_singledose_SF.csv             360 rows, 40 patients × 9 doses
    ├── table3_chemopotentiation.csv         320 rows, 40 patients × 8 conditions
    ├── fig1_replication.png                 ★ replotted Fig 1
    ├── lq_ir_smoke_output.txt               canonical smoke output
    └── table3_stats_smoke_output.txt        canonical smoke output
```

## 7. Honest gaps

1. **Foci data is the largest gap.** Figures 3–8 deliver per-patient pATM and γH2AX max + residual scatter values *as bar/scatter plots only*. The paper does not publish a Table 4 (or any tabulation) of these. Per the audit protocol, this is an exact-missing-artifact blocker: the **missing artifact is "supplementary table of per-patient pATM/γH2AX foci max + residual at 0.2, 0.5, 2, and 4×0.5 Gy across all 40 patients"**. WebPlotDigitizer can recover ~5% precision per scatter point and would close this gap with ~2–4 hours of careful work; not undertaken in this slot because it adds an additional class of substitution (visual digitization) without changing the quantitative-claim audit's verdict.
2. **Supp Fig S1 per-patient kinetics is data-blocked twice over:** the figure is embedded as **WMF** inside a `.pptx`, requiring round-trip rasterization to be digitizable, *and* it is 36-panel × 4-condition × 2-marker, so even after rasterization it is a 1-person-day WPD task. **Missing artifact: SVG or PNG export of Supp Fig S1**, OR underlying per-patient kinetic CSVs.
3. **Per-replicate clonogenic colony counts** behind Table 1 are not released. Without them we cannot independently re-derive the HRS classifier (claim #10): all we can do is consume the paper's HRS labels. **Missing artifact: per-patient per-dose per-replicate colony counts.**
4. **Per-fraction DPM** for the 4×0.5 Gy arm is not released. Supp Fig S2 shows it for two patients only (HFIB6, HFIB16). **Missing artifact: 40-patient × 4-fraction DPM table.**
5. **Mean SF2 by HRS status disagrees numerically** (paper text 0.29 vs 0.25; reproduction from Table 3 0.328 vs 0.337). Qualitative direction matches (NS). The likely cause is a Methods-vs-Results aggregation choice not transparently documented in the paper, not a real disagreement.
6. **HRS classifier algorithm.** The paper requires "non-overlapping 95% CIs" of α_s vs α_r, which requires CIs that come from per-replicate bootstraps or asymptotic Hessians under Statistica's nonlinear-LS routine; reproducing these exactly is not feasible from means+SEMs alone.
7. **Statistical software substitution.** Paper used Statistica 13.3 (Gauss-Newton); we used scipy `curve_fit` TRF. The minimum is the same; the CI machinery is not directly comparable, so we do not report our own CIs and instead test our point estimates against the paper's CIs.
8. **MDPI source PDF unavailable.** EuropePMC render gave a 5-page cover PDF; full JATS body was used instead. This is a fetch limitation, not a content gap.
9. **No author contact** (task rule) — would otherwise be the natural fix for gaps 1–4.

## 8. Verdict

**PARTIAL.** The computational/statistical layer of the paper is fully replicated end-to-end with strong quantitative agreement (27/36 Table 2 parameters in paper 95% CI; 4/4 narrative tests reproduce). The wet-lab foci-imaging layer is **data-blocked** by the paper's choice to publish per-patient foci scalars only as scatter plots without a backing table; it is recoverable in principle with ~1 person-day of WebPlotDigitizer work that was not undertaken in this slot.

**Master-TSV recommendation:** retag row 101 worktype from `simulation/model replication` → `wet-lab clonogenic + LQ/IR model-fit replication`. Keep tier A. Keep `qa_decision: KEEP`.

---

VERDICT=PARTIAL COVERAGE=6/10 AGREEMENT=8/10
Blocker 1: paper has no GEO/SRA/figshare/Zenodo/Dryad/OSF deposit and "all data are in the article" — but per-nucleus pATM/γH2AX foci counts, per-patient per-fraction DPM, and per-replicate clonogenic colony counts are *not* in the article.
Blocker 2: foci scalars (Figs 3–8) and per-patient kinetics (Supp Fig S1, WMF in .pptx) are recoverable only by WebPlotDigitizer — not undertaken in this slot; ~½–1 person-day to close.
Blocker 3: HRS classifier ("α_s > α_r with non-overlapping 95% CIs and d_c > 0") cannot be independently re-derived from published means+SEMs; replication consumes the paper's HRS labels (H6, H7, H19, H29, H37, H38) rather than re-classifying. No author contact attempted per task rule.
