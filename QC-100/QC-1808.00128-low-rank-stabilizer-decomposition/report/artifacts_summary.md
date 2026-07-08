# Artifacts Summary — arXiv:1808.00128 replication

**Dir:** `QC-100/QC-1808.00128-low-rank-stabilizer-decomposition/`
**Verdict:** REPLICATED

## Top-level layout
```
QC-1808.00128-low-rank-stabilizer-decomposition/
├── paper/                       # 1808.00128v2.pdf (upstream)
├── extraction/                  # OCR/mmd extraction outputs
│   └── nougat.mmd               # extraction stub (equations parsed by hand)
├── src/                         # first-principles reimplementations
│   ├── verify_extent.py         # C1–C5, C7-analytic
│   ├── verify_soc_sim.py        # C6 (sum-over-Cliffords, corrected)
│   └── stabilizer_rank_sim.py   # C7 (H-state sparse decomp) + α scan
├── work/venv/                   # python venv (numpy 2.5.0, py 3.14)
├── evidence/                    # numeric outputs
│   ├── verify_extent_results.json
│   ├── exp1_H_decomposition.json
│   ├── verify_scaling.json
│   ├── exp2_soc_corrected.json                              (canonical)
│   ├── exp2_runtime_scaling_SUPERSEDED_buggy_T_coeffs.json  (do NOT cite)
│   └── exp3_stab_rank_table.json                            (C8 target only)
└── report/
    ├── REPORT.md                        # original narrative report
    ├── REPORT.tex                       # LaTeX version with critique section
    ├── open_questions.json              # 5 bare-list open questions
    ├── open_questions_section.tex       # LaTeX version of Q1–Q5
    ├── workflow.md                      # end-to-end procedure
    ├── artifacts_summary.md             # this file
    └── failure_analysis.md              # honest critique
```

## Artifact inventory (the 8-artifact standard)

| # | Artifact | Path | Status |
|---|---|---|---|
| 1 | Paper PDF | `paper/1808.00128v2.pdf` | preserved (upstream) |
| 2 | Paper extraction | `extraction/nougat.mmd` | stub (equations parsed by hand for the small exact-number claims that mattered) |
| 3 | Report (narrative) | `report/REPORT.md` | preserved |
| 4 | Report (LaTeX + critique) | `report/REPORT.tex` | **new (backfill)** |
| 5 | Workflow | `report/workflow.md` | **new (backfill)** |
| 6 | Failure analysis | `report/failure_analysis.md` | **new (backfill)** |
| 7 | Open questions (JSON) | `report/open_questions.json` | **new (backfill)** |
| 8 | Open questions (LaTeX) | `report/open_questions_section.tex` | **new (backfill)** |

Plus supporting src/ (3 scripts) and evidence/ (5 canonical JSONs + 1 audit-trail
superseded file).

## Evidence JSON pointers (what each proves)

| Evidence file | Claims |
|---|---|
| `verify_extent_results.json` | C1 (ξ(CCZ)=16/9 exact), C2 (Prop.2), C3 (Eq.30 ‖c‖₁), C4 (ξ(T) 3 methods), C5 (α), stabilizer state counts 6/1080 |
| `exp1_H_decomposition.json` | C7 (H-state sparse product-stabilizer decomp, exact recon at k=2^m, monotone decay) |
| `verify_scaling.json` | C5 (α scan) |
| `exp2_soc_corrected.json` | C6 (sum-over-Cliffords: exact all-branch match to 1.7e-15; sampled k~100 error 0.01-0.08) |
| `exp3_stab_rank_table.json` | C8 (target values from Ref.[14]; not independently re-derived) |
| `exp2_runtime_scaling_SUPERSEDED_buggy_T_coeffs.json` | audit-trail only — DO NOT CITE (wrong T coefficients) |

## Reproduction (5 minutes on a laptop)
```
cd QC-1808.00128-low-rank-stabilizer-decomposition
python3 -m venv work/venv && work/venv/bin/pip install numpy
work/venv/bin/python src/verify_extent.py
work/venv/bin/python src/verify_soc_sim.py
work/venv/bin/python src/stabilizer_rank_sim.py
```
Outputs go to `evidence/*.json`. Compare to Table 4 in REPORT.md / REPORT.tex.

## What is NOT in this dir
- The paper's flagship 50-qubit QAOA / 40–64-T Hidden-Shift demos (out of scope; see `failure_analysis.md`).
- Independent search for χ(T^m) exact ranks (C8; requires heavy compute per paper).
- Comparison against stabilizer-frames / sparse-stab / stim reference implementations (Q3 in `open_questions.json`).
- GPU-accelerated tableau backend (Q3).
