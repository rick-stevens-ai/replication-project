# Method Extract — TEXTURE-polar-gao2025 (arXiv:2502.14236)

**Title:** Poincaré sphere engineering of dynamical ferroelectric topological solitons
**Authors:** L. Gao, Y. Shen, S. Prokhorenko, Y. Nahas, L. Bellaiche (Arkansas / NTU / Tel Aviv). Texture class: **polar**.

- **Core physics:** Ferroelectric topological solitons (polar skyrmions/antiskyrmions) driven by **structured light** carrying tunable orbital angular momentum (OAM). Uses the **Poincaré sphere (PS)** as a geometric parameterization of the light state to control the resulting polar texture.
- **Headline claim 1:** PS engineering enables **controlled creation of dynamic polar antiskyrmions** — a texture rarely found in ferroelectrics.
- **Headline claim 2:** The topological transition is linked to tuning the light beam as a "knob" from OAM (PS pole) to non-OAM (PS equator) modes.
- **Headline claim 3:** Intermediate OAM states yield **new temporally-hybrid skyrmion–antiskyrmion states**.
- **Method:** Atomistic/**second-principles effective-Hamiltonian molecular dynamics** (Bellaiche-group style, e.g. for PbTiO3/BaTiO3 solitons) under a time-dependent OAM light field. Computes the polar dipole field p(r,t) and its topological charge over time.
- **Replication target:** Reproduce antiskyrmion creation vs PS position of the drive; reproduce the hybrid skyrmion-antiskyrmion dynamics for intermediate OAM.
- **Compute profile:** **Model/theory (effective-Hamiltonian MD).** Uses a parameterized effective Hamiltonian, not plane-wave DFT — **tractable in-process or on a GPU/workstation** (the effective-Hamiltonian coefficients are pre-fit). Long time-dependent MD may benefit from a GPU but does not require DFT cluster. **Classed: theory/model (tractable now, possibly GPU-accelerated).**
