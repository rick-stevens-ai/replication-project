# LUCID-100 Replication Report

**Paper:** Nair S, Engelbrecht M, Miles X, Ndimba R, Fisher R, du Plessis P, Bolcaen J, Nieto-Camero J, de Kock E, Vandevoorde C. (2019).
*The Impact of Dose Rate on DNA Double-Strand Break Formation and Repair in Human Lymphocytes Exposed to Fast Neutron Irradiation.*
**Int. J. Mol. Sci.** 20(21): 5350. doi:10.3390/ijms20215350.
PMID 31661782 • PMCID PMC6862539 • OA (CC-BY 4.0)

**Slot:** `lucid100-fast-neutron-lymphocyte-dsbs-doserate` (LUCID-100 master row 80, Wave 5)
**Auditor:** Ollie subagent (`cac03b58`), 2026-06-22 16:58 CDT, host CherryRd.
**Local + free tools only. No author contact, no paid endpoints, no heavy compute.**

## TL;DR

I re-ran every quantitative claim the paper makes that can be reconstructed from
its Tables 1–3 and the Discussion text. Of **8 testable headline claims**,
**7 verify** within stated tolerances (per-dose ratio, mean ~40 % HDR-over-LDR
effect, K-coefficient max at 0.250 Gy, 2nd-order polynomial fit quality,
24 h-residual non-significance, dose-rate ratio, and the qualitative HDR-faster /
LDR-slower repair ordering). **1 claim partially contradicts the paper's
self-stated method:** the paper says the repair half-life was computed *after*
subtracting the residual at 24 h and dropping the 24 h point; doing exactly that
on the published Table 3 means yields ~3 h, not 8.6 h / 12 h. The 8.6 h / 12 h
numbers are reproducible only with a *raw* single-exponential fit (no
subtraction) over t ≥ 2 h — so either the Methods text doesn't match what the
authors actually computed, or there is unreleased intermediate processing. I
flag this and pass on the rest.

The paper is **table-replicable but not data-reproducible** in any deeper sense:
no per-cell foci CSV, no Metafer/MetaCyte scoring parameters, no GraphPad Prism
project file, no dosimetry traces, no raw images. The hardest reproducibility
blocker is the **absence of the per-cell γ-H2AX foci counts** (n=4 donors ×
~500 cells/condition × 16 dose/time conditions ≈ 32 k cells). Without that, no
proper non-linear regression, ANOVA, or bootstrap on the actual data is
possible.

## 1. Data sources

### Acquired

| Artifact | Source | Size | Notes |
|---|---|---|---|
| `artifacts/paper.pdf` | Europe PMC `articles/PMC6862539?pdf=render` | 1.3 MB | full 13-page OA PDF |
| `artifacts/paper_fulltext.xml` | EPMC `/PMC6862539/fullTextXML` | 119 KB | JATS structured text |
| `artifacts/paper.txt` | local `pdftotext -layout` | 49 KB | for grep + table digitization |
| `artifacts/paper_unpaywall_s2_acquired.pdf` | Unpaywall/S2 route, 2026-06-09 | 4.5 MB | secondary copy |
| `data/table1_induction.csv` | digitized from `pdftotext` Tables 1 | 5 doses × HDR/LDR mean+SD |
| `data/table2_hdr_ldr_ratio.csv` | digitized from Table 2 | per-dose HDR/LDR ratio |
| `data/table3_repair_kinetics.csv` | digitized from Table 3 | 6 time points × HDR/LDR mean+SD at 1 Gy |
| `data/paper_key_numbers.json` | hand-extracted abstract / Discussion claims | for smoke harness |
| `artifacts/epmc_search.json` | EPMC search API | metadata + OA flags |

### NOT acquired (explicit missing artifacts; see §7)

- **Per-cell γ-H2AX foci counts** — not deposited anywhere (no Zenodo/Figshare/GEO/PMC supp). EPMC `hasSuppl: N`. No code repo cited.
- **Metafer/MetaCyte classifier settings / spot-detection parameters** — not published.
- **GraphPad Prism v5 project file** — authors say they used it; not released.
- **Raw fluorescence micrographs** — not deposited.
- **iThemba LABS p(66)/Be(40) neutron spectrum file / dosimetry traces** — not provided.
- **Per-donor (n=4) breakdown** — paper only reports cross-donor mean ± SD.

## 2. Methods comparison

| Step | Paper method | My replication | Match? |
|---|---|---|---|
| Cell prep | Whole blood from 4 donors, irradiated, then PBL isolation, fixation, γ-H2AX immunostaining, MetaCyte automatic foci scoring | **Skipped (wet-lab; we have only the summary tables)** | wet-lab not re-runnable |
| Dose rates | HDR = 0.400 Gy/min, LDR = 0.015 Gy/min p(66)/Be(40) neutrons | Used as given (E7) | ✅ |
| Induction curve | "best fitted to a second-order polynomial" (a + bD + cD²) | numpy.polyfit deg=2 with intercept | ✅ same model class |
| Induction comparison | "On average, HDR neutron irradiation induced 40 % more DSBs per cell" | mean of per-dose HDR/LDR ratios (E2) | ✅ 39.77 % vs 40 % |
| Per-dose ratio (Table 2) | HDR foci / LDR foci, per dose | direct division (E1) | ✅ max abs err 0.005 |
| K-coefficient | Ulyanenko-style K = foci/Gy; "max difference 1.87 at 0.250 Gy" | K_HDR/K_LDR per dose; locate max (E3) | ✅ 1.872 at 0.250 Gy |
| Repair half-life (Methods text) | "When the residual foci number at 24 h post-irradiation was subtracted from the foci yields obtained at earlier time points post-irradiation, all remaining foci data of the present study for 0.400 Gy/min were consistent with a repair half-life of 8.6 h" | three variants: (A) raw single-exp from t≥2h, (B) paper's stated method = subtract foci(24h), drop 24h, t∈{2,4,8,12}, (C) subtract & keep 24h | **variant A matches paper's reported half-lives (8.6 / 12.0); variant B (the stated method) gives ~3 h. Reported method ≠ reported numbers.** |
| Statistics | GraphPad Prism v5, ANOVA via total sum-of-squares, p<0.05 | I cannot replicate ANOVA without per-cell counts. For the one explicit "not significant" claim at 24 h (Discussion p.8) I run a Welch's two-sample t-test with n=4 and the inter-donor SDs published in Table 3 (E6) | qualitative agreement (p > 0.05) |
| Image analysis | Metafer / MetaCyte, automated scoring | not re-runnable (no images, no classifier) | n/a |
| Dosimetry | p(66)/Be(40), iThemba LABS cyclotron, "see ref [42]" | not re-runnable (no Monte Carlo, no spectrum file) | n/a |

## 3. Quantitative claim audit

Testable headline claims pulled from Abstract + §2 Results + §3 Discussion + Tables.

| # | Claim (verbatim or close) | Paper value | My value | Tol | Verdict |
|---|---|---|---|---|---|
| C1 | "On average, HDR neutron irradiation induced 40 % more DNA DSBs per cell compared to LDR" | +40 % | +39.77 % | ±2 pp | **VERIFIED** |
| C2 | Per-dose HDR/LDR ratio (Table 2) | [1.22, 1.87, 1.44, 1.30, 1.16] | [1.216, 1.872, 1.435, 1.302, 1.163] | max abs err <0.02 | **VERIFIED** (max 0.005) |
| C3 | Maximum K-coefficient difference 1.87 at 0.250 Gy | 1.87 @ 0.250 Gy | 1.872 @ 0.250 Gy | ±0.02 | **VERIFIED** |
| C4 | Dose-response best fit by 2nd-order polynomial | poly2 chosen; no R² reported | poly2 R² = 0.994 (LDR), 0.988 (HDR); AICc beats linear by ~6.6 (LDR) and ~5.2 (HDR) | R² ≥ 0.95 | **VERIFIED** |
| C5 | Dose-rate ratio HDR/LDR ≈ 26.7× | 0.400 / 0.015 = 26.67 | 26.67 | exact | **VERIFIED** |
| C6 | Residual foci at 24 h HDR (1.29 ± 0.45) vs LDR (1.65 ± 0.46) "difference not statistically significant" | not significant | Welch two-sided p = 0.306, df = 6.0 (n=4 donors each) | p>0.05 | **VERIFIED** |
| C7 | Repair half-life HDR = 8.6 h, LDR = 12 h (Discussion p.10) | 8.6 / 12.0 h | **Variant A (raw exp, t≥2h):** 9.92 h (HDR), 13.08 h (LDR); bootstrap 95 % CI [5.58, 15.45] / [7.73, 21.98] | ±25 % | **VERIFIED (variant A); CONTRADICTED for the stated method (variant B)** |
| C8 | "[Repair] half-life of foci disappearance was marginally longer for LDR neutrons than that for HDR neutrons" (qualitative ordering) | LDR > HDR | LDR 13.08 h > HDR 9.92 h (variant A); LDR 3.27 h > HDR 2.89 h (variant B) | ordering only | **VERIFIED** (both variants) |

**Score: 7 fully verified, 1 verified-with-caveat (C7) → 8/8 reachable claims tested, 7/8 cleanly pass. ≈87.5 % verified, 100 % tested.**

### Critical anomaly on C7 (single-exponential repair half-life)

The paper says (Results §2.2, p.7):

> "When the residual foci number at 24 h postirradiation was subtracted from the
> foci yields obtained at earlier time points postirradiation, all remaining
> foci data of the present study for 0.400 Gy/min were consistent with a repair
> half-life of 8.6 h. For dose rate of 0.015 Gy/min, the repair half-life was
> longer, namely, 12 h."

I implemented that **literally**: take Table 3 means, subtract `foci(24h)`,
fit `y = A·exp(-k·t)` over t ∈ {2, 4, 8, 12} h. Result: t½ = 2.89 h (HDR),
3.27 h (LDR). Bootstrap 95 % CI [0.84, 7.50] / [0.83, 6.73]. **The
paper-reported half-lives (8.6 / 12.0) sit outside that interval.**

The only fit that reproduces 8.6 / 12.0 is a **raw** single-exponential from
t = 2 h onwards, **without subtraction** (variant A: 9.92 / 13.08 h). Both
half-lives are within 9–16 % of the paper's values and inside the bootstrap CI.

Either the Methods text mis-describes what the authors did (most likely), or
there was a different baseline (e.g. unirradiated control rather than t=24 h)
that was not stated, or GraphPad Prism v5 was using a different parametrization
(e.g. plateau + exponential decay, where the plateau is *fitted* rather than
subtracted from the data — that recovers the raw fit numerically). I flag this
as a real reproducibility defect, not a digitization error: the Table 3 numbers
match the paper to ≤0.01 foci/cell, and the discrepancy is structural in the
described method.

## 4. Scope audit

The paper has **one experimental enterprise** with two phases:

| Primary analyzable unit | Paper covers | Replication covers | Pct |
|---|---|---|---|
| Induction dose-response (5 doses × 2 dose rates, 4 donors, 2 indep. expts) → Table 1, Figure 1 | yes | summary table + poly2 + LQ + linear model comparison + AICc | **100 % at table level**, 0 % at per-donor / per-cell level |
| Induction comparison (HDR vs LDR, abstract claim + Table 2) | yes | yes (E1, E2, E3) | **100 %** |
| Repair kinetics (6 time points × 2 dose rates at 1 Gy) → Table 3, Figures 3 & 4 | yes | exp fit + bootstrap CI + three method variants | **100 % at table level**, 0 % at per-donor / per-cell level |
| Repair half-life estimates (single-exponential) | 2 numbers (8.6 / 12.0 h) | 6 numbers (3 variants × 2 dose rates) + CI + anomaly flag | **>100 % (audit-grade)** |
| Statistical inference (ANOVA, p-values) | uses Prism v5 | only the one explicit 24 h-residual t-test (E6) | **~15 %** (limited by absence of per-cell data) |
| Image analysis (Metafer/MetaCyte) | yes | **not attempted** | **0 %** — no images released |
| Dosimetry (p(66)/Be(40) neutron field) | references prior work | **not attempted** | **0 %** — separate Monte Carlo enterprise, out of scope without spectrum file |

**Coverage on the paper's primary analyzable units (induction curve + comparison + repair kinetics + half-life): 4/4 = 100 % at table-level granularity.**

**Coverage on the paper's secondary infrastructure (image analysis + dosimetry + per-donor stats): 0/3 = 0 % — explicitly blocked by missing artifacts.**

Net scope: I replicate everything the paper made *replicable*. Anything else
needs upstream data the authors did not release.

## 5. What I actually ran

All commands ran on CherryRd, Python 3.14, numpy only. Total wall-time < 2 s.
Two scripts:

### `scripts/smoke_replicate.py` (pre-existing first-pass; re-verified)

3 reduced claim checks: C1 (mean ratio), C2 (poly2 R²), C7 (repair half-life
variant A primary + variant B sensitivity). Writes
`scripts/smoke_outputs/smoke_results.json` + `smoke_plots.png`. **Result: 3/3
PASS** as of 2026-06-22 17:00 CDT, identical to the 2026-06-09 first-pass run.

### `scripts/extended_replicate.py` (this audit)

7 extended checks (E1–E7) including:
- Per-dose ratio match vs Table 2 (E1)
- Mean ratio vs abstract claim (E2)
- K-coefficient max-locus check (E3) — confirms 1.87 @ 0.250 Gy
- Induction model comparison: linear vs poly2 vs LQ-style (alpha·D + beta·D²)
  with AICc (E4)
- Three-variant repair half-life with parametric bootstrap 95 % CI (E5)
- Welch's t-test on 24 h residual (E6) using the inter-donor SDs
- Dose-rate ratio sanity (E7)

Writes `results/extended_results.json` + `results/extended_summary.md`.

```bash
$ cd lucid100-fast-neutron-lymphocyte-dsbs-doserate
$ python3 scripts/smoke_replicate.py        # 3/3 PASS
$ python3 scripts/extended_replicate.py     # 7/7 PASS at the table level;
                                            # 1 method-text anomaly flagged
$ ls results/
extended_results.json
extended_summary.md
induction_and_repair_overlay.png
```

## 6. Key output files

| File | Purpose |
|---|---|
| `REPORT.md` | this audit report |
| `FIRST_PASS_REPORT.md` | original 2026-06-09 first-pass report |
| `PROGRESS.md` | running log |
| `README.md` | folder overview |
| `data/table1_induction.csv` | digitized Table 1 (5 × 5) |
| `data/table2_hdr_ldr_ratio.csv` | digitized Table 2 (5 × 2) |
| `data/table3_repair_kinetics.csv` | digitized Table 3 (6 × 5) |
| `data/paper_key_numbers.json` | hand-extracted abstract/Discussion claims |
| `artifacts/paper.pdf` | OA PDF (Europe PMC) |
| `artifacts/paper_fulltext.xml` | JATS XML |
| `artifacts/paper.txt` | pdftotext output (digitization source) |
| `artifacts/MANIFEST.md` | provenance manifest for harvested files |
| `scripts/smoke_replicate.py` | first-pass 3-check harness |
| `scripts/extended_replicate.py` | this audit's 7-check harness |
| `scripts/smoke_outputs/smoke_results.json` | first-pass JSON |
| `scripts/smoke_outputs/smoke_plots.png` | induction + repair overlay |
| `results/extended_results.json` | this audit's JSON (E1–E7) |
| `results/extended_summary.md` | machine-readable claim table |
| `results/induction_and_repair_overlay.png` | copy of overlay plot for the report |

## 7. Honest gaps

The fundamental reproducibility ceiling for this paper is the **complete
absence of underlying primary data**. Per Rick's 2026-06-22 hard rule, the
exact missing artifacts that block deeper reproduction are:

1. **`per_cell_foci_counts.csv`** (or equivalent) — a table of ~32 000 rows:
   `donor_id, experiment_replicate, dose_Gy, dose_rate, time_post_IR_h,
   nucleus_id, n_foci, mean_foci_intensity, dapi_area_px`. Without this we
   cannot:
   - Reproduce the ANOVA / Tukey post-hoc / p<0.05 statements.
   - Reproduce per-donor variability (Table 1 SDs only show cross-donor variation, not within-donor cell-to-cell variation).
   - Do proper non-linear regression with point-wise weights.
   - Re-estimate the repair half-life with a fit-resolved baseline rather than the ad-hoc subtraction described in the text.
2. **Metafer / MetaCyte classifier configuration** — the spot-detection
   parameters (threshold, min spot size, exclusion mask) used by the automated
   scorer. Without this the wet-lab assay cannot be re-run by any third party
   even with new blood.
3. **GraphPad Prism v5 project file** (`.pzfx` or `.pzf`) — would directly
   resolve the C7 method-vs-numbers anomaly by showing exactly what
   transformation and fit equation produced 8.6 / 12.0 h.
4. **iThemba LABS p(66)/Be(40) neutron energy spectrum + LET distribution
   file at the irradiation point** — the paper references prior dosimetry work
   ([42]) but does not include the spectrum needed to feed a Monte Carlo DSB
   induction model (PARTRAC / MCDS / TRAX). This is the actual blocker for
   the "mechanistic simulation" upgrade path the LUCID-100 master TSV
   originally labeled this work as.
5. **Raw immunofluorescence micrographs** (DAPI + γ-H2AX channels, one
   field per donor × condition) — needed for any image-analysis replication
   or to validate the MetaCyte spot count.
6. **Original donor consent forms / IRB / ethics approval number** — paper
   says approval was granted but does not give a number; cannot re-derive
   experimental ethics chain.

In addition to data gaps, the paper has **one method-text defect** (C7,
above) that is itself a reproducibility hazard regardless of data
availability: the stated half-life-fit procedure does not reproduce the
reported half-lives.

The paper does **not** provide a mechanistic model (no Monte Carlo, no ODE,
no agent model). It only fits two empirical curves to summary tables. So the
LUCID-100 master TSV's original `worktype = simulation/model replication` tag
is **inaccurate** — this paper is a wet-lab radiobiology assay with reduced
phenomenological curve fitting. The recommended retag (already in
`FIRST_PASS_REPORT.md`) is `wet-lab assay / radiobiology table replication`.

## 8. Verdict

**REPLICATED** for the table-level scope the paper actually exposes:
8/8 testable headline claims tested, 7/8 cleanly verify, 1 (C7) verifies
numerically but the paper's stated method does **not** reproduce its own
numbers (variant A passes, variant B as written fails). The 100 % per-dose
ratio match (max abs err 0.005), the exact 1.87 K-coefficient locus, the
verified 39.77 % vs 40 % aggregate effect, the verified poly2 fit quality
(R² > 0.987 both arms), and the verified Welch t-test on the 24 h-residual
non-significance claim are unambiguous wins.

The hard gaps are all upstream-data gaps (per-cell foci CSV, Metafer config,
Prism project, neutron spectrum), none of which can be closed without
author contact (disallowed) or new wet-lab work. The C7 method-text anomaly
is documented and is a real reproducibility critique to feed back to the
LUCID-100 program.

- **Coverage:** 9/10
  (every primary analyzable unit at table-level granularity replicated; loss
  of 1 point for the per-donor / per-cell / image-analysis layer that is
  permanently blocked by missing data deposits.)
- **Agreement:** 8/10
  (7/8 cleanly verified, 1 method-vs-number inconsistency on the repair
  half-life; the reported numbers ARE reproducible — just not by the
  method the paper says it used.)

```
VERDICT=REPLICATED COVERAGE=9/10 AGREEMENT=8/10
```

**Three-line repro-blocker summary:**
1. **No per-cell γ-H2AX foci CSV** anywhere (PMC `hasSuppl: N`, no Zenodo/Figshare/GEO, no GitHub) — blocks ANOVA, per-donor stats, properly-weighted curve fits, and any image-analysis re-run.
2. **No deposited Metafer/MetaCyte classifier parameters and no GraphPad Prism v5 project file** — blocks both the wet-lab pipeline re-execution and the C7 half-life method/number reconciliation (the stated subtraction method does not reproduce the reported 8.6 h / 12 h half-lives; a raw single-exponential from t≥2 h does, with ~10–15 % residual).
3. **No iThemba LABS p(66)/Be(40) neutron energy spectrum / LET file at the irradiation point** — blocks the mechanistic Monte Carlo (PARTRAC/MCDS) "simulation replication" worktype the LUCID-100 master TSV originally labeled this paper as; the published artifact only supports a phenomenological curve-fit replication, not a from-first-principles DSB-induction prediction.

VERDICT=REPLICATED COVERAGE=9/10 AGREEMENT=8/10
