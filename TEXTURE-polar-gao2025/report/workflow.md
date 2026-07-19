# Workflow — TEXTURE-polar-gao2025 (arXiv:2502.14236)

## Goal
Reproduce the topological-charge claims of Gao et al.: Poincaré-sphere (PS)
position of an OAM Laguerre–Gauss drive controls Q of the ferroelectric polar
texture (equator → vortex Q≈0; tilt → antiskyrmion Q=−1; conjugate → skyrmion
Q=+1; intermediate → hybrid).

## Steps executed
1. **Field construction** (`code/gao2025_replication.py::build_field`).
   Mapped the PS superposition |Ψ⟩ = cosθ e^{+iφ}|+1⟩ + sinθ e^{−iφ}|−1⟩ to a
   real-space 3-vector n(r)=(px,py,pz) on a 201×201 grid.
   - In-plane winding χ from the OAM azimuthal phase: χ=−φ (antiskyrmion),
     χ=+φ (skyrmion).
   - Core polar angle β_core = 2θ (in-plane at equator, lifts to pole below).
   - Radial profile Θ(r)=β_core+(π−β_core)(1−e^{−(r/w)²}).
2. **Topological charge** (`topo_charge_berg`, `topo_charge_fd`).
   Berg–Lüscher lattice solid-angle sum (integer-robust) + finite-difference
   Pontryagin integral (crossover check). The two agree on integer topology.
3. **Named-state evaluation** for the 4 claims + full Q(2θ) sweep 90°→45°.
4. **Hybrid construction** (`build_hybrid`, `local_Q`): two opposite-winding
   cores planted at ±sep; global and per-lobe Q computed.
5. **Save** `work/results.json` (all Q values) — done *before* report writing so
   a timeout cannot lose the physics.
6. **Figures** `figs/textures.png`, `figs/Q_vs_2theta.png`, `figs/hybrid.png`.
7. **Report artifacts** written (REPORT.tex/pdf, open_questions, this file,
   artifacts_summary, failure_analysis, META update).

## Key modeling decision
Quantization of Q requires full-sphere coverage: core at one pole, far field at
the opposite pole, in-plane winding wrapping the equator once. The PS latitude
2θ is used as the *core-tilt* knob — this is the physical content of the paper's
"PS knob" claim and is what flips Q from ~0 (equator/hemisphere) to integer.

## Reproduce
```
cd TEXTURE-polar-gao2025
python3 code/gao2025_replication.py     # numpy + matplotlib, CPU, <5 s
```

## Runtime
CPU-only, numpy/matplotlib. Full run (named states + sweep + 3 figures) < 5 s.
