# Artifacts summary — QC-1904.10246-amplitude-estimation-no-pe

**Paper:** Suzuki et al., "Amplitude estimation without phase estimation,"
Quantum Information Processing 19, 75 (2020). arXiv:1904.10246.

**Set:** QC-100
**Verdict:** REPLICATED
**Runner:** Ollie (subagent), 2026-07-03 run + 2026-07-05 backfill

## Directory layout
```
QC-1904.10246-amplitude-estimation-no-pe/
├── code/
│   └── mlae_replicate.py              # from-scratch Qiskit MLAE implementation
├── extraction/
│   └── nougat.mmd                     # extraction stub (backfill)
├── logs/
│   └── main.log                       # stdout of the run
└── report/
    ├── REPORT.md                      # canonical replication narrative
    ├── REPORT.tex                     # LaTeX version (backfill)
    ├── open_questions.json            # 5 open questions with next steps (backfill)
    ├── open_questions_section.tex     # LaTeX open-questions section (backfill)
    ├── workflow.md                    # replication workflow (backfill)
    ├── artifacts_summary.md           # this file (backfill)
    ├── failure_analysis.md            # honest critique (backfill)
    └── evidence/
        └── results.json               # raw per-point RMSE + slopes
```

## Artifact inventory (8-artifact standard)

| # | Artifact | Path | Origin |
|---|---|---|---|
| 1 | REPORT.md | `report/REPORT.md` | 2026-07-03 run |
| 2 | REPORT.tex | `report/REPORT.tex` | 2026-07-05 backfill |
| 3 | open_questions.json | `report/open_questions.json` | 2026-07-05 backfill |
| 4 | open_questions_section.tex | `report/open_questions_section.tex` | 2026-07-05 backfill |
| 5 | workflow.md | `report/workflow.md` | 2026-07-05 backfill |
| 6 | artifacts_summary.md | `report/artifacts_summary.md` | 2026-07-05 backfill |
| 7 | failure_analysis.md | `report/failure_analysis.md` | 2026-07-05 backfill |
| 8 | extraction/nougat.mmd | `extraction/nougat.mmd` | 2026-07-05 backfill stub |

Plus supporting evidence: `code/mlae_replicate.py`, `logs/main.log`,
`report/evidence/results.json` (raw scientific outputs).

## Headline result
Three scaling slopes (log₁₀ RMSE(a) vs log₁₀ Nq) at a = 1/48, N_shot = 100,
100 trials/point:

| Schedule | Ours | Paper | Δ |
|---|---:|---:|---:|
| Classical | −0.516 | −0.50 | +0.016 |
| LIS       | −0.727 | −0.76 | +0.033 |
| EIS       | −0.930 | −0.95 | +0.020 |

All within ±0.04. At matched Nq ≈ 5×10⁴, EIS delivers ~10× lower RMSE than
classical extrapolation, confirming the paper's "quantum advantage without
QFT" practical claim.

## What was exercised (headline test)
- Independent from-scratch Qiskit reimplementation of A and Q ✓
- Real shot-based simulation on qiskit-aer (not analytic) ✓
- Independent MLE estimator (grid + polish) ✓
- All three scaling slopes reproduced within ±0.04 ✓
- Head-to-head RMSE at matched query budget ✓ (~10× advantage confirmed)

## What was NOT exercised (see failure_analysis.md)
- No canonical QAE (QPE-based) side-by-side comparison
- Noiseless simulation only (no NISQ noise model)
- Single amplitude only (a = 1/48; no branch-identifiability sweep)
- No comparison to modern successors (Iterative QAE, Faster QAE)
- No end-to-end application benchmark (quant finance, etc.)

## No-cost, local-only
No paid API calls. No proprietary data. Entirely local classical simulation
on CherryRd. Reproducible by anyone with qiskit + qiskit-aer.
