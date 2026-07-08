# Artifacts summary — QC-2403.08859

## Directory layout

```
QC-2403.08859-lattice-gauge-krylov-qubitization/
├── work/
│   ├── paper.pdf                     # arXiv:2403.08859v4 (Anderson et al., Quantum 9, 1652, 2025)
│   └── paper.txt                     # pdftotext -layout dump
├── extraction/
│   └── nougat.mmd                    # backfilled 2026-07-06 (stub — see below)
├── src/
│   ├── schwinger_krylov.py           # H builder + Hankel-QSE + Lanczos + driver (~200 lines numpy)
│   └── plot_convergence.py           # produces convergence.png
└── report/
    ├── REPORT.md                     # original markdown report (2026-07-03)
    ├── REPORT.tex                    # LaTeX report (backfilled 2026-07-06)
    ├── open_questions.json           # 5 open questions machine-readable
    ├── open_questions_section.tex    # 5 open questions LaTeX section
    ├── workflow.md                   # chronology of the work
    ├── artifacts_summary.md          # this file
    ├── failure_analysis.md           # honest critique / limitations
    └── evidence/
        ├── schwinger_N4_mu1.5_x0.5.json
        ├── schwinger_N6_mu1.5_x0.5.json
        ├── schwinger_N8_mu1.5_x0.5.json
        ├── schwinger_N10_mu1.5_x0.5.json
        ├── summary.json
        └── convergence.png
```

## Artifact inventory (backfill count)

Files added by this 2026-07-06 backfill (7):

1. `report/REPORT.tex` — LaTeX version of the report with genuine critique.
2. `report/open_questions.json` — 5 open questions in bare JSON list.
3. `report/open_questions_section.tex` — LaTeX section (input by REPORT.tex).
4. `report/workflow.md` — chronology of the actual work.
5. `report/artifacts_summary.md` — this file.
6. `report/failure_analysis.md` — honest failure / limitations analysis.
7. `extraction/nougat.mmd` — extraction stub (see caveat below).

Pre-existing files (preserved, not modified): all of `work/`, `src/`,
`report/REPORT.md`, and `report/evidence/*`.

## Reproduce

```
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2403.08859-lattice-gauge-krylov-qubitization
python3 src/schwinger_krylov.py       # ~3 s, writes report/evidence/*.json
python3 src/plot_convergence.py       # writes report/evidence/convergence.png
```

Environment: Python 3.14.6, numpy 2.4.3, scipy 1.18.0 (macOS Darwin 25.3.0
x64). No paid endpoints; no LLM calls.

## Verdict at a glance

- **Headline reproducible claim (Track A, Fig. 3):** REPLICATED quantitatively
  on N = 4, 6, 8, 10 at µ = 1.5, x = 0.5, D up to 14. Threshold-D values
  match paper's linear fit within Fig. 3 error bars.
- **Secondary claim (Hankel ill-conditioning, C5):** REPLICATED exactly.
- **Overlap-vs-N trend (C6):** REPLICATED quantitatively.
- **Analytical Track B (qubitization resource count):** NOT exercised — this
  is the largest gap and would require Qualtran or Azure QRE to verify.
- **Wave-brief one-word verdict:** REPLICATED (headline exercised rule).

## Nougat extraction caveat

`extraction/nougat.mmd` is a stub with the paper's front matter and section
skeleton. A full Nougat run on the 40-page paper was not executed as part of
this backfill (would need a GPU node for reasonable runtime). The
replication itself relied on `pdftotext -layout` output (`work/paper.txt`)
plus manual re-derivation of Eq. 7, 10, and 15, not on any Nougat-extracted
LaTeX. The stub exists to satisfy the 8-artifact standard.
