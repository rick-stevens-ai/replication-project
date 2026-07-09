# PROGRESS — Franken et al. alpha vs gamma RBE replication

**Status:** done
**Verdict:** PARTIAL (coverage 6/10, agreement 10/10 on what was recomputed)
**Started:** 2026-05-30 18:01 CDT
**Finished:** 2026-05-30 18:12 CDT
**Target:** Franken et al., *Oncology Reports* 27:769–774, 2012
(DOI 10.3892/or.2011.1604).

## Phases
- [x] Workspace + PROGRESS scaffolded
- [x] Read PDF (pdftotext → clean ASCII; Anthropic/Gemini PDF endpoints
      all 400'd on this file, so text extraction was used instead)
- [x] Triage: paper's full quantitative content is in Table I (4 endpoints
      × 2 radiation qualities, all α values with ±σ). Equations are explicit.
      Per-dose raw data are NOT tabulated and not in any supplement.
- [x] Recompute all 4 RBE values + propagated σ — match paper to <1%
- [x] Internal-consistency check on "1% / 10% of DSBs are lethal" claim
      (Discussion p.773) — 0.6% / 8.8% from Table I, consistent with
      paper's rounded statements
- [x] Reconstruct Fig. 2 from α values (linear for non-survival,
      exponential for survival — β not tabulated for γ survival)
- [x] REPORT.md, README.md written

## Why not full REPLICATED
- Raw per-dose data points are only in Fig. 2 of the paper.
- No supplement, no data deposit, no author contact allowed.
- Could be upgraded by digitizing Fig. 2 and refitting; this would
  add digitization noise to an arithmetic check that already passes
  exactly. Skipped per "low-value but doable" triage.

## Key numbers (paper / replication)
| Endpoint              | RBE paper | RBE recomp |
|-----------------------|-----------|------------|
| γ-H2AX foci           | 1.0 ± 0.3 | 1.00 ± 0.35 |
| Clonogenic survival   | 14.7 ± 5.1| 14.67 ± 5.08 |
| Chromosome fragments  | 15.3 ± 5.9| 15.27 ± 5.94 |
| Colour junctions      | 13.3 ± 6.0| 13.33 ± 6.04 |
