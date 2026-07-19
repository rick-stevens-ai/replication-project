# Artifacts Summary — TEXTURE-spin-sasioglu2026

| # | Artifact | Path | Description |
|---|----------|------|-------------|
| 1 | Replication code | `code/sasioglu2026_replication.py` | d-wave altermagnet TB H(k), 4×4 Bloch cross-check, zone folding, θ sweep, cos(2θ) fit |
| 2 | Results JSON | `work/results.json` | numeric checks, θ arrays, per-claim expectation/reproduced/match/note, fit R² |
| 3 | Figure 1 | `figs/fig1_dwave_spinsplit_FS.png` | bulk d-wave spin-split map + spin-split Fermi surfaces |
| 4 | Figure 2 | `figs/fig2_spinsplit_vs_theta.png` | spin splitting vs θ with cos(2θ) fit; robustness across tubes |
| 5 | Report (TeX) | `report/REPORT.tex` | full writeup |
| 6 | Report (PDF) | `report/REPORT.pdf` | compiled report |
| 7 | Open questions | `report/open_questions.json` | 5 {q, basis, next_steps} |
| 8 | Workflow | `report/workflow.md` | step-by-step reproduction |
| + | Failure analysis | `report/failure_analysis.md` | what broke on first run + fixes |
| + | Method extract | `report/method_extract.md` | pre-supplied physics (input) |
| + | META | `META.json` | status + verdict |

## Headline result
- **Bulk d-wave altermagnet:** Δ(k) = -4 t_AM (cos kx - cos ky); net magnetization = 0,
  diagonal nodes exact, antinodal amplitude 2.4. Analytic vs Bloch diff = 0.
- **Nanotube cos(2θ) law:** zone-folded axial spin splitting fits A cos(2θ)+B with
  **R² = 1.000**, A = -0.593, node at **45°**, antinodes at **0/90°**, identical across
  tube indices N = 8, 12, 16.

## Verdict: REPLICATED (tight-binding core). DFT confirmation out of scope.

## Runtime
~1.2 s, CPU-only.
