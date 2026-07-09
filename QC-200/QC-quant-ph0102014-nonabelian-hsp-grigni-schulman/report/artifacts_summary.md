# Artifacts Summary

Files produced by this replication:

## Top-level
- `paper.pdf` — the arXiv paper (174 143 B)

## `extraction/`
- `marker.md` — human/marker-style structured extraction: identification correction, section-by-section technical summary, claims table (C1–C6)
- `nougat.mmd` — fallback notice explaining marker/nougat unavailability and the pdftotext fallback

## `work/`
- `paper.txt` — pdftotext output of paper.pdf (606 lines, 43 825 B). Full textual fidelity.
- `hsp_ims_theorem13.py` — Theorem 13 replication driver (WreathGroup, oracle builder, 3-step reduction, dual computation paths, sweep loop)
- `lemma9_verify.py` — Lemma 9 quantum-oracle exact-marginal verifier
- `run_final.log`, `run2.log`, `run3.log` — successive execution logs (kept for debug provenance)
- `.venv/` — Python 3 virtualenv with qiskit, qiskit-aer, numpy

## `report/`
- `REPORT.md` — full report (paper summary, claims, method, results, verdict, 5 open questions)
- `REPORT.tex` — LaTeX version of REPORT.md
- `brief.md` — one-paragraph summary
- `attempt_log.md` — chronological narrative of the session (what worked, what broke)
- `artifact_harvest.md` — external artifacts pulled or referenced
- `workflow.md` — data-flow diagram + repro commands + effort estimate
- `open_questions.json` — 5 heavy-duty follow-on questions with `{q, basis, next_steps}`
- `failure_analysis.md` — post-mortem on the two implementation bugs encountered
- `artifacts_summary.md` — this file

### `report/evidence/`
- `theorem13_wreath_results.json` — 24 trials, k ∈ {1,2,3,4}, |G| up to 512, ALL PASSED. Includes planted vs recovered subgroups (as sets), sample counts, wall time.
- `theorem13_run.log` — verbose per-trial Abelian-HSP sampling trace for k=1, k=2, k=3, k=4 first trials.
- `lemma9_verification.json` — 20 Lemma-9 trials with per-trial max_in_perp_deviation and max_out_of_perp_prob (all at machine-epsilon).
- `llm_judge_verdict.json` — LLM-judge run (argo:gpt-5 via litellm aggregator) with the exact prompt-in and JSON-out verdict PARTIAL / confidence high.

## 8-artifact bar status

| # | File | Present |
|--:|---|:-:|
| 1 | `paper.pdf` | ✅ |
| 2 | `extraction/marker.md` | ✅ |
| 3 | `extraction/nougat.mmd` | ✅ (fallback notice; real nougat unavailable in env) |
| 4 | `report/REPORT.tex` | ✅ |
| 5 | `report/open_questions.json` (5 heavy `{q, basis, next_steps}`) + `## Open Questions` in REPORT.md | ✅ |
| 6 | `report/workflow.md` | ✅ |
| 7 | `report/artifacts_summary.md` | ✅ |
| 8 | `report/failure_analysis.md` | ✅ |
