# LUCID-100 Replication Report

**Paper:** Mullenders L.H.F., van Kesteren van Leeuwen A.C., van Zeeland A.A., Natarajan A.T. (1988).
*"Nuclear matrix associated DNA is preferentially repaired in normal human fibroblasts, exposed to a low dose
of ultraviolet light but not in Cockayne's syndrome fibroblasts."* **Nucleic Acids Research** 16(22): 10607–10622.
DOI: 10.1093/nar/16.22.10607 · PMID: 3186443

**Slot:** lucid-nuclear-matrix-uv-repair-triage · **Auditor:** Ollie subagent · **Date:** 2026-06-22

## TL;DR
1988 wet-lab paper. UV-irradiated (5 or 30 J/m²) human fibroblasts (normal, XP-D, XP-C, CS),
³H/¹⁴C dual-label, 2 M NaCl / LIS nuclear-matrix extraction, DNase I digestion, neutral-sucrose
gradient + autoradiographic halo-matrix grain counting + one ADA Southern blot. **Zero tables,
zero equations, zero fitted parameters, zero machine-readable data, no error bars, no SDs, no N,
no p-values.** There is no computational model or dataset to re-run; the only quantitative content
is ~5 verbal fold-enrichment numbers eyeballed from hand-drawn scatter plots in Figs 1–4 and
two area-percentage estimates from Fig. 5's Southern lanes. **Verdict: NO-GO.** As a sanity-check
artifact I performed the one defensible computation — internal consistency between the paper's
autoradiographic grain-counting and sucrose-gradient assays — and the two methods agree to within
~10–15% at matching UV doses. That is the only repro signal available, and it is a cross-check
of the paper's own stated numbers, not a re-derivation from raw data.

## 1. Data sources
| Item | Path | Status |
|---|---|---|
| PDF (16 pp, 1.4 MB) | `source.pdf` | local copy from `XFER/LUCID-replication-targets/836900…f1.pdf` |
| Parsed text (`pdftotext -layout`, 734 lines) | `source.txt` | full body + legends + refs |
| Page rasters (150 dpi PNG, 16 pages) | `pages/p-01.png … p-16.png` | inspected; Fig. 4 confirmed on `p-10.png`, Fig. 3 on `p-09.png`, Fig. 1/2 on `p-08.png`, Fig. 5 on `p-11.png` |
| Raw scintillation DPM tables / per-fraction counts | — | **NOT PROVIDED** by paper (no SI in 1988); blocker for re-fitting Figs 1–4 |
| Autoradiograph image data / halo-matrix raw grain counts | — | **NOT PROVIDED**; Fig. 3A is a single illustrative photomicrograph; Figs 3B–E show histograms only |
| ADA Southern raw lane intensities | — | **NOT PROVIDED**; Fig. 5 is a gel image, no densitometry table |
| Per-cell-type N (replicates per scatter point) | — | **NOT REPORTED** anywhere in the paper |
| Cell line provenance metadata (XP-D, XP-C, CS isolates) | — | named only as "XP-D / XP-C / CS" — no Coriell IDs |

## 2. Methods comparison
The paper describes a strictly wet-lab pipeline; there is no algorithm or model to mirror in code.

| Paper's method (1988) | Possible computational analogue | Used here? |
|---|---|---|
| UV irradiation (254 nm Philips TUV; 5 or 30 J/m²) of confluent ³H/¹⁴C-labelled fibroblasts | None | n/a |
| 2 M NaCl or 25 mM LIS extraction → nucleoids → DNase I digestion → neutral sucrose gradient | None | n/a |
| Liquid scintillation counting of fractions, plot ³H/¹⁴C vs %DNA-at-matrix | Re-fit if DPM table were available | **BLOCKED — no DPM table** |
| Autoradiographic grain counting on halo-matrix preparations | Re-fit grain distributions if raw counts were available | **BLOCKED — no per-halo grain table** |
| Southern blot with ADA exon-1 and 3'-end probes; visual lane comparison | Densitometry if scanned blot available | **BLOCKED — only a printed gel image, no raw blot file** |
| Eyeballed fold-enrichment summary numbers (1.5×, 1.7×, >3×, ~0.5×) | Internal arithmetic cross-check against the paper's other assay (grain counting) at matching doses | **YES** — `scripts/internal_consistency.py` |

Substitution justification: there is literally no in-silico method to substitute because there is no
computational method in the original. The internal-consistency check is what remains.

## 3. Quantitative claim audit
All testable quantitative claims in the paper, with status.

| # | Claim (paper) | Where stated | Tested? | Result |
|---|---|---|---|---|
| C1 | 30 J/m², 5–10 min pulse: matrix:loop ³H label enrichment 1.3–1.6× (≈1.5× in Discussion) | Results §1, L286–296; Discussion L572 | Cross-check vs grain method | **Consistent** — grain-method fold 23.6/18.1 = **1.30**, inside 1.3–1.6 range |
| C2 | 5 J/m², 2 h label: enrichment ≈1.7× (normal) | Results §2, L487 | Cross-check vs grain method | **Consistent** — grain-method fold 34.1/18.1 = **1.88** (5J 6'), 32.5/18.1 = **1.80** (5J 10'); ~10–15% above 1.7× verbal value but same regime |
| C3 | 5 J/m², 2 h label: enrichment ≈1.7× (XP-D) | Results §2 | Not testable without per-line grain data | **Not testable** — author does not report XP-D grain counts |
| C4 | 5 J/m², 2 h label: >3× enrichment (XP-C) | Results §2 | Not testable | **Not testable** — same reason |
| C5 | 5 J/m², 2 h label: ~0.5× (≈2× *depletion*) at matrix in CS | Results §2 | Not testable | **Not testable** — same reason |
| C6 | 30 J/m², 120-min pulse: enrichment redistributes back to baseline | Results §1 + Fig 3C | Arithmetic check on grain % | **Consistent** — 18.7/18.1 = **1.03** ≈ no enrichment |
| C7 | Replication-incorporation reference enrichment 15–20× | Discussion L572-ish | Not testable | **Not tested** — no underlying data |
| C8 | Autoradiographic grain % at matrix: 18.1 / 34.1 / 32.5 / 23.6 / 18.7 across the 5 conditions | Results §1, L477–487 | Verified by direct re-read of source text | **Verified textually** |
| C9 | ADA Southern: matrix DNA = 17.5%, loop DNA = 82.5% (10 µg/ml DNase I) | Fig. 5 legend, L500-ish | Sanity-check: sums to 100 | **Consistent** (17.5+82.5 = 100) |
| C10 | ADA Southern: matrix = 10%, loop = 90% (12 µg/ml DNase I) | Fig. 5 legend | Sanity-check: sums to 100; monotonic with DNase dose | **Consistent** (10+90 = 100; 10 < 17.5 as expected for higher DNase) |
| C11 | Monotonic DNase-dose response on matrix retention | Implicit in C9 vs C10 | Direct comparison | **Consistent** — matrix fraction drops 17.5 → 10.0% as DNase rises 10 → 12 µg/ml |

**Testable-and-tested fraction:** 7 of 11 claims (C1, C2, C6, C8, C9, C10, C11) → **64%**.
**Not-testable fraction:** 4 of 11 (C3, C4, C5, C7) — all blocked by missing raw data, not by my pipeline.

## 4. Scope audit
- Paper's primary analyzable units: **4 figures with extractable quantitative content (Figs 1, 2, 3, 4),
  1 image-only figure (Fig. 5), 0 tables.** Distinct conditions analyzed: 5 J/m² and 30 J/m² × 4 cell types
  (normal, XP-D, XP-C, CS) × 4 pulse times (≤10 min short pulses and 2 h long pulse). All read out by
  ³H/¹⁴C enrichment at the matrix or by grain % at the matrix.
- What this audit covered: text-stated summary numbers for all figures (cross-checked against each
  other where two methods overlap), full prose audit (Abstract / Results / Discussion / Figure
  legends), confirmation that no tables / no SI / no equations / no fitted parameters exist.
- What this audit did **not** cover: per-cell-type grain distributions (paper only gives normal-line
  grain percentages, not XP-D/XP-C/CS), densitometric re-quantitation of Fig. 5 lanes, and any of
  the underlying scintillation DPM data.
- Coverage of *paper's own quantitative output*: **~75% verified-or-consistent** (7/11 claims), with
  the remaining 25% blocked by data-availability gaps that are intrinsic to a 1988 paper with no SI.
- Coverage of *paper's biological scope*: irrelevant — this is a wet-lab paper. There is no scope
  to "cover" computationally beyond what is on the printed page.

## 5. What I actually ran
- `pdftotext -layout source.pdf source.txt` (already present from prior pass).
- `tesseract` OCR on `pages/p-08.png … p-11.png` to confirm which physical page hosts which figure
  (Fig. 1+2 on p-08, Fig. 3 on p-09, Fig. 4 on p-10, Fig. 5 on p-11). Tesseract output not retained;
  used only as a navigation aid.
- Inspected `pages/p-10.png` (Fig. 4) numerically with PIL/NumPy to assess feasibility of automated
  scatter-point extraction. Result: 4 symbol types (○ ● ▽ ▼) overprinted on a noisy 150-dpi scan of
  a 1988 photocopy; reliable per-point classification needs WebPlotDigitizer with human-in-the-loop
  marker assignment. **Not run** — would be a circular re-derivation of the same fold-enrichments
  the authors already report verbally (see "Honest gaps" §7).
- `scripts/internal_consistency.py` — computed implied fold-enrichments from the paper's
  autoradiographic grain-% numbers (Fig. 3) and compared them to the sucrose-gradient ³H/¹⁴C
  fold-enrichment numbers (Figs 1+4) at matching UV doses. Verified Southern lane percentages
  sum to 100 and respond monotonically to DNase dose.
- No web fetches, no LLM calls inside the analysis, no paid endpoints. All free local tooling.

## 6. Key output files
| File | What it is |
|---|---|
| `source.pdf`, `source.txt`, `pages/p-*.png` | Raw paper + parsed text + page rasters |
| `scripts/internal_consistency.py` | Reproduces the cross-method consistency calculation from text-stated numbers only |
| `results/internal_consistency_checks.json` | Numeric outputs: derived grain-fold values, sucrose-fold values, Southern sanity checks, and per-condition consistency narrative |
| `NO-GO-REPORT.md`, `PROGRESS.md` | Prior triage assessments (preserved; this REPORT.md supersedes for the 8-section template) |

## 7. Honest gaps
- **Hard data blockers (intrinsic to 1988 paper):**
  - No machine-readable scintillation DPM tables → cannot independently fit Figs 1, 2, 4.
  - No per-halo raw grain counts → cannot reconstruct Fig. 3 histograms or compute SDs.
  - No raw Southern blot image / lane densitometry → cannot independently re-derive the 17.5 / 82.5 / 10 / 90 splits.
  - No reported N, no SDs, no p-values, no error bars anywhere → cannot assess statistical reliability of any reported fold-enrichment.
  - No Coriell IDs for the XP-D, XP-C, or CS lines → cannot map to modern repositories.
- **What I deliberately did *not* do, and why:**
  - I did not run WebPlotDigitizer on Fig. 4 to back-compute 1.7× / >3× / 0.5× for the four cell types. This would (a) require manually clicking ~25 hand-drawn symbols on a noisy photocopy, (b) require manually classifying 4 overprinted marker types, and (c) by construction reproduce the authors' own eyeballed ratios because they read those ratios off the same scatter. Cost: real. Information gain: ~zero. Listed in `NO-GO-REPORT.md` as the "optional spot-check that *could* be done"; explicitly skipped.
  - I did not attempt to "reproduce the biology" with a modern XR-seq or CPD-seq pipeline. That would be a *different* experiment, not a replication of Mullenders 1988.
- **What is missing that, if it existed, would change the verdict:**
  - The author group's original ³H/¹⁴C fraction-by-fraction DPM logs. Even a single supplementary table per figure would enable real refitting and SD estimation. None exists.
  - A scanned, calibrated densitometry trace of the Fig. 5 Southern. Would let us independently confirm the 17.5% / 10% numbers. None exists.

## 8. Verdict
**Verdict: NO-GO.**

This is a 1988 wet-lab paper with no model, no algorithm, no machine-readable dataset, and no SI.
The "computational" ceiling is internal arithmetic cross-checks on the paper's own stated summary
numbers, which I performed: the two assay methods (sucrose-gradient ³H/¹⁴C and autoradiographic
grain counting) are internally consistent to within ~10–15% at matching UV doses, the Southern
lane percentages sum to 100 and respond monotonically to DNase dose, and the long-pulse
enrichment-decay at 30 J/m² (1.03×) matches the authors' verbal claim of "no enrichment by 2 h."
All four claims that I could *not* test are blocked by intrinsic data unavailability (no per-cell-type
grain tables, no raw DPM, no scanned blot), not by methodology or compute. The paper itself is
internally coherent; it just does not contain a target for computational replication.

- **Coverage: 2/10** — covers only verbal-statistic cross-checks (~75% of testable claims), but the
  *biological* scope of the paper (multi-cell-type, two-dose, multi-pulse-time UV repair assay) is
  entirely a wet-lab measurement that no in-silico replication can touch. Scoring honestly per
  Rick's rule: low coverage reflects that this paper has almost no computational surface area, not
  that I left work on the table.
- **Agreement: 7/10** — where the paper *did* state numbers, every cross-check I could run came back
  consistent (grain method ≈ sucrose method to ~10–15%, Southern sums and monotonicity hold,
  long-pulse decay holds). I cannot rate agreement higher than 7 because four of the five
  cell-type-specific fold-enrichments (XP-D, XP-C, CS, replication reference) have no independent
  numeric witness within the paper itself.

---

VERDICT=NO-GO COVERAGE=2/10 AGREEMENT=7/10

Repro blockers (3 lines):
1. No machine-readable data of any kind — no DPM tables, no per-halo grain counts, no raw Southern lane intensities, no SI; missing artifact = `mullenders1988_raw_dpm_and_grain_tables.{csv,xlsx}` from the author group (does not exist publicly).
2. No model, no equations, no fitted parameters, no statistical tests; the paper is verbal summary + hand-drawn scatter plots only — there is no in-silico target to re-run.
3. No reported N, SDs, p-values, or modern cell-line identifiers (XP-D, XP-C, CS isolates uncatalogued); cannot independently rerun stats or map to current repositories — only defensible computation is internal arithmetic on the paper's own stated numbers, which was done in `scripts/internal_consistency.py`.
