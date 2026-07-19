# Method Extract — Zhou et al. 2021 (arXiv:2104.12990)
**Title:** Local Manipulation and Topological Phase Transitions of Polar Skyrmions
**Texture class:** polar (ferroelectric **polar skyrmions** in PbTiO3/SrTiO3 superlattice)

- **Core physics:** **Phase-field simulation** of ferroelectric polar-skyrmion textures in a PTO/STO oxide superlattice, locally controlled by an **electric potential applied through a top electrode**.
- **Headline claims (replication targets):**
  1. Under small electric potential, skyrmions under the electrode are **reversibly erased and recovered**.
  2. A **topologically protected transition from symmetric → asymmetric skyrmion bubbles** at the electrode edge.
  3. High potential drives skyrmion → **labyrinthine domain**; reverts to skyrmion at small potential. Topological charge transition **+1 → 0** occurs *before* full bubble destruction.
  4. Shrinking/bursting of skyrmions → large **reduction in dielectric permittivity**, magnitude set by electrode size.
- **Key equations:** Time-dependent **Ginzburg-Landau (TDGL) / phase-field** evolution of the polarization field P(r,t): ∂P/∂t = −L δF/δP, with free energy F = Landau bulk + gradient (domain-wall) + elastic + electrostatic (depolarization) + electrostrictive terms; electrode boundary condition sets local electric potential. Topological (skyrmion) charge computed from P texture.
- **DFT-heavy or theory?** **THEORY / PHASE-FIELD SIMULATION — tractable but 3D and multi-physics.** No DFT (coefficients are literature/experiment-derived). Requires a 3D coupled electrostatic+elastic phase-field solver — nontrivial to stand up but in-principle in-process for a reduced model; full superlattice reproduction may want a workstation. Classify: moderately heavy, tractable-with-effort.
