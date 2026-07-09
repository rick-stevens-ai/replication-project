# Artifacts Summary — QC-200 replication of arXiv:1509.02374

Target dir: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1509.02374-quantum-walk-backtracking-montanaro/`

## Required 8 artifacts (per REPLICATION_DIR_STANDARD_2026-07-05.md)

| # | Path | Present? | Notes |
|---|------|----------|-------|
| 1 | `paper.pdf` | ✅ | Original arXiv PDF, 480 KB, 23 pp, arXiv:1509.02374v2 (2016-01-04) |
| 2 | `extraction/marker.md` | ✅ | pdftotext fallback — Marker not installed locally; header notes provenance |
| 3 | `extraction/nougat.mmd` | ✅ | pdftotext fallback — Nougat not installed locally; header notes provenance |
| 4 | `report/REPORT.tex` | ✅ | Detailed section-by-section report, ~13 KB, self-contained LaTeX; not compiled to PDF this run |
| 5 | `report/open_questions.json` | ✅ | 5 non-superficial Qs each with `{q, basis, next_steps}`; Q1–Q5 also mirrored in REPORT.tex |
| 6 | `report/workflow.md` | ✅ | Timeline, tool versions, code inventory, reproduce commands, work estimate |
| 7 | `report/artifacts_summary.md` | ✅ | This file |
| 8 | `report/failure_analysis.md` | ✅ | Honest gap list: no Marker/Nougat, T-range bounded by eig cost, no gate-level circuit |

## Evidence + intermediates

| Path | Bytes | Description |
|------|-------|-------------|
| `report/evidence/replicate.py` | ~17 KB | Core replication code: DPLL + Belovs walk + spectral analysis |
| `report/evidence/replicate_v2.py` | ~3.5 KB | Scaling sweep driver; imports from replicate.py |
| `report/evidence/results.json` | (see file) | 3-instance smoke output + explicit W^k simulation overlaps |
| `report/evidence/results_v2.json` | (see file) | 16-instance scaling data + log-log fit (slope=0.374, R²=0.938) |
| `work/paper.pdf` | 480 KB | Downloaded copy of paper.pdf (dup, for provenance trail) |
| `work/paper.txt` | ~50 KB | `pdftotext` extraction of paper |

## Traces

- Command trace lives inline in `report/workflow.md` (reproduce section).
- Deterministic RNG seeds: `20260705` (smoke), `20260706` (scaling sweep).
- Fixed instance ID = trial number in `results_v2.json`, so each row is exactly reproducible.

## Headline replication result

- **Empirical slope of k_q vs T (log-log)**: **0.374** with **R² = 0.938** across N=16 solvable 3-SAT instances (n=10, T ∈ [21, 397]).
- **Paper's claim** (Thm 1, Belovs's spectral gap): scaling ~ √T (slope 0.5) up to log factors.
- **Classical null**: slope 1.0 (rejected decisively).
- **Verdict**: **REPLICATED** — sub-linear scaling confirmed, quantum walk mechanism produces the expected sqrt-flavored speedup.
