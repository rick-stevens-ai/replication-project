# Artifacts Summary — lucid-bnct-radioresistant-hcc

## Directory layout

```
lucid-bnct-radioresistant-hcc/
├── REPORT.md                        # top-level authoritative narrative report (existing)
├── README.md                        # quick orientation (existing)
├── PROGRESS.md                      # run timeline (existing)
├── code/
│   └── replicate.py                 # LQ-fit + RBE recompute driver (existing)
├── results/
│   ├── fit_parameters.csv           # per-curve α, β, D10 (existing)
│   ├── rbe_table.csv                # paper vs recomputed RBE (existing)
│   └── table1_check.csv             # dose × dose-rate × time consistency (existing)
├── figures/
│   ├── clonogenic_gamma.png         # Fig 1C overlay with LQ fits (existing)
│   └── clonogenic_bnct.png          # Fig 3B overlay with LQ fits (existing)
├── extraction/
│   └── nougat.mmd                   # extraction stub (added 2026-07-06 backfill)
└── report/
    ├── REPORT.tex                   # LaTeX form of REPORT.md (added 2026-07-06)
    ├── open_questions.json          # 5 open questions, machine-readable (added 2026-07-06)
    ├── open_questions_section.tex   # LaTeX form for report inclusion (added 2026-07-06)
    ├── workflow.md                  # pipeline provenance (added 2026-07-06)
    ├── artifacts_summary.md         # this file (added 2026-07-06)
    └── failure_analysis.md          # honest critique (added 2026-07-06)
```

## Key results (headline)

| Metric | Paper | Recomputed | Note |
|---|---:|---:|---|
| D10(γ, HepG2) | 3.496 Gy | 3.368 Gy | −3.65% (LQ refit on text-quoted SFs) |
| D10(γ, HepG2-R) | 5.749 Gy | 5.548 Gy | −3.49% (LQ refit) |
| D10(BNCT, HepG2) | 0.9513 Gy | 1.127 Gy | +18.5% (digitized from Fig 3B) |
| D10(BNCT, HepG2-R) | 0.9627 Gy | 1.349 Gy | +40.1% (digitized from Fig 3B) |
| RBE(HepG2) | 3.675 | 3.67497 | ✅ exact arithmetic |
| RBE(HepG2-R) | 5.972 | 5.97175 | ✅ exact arithmetic |

Headline preserved: RBE(HepG2-R) > RBE(HepG2), i.e. BNCT overcomes γ-ray
radioresistance more effectively on the resistant line than the parental line.

## Coverage matrix

- **Replicable, replicated:** Table 1 dose-rate consistency; Table 4 RBE
  arithmetic; γ-ray LQ fits from text-quoted SFs.
- **Replicable-in-principle, digitization-limited:** BNCT LQ fits (Fig 3B).
- **Not replicable from PDF:** Fig 4A–E γH2AX foci + Westerns; Fig 5A–C
  KU70/KU80/RAD51; Fig 6 cell-cycle; Fig 7 pCHK2/pCDK1; Fig 8 caspase-3 +
  BCL2/PUMA/BAX; ¹⁰B uptake time-course; neutron-beam Monte Carlo.

## Verdict cross-check
- **Verdict:** PARTIAL
- **Justification:** roughly half the paper's claims are numerically checkable
  from the PDF; those that are checkable agree well (~8/10). The mechanism
  half + the beam physics are not independently verified.
- **Headline exercised:** YES on the RBE-amplification arithmetic; the
  qualitative HepG2-R-more-sensitive-to-BNCT-than-to-γ-ray claim is
  quantitatively supported.
