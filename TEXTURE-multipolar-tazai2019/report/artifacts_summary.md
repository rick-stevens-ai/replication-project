# Artifacts Summary — arXiv:1901.06213

**Paper:** Tazai & Kontani, *Multipole fluctuation theory for heavy fermion systems:
Application to multipole orders in CeB6*, arXiv:1901.06213 (2019).

**Verdict: PARTIAL** — Coverage 7/10, Agreement 8/10.

## Files
| Path | Description |
|---|---|
| `paper.pdf` | Source paper (fetched) |
| `extraction/paper.txt` | `pdftotext -layout` dump (644 lines) |
| `extraction/marker.md` | Distilled model params, 16 multipole matrices, U0Q table, targets, scope |
| `code/model.py` | 2D PAM Hamiltonian + 16 Gamma8 multipole operators (self-tested) |
| `code/filling.py` | C1 filling nf/ns |
| `code/rpa.py` | Bare bubble chi0_Q + channel-diagonal RPA (reported U0Q) |
| `code/qscan.py` | C2/C3 q-scan, magnetic vs quadrupole peak ratios |
| `code/stoner.py` | C4 Stoner factors alpha_mag/alpha_el vs u |
| `code/al_scaling.py` | C5 AL/MT xi-scaling + X_AL ∝ xi^{4-d} exponents |
| `code/plots.py` | Figure generation |
| `work/*.json`, `work/qscan_paths.npz` | Numerical outputs |
| `report/fig_bands.png` | Reconstructed band dispersion + Fermi surface |
| `report/fig_qscan.png` | Bare vs RPA susceptibility (magnetic dominance) |
| `report/fig_scaling.png` | AL vs MT scaling near criticality |
| `report/REPORT.tex` / `REPORT.pdf` | Full report (5 pp, compiled) |
| `report/open_questions.json` | Exactly 5 open questions |
| `report/workflow.md` | Method + reproduce commands |
| `report/failure_analysis.md` | What failed / limits / fixes |

## Key quantitative results (all from real runs)
| Claim | Paper | This work | Status |
|---|---|---|---|
| C1 total filling nf+ns | 1.27 (0.58/0.69) | 1.18 (0.99/0.19) | PARTIAL (partition convention) |
| C2/C3 chi^RPA magnetic/quadrupole peak ratio | magnetic dominates | 39.7 (bare 1.03) | REPRODUCED |
| C4 alpha_mag at u=1.08 | 0.9 | 1.02 (0.94 at u=1.0) | REPRODUCED (~13%) |
| C4 alpha_mag > alpha_el | yes | 1.02 > 0.62 | REPRODUCED |
| C5 X_AL ∝ xi^{4-d} (d=1,2,3) | 3,2,1 | 2.96, 1.97, 1.00 | REPRODUCED (<2%) |
| C5 AL/MT dominance for xi>>1 | yes | 0.74->123 (xi 2->64) | REPRODUCED |
| C6 alpha^{Gamma4}_Oxy = 0.94 with full VC | 0.94 | not computed | OUT-OF-SCOPE |

## Scope boundaries
- **In scope (done):** band model, Fermi surface, 16 multipole operators + normalization,
  bare bubble, RPA multipole susceptibilities, Stoner factors, analytic AL/MT scaling law.
- **Out of scope (marked, not faked):** full two-loop AL1/AL2/MT vertex-correction momentum
  integrals with the exact 16x16 Slater-Condon Coulomb tensor (the quantitative chi_Oxy
  enhancement, Fig. 3), field-induced octupole (Fig. 5). No DFT, no experimental data faked.
