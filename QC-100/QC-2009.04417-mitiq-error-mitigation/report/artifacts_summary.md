# Artifacts Summary — QC-2009.04417 Mitiq

## Layout

```
QC-2009.04417-mitiq-error-mitigation/
├── code/
│   ├── zne_replicate.py                      # ZNE sweep (Qiskit-Aer)
│   └── cdr_replicate.py                      # CDR bonus (Cirq DM sim)
├── report/
│   ├── REPORT.md                             # narrative report (original, 2026-07-03)
│   ├── REPORT.tex                            # LaTeX equivalent + honest critique (backfill)
│   ├── open_questions.json                   # 5 open questions w/ concrete next_steps
│   ├── open_questions_section.tex            # LaTeX section, \input'd from REPORT.tex
│   ├── workflow.md                           # end-to-end procedure
│   ├── artifacts_summary.md                  # this file
│   ├── failure_analysis.md                   # honest critique of what was NOT done
│   └── evidence/
│       ├── zne_results.json                  # per-circuit ZNE table
│       └── cdr_results.json                  # CDR truth/raw/mitigated
├── extraction/
│   └── nougat.mmd                            # extraction stub (see note below)
├── logs/
│   ├── zne_run.log
│   └── cdr_run.log
├── work/
│   ├── paper.pdf                             # arXiv 2009.04417v4
│   └── paper.txt                             # pdftotext dump
└── .venv/                                    # Python 3.12 venv (mitiq 1.0.0 + qiskit 2.5.0)
```

## Original artifacts (2026-07-03 replication)

1. **code/zne_replicate.py** — 10-seed Qiskit-Aer ZNE sweep, three inference methods, depolarizing noise (p1=0.01, p2=0.04), depth-8 RB-like 2-qubit circuits.
2. **code/cdr_replicate.py** — Cirq DM CDR bonus, 7-op circuit, ⟨Z⊗I⟩ observable.
3. **report/REPORT.md** — full narrative report, verdict = REPLICATED.
4. **report/evidence/zne_results.json** — per-circuit truth/raw/richardson/poly/linear values (10 circuits × 5 fields).
5. **report/evidence/cdr_results.json** — {truth, raw, cdr} scalars.
6. **logs/zne_run.log**, **logs/cdr_run.log** — stdout captures from both scripts.
7. **work/paper.pdf**, **work/paper.txt** — arXiv 2009.04417v4 + text dump.

## Backfill artifacts (2026-07-06, this pass)

1. **report/REPORT.tex** — LaTeX version of REPORT.md, adds §"Honest critique" and §"Headline-exercised check", `\input`s open_questions_section.tex.
2. **report/open_questions.json** — bare JSON list of exactly 5 objects `{q, basis, next_steps}`. Each next_steps is concrete, uses free endpoints, and does not require re-running the existing sims.
3. **report/open_questions_section.tex** — LaTeX rendering of the 5 open questions, meant to `\input` from REPORT.tex.
4. **report/workflow.md** — end-to-end reproducer for the original replication (env build → script runs → verdict rule).
5. **report/artifacts_summary.md** — this file.
6. **report/failure_analysis.md** — honest, critical inventory of what the replication did NOT do.
7. **extraction/nougat.mmd** — extraction stub. Note: no full-paper Nougat OCR was run for this replication (the paper is open-access with a clean arXiv PDF; `pdftotext` on work/paper.txt was sufficient for claim extraction). Stub explains the deferral and lists the free-endpoint command that would produce a real .mmd if needed downstream.

## Verdict trace

- Original REPORT.md §5 → **REPLICATED**.
- Backfill REPORT.tex → **REPLICATED** (unchanged).
- Verdict rationale: both headline capability claims (ZNE Fig. 3, CDR §6) exercised on independent circuits + simulators; all three ZNE variants and CDR beat raw noisy on absolute error.

## Files preserved

All original files (REPORT.md, evidence/*.json, code/*.py, logs/*.log, work/*) were NOT modified during backfill. Only new files were added under report/ and extraction/.
