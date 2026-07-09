# Artifacts summary — arXiv:1507.00432

All paths are relative to the target dir:
`~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1507.00432-approximate-span-programs-ito-jeffery/`

## The 8 mandatory artifacts

| # | Artifact | Path | Provenance / notes |
|---|---|---|---|
| 1 | Original PDF | `paper.pdf` | Fetched 2026-07-05 from `https://arxiv.org/pdf/1507.00432` (388 KB, 31 pages, v1) |
| 2 | Marker extraction | `extraction/marker.md` | Surrogate: PyMuPDF fitz v1.27.2.3 (Marker not installed on host — see `extraction/README.md`); 94 KB |
| 3 | Nougat extraction | `extraction/nougat.mmd` | Surrogate: `pdftotext -layout` (Nougat not installed on host — same README); 144 KB |
| 4 | LaTeX report | `report/REPORT.tex` | 18 KB, 7 sections + claims table + per-claim verdict + Q1..Q5. Compilation to PDF attempted; see `failure_analysis.md`. |
| 5 | Five open questions | `report/open_questions.json` + `Open Questions` section in REPORT.tex | 5 objects `{q, basis, next_steps}`, 4.9 KB; heavy-duty, grounded in this specific replication (non-monotone $w_-$, target-vs-input perturbation duality, learning-graph triangle span program, etc.) |
| 6 | Workflow | `report/workflow.md` | Timeline, tools/versions, LOC, effort, reproducibility one-liner |
| 7 | Artifacts summary | this file | Inventory + traces + sizes |
| 8 | Failure analysis | `report/failure_analysis.md` | Two real mid-replication frictions + one deliberate scope-cut |

## Evidence & code

| Path | Bytes | Description |
|---|---|---|
| `report/evidence/span_programs.py` | ~22 KB | Full implementation (533 LOC): SpanProgram class + 3 examples + main driver |
| `report/evidence/results.json` | ~6 KB | Machine-readable numerical results |
| `report/evidence/run_log.txt` | ~4 KB | Human-readable stdout of the run |

## Work directory

| Path | Description |
|---|---|
| `work/paper.txt` | `pdftotext -layout` dump of paper (used for skim + Sec 2 close reading) |

## Traces (what changed and when)

- `2026-07-05 18:11 CDT` — target dir created, `paper.pdf` fetched.
- `2026-07-05 18:13 CDT` — extractions written.
- `2026-07-05 18:15 CDT` — first `span_programs.py` written; first run: OR clean, AND anomaly at n>=6.
- `2026-07-05 18:17 CDT` — `span_programs.py` patched for AND single-zero sampling; rerun; ratio C/Q = 1.000 for all n. Final `results.json` produced.
- `2026-07-05 18:20 CDT` — `REPORT.tex`, `open_questions.json`, `workflow.md`, this file, and `failure_analysis.md` written.
- `2026-07-05 18:25 CDT` — LaTeX compile attempt for `REPORT.pdf` (see failure_analysis).

## Checksums

Run `md5 paper.pdf report/evidence/*.py report/evidence/*.json` to verify. Not embedded in this file to avoid staleness on rerun.

## No fabrication statement

Every numerical value in `report/evidence/results.json` and in the REPORT.tex Results tables is produced by executing `report/evidence/span_programs.py`. No values were hand-copied from the paper into results. Where the paper is cited (paper's $Q(\mathrm{OR}_n) = \Theta(\sqrt{n})$, paper's Sec 2.3 formula $w_+(x) = 1/|x|$), those are cross-checks *against* the numerical computation, not sources of numerical values.
