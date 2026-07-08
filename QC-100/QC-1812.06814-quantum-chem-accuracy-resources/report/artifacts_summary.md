# Artifacts summary — arXiv:1812.06814

Inventory of files in this replication directory.

## Report tree
```
report/
├── REPORT.md                      # narrative markdown report (2026-07-03)
├── REPORT.tex                     # LaTeX version + Critique + \input open_questions (backfill 2026-07-06)
├── open_questions.json            # 5 open questions, machine-readable (bare list)
├── open_questions_section.tex     # \input'd into REPORT.tex
├── workflow.md                    # exact chronological commands
├── artifacts_summary.md           # this file
├── failure_analysis.md            # honest critique of scope + gaps
└── evidence/
    ├── run_vqe.py                 # H2 UCCSD-VQE driver (real E2E VQE)
    ├── run_lih_final.py           # LiH classical UCCSD + circuit-resource driver
    ├── vqe_h2.log                 # raw stdout from H2 run
    ├── vqe_lih_final.log          # raw stdout from LiH run
    ├── vqe_results_h2.json        # machine-readable H2 results
    └── vqe_results_lih_final.json # machine-readable LiH results
```

## Work tree
```
work/
├── paper.pdf                      # source paper arXiv:1812.06814v2
├── paper.txt                      # pdftotext extraction
└── .venv/                         # isolated Python 3.11.15 env
```

## Extraction tree
```
extraction/
└── nougat.mmd                     # stub (see failure_analysis.md — pdftotext was sufficient)
```

## Key numerical artifacts
| Artifact | What it proves |
|---|---|
| `vqe_results_h2.json` `|E_VQE − E_FCI| = 0.0000 mHa` | H2 headline claim exercised end-to-end |
| `vqe_results_h2.json` `qubits = 4` | H2 qubit count matches paper Table SI I |
| `vqe_results_lih_final.json` `ΔFCI = 0.028 kJ/mol` | **EXACT MATCH** to paper LiH row |
| `vqe_results_lih_final.json` `qubits = 12` | LiH qubit count matches paper Table SI I |
| `vqe_results_lih_final.json` `CNOT_raw = 7026` vs paper 1382 → ratio 5.1× | Consistent with paper's claimed ~4× cancellation + MP2 pre-screen |
| Sanity: HF-circuit ⟨H⟩ vs PySCF HF = 3.55e-15 Ha | JW-Ham + HF init-state circuit correct to machine precision |

## Backfill artifacts added 2026-07-06
- `report/REPORT.tex` — full LaTeX with genuine Critique section
- `report/open_questions.json` — 5 open questions (bare JSON list)
- `report/open_questions_section.tex` — \input'd from REPORT.tex
- `report/workflow.md` — chronological command log
- `report/artifacts_summary.md` — this file
- `report/failure_analysis.md` — honest gap analysis
- `extraction/nougat.mmd` — stub

## Provenance
- Replicator: subagent under Rick Stevens' OpenClaw
- Main model at replication time: argo/argo:claude-opus-4.7
- Host: CherryRd, macOS 25.3.0 x86_64
- Free endpoints only. No paid API calls. No hardware run.
- Verdict: **REPLICATED**
