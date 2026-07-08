# Artifacts Summary — QC-2004.10344-two-electron-ansatz-benchmark

**Set:** QC-100. **Verdict:** REPLICATED (headline exercised). **Backfilled:** 2026-07-05.

## Top-level layout

```
QC-2004.10344-two-electron-ansatz-benchmark/
├── code/
│   ├── vqe_h2_compact.py          # main VQE run (openfermion + expm_multiply path)
│   ├── circuit_gate_counts.py     # Qiskit circuit build + statevector cross-check
│   └── plot_curve.py              # Fig. 1 replica plotter
├── results/
│   ├── h2_curve.json              # 18-point curve, raw numbers
│   ├── h2_curve.csv               # same, CSV
│   ├── h2_dissociation_curve.png  # visual reproduction of paper Fig. 1
│   ├── gate_counts.json           # parameter/CNOT/depth comparison table
│   ├── compact_circuit.txt        # compact-ansatz Qiskit circuit ASCII
│   └── uccsd_circuit.txt          # UCCSD-baseline Qiskit circuit ASCII
├── logs/
│   ├── vqe_run.log                # stdout of vqe_h2_compact.py
│   └── gate_counts.log            # stdout of circuit_gate_counts.py
├── work/
│   ├── paper.pdf                  # arXiv snapshot of 2004.10344v1
│   └── paper.txt                  # pdftotext extraction
├── extraction/
│   └── nougat.mmd                 # OCR stub (backfilled 2026-07-05)
└── report/
    ├── REPORT.md                  # original 2026-07-03 replication report
    ├── REPORT.tex                 # LaTeX rendering (backfilled)
    ├── open_questions.json        # 5 open questions, structured (backfilled)
    ├── open_questions_section.tex # LaTeX section for above (backfilled)
    ├── workflow.md                # method + reproduction recipe (backfilled)
    ├── artifacts_summary.md       # THIS FILE (backfilled)
    ├── failure_analysis.md        # honest critique (backfilled)
    └── evidence/                  # snapshotted copies of results/ for report
```

## Backfill inventory (2026-07-05)

Added 7 artifacts to bring this directory up to the 8-artifact standard:

| # | Artifact | Purpose |
|---|----------|---------|
| 1 | `report/REPORT.tex` | Publication-form LaTeX version of REPORT.md |
| 2 | `report/open_questions.json` | 5 machine-readable open questions with basis + next steps |
| 3 | `report/open_questions_section.tex` | LaTeX section rendering of (2) |
| 4 | `report/workflow.md` | Method + reproduction recipe + scope cuts |
| 5 | `report/artifacts_summary.md` | This file |
| 6 | `report/failure_analysis.md` | Honest critique of what was NOT properly exercised |
| 7 | `extraction/nougat.mmd` | Nougat OCR stub (paper text was extracted via pdftotext; nougat rerun deferred) |

The pre-existing REPORT.md (2026-07-03) is the 8th artifact and remains authoritative.

## Preservation contract

- **Nothing existing was overwritten.** All original code/, results/, logs/,
  work/, report/REPORT.md files are byte-identical to their 2026-07-03 state.
- **No re-runs.** No new simulation executed during backfill; all numbers cited
  in the new artifacts come from the pre-existing `results/` payload.
- **Free endpoints only.** Backfill involved no paid API calls, no cloud
  compute, no IBM Quantum runtime charges.

## Headline-exercised check

**YES.** The paper's headline (H2/STO-3G noise-free ansatz-expressiveness
curve) was independently reimplemented, run at 18 bond lengths, cross-checked
via two independent code paths (openfermion `expm_multiply` and Qiskit
`Statevector`), and compared against a self-built UCCSD baseline for
parameter and CNOT counts. Hardware-specific claims (C4, C5) are declared
out of scope in REPORT.md §2 with device-retirement rationale.
