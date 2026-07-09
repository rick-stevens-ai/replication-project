# Artifacts Summary — quant-ph/0206003 Replication

Target dir:
`~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0206003-how-powerful-adiabatic-quantum-computation/`

## The 8 mandatory artifacts (per Rick 2026-07-05 completion bar)

| # | Artifact | Path | Size | Status |
|---|----------|------|------|--------|
| 1 | Original PDF | `paper.pdf` | 155,763 B | ✅ downloaded from arXiv |
| 2 | Marker parse | `extraction/marker.md` | 5,981 B | ✅ surrogate (see failure_analysis.md) |
| 3 | Nougat parse | `extraction/nougat.mmd` | 5,151 B | ✅ surrogate (see failure_analysis.md) |
| 4 | Detailed report | `report/REPORT.tex` (+ `REPORT.pdf`, 5 pages, 247,753 B) | 13,370 B src | ✅ compiles cleanly |
| 5 | Open questions | `report/open_questions.json` (+ `## Open Questions` in REPORT.tex) | 3,659 B | ✅ 5 heavy-duty questions |
| 6 | Workflow doc | `report/workflow.md` | 3,745 B | ✅ tools/versions/effort |
| 7 | Artifacts inventory | `report/artifacts_summary.md` | this file | ✅ |
| 8 | Failure analysis | `report/failure_analysis.md` | see it | ✅ |

## Evidence (report/evidence/)

| File | Size | Purpose |
|------|------|---------|
| `adiabatic_grover.py` | 7,566 B | Full replication code (numpy + scipy exact diagonalization + Schrödinger integrator). |
| `results.json` | ~5 KB | Structured raw numbers: C1 gap-formula check, C2 min-gap scan, C2 fit, C3 convergence, C3b T-vs-N scaling. |
| `gap_curve_n3.npz` | ~100 KB | Numeric gap curve g(s) for n=3 (4001-point s-grid) + paper Eq.(1) values for direct point-wise comparison. |

## Intermediates (work/)

| File | Size | Purpose |
|------|------|---------|
| `paper.txt` | ~30 KB | `pdftotext -layout paper.pdf` output. |

## Traces / provenance

- **Paper source:** `https://arxiv.org/pdf/quant-ph/0206003`, fetched 2026-07-05 at ~12:59 CDT via `curl`.
- **Environment:** cherryrd (Darwin 25.3, x64), Python 3, numpy 2.4.3, scipy 1.18.0.
- **Code hash:** `report/evidence/adiabatic_grover.py` byte-identical to what was executed to produce `results.json` (single run, no post-hoc edits).
- **Reproducer:** `cd <this dir> && python3 report/evidence/adiabatic_grover.py` — deterministic (no RNG), 3.71 s.
- **Compile:** `cd report && pdflatex REPORT.tex` → REPORT.pdf (5 pages).

## Key numerical results, tl;dr

| Claim | Paper value | Our value | Match? |
|-------|-------------|-----------|--------|
| Δ_min at n=3 (Eq. 1 at s=1/2)                 | 1/√8 = 0.353553    | 0.353553390593 | YES (machine ε) |
| Δ_min at n=4                                   | 1/√16 = 0.25       | 0.250000000000 | YES (machine ε) |
| Slope of log Δ_min vs log N                    | −0.5               | −0.500000       | YES (exact)     |
| P_success → 1 as c grows (n=3, c=50)          | → 1                | 1.000000        | YES             |
| Constant-schedule T for P≥0.9, scaling with N | linear (Ω(N))      | 16, 32, 64 for N=4,8,16 → 4N linear | YES |
| Adaptive-schedule integral T (asymptotic)      | O(√N) via arctan    | verified analytically at n=10 | YES |

## Verdict

**REPLICATED.** The directly-testable numerical core of Section 5
(spectral gap formula, N^{-1/2} scaling, adiabatic convergence, and the
Ω(N) constant-schedule bound) reproduces to machine precision on real
exact-diagonalization + Schrödinger simulation.
