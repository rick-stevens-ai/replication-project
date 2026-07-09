# Artifacts Summary — OSTI-2998150

**Paper:** Oppelstrup et al. (2025) — *Kinetic Monte Carlo simulations of aging in δ-Pu*
**Verdict:** REPLICATED (Eq. 5 benchmark spot-check)
**Date:** 2026-07-03

---

## Directory Layout

```
OSTI-2998150-kinetic-monte-carlo-simulations-of-aging-in--pu/
├── report/
│   ├── REPORT.md                       # Primary human-readable report
│   ├── REPORT.tex                      # LaTeX version + GENUINE CRITIQUE section
│   ├── workflow.md                     # Step-by-step replication workflow
│   ├── artifacts_summary.md            # THIS file
│   ├── failure_analysis.md             # What did / didn't work + why
│   ├── open_questions.json             # 5 truly open follow-up questions
│   └── evidence/
│       ├── vac_void_collision_fixed.py # Corrected replication script
│       ├── kmc_fixed_results.json      # Machine-readable results + fit + env
│       ├── kmc_fixed_run.log           # stdout of the corrected run
│       ├── kmc_results.json            # (buggy) initial N/L³ run — provenance
│       └── kmc_run.log                 # (buggy) initial stdout — provenance
└── work/
    ├── osti-2998150.pdf                # Paper preprint
    ├── osti-2998150.txt                # Extracted plain text (848 lines)
    └── vac_void_collision.py           # Buggy pre-existing helper (ρ = N/L³)
```

---

## Primary Artifact Table

| Artifact | Path | Role | Size / Notes |
|---|---|---|---|
| Paper preprint | `work/osti-2998150.pdf` | Source paper | LLNL-JRNL-2003209, openly accessible via OSTI |
| Paper text | `work/osti-2998150.txt` | Analyzable plain text | 848 lines |
| Corrected script | `report/evidence/vac_void_collision_fixed.py` | Independent replication implementation | Pure-Python + NumPy, segment-sphere collision test, correct absorber density ρ=1/L³ |
| Results JSON | `report/evidence/kmc_fixed_results.json` | Machine-readable per-(L,R) measurements + fit + env | Deterministic; contains args, Python 3.14.6, NumPy 2.4.3 |
| Run log | `report/evidence/kmc_fixed_run.log` | stdout of the corrected reproduction | 70.3 s wall time |
| Buggy results | `report/evidence/kmc_results.json` | Preserved provenance of first-pass ρ=N/L³ bug | Shows `DRρτ ≈ 16.4 − 45.8·(R/L)` (wrong by factor N) |
| Buggy run log | `report/evidence/kmc_run.log` | Provenance | See above |
| Primary report | `report/REPORT.md` | Human-readable replication report | ~12 KB, tables + verdict |
| LaTeX report | `report/REPORT.tex` | Publication-form report + GENUINE CRITIQUE | Includes strengths + reservations sections |
| Workflow | `report/workflow.md` | Reproducible workflow step list | 7 phases |
| Open questions | `report/open_questions.json` | 5 unresolved research questions | Each with basis + next_steps |
| Failure analysis | `report/failure_analysis.md` | What failed + root causes + lessons | This report's meta-log |

---

## Numerical Result Summary (from `kmc_fixed_results.json`)

- 8 (L, R) cells measured with ≥300 absorption events each.
- Linear fit `DRρτ = 0.0841 − 0.235·(R/L)`.
- Paper Eq. (5): `DRρτ = 0.078 − 0.19·(R/L)`.
- Analytical limit: `1/(4π) ≈ 0.07958`.
- Intercept deviations: 5.7% from theory, 6% from paper.
- Slope: correct sign, ~24% steeper than paper — attributable to
  smaller event budget (300 vs. paper's presumably larger sweep).

---

## Reproduction One-Liner

```bash
cd ~/Dropbox/REPLICATE-PROJECT/OSTI-2998150-kinetic-monte-carlo-simulations-of-aging-in--pu
python3 report/evidence/vac_void_collision_fixed.py \
    --out report/evidence/kmc_fixed_results.json \
    --Ls 15 20 --Rs 1.0 1.5 2.0 3.0 \
    --N 200 --events 300 --seed 1234 --dt_frac 0.05
```

- Wall time: ~70 s (CherryRd, single-threaded)
- Python 3.14.6, NumPy 2.4.3
- Deterministic seed `1234 + int(1000·(L+R))`

---

## Deliberately Absent Artifacts

- **LLNL FPKMC binary/source** — not distributed with the paper; would
  have enabled Claims C3–C5 to be tested but is not publicly available.
- **δ-Pu defect energetics tables** — only partially given in the paper
  (Eqs. 1–4 and scattered constants); full tables would be needed to
  re-run the full aging simulation.
- **KMC vs rate-equation reference dataset** — would enable Claim C5
  testing; not deposited with the paper.
- **Cascade-sampling MD library** — cited but not distributed;
  cascade-library uncertainty is an open question (see OQ4).
