# Workflow — TEXTURE-polar-zhou2021 replication

## Paper
Zhou, Wu, Das, Tang, Li, Huang, Tian, Chen, Ramesh, Hong,
"Local Manipulation and Topological Phase Transitions of Polar Skyrmions",
arXiv:2104.12990 (2021). Class: polar texture / phase-field simulation.

## Environment
- Host: CherryRd (macOS 26.5.2)
- Python 3.x, numpy 2.4.3, scipy 1.18.0, matplotlib 3.10.8
- No GPU / no HPC used. Pure CPU, minutes-scale runtime.
- No external endpoints or paid APIs used (free/local only).

## Decision: scope reduction
The paper's full method (3D 320x320x350 coupled electrostatic+elastic+6th-order
Landau phase field, iterative-perturbation elastic solver, superposition
electrostatics over film/substrate/air) is workstation/HPC scale and out of
scope for an independent smoke replication. Chose the **tractable topological
core**: a reduced 2D 3-component TDGL model of the top PTO layer that stabilizes
Neel polar skyrmion bubbles and responds to an electrode field. This preserves
every *topological* claim while dropping absolute-units multiphysics.

## Steps
1. Read `paper.pdf` (pdf tool), `extraction/marker.md`, `report/method_extract.md`.
2. Extracted 5 machine-checkable claims (see REPORT.tex sec. 1).
3. Implemented `code/phasefield.py`:
   - Berg-Luscher lattice topological charge (exact integer).
   - Continuous Pontryagin density for line profiles.
   - TDGL free-energy derivative: Landau 6th-order + gradient + Neel-DMI + uniaxial + electrostatic.
   - Neel skyrmion initializer + lattice builder.
   - Electrode field model (downward Ez under electrode + fringing Ex at edges).
4. `code/exp1_topo_charge.py` -> Claim 1 (Q=+1, ring, two-peak profile).
5. `code/exp2_erase_recover.py` -> Claims 2 & 3 (reversible erase/recover; neighbour protected).
6. `code/exp3_highfield_dielectric.py` -> Claims 4 & 5 (Q+1->0 before destruction; dielectric drop).
7. `code/exp4_recovery_asymmetry.py` -> Claim 4 refinement (small recovers / large locked in).
8. `code/make_figs.py` -> figures A-D in `figs/`.

## Reproduce
```bash
cd ~/Dropbox/REPLICATE-PROJECT/TEXTURE-polar-zhou2021
python3 code/exp1_topo_charge.py
python3 code/exp2_erase_recover.py
python3 code/exp3_highfield_dielectric.py
python3 code/exp4_recovery_asymmetry.py
python3 code/make_figs.py
```
Results land in `work/*.json` and `figs/*.png`. Deterministic (fixed seeds).

## Outputs
- `work/exp1_result.json` … `work/exp4_result.json` — machine-checkable metrics
- `work/*.npy` — polarization fields for figures
- `figs/figA..D_*.png` — visualizations
