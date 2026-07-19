# Artifacts Summary — TEXTURE-orbital-coh2010

Paper: Coh, Vanderbilt, Malashevich, Souza, "Chern-Simons orbital
magnetoelectric coupling in generic insulators", arXiv:1010.6071.

## Verdict
**PARTIAL** (core-physics SPOT-CHECK) — Coverage 6/10, Agreement 9/10.
4 of 5 identified claims machine-checked; all agree with the paper; the
remaining claims need DFT+Wannier (out of scope).

## Inputs (pre-existing)
- `paper.pdf` — the paper.
- `extraction/marker.md` — full pdftotext extraction (formulas, Eq. 22/27,
  numerical results).
- `report/method_extract.md` — prior method summary.
- `META.json` — scaffold metadata.

## Code (`code/`) — all runnable, no network, no DFT
| file | role |
|------|------|
| `run_replication.py` | production driver → `work/results.json` + 3 figs |
| `theta_z2_robust.py` | **Fu-Kane parity oracle (primary θ)** + Wilson-loop utils |
| `cs_theta.py` | naive direct Eq.(22) — shows gauge-scramble failure |
| `cs_theta_smooth.py` | smooth-gauge Eq.(22) — works trivial, fails TI (Z2 obstruction) |
| `cs_theta_wilson.py` | parity + HWCC experiment |
| `theta_final.py` | per-band A·Ω integral (degeneracy-lifted) |
| `theta_hwcc_flow.py` | HWCC flow / A·Ω estimators |
| `theta_z2pack.py` | SV largest-gap HWCC (noisy diagnostic) |

## Outputs / traces (`work/`)
| file | content |
|------|---------|
| `results.json` | all numeric results: C1 phase diagram, C2 unit conversion, C3 trivial θ, C4 gap-vs-b_z, C1 WCC-flow spectrum |
| `fig_phase_diagram.png` | θ/π vs m0 — TI (θ=π) for 1<|m0|<3, trivial elsewhere |
| `fig_wcc_flow.png` | hybrid Wannier center flow, TI vs trivial (diagnostic) |
| `fig_Tbreaking.png` | bulk gap collapsing to a metal at b_z=1 (paper Fig. 8 text) |

## Reports (`report/`)
| file | content |
|------|---------|
| `REPORT.tex` / `REPORT.pdf` | detailed section-by-section replication report (compiled) |
| `open_questions.json` | 5 new open questions from this replication |
| `workflow.md` | tools, codes, run instructions, work estimate |
| `failure_analysis.md` | what didn't reproduce + root causes |
| `artifacts_summary.md` | this file |
| `method_extract.md` | (pre-existing) method summary |

## Key numbers reproduced
- Phase diagram: θ/π ∈ {0 (trivial), 1 (strong TI)}, boundaries at |m0|=1,3 — exact.
- α_EH(θ=π) = **24.34 ps/m** vs paper **24.3 ps/m** (0.2% agreement).
- α_r(θ=π) = fine-structure constant 7.297e-3 (paper Sec. II.A) — exact.
- Trivial-insulator θ = 0 (paper: Cr2O3 1.3e-3, BiFeO3 0.9e-4, GdAlO3 1.1e-4 — qualitative).
- T-breaking staggered Zeeman closes the gap → **metal at b_z=1.0** (paper Fig. 8).

## Out of scope (DFT-required, not faked)
Material θ values, band gaps, magnetic moments (Cr2O3/BiFeO3/GdAlO3/Bi2Se3),
θ-vs-λ_SO (Fig. 6), direct Wannier Eq.(27) implementation, continuous θ(b_z)
slope.
