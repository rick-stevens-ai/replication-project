# Artifacts summary — QC-200 / quant-ph/0507190

## The 8 required artifacts (per REPLICATION_DIR_STANDARD_2026-07-05.md)

| # | Path | Purpose | Status |
|---|---|---|---|
| 1 | `paper.pdf` | Original arXiv PDF (fetched 2026-07-05) | ✓ 222 KB, 16 pages |
| 2 | `extraction/marker.md` | Marker parse | ✓ pdftotext-derived fallback (marker not installed, no corpus copy) |
| 3 | `extraction/nougat.mmd` | Nougat parse | ✓ pdftotext-derived fallback (nougat not installed) |
| 4 | `report/REPORT.tex` (+ `REPORT.pdf`) | Detailed section-by-section replication report | ✓ full LaTeX; **REPORT.pdf compiled** (~400 KB, 7 pages, TeXLive 20260301) |
| 5 | `report/open_questions.json` | 5 heavy-duty non-superficial open questions | ✓ each has {q, basis, next_steps}; also mirrored as "Open Questions" section in REPORT.tex |
| 6 | `report/workflow.md` | Comprehensive workflow + tool inventory + estimate | ✓ this session's timeline, tool versions, re-run instructions |
| 7 | `report/artifacts_summary.md` | Inventory of all artifacts | ✓ THIS file |
| 8 | `report/failure_analysis.md` | Honest failure analysis / friction / residual gaps | ✓ documents 2 bugs, 2 unimplemented pieces, 1 tolerance gap |

## Full directory inventory

```
QC-quant-ph-0507190-generalized-hidden-shift/
├── paper.pdf                                      # arXiv PDF
├── work/
│   └── paper.txt                                  # pdftotext (~1200 lines)
├── extraction/
│   ├── marker.md                                  # 5.0 KB (pdftotext fallback)
│   └── nougat.mmd                                 # 4.3 KB (pdftotext fallback)
├── code/
│   ├── childs_vandam_pgm.py                       # 17.2 KB, main sim
│   └── make_figures.py                            # 3.5 KB, matplotlib
├── figures/
│   ├── fig1_pgm_success_vs_N.png                  # Eq. (15) sweep
│   ├── fig2_lemma2_fraction.png                   # Pr(1≤η≤4) sweep
│   └── fig3_M_too_small_regime.png                # decay when M<N^(1/k)
├── report/
│   ├── REPORT.tex                                 # 16.8 KB LaTeX report
│   ├── open_questions.json                        # 5 questions with basis+next_steps
│   ├── workflow.md                                # 5.7 KB
│   ├── artifacts_summary.md                       # THIS
│   ├── failure_analysis.md                        # honest critique
│   └── evidence/
│       ├── results.json                           # all 24+4+3 test rows machine-readable
│       └── run_log.txt                            # full stdout of run
└── .venv/                                         # virtualenv (untracked; recreate via pip)
```

## Evidence traces

- **Sweep Test A** (24 rows: k∈{2,3,4} × N∈{4..64/24}): `report/evidence/results.json` → `tests[0].rows`
- **Operational Test B** (4 rows): `results.json` → `tests[1].rows`
- **Qiskit Test C** (3 rows): `results.json` → `tests[2].rows`
- **Full run log** with per-row timings: `report/evidence/run_log.txt`

## Key numerical results (paper-vs-mine)

| Paper claim | My value | Match? |
|---|---|---|
| Eq. (15) closed form | Enumerated exactly for N∈[4,64] | ✓ (tautological) |
| Tr(E_s ρ_s^⊗k) via Σ^(-1/2) construction = Eq. (15) | 1e-16 numerical agreement | ✓ machine precision |
| Lemma 2: Pr(1≤η≤4) is constant when M=⌊N^(1/k)⌋, k≥3 | k=3, N=27, M=3: 0.651; N=32, M=3: 0.558 | ✓ (finite-N trend supports the asymptotic constant lower bound) |
| Theorem 3 success prob ≥ constant | k=3, N=32, M=3: 0.547; k=4, N=24, M=2: 0.479 | ✓ (well above 0) |
| Qiskit end-to-end matches Eq. (15) at 500 shots | 0.006–0.043 |emp−analytic| for 3 cases | ✓ within Monte Carlo σ |

## Not-verified pieces

| Item | Reason not verified |
|---|---|
| Asymptotic poly(log N) time complexity (Theorem 3) | Only reachable at N > 10^6; our sim is at N ≤ 64 |
| Lenstra IP subroutine correctness | We brute-force enumerate matrix-sum solutions instead |
| Optimality of PGM among all POVMs for this ensemble | Would require solving Yuen-Kennedy-Lax SDP; interesting follow-up |
| Generalization to graph isomorphism variant (Sec. 5 of paper) | Left as Open Question Q5 |
