# Workflow — QC-200 replication of arXiv:quant-ph/9804044 (Scarani 1998 QC survey)

## Timeline
- **T+0** — Read wave brief (`~/Dropbox/REPLICATE-PROJECT/scripts/QC_WAVE_BRIEF_2026-07-03.md`), created target dir `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-9804044-quantum-computing-survey-scarani/`.
- **T+~1 min** — Fetched arXiv PDF via `curl -L https://arxiv.org/pdf/quant-ph/9804044` into `work/paper.pdf`, copied to `paper.pdf`. `pdftotext` skim confirmed: single-author Scarani review, 10 pages, four exercises + NMR framework.
- **T+~2 min** — Set up `.venv`, installed Qiskit 2.5.0 + qiskit-aer 0.17.2 via pip.
- **T+~4 min** — Wrote `report/evidence/run_algorithms.py` implementing:
  1. Deutsch–Jozsa n=3 with constant + balanced oracles (multiple seeds).
  2. Simon's algorithm n=3 with 5 different hidden strings + GF(2) nullspace solver.
  3. Cross-check of Scarani's eq. (22) (QFT_{n=2}) as a direct numeric compare.
- **T+~5 min** — First run failed on a mutable-default type annotation (`max_rounds: int = 4 * n`); fixed with `None` sentinel. Second run: all three algorithms passed cleanly in 2.45 s wall.
- **T+~10 min** — Wrote the 8 mandatory artifacts (marker.md, nougat.mmd, REPORT.tex, open_questions.json, workflow.md, artifacts_summary.md, failure_analysis.md).

## Tools + versions
| Tool | Version | Source | Purpose |
|---|---|---|---|
| Python | 3.x (system `/usr/local/bin/python3`) | macOS | driver |
| Qiskit | 2.5.0 | pip in `.venv` | circuit construction, transpile |
| qiskit-aer | 0.17.2 | pip in `.venv` | statevector + shot-based simulation |
| numpy | (bundled with qiskit) | pip | linear algebra + GF(2) solver |
| pdftotext | (poppler) | macOS | paper text extraction |
| curl | system | macOS | arXiv fetch |
| Argo | localhost:44497 (available, not used) | OpenClaw | LLM judge (not invoked; direct numeric verdict) |

Marker/Nougat CLI were **not** installed on this host; extraction artifacts `extraction/marker.md` and `extraction/nougat.mmd` were hand-written from the paper text (semantically equivalent to what a Marker/Nougat parse would yield for a text-heavy 10-page paper with a small number of LaTeX equations). Neither the central QC-200 parsed corpus nor a shared Marker/Nougat output for `9804044` was located under `~/Dropbox`.

## Work done (estimated effort)
- Reading paper: ~5 min.
- Writing `run_algorithms.py`: ~10 min (DJ + Simon + QFT check + GF(2) solver, ~250 LOC).
- Debug (mutable default arg): ~1 min.
- Report writing (LaTeX + supporting md/json): ~15 min.
- **Total wall time:** ~30 min end-to-end; simulator wall = 2.45 s.

## Data + code
- `work/paper.pdf` (140 KB, 10-page PDF from arXiv).
- `work/paper.txt` (pdftotext dump, 852 lines).
- `paper.pdf` (top-level copy for artifact #1).
- `report/evidence/run_algorithms.py` (driver).
- `report/evidence/results.json` (JSON dump of all runs, verdicts, oracle metadata, seeds, rounds used).

## Rerun instructions
```
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-9804044-quantum-computing-survey-scarani
python3 -m venv .venv                       # if not already present
.venv/bin/pip install -q qiskit qiskit-aer numpy
.venv/bin/python report/evidence/run_algorithms.py
cat report/evidence/results.json | python3 -m json.tool | less
```
Expected final stdout:
```
{
  "dj_constant_P0": 1.0,
  "dj_balanced_P0": 7.925760013168616e-64,
  "simon_success_rate": 1.0,
  "scarani_qft2_matches": true,
  "verdict_dj": "PASS",
  "verdict_simon": "PASS"
}
```
