# Artifacts Summary: MTW 2002 Darcy-Stokes Replication

Directory: `~/Dropbox/REPLICATE-PROJECT/PDE-Mardal-Tai-Winther-DarcyStokes-2002/`
Verdict: **REPLICATED** (2026-07-04)

## Top-level layout

```
PDE-Mardal-Tai-Winther-DarcyStokes-2002/
├── work/                       ← source code, cached paper, temp outputs
│   ├── paper_MTW2002.pdf       ← Wayback Machine 2024-05-03, SHA1 c9eee75…, 270 KB, 28 pp
│   ├── paper.txt               ← pdftotext -layout dump, 1564 lines
│   ├── darcy_stokes_standard.py← scikit-fem sweep for P2-P0, Mini, CR (C2)
│   ├── mtw_element.py          ← local V(T) construction (Lemma 4.1)
│   ├── mtw_solver.py           ← global assembly, BC, solve, error norms (C1, C3, C4)
│   └── (assorted scratch/debug .txt)
├── extraction/                 ← (empty apart from placeholder marker)
└── report/                     ← THIS directory
    ├── REPORT.md               ← canonical narrative (this run's source of truth)
    ├── REPORT.tex              ← LaTeX version + dedicated critique
    ├── open_questions.json     ← 5 genuinely-open follow-ups
    ├── workflow.md             ← stage-by-stage recipe
    ├── artifacts_summary.md    ← THIS file
    ├── failure_analysis.md     ← dead-end post-mortem
    └── evidence/               ← logs + machine-readable results
        ├── mtw_selftest.log
        ├── run_mtw.log
        ├── run_standard.log
        ├── mtw_convergence.json
        └── standard_elements_results.json
```

## Code artifacts

| File | Purpose | Lines (approx) | Depends on |
|------|---------|----------------|------------|
| `work/mtw_element.py` | Local V(T) basis construction: 20-monomial P₃² parameterization, 11-row constraint matrix (5 div-in-P₀ + 6 (v·n)-in-P₁), 9-row DOF matrix (5-pt Gauss–Legendre), solve M·Q = I on ker C, self-tests. | 250+ | NumPy, SciPy, SymPy |
| `work/mtw_solver.py` | Global mesh, per-edge orientation, per-triangle sign transform R_T (both s_t = ±1 cases), 12-point Dunavant assembly, boundary conditions, pressure pin, error norms, ε×h sweep, JSON output. | 300+ | mtw_element.py, NumPy, SciPy |
| `work/darcy_stokes_standard.py` | scikit-fem baseline for P2-P0, Mini, CR: mesh construction to match paper convention, symbolic manufactured solution, assembly, sweep, JSON output. | 200+ | scikit-fem, SymPy |

**Total custom LOC:** ~500+ for the from-scratch MTW implementation
(mtw_element.py + mtw_solver.py). Standard-elements sweep is
~200 additional LOC, mostly bookkeeping around scikit-fem calls.

**Third-party code:** NumPy 2.4.3, SciPy 1.18.0, SymPy 1.14.0,
scikit-fem 12.0.1. No FEniCS, no Firedrake, no compiled C.

## Evidence artifacts

| File | Content |
|------|---------|
| `report/evidence/mtw_selftest.log` | DOF-of-basis identity check (‖M @ Q − I‖ = 2.9e-14), per-basis-function div-constancy check (max nonconstant residual < 1e-12). Verifies C1. |
| `report/evidence/run_mtw.log` | Full MTW solver stdout across the 5×4 ε×h sweep: per-solve DOF count, wall-clock, ‖u−u_h‖_0, ‖p−p_h‖_0, energy, ‖div u_h‖_0. |
| `report/evidence/mtw_convergence.json` | Machine-readable ε×h×metric table for the MTW sweep. Consumed by rate-fitting cell in REPORT.md §4.1. |
| `report/evidence/run_standard.log` | scikit-fem sweep stdout for P2-P0, Mini, CR. |
| `report/evidence/standard_elements_results.json` | Machine-readable rates for the standard-elements baseline. |

## Cached inputs

| File | Provenance | Integrity |
|------|-----------|-----------|
| `work/paper_MTW2002.pdf` | Internet Archive Wayback Machine snapshot 2024-05-03 of dr.ntu.edu.sg Green OA copy | SHA1 `c9eee75…`, 270 KB, PDF v1.4, 28 pages |

## Reports

| File | Audience | Format |
|------|----------|--------|
| `report/REPORT.md` | Human-first, canonical | Markdown with rate-comparison tables |
| `report/REPORT.tex` | Publication-ready, dedicated critique section | LaTeX |
| `report/workflow.md` | Reproducer / auditor | Markdown, stage-by-stage |
| `report/open_questions.json` | Follow-up planning | JSON, 5 questions with basis + next_steps |
| `report/failure_analysis.md` | Post-mortem, dead ends | Markdown |
| `report/artifacts_summary.md` | This index | Markdown |

## Quantitative match summary

- **MTW element (Table 5.1):** 15 tabulated rates reproduced within
  ±0.07; mean |Δ| = 0.024.
- **Divergence error (C4):** max ‖div u_h‖_0 = 6.4e-11 across all 20
  solves (machine zero for a div-free exact solution).
- **Standard elements (Tables 3.1, 3.3, 3.5, 3.6):** all reported
  rates reproduced within ±0.20 (measurement noise from different
  linear-solver stack).

## To reproduce end-to-end

```bash
cd work/
python3 darcy_stokes_standard.py all    # ~2 min
python3 mtw_solver.py                   # ~90 s
```

All outputs (logs + JSONs) are regenerated into `report/evidence/`.
