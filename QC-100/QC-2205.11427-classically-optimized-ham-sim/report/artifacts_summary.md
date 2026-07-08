# Artifacts Summary — QC-2205.11427

Directory: `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2205.11427-classically-optimized-ham-sim/`

## Top-level layout

```
QC-2205.11427-classically-optimized-ham-sim/
├── .venv/                           (python 3.13; numpy, scipy, qiskit, qiskit-aer)
├── src/
│   ├── replicate.py                 ~13 KB — numpy sim (H, ansatz, Trotter, optimizer, ε_approx)
│   └── qiskit_crosscheck.py         numpy vs Qiskit 2.5 native-gate unitary comparison
├── work/
│   ├── 2205.11427.pdf               arXiv v5 (2 Jun 2023) as pulled 2026-07-03
│   └── 2205.11427.txt               pdftotext dump used for reading
├── report/
│   ├── REPORT.md                    original replication report (source of truth)
│   ├── REPORT.tex                   LaTeX-packaged version (this backfill)
│   ├── open_questions.json          5 open questions with basis + next_steps (bare list)
│   ├── open_questions_section.tex   same 5 open questions, LaTeX enumerate
│   ├── workflow.md                  step-by-step replication procedure
│   ├── artifacts_summary.md         this file
│   ├── failure_analysis.md          honest critique of what was NOT done
│   └── evidence/
│       ├── sweep.csv                4 × 3 × 3 = 36 rows of ε_approx (raw)
│       ├── sweep.json               same, machine-readable
│       ├── sweep.log                stdout of replicate.py (optimizer traces + timing)
│       ├── qiskit_crosscheck.json   Frobenius-norm + ε_approx comparison
│       ├── qiskit_crosscheck.log    stdout of qiskit_crosscheck.py
│       └── opt_L2_qiskit_circuit.qasm   OpenQASM 3.0 of the optimized L=2 brickwall (31 gates, depth 13)
└── extraction/
    └── nougat.mmd                   stub — no Nougat OCR was run (native LaTeX source on arXiv)
```

## What each artifact certifies

- **REPORT.md / REPORT.tex** — narrative summary + verdict (REPLICATED) with claim table and citation to raw evidence.
- **open_questions.json / open_questions_section.tex** — 5 concrete follow-on questions on the frontier of the paper (time-dependent H, higher-order composition, chemistry / lattice-gauge, noise robustness, meta-learned optimizer).
- **workflow.md** — step-by-step procedure so a third-party can reproduce start to finish.
- **failure_analysis.md** — HONEST enumeration of what was NOT tested, quantitative under-shoots, and threats to the verdict.
- **evidence/sweep.csv,json,log** — raw numerical output of `src/replicate.py`. All ratios in the report table are recomputable from these.
- **evidence/qiskit_crosscheck.json,log** — independent-implementation cross-check demonstrating the numpy unitaries agree with a native-gate Qiskit circuit to machine precision.
- **evidence/opt_L2_qiskit_circuit.qasm** — the actual OpenQASM 3.0 program that realizes the classically-optimized L=2 brickwall. Portable to any OpenQASM-3-compatible backend.
- **extraction/nougat.mmd** — stub only. Paper has native LaTeX source on arXiv; PDF text extraction was via `pdftotext` (`work/2205.11427.txt`), not Nougat. No LUCID-style OCR was needed.

## Artifact count

- Pre-existing (before this backfill): REPORT.md + 6 evidence files + 2 source files + 2 work files = 11 artifacts.
- Added by this backfill: REPORT.tex, open_questions.json, open_questions_section.tex, workflow.md, artifacts_summary.md, failure_analysis.md, extraction/nougat.mmd stub = **7 artifacts added**.
- Total after backfill: 18 artifacts.
