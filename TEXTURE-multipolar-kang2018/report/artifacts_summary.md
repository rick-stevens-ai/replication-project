# Artifacts Summary — Kang, Shiozaki, Cho (2018/2019)

**Paper:** Many-Body Order Parameters for Multipoles in Solids
(arXiv:1812.06999v4; Phys. Rev. B 100, 245134).

## Files
| Path | Role |
|---|---|
| `paper.pdf` | Source paper (arXiv v4). |
| `extraction/marker.md` | Extracted claims, equations, model, results. |
| `code/bbh_multipole.py` | BBH model + many-body order parameter (det identity). |
| `code/run_all.py` | Runs claims C1–C5 -> `work/results.json`. |
| `code/make_figures.py` | Plots -> `work/replication_figures.png`. |
| `work/results.json` | Numerical outputs for all claims. |
| `work/replication_figures.png` | Transition + Thouless-pump figures. |
| `report/REPORT.tex` / `.pdf` | Write-up. |
| `report/open_questions.json` | 5 open questions. |
| `report/workflow.md` | How it was run. |
| `report/failure_analysis.md` | What broke and why. |

## Machine-checkable claims and outcomes

| ID | Claim (from paper) | Test | Result | Verdict |
|---|---|---|---|---|
| C1 | Trivial quadrupole insulator (γ>λ, δ=0): Q_xy = 0 mod 1 | referenced Q_xy, L=6–12, γ=1.5,λ=1 | Q_xy = 0.0000 (all L) | **PASS** |
| C2 | Topological quadrupole insulator (γ<λ, δ=0): Q_xy = 1/2 mod 1 | referenced Q_xy, L=6–12, γ=0.5,λ=1 | Q_xy = 0.5000 (all L) | **PASS** |
| C3 | Sharp transition at Wannier-gap closing \|γ/λ\|=1 (Fig 1c cut γ_x=0.5) | sweep γ_y 0.2→1.8 | \|Q\|=0.5 for γ_y<1, 0 for γ_y>1; jump exactly at γ_y=1 | **PASS** |
| C4 | Total polarization P_x=P_y=0 required for Q_xy well-defined (mirror/C2) | dipole Eq. 1, both phases | P_x=P_y=0.0000 | **PASS** |
| C5 | Isotropic Thouless pump: Q_xy quantized (0 / 1/2) at δ=0 crossings, continuous otherwise | pump Eq. 9, θ∈[0,2π] | Q=0.5 at θ=π/2 (topo, δ=0); Q=0 at θ=3π/2 (trivial, δ=0); continuous in between | **PASS** |

## Quantitative comparison

| Quantity | Paper | This work | Match |
|---|---|---|---|
| Q_xy, trivial phase | 0 | 0.0000 | exact |
| Q_xy, topological phase | 1/2 | 0.5000 | exact |
| Phase-boundary location | \|γ/λ\| = 1 | γ_y = 1.00 (with γ_x=0.5,λ=1) | exact |
| \|⟨Û₂⟩\| at boundary | → 0 | dips to ~1e-4 near γ_y=1 | qualitative ✓ |
| Pump quantized points (δ=0) | 0 and 1/2 | 0.0000 and 0.5000 | exact |
| Dipole in quadrupole phase | 0 | 0.0000 | exact |

## Scope
- **In scope & reproduced:** non-interacting BBH quadrupole insulator; dipole &
  quadrupole many-body order parameters; phase diagram; Thouless pumping.
- **Out of scope (marked in open_questions):** interacting/bosonic ground
  states; anomalous quadrupole insulator (Fig 1d); partial-region operators
  V(l) (Fig 3); octupole; nested-Wilson-loop cross-check.
