# Workflow — arXiv:1210.1148 replication (QC-200 wave)

Date: 2026-07-05
Sub-agent execution time (wall): ~30 min end-to-end.
Host: CherryRd (macOS arm64), CPU only.

## Steps executed

1. **Read the QC wave brief** (`~/Dropbox/REPLICATE-PROJECT/scripts/QC_WAVE_BRIEF_2026-07-03.md`).
2. **Created target dir** `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1210.1148-wildcards-group-testing-ambainis-montanaro/` with `work/`, `extraction/`, `report/evidence/`.
3. **Fetched paper PDF** via `curl -sL https://arxiv.org/pdf/1210.1148` → 383006 bytes, version v4 (2013-05-20 metadata). Saved to `work/paper.pdf` and mirrored to top-level `paper.pdf`.
4. **Verified paper metadata from PDF** (not from the arXiv HTML page):
   - Title: "Quantum algorithms for search with wildcards and combinatorial group testing" ✓
   - Authors: Andris Ambainis (U. Latvia) & Ashley Montanaro (DAMTP Cambridge) ✓
5. **Text-extracted the paper** with `pdftotext -layout` (881 lines) and skimmed the intro, Sections 2, 4, 5, and the two headline theorems.
6. **Identified the two headline testable claims** (Theorem 1 for wildcards, Theorem 2 for CGT, and Lemma 3 which underpins Theorem 1).
7. **Wrote `report/evidence/wildcards_pgm.py`** — an exact PGM numerical replication of Lemma 3 and a query-counting simulator for the full wildcards algorithm.
8. **Wrote `report/evidence/group_testing_qm.py`** — an exact numpy state-vector simulation of the paper's Section 4 OR-oracle subroutine (Bernstein-Vazirani-style), plus classical binary-search and non-adaptive Bernoulli/COMP baselines.
9. **Ran both scripts** to completion, saving raw stdout to `wildcards_stdout.txt` / `group_testing_stdout.txt` and structured results to `wildcards_results.json` / `group_testing_results.json`.
10. **Reviewed one iteration bug** (Bernoulli baseline decoder was O(n^2) and looped for larger `n`; also the AM CGT algorithm was blowing up the state vector when `|S| > 20`). Fixed both (added simulation cap `SIMU_S_MAX=12` and rewrote the COMP decoder as O(m·n)), reran successfully in ~1 minute.
11. **Wrote extraction fallbacks** `extraction/marker.md` and `extraction/nougat.mmd` from the `pdftotext -layout` output (marker/nougat not installed on this host — see `failure_analysis.md`).
12. **Wrote the LaTeX report** `report/REPORT.tex` (section-by-section, 8 tables of real data).
13. **Wrote the 5 open questions** as both a numbered section in the report and the machine-readable `report/open_questions.json` (each with `q`, `basis`, `next_steps`).
14. **Wrote this workflow, `artifacts_summary.md`, and `failure_analysis.md`.**
15. **Attempted `pdflatex REPORT.tex`** to produce `REPORT.pdf` (see `failure_analysis.md` for outcome).
16. **Printed WAVE_RESULT one-liner.**

## Tools and versions

| Tool | Version | Used for |
|---|---|---|
| python | 3.13 (system) | Everything |
| numpy | 2.4.3 | State vectors, SVD, Hadamard-tensor |
| scipy | 1.18.0 | (imported but the code uses only numpy) |
| pdftotext (poppler) | system | PDF → text extraction |
| curl | system | Paper download from arXiv |
| pdflatex (TeX Live) | attempted | Report PDF compile — see failure_analysis.md |

## Compute estimate

- CPU time (single core, macOS arm64):
  - `wildcards_pgm.py`: ~1s (SVDs are all under 1800×1800)
  - `group_testing_qm.py`: ~60s (dominated by n=32 Bernoulli baseline & many random rounds)
- No GPU, no LLM inference, no paid API calls.
- Peak memory: <200 MB.

## Effort

- Wall-clock: ~30 minutes (agent time, including one debug cycle for the Bernoulli decoder + state-vector blow-up).
- Human effort saved: this replication would take a manual grad-student ~2-4 hours to code + run + report if familiar with quantum query complexity, and 1-2 days if not.
