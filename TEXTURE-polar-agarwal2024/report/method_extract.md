# Method Extract — TEXTURE-polar-agarwal2024 (arXiv:2408.04017)

**Title:** Shift photocurrent vortices from topological polarization textures
**Authors:** A. Agarwal, W. J. Jankowski, D. Bennett, R.-J. Slager (Cambridge / Harvard / Manchester). Texture class: **polar**.

- **Core physics:** Twisted van der Waals ferroelectric bilayers form moiré polar domains (MPDs) — networks of in-plane polar **merons/antimerons** (winding numbers Q = ±1/2). Question: how to detect these textures optically.
- **Headline claim 1:** Topological polarization textures produce **exotic nonlinear optical responses** — specifically the **shift photocurrent forms a vortex-like structure in real space**, mirroring the underlying polar meron/antimeron network.
- **Headline claim 2:** For a frequency window with transitions between topologically trivial bands at the BZ edge, the shift photocurrents are **antiparallel to the in-plane electronic polarization field** — a sought-after optical fingerprint for experimental detection.
- **Method:** Analytic derivation using **non-Abelian Berry connections + quantum-geometric framework** for the shift-current tensor; supported by **tight-binding** model calculations AND **first-principles (DFT)** calculations.
- **Replication target:** Reproduce the real-space shift-photoconductivity vortex pattern from a tight-binding moiré model; show antiparallel-to-P behavior in the predicted frequency range. The analytic + tight-binding parts are the natural replication core.
- **Compute profile:** **Mostly theory/model.** The quantum-geometric analytics and tight-binding shift-current computation are **tractable in-process** (Python + numpy, standard shift-current formula over a k-grid). The DFT confirmation is a bonus that WOULD need a cluster, but the headline result is reproducible at tight-binding level. **Classed: theory/model (tractable now); optional DFT cross-check = cluster.**
