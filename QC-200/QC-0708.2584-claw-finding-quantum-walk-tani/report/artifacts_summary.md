# Artifacts summary — 0708.2584 (Tani, 2007)

## 8-artifact bar (mandatory per REPLICATION_DIR_STANDARD_2026-07-05.md)

| # | Artifact | Path | Present? | Notes |
|---|----------|------|----------|-------|
| 1 | Original PDF | `paper.pdf` | YES | 121 792 B, 12 pp, PDF 1.4 (arXiv v2, 3 Mar 2008) |
| 2 | Marker extraction | `extraction/marker.md` | YES (surrogate) | PyMuPDF fitz 1.27.2.3 — Marker not installed; header labels the tool |
| 3 | Nougat extraction | `extraction/nougat.mmd` | YES (surrogate) | Poppler pdftotext -layout — Nougat not installed; header labels the tool |
| 4 | LaTeX report | `report/REPORT.tex` | YES | Full section-by-section detailed report, `\input`s open questions |
| 5 | Open questions | `report/open_questions.json` (+ `open_questions.tex`) | YES | Exactly 5 non-generic, each with `q`/`basis`/`next_steps` |
| 6 | Workflow + tools + effort | `report/workflow.md` | YES | Chronological + versions + LOC + wall-clock |
| 7 | Artifacts summary | `report/artifacts_summary.md` | YES | (this file) |
| 8 | Failure analysis | `report/failure_analysis.md` | YES | Honest scope + gap statement |

## Additional artifacts

| Path | Bytes | Purpose |
|------|------:|---------|
| `work/paper.txt` | — | pdftotext dump used for claim extraction |
| `work/sim_claw_qwalk.py` | 9 602 | Main simulation code |
| `work/sim_r_sweep.py` | 1 981 | r-sweep code |
| `work/run.log` | — | stdout of main sim |
| `work/r_sweep.log` | — | stdout of r-sweep |
| `report/evidence/results.json` | — | N-sweep numeric results (per-N k*, eps, dim, planted claw) |
| `report/evidence/r_sweep.json` | — | r-sweep numeric results incl. empirical arg-min per N |
| `extraction/README.md` | 693 | Surrogate provenance note (same convention as QC-0704.3628) |

## Traces
- `work/run.log`: full N-sweep output including per-N `k*`, `peak_marked_mass`, `wall_s`, and the log-log fit slopes (`k*` vs N: 0.453; total-Q vs N: 0.512; grover-ideal vs N: 0.365).
- `work/r_sweep.log`: full r-sweep at N ∈ {6,8,10,12}, with the empirical arg-min r and total-Q at each N (4/4 match theory r=⌈N^(2/3)⌉).

## Provenance and verification chain
- Paper hash: `sha256sum paper.pdf` (see below).
- Marker surrogate: PyMuPDF version pinned in header line.
- Nougat surrogate: `pdftotext -layout` (Poppler) — deterministic on the same PDF.
- Simulation seed: `numpy.random.default_rng(42)` (fixed across all runs).
- All claims cross-checkable by running `python3 work/sim_claw_qwalk.py` and `python3 work/sim_r_sweep.py`.
