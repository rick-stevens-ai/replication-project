# Artifacts Summary — QC-1712.03554 Stabilizer Frames

Target dir: `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1712.03554-stabilizer-frames-circuit-sim/`
Set: QC-100
Verdict: **REPLICATED**

## Files present (post-backfill)

### Top-level reports
| Path | Purpose | Origin |
|---|---|---|
| `report/REPORT.md` | Full narrative replication report (Markdown, canonical) | original run 2026-07-04 |
| `report/REPORT.tex` | LaTeX version of report with honest Critique section + `\input{open_questions_section.tex}` | backfill 2026-07-06 |
| `report/open_questions.json` | 5-item structured open questions | backfill 2026-07-06 |
| `report/open_questions_section.tex` | LaTeX render of the 5 open questions (input to REPORT.tex) | backfill 2026-07-06 |
| `report/workflow.md` | End-to-end pipeline walk (paper → claims → code → sims → judge → verdict) | backfill 2026-07-06 |
| `report/artifacts_summary.md` | This file | backfill 2026-07-06 |
| `report/failure_analysis.md` | Honest self-critique: what wasn't tested, why, and confidence-lowering caveats | backfill 2026-07-06 |

### Evidence (`report/evidence/`)
| Path | Purpose |
|---|---|
| `stabilizer_frame.py` | From-scratch stabilizer-frame simulator, ~205 lines Python (Branch class + Clifford append + rank-2 T-split + Qiskit sum-out) |
| `run_experiment.py` | Deterministic-seed driver: main sweep n∈{6,8,10}×t∈{0..4} + scaling probe t∈{5..8} + Stim cross-check |
| `results.json` | Raw JSON of every (n, t) run: χ, frame_time_s, qiskit_time_s, max_amp_err, l2_err |
| `judge.json` | Raw + parsed replies from 3-endpoint LLM-judge panel (gpt-4.1, gemini-2.5-pro, gpt-5.2) |

### Work dir (`work/`)
Source-of-truth copies of the simulator + driver (same as `report/evidence/` copies; kept for the "run this to reproduce" recipe in REPORT.md §3e).

### Extraction (`extraction/`)
| Path | Purpose |
|---|---|
| `nougat.mmd` | Nougat OCR stub (arXiv 1712.03554 is text-native; no OCR needed for this paper) |

## Reproduce

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1712.03554-stabilizer-frames-circuit-sim/
python3 -m venv .venv && source .venv/bin/activate
pip install stim qiskit qiskit-aer numpy
python work/run_experiment.py
```

Deterministic seeded runs; every reported number in the results table is regenerable.

## Verified versions
- Python 3.14.6, macOS 25.3.0 x64 (m1)
- stim 1.16.0, qiskit 2.5.0, qiskit-aer 0.17.2, numpy 2.5.0
- All free/open. No paid endpoints.

## Claim coverage vs 8-artifact standard
| Standard slot | Present? | File |
|---|:---:|---|
| Full report (MD) | ✅ | `report/REPORT.md` |
| Full report (LaTeX) | ✅ | `report/REPORT.tex` |
| Open questions (JSON) | ✅ | `report/open_questions.json` (5 items) |
| Open questions (LaTeX section) | ✅ | `report/open_questions_section.tex` |
| Workflow | ✅ | `report/workflow.md` |
| Artifacts summary | ✅ | `report/artifacts_summary.md` |
| Failure analysis | ✅ | `report/failure_analysis.md` |
| Extraction stub | ✅ | `extraction/nougat.mmd` |
