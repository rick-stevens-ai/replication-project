# Method Extract — Pendse & Bhattacharyay 2016 (arXiv:1602.05303)
**Title:** Effect of non-local interactions on the vortex solution in Bose-Einstein Condensates
**Texture class:** polar (quantized vortex = topological texture in BEC order parameter)

- **Core physics:** Single vortex line in a BEC described by the **Gross-Pitaevskii (GP)** equation, but with **non-local repulsive s-wave scattering** added on top of the usual contact interaction.
- **Headline claim (replication target):** Besides the conventional vortex whose core width ~ healing length ξ₀, non-locality admits a **second class of "thin" vortex solution** whose core width is set by the microscopic **s-wave scattering length a**, independent of ξ₀. They map the parameter regime where the thin vortex can appear (ξ₀ ~ D limit where the thick-vortex Padé solution breaks down).
- **Key equations:** Local GP equation + leading-order **non-local interaction correction term** (gradient/Taylor expansion of the interaction kernel). Vortex ansatz ψ = f(r)e^{iφ}; radial ODE for f(r); energy comparison of thick (ξ₀) vs thin (a) solutions.
- **DFT-heavy or theory?** **THEORY / MODEL — tractable in-process.** 1D-radial nonlinear ODE (shooting/relaxation) for the GP vortex profile plus energy integrals. No cluster/DFT. Clean numerical replication candidate: solve modified-GP radial equation, reproduce two-length-scale vortex cores and the energy crossover.
