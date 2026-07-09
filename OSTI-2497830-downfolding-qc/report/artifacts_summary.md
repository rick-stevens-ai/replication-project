# Artifacts Summary — OSTI-2497830-downfolding-qc

Paper: Alvertis, Khan, Tubman, *Physical Review Applied* **23**, 044028 (2025) — "Compressing Hamiltonians with ab initio downfolding for simulating strongly-correlated materials on quantum computers." OSTI 2497830.

Verdict: **PARTIAL REPLICATION.**

## Directory layout

```
OSTI-2497830-downfolding-qc/
├── report/
│   ├── REPORT.md                     ← primary narrative report (2026-07-02, Ollie)
│   ├── REPORT.tex                    ← LaTeX render, inputs open_questions_section (2026-07-06 backfill)
│   ├── open_questions.json           ← 5 open questions, bare JSON list (backfill)
│   ├── open_questions_section.tex    ← LaTeX version of the 5 questions (backfill)
│   ├── workflow.md                   ← chronology (backfill)
│   ├── artifacts_summary.md          ← THIS FILE (backfill)
│   ├── failure_analysis.md           ← honest critique (backfill)
│   ├── brief.md                      ← original task brief (2026-07-02)
│   ├── attempt_log.md                ← blow-by-blow execution log (2026-07-02)
│   ├── artifact_harvest.md           ← source-material catalog (2026-07-02)
│   └── evidence/
│       ├── ca2cuo3_ed_results.json          ← ground-state energy, spin correlations
│       ├── srvo3_ed_results.json            ← 2×2 sanity-check ED results
│       └── table_II_cross_check.json        ← 0.999^290 = 0.7476 arithmetic check
├── extraction/
│   └── nougat.mmd                    ← placeholder stub (backfill)
└── work/
    ├── osti_2497830.pdf              ← paper PDF, 2.17 MB, 45 pp (fetched via uicgpu curl)
    ├── osti_2497830.txt              ← pdftotext -layout extraction, 997 lines
    ├── ca2cuo3_ed.py                 ← 8.2 KB, from-scratch SciPy sparse ED
    ├── ca2cuo3_ed_results.json       ← ED output (duplicate of report/evidence/)
    ├── srvo3_charge_order.py         ← 7.0 KB, 2×2 ED for sanity check
    └── srvo3_ed_results.json         ← SrVO3 output (duplicate)
```

## Reporting artifacts (the 8-artifact standard)

| # | Artifact | Purpose | Author | Timestamp |
|---|---|---|---|---|
| 1 | `report/REPORT.md` | Primary narrative (Markdown) | Ollie | 2026-07-02 |
| 2 | `report/REPORT.tex` | LaTeX render for typeset output | Kukla backfill | 2026-07-06 |
| 3 | `report/open_questions.json` | Machine-readable 5 open questions | Kukla backfill | 2026-07-06 |
| 4 | `report/open_questions_section.tex` | LaTeX rendering of #3 | Kukla backfill | 2026-07-06 |
| 5 | `report/workflow.md` | Chronology of the replication | Kukla backfill | 2026-07-06 |
| 6 | `report/artifacts_summary.md` | THIS FILE | Kukla backfill | 2026-07-06 |
| 7 | `report/failure_analysis.md` | Honest critique of what was NOT exercised | Kukla backfill | 2026-07-06 |
| 8 | `extraction/nougat.mmd` | Placeholder for a real Nougat parse | Kukla backfill | 2026-07-06 |

Plus the 2026-07-02 supporting artifacts (`brief.md`, `attempt_log.md`, `artifact_harvest.md`, `evidence/*.json`, `work/*.py`, `work/osti_2497830.pdf`, `work/osti_2497830.txt`) which remain untouched.

## Key numbers (independently reproduced)

| Quantity | Paper | This work | Provenance |
|---|---:|---:|---|
| Ca$_2$CuO$_3$ downfolded $E_0$ (eV) | 6.005 (DMRG) | 6.005055 (ED) | `evidence/ca2cuo3_ed_results.json`, code `work/ca2cuo3_ed.py` |
| Ca$_2$CuO$_3$ AFM sign alternation | perfect (Fig 3b) | perfect | same |
| Table II circuit fidelity ($0.999^{290}$) | 74.8% | 74.76% | `evidence/table_II_cross_check.json` |

## Compute footprint

- ED wall time (Ca$_2$CuO$_3$, 63504-dim): 0.84 s
- SrVO$_3$ 2×2 ED (36-dim): sub-second
- LLM-judge call: single Argo GPT-5.2 completion (~2 kB in, ~200 B out)
- Total wall time end-to-end (Ollie 2026-07-02): ~15 min human + ~seconds compute.
- Backfill compute (Kukla 2026-07-06): zero simulation, LaTeX + JSON authoring only.

## Provenance guarantees

- `work/osti_2497830.pdf`: canonical OSTI copy fetched over TLS via `curl -sSL` on `uicgpu` on 2026-07-02.
- `work/osti_2497830.txt`: pdftotext output; every Appendix C matrix was checked against the two-column PDF by eye.
- All ED code (`work/*.py`) is from-scratch: no external Hubbard library, no import from any Alvertis / Khan / Tubman codebase. Ground state was obtained by a fully independent path.
- LaTeX + open-questions authored 2026-07-06 without any additional simulation.
