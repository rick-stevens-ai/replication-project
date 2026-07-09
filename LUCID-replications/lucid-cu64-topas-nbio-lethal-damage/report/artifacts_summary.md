# Artifacts Summary — lucid-cu64-topas-nbio-lethal-damage

**Set:** LUCID
**Paper:** Carrasco-Hernández et al. 2023, *Front. Med.* 10:1253746
**Verdict:** PARTIAL
**Coverage:** 5/10 (analytic chain + scoring rule + spectrum spot-check;
MC primitive not re-derived)

## Files on disk (post-backfill)

### Top-level (pre-existing, preserved)
- `REPORT.md` — original detailed replication narrative (kept in place per
  Rick's rule; NOT moved into `report/`)
- `paper.pdf` — open-access source paper
- `code/01_lethal_damage_equation.py` — R1 implementation
- `code/02_proximity_dsb_scoring.py` — R2 implementation + unit tests
- `code/03_track_correlated_dsb.py` — R3 implementation
- `figures/fig01_eq1_crosscheck.png` — R1 vs Table 2 comparison
- `figures/fig02_dsb_ssb_ratio.png` — R3 DSB:SSB ratios vs regime

### report/ (backfilled 2026-07-06)
- `report/REPORT.tex` — LaTeX report with honest Critique section and
  `\input{open_questions_section.tex}` at end
- `report/open_questions.json` — bare JSON list of 5 open-question objects
  with `q`, `basis`, `next_steps` fields
- `report/open_questions_section.tex` — matching LaTeX section
- `report/workflow.md` — stage-by-stage what-was-done/not-done
- `report/artifacts_summary.md` — this file
- `report/failure_analysis.md` — honest limitations and MC-never-rerun
  pattern discussion

### extraction/ (backfilled 2026-07-06)
- `extraction/nougat.mmd` — stub (Nougat OCR not run; paper is
  text-native OA PDF, extraction stub only for pipeline uniformity)

## Reproduced numbers (from R1)

| Nuclide | N₀ paper | N₀ ours | rel. err |
|---|---:|---:|---:|
| ¹²⁵I  | 17 416 | 17 453 | +0.21 % |
| ¹²³I  |    451 |    452 | +0.16 % |
| ¹¹¹In |  1 625 |  1 626 | +0.05 % |
| ⁹⁹ᵐTc |  1 095 |  1 095 | +0.01 % |
| ⁶⁴Cu  |  3 107 |  3 108 | +0.02 % |

All within 0.21 % of paper. Analytic Table 2 = fully audited.

## Numbers NOT reproduced (headline)

| Quantity | Paper value | Our value |
|---|---|---|
| DSB/decay ⁶⁴Cu @ 0.25 nm | 0.171 ± 0.003 | not computed |
| DSB/decay ⁶⁴Cu @ 1.15 nm | 0.190 ± 0.003 | not computed |
| Figure 5 (mono-e⁻ vs energy) | — | not computed |

## Verdict rationale
PARTIAL: the analytic chain that Table 2 rests on is verifiable end-to-end
from public data and paper prose (5/10 coverage, 10/10 agreement on the
reproduced fraction). The upstream MC primitive is honestly out of scope
for a subagent without TOPAS-nBio + cluster time. Not REPLICATED (headline
number not re-derived); not NO-GO (analytic half is airtight); not
SPOT-CHECK (more than a spot-check — algorithm re-implementation + 5-way
Table 2 rebuild).
