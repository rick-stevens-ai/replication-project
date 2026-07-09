# Artifacts Summary

**Target dir:** `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0301093-exact-qft-discrete-log-hallgren/`

## The 8 required artifacts (per QC wave brief, Rick 2026-07-05 standard)

| # | Artifact | Path (relative) | Status | Notes |
|---|---|---|---|---|
| 1 | Original PDF | `paper.pdf` | ✅ | 147,602 bytes, fetched from arXiv 2026-07-05 |
| 2 | Marker parse | `extraction/marker.md` | ⚠️ FALLBACK | Marker not installed on host; labeled `pdftotext -layout` fallback with clear provenance header |
| 3 | Nougat parse | `extraction/nougat.mmd` | ⚠️ FALLBACK | Nougat not installed on host; labeled `pdftotext -layout` fallback with clear provenance header |
| 4 | Detailed LaTeX report | `report/REPORT.tex` | ✅ | Full section-by-section with abstract, claims table, method, results table, verdict, open questions. LaTeX source only — PDF compilation not attempted in this session (see failure analysis) |
| 5 | Open questions | `report/open_questions.json` + `## Open Questions` in REPORT.tex | ✅ | 5 heavy-duty questions with `{q, basis, next_steps}`; all grounded in what was actually observed/run |
| 6 | Workflow | `report/workflow.md` | ✅ | Full pipeline with pinned tool versions and time-estimate |
| 7 | Artifacts summary | `report/artifacts_summary.md` | ✅ | (this file) |
| 8 | Failure analysis | `report/failure_analysis.md` | ✅ | Honest analysis of what failed, why, and what remains |

## Evidence files

| File | Bytes | Contents |
|---|---|---|
| `report/evidence/exact_qft_verify.py` | ~5 KB | Script: verify DFT_N unitarity + Qiskit QFT cross-check |
| `report/evidence/results_qft.json` | ~3 KB | Numeric results: max unitarity err 4.0e-14, formula err 3.5e-16 |
| `report/evidence/pbar_success_prob.py` | ~3 KB | Script: compute p_bar and its p → ∞ limit |
| `report/evidence/results_pbar.json` | ~3 KB | Convergence table + 0.451412 vs paper 0.4514 |
| `report/evidence/shor_dlog_p7.py` | ~5 KB | Script: Shor dlog for cyclic group of prime order p |
| `report/evidence/results_dlog.json` | ~5 KB | Per-instance success probs for p=7 (0.85714) and p=11 (0.90909) |

## Work-in-progress / staging

| File | Contents |
|---|---|
| `work/paper.pdf` | Source PDF (duplicate of top-level) |
| `work/paper.txt` | pdftotext -layout extraction, 447 lines, 27 KB |
| `work/debug_dlog.py` | Diagnostic used to trace initial sign-convention slip |
| `work/debug_dlog2.py` | Second diagnostic that revealed the wrong-order (r = p-1) setup |
| `venv/` | Local Python virtualenv (not tracked; recreate from `pip install ...`) |

## Traces (what the human/agent chain-of-work looked like)

1. Fetched arxiv → verified author (Mosca & Zalka, not Hallgren)
2. `pdftotext` → skim → extract 3 headline testable claims
3. Set up venv, install qiskit/numpy/scipy/sympy
4. Wrote 3 simulation scripts + ran; QFT + p_bar passed on first run; dlog failed
5. Debug: first `debug_dlog.py` showed a=2, r=6 gives d ∈ {0,2,4} due to gcd(2,6)=2; second `debug_dlog2.py` confirmed that inverse-QFT convention didn't help
6. Traced back to paper Sec 3 — the paper uses cyclic group of *prime order p* (α^p = e), i.e., register dim = p, arithmetic mod p, QFT_p. Not r = p-1.
7. Rewrote `shor_dlog_p7.py` per correct convention → clean 1 - 1/p match to 1e-16
8. Wrote LaTeX report, workflow, open questions, artifacts summary, failure analysis
9. Generated fallback extraction/marker.md + extraction/nougat.mmd

## Verdict

**REPLICATED** — all three testable numeric claims of the paper reproduced within machine precision (1e-14 unitarity, 1e-16 dlog, 1e-5 p_bar asymptotic).
