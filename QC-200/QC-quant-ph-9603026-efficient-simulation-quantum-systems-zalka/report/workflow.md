# Workflow — Zalka (1996) reproduction

Independent replication of arXiv:quant-ph/9603026 (Christof Zalka, Bern,
"Efficient Simulation of Quantum Systems by Quantum Computers") for the
QC-200 wave.

## Timeline (elapsed wall ~10 min)

1. **T+0**   Read wave brief `~/Dropbox/REPLICATE-PROJECT/scripts/QC_WAVE_BRIEF_2026-07-03.md`.
2. **T+1**   Create target dir; `curl` PDF from
   `https://arxiv.org/pdf/quant-ph/9603026` (113 kB, 8 pages).
3. **T+2**   `pdftotext -layout paper.pdf work/paper.txt`; verify title +
   author from the layout dump. Skim Sections 2–5.
4. **T+3**   Write `report/evidence/trotter_heisenberg.py` — the real
   numerical reproduction. Choose:
   - system: 1D Heisenberg XXX, n=4 qubits, open BC
   - split: $H_{\rm odd}+H_{\rm even}$ (parity of bond index)
   - gold: `scipy.linalg.expm(-i H T)`
   - approximants: 1st-order product, 2nd-order symmetric Strang
   - sweep: $K\in\{10,20,50,100,200\}$
   - error: $\|U_{\rm Trotter}-U_{\rm exact}\|_F$ + state-vector error on
     a fixed random $|\psi\rangle$ (seed 0)
   - fit: `numpy.polyfit(log(dt), log(eps), 1)`
   - unitarity check on all approximants.
5. **T+4**   Run the reproducer — got slopes 1.012, 2.002.
6. **T+5**   Log-log plot (matplotlib, PNG at 140 DPI).
7. **T+6**   Write hand-cleaned `extraction/marker.md` and
   `extraction/nougat.mmd` fallbacks (see failure_analysis.md).
8. **T+7**   Write `report/REPORT.tex`, this workflow, artifacts_summary,
   failure_analysis, open_questions.json.
9. **T+8**   Compile REPORT.tex → REPORT.pdf with `pdflatex` (if available)
   and print `WAVE_RESULT` line.

## Tools & versions

| Tool | Version | Role |
|---|---|---|
| macOS Darwin | 25.3.0 (x64) | host |
| Python | 3.13 (`/usr/local/bin/python3`) | driver |
| NumPy | 2.4.3 | linear algebra |
| SciPy | 1.18.0 | `scipy.linalg.expm` gold-standard matrix exponential |
| Matplotlib | 3.x (backend `Agg`) | log-log plot |
| pdftotext (poppler) | system | quick text extraction of the PDF |
| pdflatex | TeX Live (if present) | REPORT.tex → REPORT.pdf |
| curl | system | arXiv PDF fetch |
| — | — | **No LLM was used for the numerical claim.** |
| — | — | **No paid APIs.** |

## Files produced

```
QC-quant-ph-9603026-efficient-simulation-quantum-systems-zalka/
├── paper.pdf                              # arXiv v2 (113 kB, 8 pages)
├── extraction/
│   ├── marker.md                          # Marker-style extraction (fallback)
│   ├── nougat.mmd                         # Nougat-style extraction (fallback)
│   └── paper_pdftotext.txt                # raw poppler dump
├── work/
│   └── paper.txt                          # `pdftotext -layout` dump
└── report/
    ├── REPORT.tex                         # detailed LaTeX report (this file's twin)
    ├── REPORT.pdf                         # compiled (if pdflatex available)
    ├── workflow.md                        # this file
    ├── artifacts_summary.md               # inventory
    ├── failure_analysis.md                # honest gaps
    ├── open_questions.json                # 5 heavy-duty Q1-Q5
    └── evidence/
        ├── trotter_heisenberg.py          # the reproducer script
        ├── make_plot.py                   # log-log plot generator
        ├── trotter_results.json           # per-K measurements + fits
        ├── trotter_verdict.json           # bool gates + verdict
        ├── trotter_run.log                # stdout of the run
        └── trotter_error_vs_dt.png        # figure in REPORT
```

## Repro one-liner

```
python3 report/evidence/trotter_heisenberg.py
python3 report/evidence/make_plot.py
pdflatex -interaction=nonstopmode -output-directory=report report/REPORT.tex
```

## Estimated work

Roughly one subagent-turn (~10 min of wall time) end-to-end on CherryRd,
of which the actual scientific computation was <1 s (dim=16 matrices).
The rest is document authoring, PDF fetching, and pdftotext extraction.
