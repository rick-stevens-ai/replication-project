# Method Extract — Romaguera, Doria & Peeters 2010 (arXiv:1001.1715)
**Title:** Vortex patterns in a superconducting-ferromagnetic rod
**Texture class:** polar (superconducting vortex textures under inhomogeneous field)

- **Core physics:** A superconducting **rod** (radius R, thickness D) with a **magnetic dot on top** develops vortices, computed via full **3D Ginzburg-Landau (GL) theory**. The magnet's inhomogeneous stray field controls the vortex morphology.
- **Headline claim (replication target):** Vortex patterns depend qualitatively on rod thickness: **thin rods (disks, D~ξ) → giant-vortex states** (as under a homogeneous field); **thick rods (D≫ξ) → novel patterns where vortices are curved lines in 3D that exit through the lateral surface** (top-to-bottom giant + top-to-side multivortex crossover). Minimal geometric conditions for vortex onset.
- **Key equations:** Time-dependent / free-energy **Ginzburg-Landau equations** for complex order parameter Ψ(r) and vector potential A, with an inhomogeneous applied field from a point/dipole magnet 2ξ above the top surface; solved on a 3D mesh. Coherence length ξ sets scales.
- **DFT-heavy or theory?** **THEORY / NUMERICS — mostly tractable but 3D.** No DFT. Requires a **3D GL solver** (finite-difference/link-variable relaxation) — heavier than a 1D/2D problem but runnable in-process for modest meshes; large/high-res 3D sweeps could want a workstation/cluster. Classify: tractable-now for a reduced reproduction (few geometries), scale up if needed.
