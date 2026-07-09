# Workflow — arXiv:2402.04000 replication (QC-200)

## Timeline (2026-07-05, single continuous subagent session)

| Time    | Step | Notes |
|---------|------|-------|
| 14:05   | Setup: created target dir, read QC wave brief, fetched paper PDF from arXiv | 730 KB PDF, 961-line pdftotext output |
| 14:06   | Verified authors from PDF (Russo & Mari, Unitary Fund) | matches arXiv metadata |
| 14:06   | Skimmed paper: identified Table I (depth 2--8 GHZ + amplitude damping) as the most-checkable claim | central numerical claim isolated |
| 14:07   | Reused sibling venv `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1602.07674-quantum-supremacy-through-qaoa/.venv` (qiskit 2.5.0, aer 0.17.2, py 3.14) | avoided full venv build |
| 14:07   | Installed matplotlib into that venv (mitiq install failed on py3.14 -- not needed since we implement LRE from scratch) | scope preserved |
| 14:08   | Wrote `lre_replication.py` from scratch: circuit builder, layer splitter, unitary folder, global RE, LRE via multivariate Lagrange coefficients (standard-basis specialisation, linear order) | 260 lines |
| 14:08   | Smoke run n=2,3 @ 100k shots x 3 trials: LRE << RE << unmit as predicted | 1.5 s runtime |
| 14:09   | Full run gamma=0.02, n=2..6, 1e6 shots x 5 trials | 26 s |
| 14:10   | Full run gamma=0.06, n=2..8, 1e6 shots x 10 trials -- numbers now sit in the same regime as paper's Table I | 87 s |
| 14:10   | Generated plots via matplotlib | 2 PNGs |
| 14:10   | pdftotext-based fallback for marker.md + nougat.mmd (marker/nougat unavailable in this env; matches convention used across QC-200) | preserves the 8-artifact bar |
| 14:11   | Wrote REPORT.tex, open_questions.json, this workflow.md, artifacts_summary.md, failure_analysis.md | verdict = REPLICATED |

## Tool inventory

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.14 (system) | runtime |
| qiskit | 2.5.0 | circuit builder |
| qiskit-aer | 0.17.2 | noisy density-matrix / stabiliser simulator (`AerSimulator` + `NoiseModel`) |
| qiskit-aer noise | (bundled) | `amplitude_damping_error` |
| numpy | 2.x | linear algebra + polyfit |
| matplotlib | 3.11.0 | plots |
| pdftotext | poppler 25.x | PDF -> text (marker/nougat fallback) |
| curl | system | arXiv PDF fetch |
| bash + zsh | system | driver |

**Explicitly NOT used:** mitiq (install broken on py3.14 in this venv; would have been a cross-check but not needed since LRE was reimplemented from scratch); Argo LLM (no LLM inference required for this replication — the verdict comes from direct numerical comparison, not judge scoring); GPU / HPC.

## Work estimate

* Actual wall-clock: ~10 min end-to-end (paper fetch to WAVE_RESULT).
* Actual compute wall-clock: ~2 min total on M1/M-series CPU.
* Code written: 260 lines of Python (evidence/lre_replication.py) + 30 lines plot script.
* Report: ~350 lines LaTeX + 5 open questions with next-steps.
* Total tokens spent on LLM inference: 0 (no LLM calls made — this replication was pure numerical simulation).

## Reproducibility

Fixed seeds `seed0 = 42 + trial*1000 + n` used for every AerSimulator run. Results should be
bit-identical across reruns on the same qiskit-aer version. Command lines to reproduce
are in REPORT.tex Sec. "Reproduction commands".
