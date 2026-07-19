# Method Extract — TEXTURE-polar-kesharpu2023 (arXiv:2305.13423)

**Title:** Factors affecting the topological Hall effect in strongly correlated layered magnets: spin of the magnetic atoms, polar and azimuthal angle subtended by the spin texture
**Author:** K. K. Kesharpu (JINR Dubna). Texture class: **polar** (named per directory; physically a spin-texture / THE paper).

- **Core physics:** 2D magnetic material in the strong-correlation regime with a **spin texture** where both azimuthal and polar angles vary. Electrons in the strong-coupling (adiabatic) limit follow local magnetization and acquire a Berry phase → topological Hall effect (THE).
- **Method:** Hamiltonian solved via the **su(2) path-integral method** on a bipartite honeycomb lattice; Chern number computed as a function of atomic spin S, azimuthal modulation vector q1, polar modulation vector q2.
- **Headline claim 1:** For S ≤ 3, the **Chern number depends strongly on q2 (polar angle modulation) and S**.
- **Headline claim 2:** Experimentally testable — increasing the spin modulation vector should **flip the sign of the topological Hall conductivity** (+σ^THE_xy → −σ^THE_xy) at fixed S.
- **Headline claim 3:** Proposes several vdW-magnet heterostructures for experimental realization.
- **Replication target:** Reproduce Chern-number / σ^THE phase diagram vs (S, q1, q2) on the honeycomb lattice; reproduce the sign-change of THE with modulation vector.
- **Compute profile:** **Pure theory/model.** Analytic su(2) path integral + tight-binding Chern-number evaluation over a k-grid (TKNN / Berry-curvature integration). Fully **tractable in-process** (numpy/scipy, small Hamiltonians). No DFT, no cluster. **Classed: theory/model (tractable now).**
