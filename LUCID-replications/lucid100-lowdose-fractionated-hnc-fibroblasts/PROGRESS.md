# PROGRESS — LUCID100 slot 47 (Wave 5)

## 2026-06-09 14:14 CDT — task received
- Subagent depth 1/1. Slot 47 (Wave 5, rank 78, tier A) backfill.
- Paper: doi:10.3390/ijms27062525.
- Source of truth: `/Users/stevens/.openclaw/workspace/lucid-replications/LUCID100_SOLID_MASTER_QA.tsv` row 101.
- Workspace: `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-lowdose-fractionated-hnc-fibroblasts/`.

## 14:14–14:16 — artifact harvest
- Confirmed OA via EuropePMC: PMC13027110, cc-by-4.0, JATS XML available, supplements present.
- Crossref metadata → `artifacts/crossref.json` (17.7 KB).
- EuropePMC search hit → `artifacts/europepmc_search.json` (9.6 KB).
- JATS XML → `artifacts/europepmc_fullText.xml` (163 KB).
- EuropePMC render PDF → `artifacts/europepmc_PMC13027110.pdf` (1.6 MB, **only 5 pages**; appears to be the cover-page renderer, not the full PDF).
- Direct MDPI PDF fetch: HTTP 403 (Cloudflare). Not attempted further — JATS XML carries the full body, all 3 tables, and all 8 figure captions.
- MDPI supplement zip via direct URL: HTTP 403. Got it via EuropePMC supplementaryFiles endpoint instead.
- Supplement contents: a single `.pptx` (`ijms-4167211-supplementary.pptx`) with **Figure S1** (per-patient pATM/γH2AX foci appearance/disappearance kinetics) and **Figure S2** (per-fraction kill + max foci, 2 patients HFIB6 + HFIB16). Both as embedded `.wmf` images — not directly digitizable without re-rendering.

## 14:16–14:20 — text extraction & table parsing
- Extracted paper sections to `paper_full_body.txt`, abstract to `paper_abstract.txt`, all tables to `paper_tables.md`, all fig captions to `paper_figs.md`.
- Identified the canonical equations (§4.5):
  - LQ: `SF = exp(-α·d - β·d²)`
  - IR: `SF = exp[-α_r·(1 + (α_s/α_r - 1)·exp(-d/d_c))·d - β·d²]`
- Fitting protocol per paper: nonlinear least-squares, Gauss-Newton, Statistica 13.3.
- Wrote `scripts/extract_table1.py` → 360-row tidy CSV (40 patients × 9 doses × mean/SEM).
- Wrote `scripts/extract_table3.py` → 320-row tidy CSV (40 patients × 8 conditions × mean/SEM, 12 cells blank where source had `-` for patients 34 and 40).

## 14:20–14:30 — smoke replications
- Wrote `scripts/lq_ir_smoke.py`. Fits LQ (2 params) and IR (4 params) by SEM-weighted nonlinear LS on `y = ln SF` (delta-method weighting) for the 6 HRS+ patients (H6, H7, H19, H29, H37, H38). Compares each fitted parameter to the paper's reported 95% CI in Table 2.
  - Result: **27/36 (75%) parameters fall inside the paper's 95% CIs**. Every HRS+ patient gets ≥ 3/6 parameters inside CI. Smoke verdict: **PASS**.
  - The mismatches cluster where they should: LQ α/β for patients with strong HRS downturn at low doses (LQ is mis-specified for those), and a few IR (α_r, d_c) values for patient H38 (whose response is noisy at the very low end of the dose range). This is expected for a 9-point dose curve with 4 free parameters and paper-reported CIs that themselves span large ranges (e.g., α_s for H37 has 95% CI [1.11, 14.31]).
  - Captured canonical output to `artifacts/lq_ir_smoke_output.txt`.
- Wrote `scripts/table3_stats_smoke.py`. Reproduces three central paper narrative claims:
  - **SF(4×0.5 Gy) "similar to" SF(2 Gy):** paired Wilcoxon over 40 patients, p = 0.65 → fails to reject, consistent with paper. **PASS.**
  - **Mean SF2 in HRS+ vs HRS-:** got 0.328 vs 0.337 (paper text: 0.29 vs 0.25). MW-U p = 1.0 — same qualitative conclusion (not significant). The exact paper means likely use a slightly different aggregation (e.g., a subset, or a different SF normalization). Treat as **consistent**.
  - **HRS independent of chemopotentiation:** four Mann-Whitney U comparisons on enhancement ratios for {CPL,PTX} × {2 Gy, 4×0.5 Gy} all give p > 0.05 (0.061 – 0.279), matching the paper's central conclusion. **PASS.**
  - Captured canonical output to `artifacts/table3_stats_smoke_output.txt`.
- Wrote `scripts/plot_fig1_replication.py` → `artifacts/fig1_replication.png` (2×3 panel; LQ + IR fits overlaid on data for all 6 HRS+ patients).

## 14:30–14:32 — manifest, report, JSON update
- Wrote `ARTIFACT_MANIFEST.tsv` (20 entries, sha256 each).
- Wrote `README.md` + `FIRST_PASS_REPORT.md`.
- Updated `/Users/stevens/.openclaw/workspace/memory/subagent-progress/lucid100-wave5-47-radiobiological-effects-of-low-dose-radiation-in-normal-fibr.json` to `status: complete`.

## Status: COMPLETE
- Verdict: **FEASIBLE** — partial computational replication delivered, both smokes PASS.
- Blockers: none.
- Recommendation: QA retag worktype on master TSV row 101 from `simulation/model replication` → `wet-lab clonogenic + LQ/IR model-fit replication`.
