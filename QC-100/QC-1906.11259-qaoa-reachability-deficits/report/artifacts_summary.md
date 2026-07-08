# Artifacts summary — QC-1906.11259-qaoa-reachability-deficits

## Directory layout
```
QC-1906.11259-qaoa-reachability-deficits/
├── code/
│   ├── qaoa_reachability.py      # ~150-line from-scratch QAOA statevector engine + sweep driver
│   ├── smoke.py                  # 3 unit tests (clause truth, plus-state, mixer unitarity)
│   └── plot_results.py           # post-processing: CSV + fig + monotonicity assertions
├── data/
│   ├── qaoa_3sat_sweep.json      # per-instance raw f values (7α × 3p × 15 inst = 315 rows)
│   └── qaoa_3sat_summary.csv     # mean±SEM table (§4.1 of REPORT.md)
├── figures/
│   └── fig1_analog_deficit_vs_alpha.png   # reproduction of paper Fig. 1 (top)
├── logs/
│   └── sweep_main.log            # timestamped stdout of full run (515s wall)
├── extraction/
│   └── nougat.mmd                # OCR/text extraction stub (backfilled)
└── report/
    ├── REPORT.md                 # main narrative (2026-07-03)
    ├── REPORT.tex                # LaTeX version w/ honest critique (backfilled)
    ├── open_questions.json       # 5 open Qs, bare JSON list (backfilled)
    ├── open_questions_section.tex
    ├── workflow.md
    ├── artifacts_summary.md      # this file
    ├── failure_analysis.md       # what didn't work / what we couldn't test
    └── evidence/                 # mirror of key outputs (CSV, JSON, fig, log)
```

## Artifact provenance
| Artifact | Generator | Verified |
|---|---|---|
| `code/qaoa_reachability.py` | hand-written NumPy | `code/smoke.py` passes 3/3 |
| `data/qaoa_3sat_sweep.json` | main sweep, seed=20260703 | reproducible bit-for-bit |
| `data/qaoa_3sat_summary.csv` | `plot_results.py` from sweep JSON | matches §4.1 table |
| `figures/fig1_analog_deficit_vs_alpha.png` | `plot_results.py` | 3 curves, error bars, α=1 marker |
| `logs/sweep_main.log` | tee of sweep run | 515 s wall, timestamps present |
| `report/REPORT.md` | manually written from data | verdict backed by §4.2 monotonicity checks |
| `report/REPORT.tex` | backfill 2026-07-06 | honest critique section §4 |
| `report/open_questions.json` | backfill | 5 items, all with basis + concrete next_steps |

## Headline-exercised check
✅ The paper's Fig. 1 reachability-deficit curves were **independently regenerated** end-to-end:
- Fresh 3-SAT instances (not paper's — different seed)
- From-scratch QAOA engine (not Qiskit/PennyLane)
- Independent optimizer (COBYLA + 4 restarts)
- Deficit computed at 7 α × 3 p cells and plotted vs α

Not quoted from paper; regenerated. Verdict: REPLICATED (qualitative, scaled-down p).

## Free-endpoint compliance
- No LLM calls during the replication itself (pure classical CPU sim).
- No paid API. No GPU. No cluster time.
- Backfill (this pass) used no external resources — pure local file writes.
