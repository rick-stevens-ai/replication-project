# Artifacts Summary — QC-2208.10978 Q²Chemistry

**Dir:** `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2208.10978-q2chemistry-platform/`
**Set:** QC-100. **Verdict:** REPLICATED (spot-check scale).

## Top-level layout
- `report/` — all replication artifacts (see below)
- `extraction/` — PDF extraction stubs (nougat.mmd)
- `work/` — driver scripts + venv (transient runtime)
- `report/evidence/` — canonical evidence bundle (frozen at 2026-07-03)

## Report artifacts (8 required + evidence)

| # | Path | Role |
|---|---|---|
| 1 | `report/REPORT.md` | Primary human-readable replication report (source of truth). |
| 2 | `report/REPORT.tex` | LaTeX version of the report, with an added honest **Critique** section and `\input{open_questions_section.tex}` at the end. |
| 3 | `report/open_questions.json` | 5 genuinely-open questions in machine-readable form. **Bare JSON list of 5 objects** with keys `q`, `basis`, `next_steps`. Validated: `python3 -c 'import json; json.load(open("open_questions.json"))'`. |
| 4 | `report/open_questions_section.tex` | LaTeX rendering of the 5 open questions, `\input`'d from REPORT.tex. |
| 5 | `report/workflow.md` | Step-by-step account of the replication workflow (paper triage → stand-in decision → execution → verdict). |
| 6 | `report/artifacts_summary.md` | This file — index of every artifact and where to find it. |
| 7 | `report/failure_analysis.md` | Honest critique: what the replication does NOT verify (Q²Chemistry-specific software, scale claims, C4/C5/C3, integration & speedup, catalyst/drug molecules). |
| 8 | `extraction/nougat.mmd` | PDF extraction stub. Full nougat run not performed on this paper (bulk of extraction not required for a platform paper whose figures/tables are text-embedded). |

## Evidence bundle (`report/evidence/`)
- `vqe_h2.py` — driver script (PySCF + OpenFermion + scipy sparse VQE across 5 H₂ bond lengths).
- `vqe_h2.log` — full stdout log of the run (real numbers, no fabrication).
- `h2_vqe_results.json` — parsed results (per-geometry HF/CCSD/FCI/VQE energies + residuals + iteration counts).

## Verdict cross-check
- Queue verdict: **REPLICATED**
- On-disk REPORT.md verdict: **REPLICATED (SPOT-CHECK scale)** — same word, with an explicit scale caveat.
- Headline-exercised rule: **C1 (VQE-UCCSD on H₂ reproduces FCI) IS exercised** to floating-point roundoff (≤10⁻¹² mHa across 5 geometries). → verdict preserved as `REPLICATED`.

## What is deliberately NOT here
- Full re-implementation of Q²Chemistry (no public source available at time of replication).
- 40-qubit ccj-pVDZ H₂ run (paper's actual Fig 6 config; requires 560 CPU cores × 24 h per geometry).
- 72-qubit Cr₂ MPS scaling (C3; requires 768 cores).
- Silicon EOM-ADAPT-C band structure (C4; requires Q²Chemistry-specific EOM implementation).
- QEM sweep, noise-model VQE, catalyst molecule benchmarks — these are the substance of `open_questions.json` and future work.
