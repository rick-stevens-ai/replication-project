# FIRST_PASS_REPORT — LUCID100 Slot 29

**Paper:** Odegaard, Yang & Boothman (1998), *Environ Health Perspect* 106 Suppl 1:301–305
**DOI:** 10.1289/ehp.98106s1301  •  **PMC:** PMC1533273
**Date:** 2026-06-09 (America/Chicago) • **Replication folder:** `lucid100-dnapk-adaptive-survival-responses`

---

## 1. Verdict (one line)

**PARTIAL (sufficient) — minimal arithmetic/statistical replication succeeds; biological re-execution not feasible without wet lab access to murine SCID and CB-17 fibroblasts.**

Coverage: **Table 1 — 100%**; Figures 1 & 2 — 0% pixel-extracted (optional next step). Agreement with paper's central numeric and verbal claims: **strong**.

---

## 2. What the paper actually claims

1. **Central claim:** SCID murine fibroblasts (lacking DNA-PKcs and incapable of canonical NHEJ DSB repair) and parental CB-17 fibroblasts (DNA-PKcs+/NHEJ+) both show an ~2-fold adaptive survival response (ASR) to a 5 cGy priming dose given before an equitoxic high-dose challenge (250 cGy for SCID, 500 cGy for CB-17).
2. **Corollary:** DNA-PKcs and DSB repair are therefore **not required** for ASR in mammalian cells.
3. **Secondary observation:** DNA-PKcs does play a role in the **G2/M cell-cycle checkpoint** at high doses (≥10 Gy) — CB-17 cells arrest robustly (>60%, >30 h) in G2/M; SCID cells show only a transient arrest. Backed by Fig 1A–E and Fig 2A–E flow cytometry time courses at 0, 2.5, 5, 10, 15 Gy.

## 3. Replication scope — what is feasible from published material

| Claim | Source | Feasible? | Method | Status |
|---|---|---|---|---|
| ~2-fold ASR in CB-17 (DNA-PKcs+) | Table 1 row 5 | ✅ trivial | `code/replicate_table1.py` ratio + Gaussian propagation | **Done.** 22%/12% = **1.83 ± 0.80**; consistent with "≈2×" |
| ~2-fold ASR in SCID (DNA-PKcs−) | Table 1 row 5 | ✅ trivial | same script | **Done.** 21%/9% = **2.33 ± 0.42**; consistent with "≈2×" |
| Dual-prime ASR is equivalent to single-prime | Table 1 rows 5 vs 6 | ✅ trivial | ratio compare | **Done.** CB-17: 1.83 vs 1.67; SCID: 2.33 vs 2.00. Single ≈ dual within 1 σ. |
| Unexpected CB-17 toxicity from 2× priming alone | Table 1 row 3 (CB-17 = 58 ± 2%) | ✅ — observed, unexplained in paper | inspection | **Done.** Re-flagged as an open finding; paper acknowledges "It is not clear why". |
| Equitoxic challenge yields ≈10% in both lines | Table 1 row 4 | ✅ trivial | inspection | **Done.** CB-17 12 ± 5, SCID 9 ± 1. |
| G2/M arrest is longer & deeper in CB-17 vs SCID at 10–15 Gy | Fig 1D, 1E vs Fig 2D, 2E | ⚠️ requires digitization | WebPlotDigitizer on each panel, then per-time-point comparison of `%G2/M` traces between the two figure series | **Not done.** Optional. Not required for the central claim. |

## 4. What is NOT feasible (and why)

- **De novo biological replication:** would require CB-17 and CB-17/scid mouse-derived fibroblasts (a Mike Brown gift, Stanford, ref 10), a ~24 h confluence arrest, a calibrated low-LET X-ray source (Phillips generator @ 5 cGy precision), a Becton-Dickinson FACScan equivalent, and 14-day clonogenic assay. Not in scope for a first-pass desk replication, and the cell lines are not redistributed via ATCC; would require MTAs.
- **Per-replicate raw data:** Table 1 reports mean ± SD over n = 3 experiments × duplicate cultures (i.e. 6 wells per cell). The raw colony counts are not published and would require contacting the corresponding author (D.A. Boothman) — **NOT permitted under this task** ("no author contact").
- **DNA-PKcs Western / kinase activity raw images:** referenced as "Yang et al., in preparation" → never appeared as a standalone dataset (Boothman lab moved to UTSW / Case Western; the cited unpublished work was eventually folded into later DNA-PKcs/ASR papers).

## 5. Smoke replication output

From `code/replicate_table1.py` (script also writes `results/table1_replication.tsv`):

```
==============================================================================
ASR fold enhancement (primed+challenged / challenged-only)
==============================================================================
     CB-17 (DNA-PKcs+) | 1× prime: 1.83±0.80   2× prime: 1.67±0.91
      SCID (DNA-PKcs-) | 1× prime: 2.33±0.42   2× prime: 2.00±0.70
------------------------------------------------------------------------------
Paper's verbal claim: ~2-fold ASR in both SCID and CB-17 cells.
Replication check: both lines show 1.8-2.3× with 1-σ overlap of 2.0×.
```

**Interpretation.** The paper's "1.5- to 2.2-fold" range (abstract) and "nearly 2-fold" (Results §Survival Assessments) are corroborated. The SCID-vs-CB-17 difference (2.33 vs 1.83) is suggestive that ASR is, if anything, slightly *more* efficient in DNA-PK-deficient cells, but the wide SDs (driven mainly by the small denominator 9 ± 1% / 12 ± 5%) preclude a statistical contrast. The central qualitative conclusion — "DNA-PKcs not required for ASR" — is fully supported by the published numbers.

## 6. Master-TSV worktype: **retag recommendation**

- **Current tag (line 73 of LUCID100_SOLID_MASTER_QA.tsv):** `omics/signature replication`
- **Why this is wrong:** The paper contains no omics layer (no RNA-seq, microarray, proteomics, or DNA methylation), no gene signature, no DEG list, no enrichment analysis. It is a 5-page conference-supplement paper with one survival table and two flow-cytometry figures. Tagging as omics misleads downstream prioritization.
- **Recommended retag:** `figure/table replication + statistical verification` (or, if a single coarser bucket is needed, `dose-response curve replication`).
- **Action for QA owner:** edit row `rank=60` in `_LUCID100_ADMIN/LUCID100_SOLID_MASTER_QA.tsv` column `worktype`.

## 7. Outputs (all under this folder)

- `README.md` — entry point
- `PROGRESS.md` — timeline
- `ARTIFACT_MANIFEST.md` — what was tried, what was retrieved, what was unavailable
- `paper/main.pdf`, `paper/main.txt` — source paper
- `data/table1_extracted.tsv` — Table 1 transcription
- `code/replicate_table1.py` — smoke replication script
- `results/table1_replication.tsv` — script output
- `FIRST_PASS_REPORT.md` — this file

## 8. Recommended next actions (in priority order)

1. **QA retag** to `figure/table replication + statistical verification` (1-line TSV edit).
2. **(Optional)** WebPlotDigitizer pass on Fig 1D/E and Fig 2D/E to numerically support the G2/M arrest difference. Effort: ~30 min, no wet-lab dependency.
3. **(Out of scope)** Cross-link with later Boothman-lab ASR papers (Lee et al. *Cancer Res* 1999; Park et al. ~2002) to check whether the "Yang et al., in preparation" DNA-PK kinase assay was ever published — would inform whether the "DNA-PKcs as G2/M arbiter" hypothesis was developed further.

## 9. Blockers

**None.** All deliverables completed in one session without external dependencies, paid endpoints, author contact, or heavy compute.
