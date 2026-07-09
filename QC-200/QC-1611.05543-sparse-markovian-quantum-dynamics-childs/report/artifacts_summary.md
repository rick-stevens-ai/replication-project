# Artifacts Summary — QC-1611.05543

Root: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1611.05543-sparse-markovian-quantum-dynamics-childs/`

## The 8 required artifacts (per REPLICATION_DIR_STANDARD_2026-07-05)

| # | Artifact | Path | Notes |
|---|---|---|---|
| 1 | Paper PDF | `paper.pdf` | 524 KB, 48 pages, arXiv:1611.05543v3 |
| 2 | Marker parse | `extraction/marker.md` | SURROGATE via PyMuPDF v1.27.2.3 (Marker CLI not installed; sibling-QC-200 convention) |
| 3 | Nougat parse | `extraction/nougat.mmd` | SURROGATE via `pdftotext -layout`; same convention |
| 4 | Detailed LaTeX report | `report/REPORT.tex` | Compiled → `report/REPORT.pdf` when `pdflatex` available |
| 5 | Open questions | `report/open_questions.json` (+ `## Open Questions` in REPORT) | 5 non-trivial questions, each `{q, basis, next_steps}` |
| 6 | Workflow | `report/workflow.md` | Tools/versions + time estimate + step-by-step |
| 7 | Artifacts summary | `report/artifacts_summary.md` | This file |
| 8 | Failure analysis | `report/failure_analysis.md` | Honest gaps + friction log |

## Evidence (under `report/evidence/`)

| File | What it is |
|---|---|
| `lindblad_sim.py` | ~370-line NumPy/SciPy simulator implementing all 5 experiments |
| `results.json` | Raw numerical outputs of every experiment (all 6 systems, all ε values, all t values, physical-sanity trajectory) |
| `sim_stdout.log` | Human-readable summary from the driver run |

## Working files (under `work/`)

| File | What it is |
|---|---|
| `paper.txt` | `pdftotext -layout` extraction — source of truth for reading the paper |

## Trace of tool invocations (chronological)

1. `curl -sL https://arxiv.org/pdf/1611.05543 -o paper.pdf`
2. `pdftotext -layout paper.pdf work/paper.txt`
3. `grep`-based location of Lemma 4, Theorem 8, Alg 1 references
4. `python3 -c "import fitz; ..."` → `extraction/marker.md`
5. `cat work/paper.txt >> extraction/nougat.mmd`
6. `python3 report/evidence/lindblad_sim.py` (attempt 1 — timed out on 1e-10 branch)
7. `python3 report/evidence/lindblad_sim.py` (attempt 2 — after ε_tot cap, ~3 s wall)
8. Reports authored.

## Result-quality signals

- `lemma4_short_time.loglog_slope` for every one of 6 tested Lindbladians is in [1.996, 1.998] against paper prediction of exactly 2.0.
- `theorem8_linear_in_t.queries_vs_t_loglog_slope` = **2.000** against paper prediction of exactly 2.0.
- Taylor sub-routine hits trace-distance error `1.03e-15` at target `ε=1e-12` on 2 qubits — floor of double-precision.
- All simulated states preserve trace to `1e-14` and non-negative eigenvalues throughout.

## Total artifact byte count

```
paper.pdf                  524 523
extraction/marker.md       108 909
extraction/nougat.mmd      198 395
report/REPORT.tex          (see file)
report/open_questions.json  ~6 400
report/workflow.md          ~4 800
report/artifacts_summary.md ~3 100
report/failure_analysis.md  ~5 000
report/evidence/*           ~25 000
work/paper.txt             ~197 000
```
