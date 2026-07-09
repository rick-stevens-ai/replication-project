# Artifact Harvest

## Primary paper (paywalled — abstract-only access via search snippets and follow-up papers)

- **DOI**: 10.1142/S0219876220410121
- **Publisher**: World Scientific (International Journal of Computational Methods)
- **Publication date**: 2021-04-11 (accepted / published online)
- **Access**: 403 Cloudflare block on WSPC, direct DOI resolver, ResearchGate, and MDPI companion page. No open-access PDF located on arXiv / OSTI / Zenodo.
- **Recovered metadata**:
  - Authors: Zhenquan Li (Senior Lecturer, Charles Sturt University; ORCID 0000-0002-3021-630X), Miao Li.
  - Method: 2D velocity-driven adaptive mesh refinement (VDAMR) applied over a vertex-centred finite-volume Navier–Stokes solve.
  - Base solver: Navier2D (Darren Engwirda, MATLAB / MATLAB Central).
  - Refinement criterion: per-CV divergence residual (mass-conservation error).
  - Benchmarks: Armaly 1983 experimental x_r/S values at low Reynolds numbers, plus Erturk 2008 numerical benchmark values.

## Method-family sibling papers (open-access snippets found; abstract-level content)

- Li & Wood (2016) JCAM, "Accuracy analysis of a 2D adaptive mesh refinement method using lid-driven cavity flow" — used ResearchGate PDF profile page (link: profile/Zhenquan-Li/publication/305291772).
- Li (2024) MDPI Mathematics 12(18):2831 "Accuracy Verification of a 2D Adaptive Mesh Refinement Method by Steady Vortex Centres" — direct DOI lookup (open access) blocked from this network but abstract text confirmed via DuckDuckGo cache: "VDAMR algorithm allows for an arbitrary number of finite mesh refinements".
- Li et al. (2024) further-accuracy verification paper on square-cylinder flow — ResearchGate publication 385943833.

## Benchmark reference data

- Armaly, B. F., Durst, F., Pereira, J. C. F., Schönung, B. (1983). "Experimental and theoretical investigation of backward-facing step flow", J. Fluid Mech. 127:473–496. Classic experimental reattachment-length data set for ER=1.94 (nominally ER=2); used by every 2D BFS numerical study since. **Convention**: Re = u_max × D_h / μ where D_h = 2 h_channel = 2 h_inlet (upstream hydraulic diameter).
- Erturk, E. (2008). "Numerical solutions of 2-D steady incompressible flow over a backward-facing step, Part I: High Reynolds number solutions". Computers & Fluids 37(6):633–655. Numerical benchmark, ER=2, stream-function/vorticity finite-difference. **Convention**: Re = u_max × h / μ where h is step height and u_max is peak inlet velocity.
- Feel++ toolbox documentation reproduces the standard benchmark quantitatively; retrieved from https://docs.feelpp.org/toolboxes/latest/cfd/backwardstep/index.html.

## Code artifacts produced by this replication (all inside `work/`)

- `bfs_solver.py` — stream-function/vorticity solver (v0; converged mass but no recirculation captured — geometry BC bug retained for provenance only, not used in verdict).
- `bfs_projection.py` — Chorin projection MAC-grid unsteady solver (v1; WORKING). Sparse pressure Poisson, first-order upwind convection, explicit Euler in time. Verified to converge to steady-state and reproduce the correct BFS recirculation topology.
- `vdamr.py` — synthetic-field driver of the VDAMR algorithm (uniform-refinement + flag-and-refine variants).
- `vdamr_on_solution.py` — VDAMR divergence-residual analysis of the real projection solutions.

## Data artifacts (all in `report/evidence/`)

- `proj_Re{50,100,150,200}_dx02.json/.npz` — steady-state fields for a Re sweep at dx=0.2.
- `refine_Re100_dx{0.25,0.2,0.15,0.1}.json/.npz` — mesh refinement study at Re=100.
- `vdamr_refine_Re100.json` — VDAMR divergence-flag analysis on the refinement sweep.
- `pilot_*` — early stream-function/vorticity pilot runs (kept for provenance).
