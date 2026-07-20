# Artifacts summary — arXiv:2502.16657 replication

**Paper:** Fernandes, Birol, Ye, Vanderbilt, *"Loop-current order through the
kagome looking glass"*, arXiv:2502.16657 (2025). Type: focused **perspective**.

**Verdict: REPRODUCED.  Coverage 8/10.  Agreement 9/10.**

## Directory contents (8-artifact standard)
| Artifact | Path | Status |
|---|---|---|
| Paper | `paper.pdf` | fetched |
| Extraction marker | `extraction/marker.md` | done |
| Code (reusable kernel) | `code/kagome_loopcurrent.py` | done, commented |
| Code (driver) | `code/run_replication.py` | done |
| Run outputs | `work/results.json`, `work/*.png`, `work/paper.txt` | done |
| Report (TeX + PDF) | `report/REPORT.tex`, `report/REPORT.pdf` | compiled (4 pp) |
| Open questions | `report/open_questions.json` | 5 entries |
| Workflow | `report/workflow.md` | done |
| Artifacts summary | `report/artifacts_summary.md` | this file |
| Failure analysis | `report/failure_analysis.md` | done |

## Machine-checkable claims and outcomes
| ID | Claim (paper) | Result | Agree? |
|---|---|---|---|
| CL1 | Kagome NN TB: flat band, Dirac at K, M-point saddle vHS with **log-divergent DOS** (Eq. 1) | E(G)={-4,2,2}, E(M)={-2,0,2}, E(K)={-1,-1,2}; flat band +2t (1e-6); Dirac gap 1e-15; DOS peak ~ ln(1/eta), **R^2=0.9999** | YES |
| CL2 | Peierls flux (Eq. 5) breaks TRS via kinetic energy and opens a gap | TRS residual 0 (plain) vs 6.65 (flux); gap 0 -> **1.61 t** | YES |
| CL3 | LC order parameter = **imaginary** part of bond operator (Box 1/2); zero in plain state | Im<c_A^dag c_B>: -0.013 (plain) vs **-0.084** (flux) | YES |
| CL3-net | Table I: 3Q=FM, 2Q-1Q=AFM, 2Q-3Q=ferro-octupolar | dipole/octupole invariants give **all three rows correct** | YES |
| CL4 | Flux/LC order -> **anomalous quantum Hall** state (refs [4,5]) | Chern (+1,0,-1) converged; lower band **C=+1 => sigma_xy=e^2/h** | YES |
| CL5 | Patch model: iCDW favored for g1<0,g2>0,g3>0 (Box 2) | rule reproduced symbolically | YES |

## Key numbers (from `work/results.json`)
- vHS log-divergence fit: peakDOS = 0.0535 * ln(1/eta) + 0.108, R^2 = 0.9999.
- Flux state (phi=pi/4, uniform): gap = 1.606 t, triangle flux +/- 3*pi/4.
- Chern numbers (flux): [+1, 0, -1], sum 0, stable over BZ grids 30-90.
- Loop current |Im| enhancement flux/plain ~ 6.6x.

## What the reusable kernel provides (for sibling loop-current papers)
`code/kagome_loopcurrent.py` — a documented tight-binding + Peierls-flux
mean-field + Kubo/Berry kernel:
- `KagomeModel(t, flux, flux_pattern)` with patterns
  `none | uniform | staggered | (phi_ab,phi_bc,phi_ca)`.
- `.hamiltonian`, `.bands`, `.dos`, `.all_eigvals`, `.gap`,
  `.chern_number` (Fukui-Hatsugai-Suzuki), `.berry`-style link method,
  `.bond_current_and_charge` (Box 1 order parameter),
  `.plaquette_fluxes`.
- module functions `triangle_flux_from_config` (Table I multipoles),
  `patch_leading_channel` (Box 2 channel rule).
- High-symmetry points `Gamma, M, K, M1, M2, M3, B1, B2`.
Designed for reuse by Christensen-Birol-Andersen-Fernandes (PRB 106 144504),
Park-Ye-Balents (PRB 104 035142), Denner-Thomale-Neupert (PRL 127 217601), etc.

## Out of scope (marked, not faked)
- Weak-coupling RG integration of the patch model (only channel logic checked).
- Full anharmonic Landau free-energy minimization.
- Ab initio (DFT / hybrid-functional) LC prediction in real AV3Sb5 / CrSi(Ge)Te3.
- Quantitative experimental magnitudes (uSR fields, Kerr/Hall values).
