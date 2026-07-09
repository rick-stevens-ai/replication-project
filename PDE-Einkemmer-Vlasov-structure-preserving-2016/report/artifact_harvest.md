# Artifact Harvest — PDE-Einkemmer-Vlasov-structure-preserving-2016

All artifacts are from public, open-access sources. No paywall.

## Paper / primary source
| Item | URL | Size | Notes |
|---|---|---|---|
| Oberwolfach Report Vol. 13(1), pp. 869–948 (workshop volume) | https://ems.press/content/serial-article-files/46621 (DOI 10.4171/OWR/2016/18) | 3.6 MB PDF, 80 pages | Contains Einkemmer talk at pp. 899–902 |
| Extracted text of Einkemmer's 4-page talk | (extracted via `pdftotext`) | ~4 KB | See `work/paper/owr-2016-18.txt` lines 1392–1510 |

## Author's production code
| Item | URL | Notes |
|---|---|---|
| SLDG framework (Einkemmer & Moriggl) | https://bitbucket.org/leinkemmer/sldg | git-cloned successfully on uicgpu at `~/work/pde-einkemmer-vlasov-2016/sldg`; 4D/6D semi-Lagrangian DG Vlasov-Poisson with MPI + CUDA; NOT built end-to-end (needs Boost/GSL/PnetCDF submodules and cluster module setup, beyond time budget) |
| Author profile / software page | https://www.einkemmer.net/software.html | Points to SLDG + Ensign (low-rank dynamics, GitHub `leinkemmer/Ensign`) |
| Ensign framework (low-rank Vlasov, related) | https://github.com/leinkemmer/Ensign | Related Vlasov work by same author; not used in this replication |

## Author identity resolution
| Item | URL |
|---|---|
| L. Einkemmer academic home | https://numerical-analysis.uibk.ac.at/lukas.einkemmer/ |
| Personal site | https://www.einkemmer.net/ |
| GitHub user | https://github.com/leinkemmer (NOT `lukaseinkemmer` — that user does not exist) |
| Bitbucket | https://bitbucket.org/leinkemmer/ |

## References cited in Einkemmer's OWR talk (for context)
- Cheng, Knorr 1976, J.Comput.Phys. 22:330 (classic spline SL)
- Crouseilles, Einkemmer, Faou 2015, J.Comput.Phys. 238:224 (Hamiltonian split V-M)
- Crouseilles, Mehrenberger, Vecil 2011, ESAIM Proc. 32:211 (DG-SL for V-P)
- Einkemmer 2016 arXiv:1601.02280 (geometric properties of sLdG)
- Einkemmer, Ostermann 2014 SIAM J.Numer.Anal. 52(2):757 (DG/Strang convergence)
- Einkemmer, Ostermann 2014 SIAM J.Numer.Anal. 52(1):140 (Strang split V-P convergence)
- Qiu, Shu 2011 J.Comput.Phys. 230:8386 (positivity-preserving sLDG)
- Rossmanith, Seal 2011 J.Comput.Phys. 230:6203 (positivity-preserving high-order sLDG)

## Reproduction outputs (in this replication)
| File | What |
|---|---|
| `report/evidence/landau/history_spline.json` | Time series of invariants for spline SL, Landau damping α=0.01, Nx=Nv=128, T=30 |
| `report/evidence/landau/history_upwind.json` | Same, first-order upwind reference |
| `report/evidence/two_stream/history_spline.json` | Spline SL, two-stream α=0.05, T=30 |
| `report/evidence/two_stream/history_upwind.json` | Upwind, two-stream α=0.05, T=30 |
| `report/evidence/landau_tiny/history_spline.json` | Spline, ultra-linear Landau α=0.001, T=15 (checks entropy in linear regime) |
| `report/evidence/combined_summary.json` | Combined numerical drifts (mass, L1, L2, entropy, energy) across all runs |
| `report/evidence/invariants_vs_time.png` | Comparison figure (mass, L2, entropy, energy vs t; spline vs upwind; both problems) |
| `report/evidence/landau_damping.png` | Electric-energy semilog vs analytic Landau damping rate |
| `report/evidence/judge_verdict.json` | LLM-judge (Argo Sonnet 4.6, FREE) verdict + justification |
| `work/vp1d_solvers.py` | From-scratch Python solvers (spline SL, upwind SL, modal Legendre sLdG, diagnostics) |
| `work/run_experiment.py` | Driver |
| `work/make_plots.py` | Plotting script |
| `work/paper/owr-2016-18.pdf` | Original workshop-volume PDF |
