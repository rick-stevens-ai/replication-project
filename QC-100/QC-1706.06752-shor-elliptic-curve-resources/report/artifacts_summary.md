# Artifacts Summary — QC-1706.06752-shor-elliptic-curve-resources

**Paper:** Roetteler, Naehrig, Svore, Lauter (2017) — ECDLP-Shor resource estimates
**Set:** QC-100 &nbsp;|&nbsp; **Verdict:** REPLICATED
**Inventory as of:** 2026-07-06 (post-backfill)

---

## Directory tree (relevant paths)

```
QC-1706.06752-shor-elliptic-curve-resources/
├── paper/
│   └── 1706.06752_roetteler_ecdlp.pdf     # arXiv v3, 866 KB
├── data/
│   └── roetteler_2017_table2.csv           # 7-row ground truth (n, qubits, toffoli, depth, sim_time)
├── code/
│   ├── analytic_reconstruction.py          # pure-Python re-derivation
│   ├── qualtran_symbolic.py                # Qualtran/Litinski-2023 symbolic cross-check
│   └── qualtran_crosscheck.py              # concrete-point attempt (fails on QROM at symbolic n; kept for provenance)
├── work/
│   ├── paper.pdf                           # scratch copy
│   ├── paper.txt                           # full pdftotext (2,239 lines)
│   └── venv/                               # local Python venv for Qualtran
├── extraction/
│   └── nougat.mmd                          # stub for downstream OSTI-style processing (backfill)
└── report/
    ├── REPORT.md                           # original narrative report
    ├── REPORT.tex                          # LaTeX version with honest Critique section (backfill)
    ├── open_questions.json                 # bare-list 5-question JSON (backfill)
    ├── open_questions_section.tex          # LaTeX version, \input by REPORT.tex (backfill)
    ├── workflow.md                         # step-by-step reproduction (backfill)
    ├── artifacts_summary.md                # this file (backfill)
    ├── failure_analysis.md                 # honest critique (backfill)
    └── evidence/
        ├── analytic_reconstruction.json    # 7-row per-n comparison output
        ├── qualtran_symbolic.json          # 7-row Qualtran cross-check + symbolic expression
        └── tool_versions.txt               # pinned versions
```

## Artifact roles

| Artifact | Role | Origin |
|---|---|---|
| `paper/1706.06752_roetteler_ecdlp.pdf` | Primary source | arXiv v3, 2017-10-31 |
| `data/roetteler_2017_table2.csv` | Ground truth (Table 2 numeric) | Manually transcribed from paper |
| `code/analytic_reconstruction.py` | Independent re-derivation of qubit + Toffoli formulas | Original |
| `code/qualtran_symbolic.py` | Cross-tool sanity check (Litinski 2023 windowed variant) | Original |
| `code/qualtran_crosscheck.py` | Failed-but-informative concrete-point attempt | Original |
| `report/evidence/analytic_reconstruction.json` | Numeric evidence for C1, C2, C3 | Script output |
| `report/evidence/qualtran_symbolic.json` | Numeric evidence for C6 + symbolic expression | Script output |
| `report/evidence/tool_versions.txt` | Reproducibility pin | `pip freeze` snapshot |
| `report/REPORT.md` | Narrative report (Markdown) | Original run |
| `report/REPORT.tex` | Narrative report (LaTeX) with Critique section | Backfill 2026-07-06 |
| `report/open_questions.json` | Machine-readable open-questions record | Backfill 2026-07-06 |
| `report/open_questions_section.tex` | LaTeX version, \input by REPORT.tex | Backfill 2026-07-06 |
| `report/workflow.md` | Reproducible step-by-step | Backfill 2026-07-06 |
| `report/failure_analysis.md` | Honest critique of scope + limits | Backfill 2026-07-06 |
| `extraction/nougat.mmd` | Nougat-style extraction stub | Backfill 2026-07-06 |

## Claims-to-artifact matrix

| Claim | Evidence artifact |
|---|---|
| C1: Qubit formula | `analytic_reconstruction.py` + `.json` (exact 7/7) |
| C2: Toffoli closed-form | `analytic_reconstruction.py` + `.json` (max 2.18%) |
| C3: Leading coeff 224 | `analytic_reconstruction.py` (structural derivation in code comments + output) |
| C4: Table 1 primitives are raw | NOT TESTED — LIQUi\|> closed |
| C5: Primitives-vs-fit gap | `analytic_reconstruction.py` `.json` "prims rel. err." column |
| C6: Qualtran cross-check | `qualtran_symbolic.py` + `.json` |

## 8-artifact standard checklist

- [x] `REPORT.md` (original narrative)
- [x] `REPORT.tex` (LaTeX, with Critique section, `\input{open_questions_section.tex}`)
- [x] `open_questions.json` (bare list, 5 items, `{q, basis, next_steps}`)
- [x] `open_questions_section.tex`
- [x] `workflow.md`
- [x] `artifacts_summary.md`
- [x] `failure_analysis.md`
- [x] `extraction/nougat.mmd`

All eight present after backfill.
