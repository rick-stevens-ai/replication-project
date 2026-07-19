# Method Extract — TEXTURE-orbital-gmitra2013 (arXiv:1303.2510)

**Title:** Magnetic control of spin-orbit fields: a first-principles study of Fe/GaAs junctions
**Authors:** M. Gmitra, A. Matos-Abiague, C. Draxl, J. Fabian (Regensburg / Humboldt). Texture class: **orbital**.

- **Core physics:** Spin-orbit coupling at the inversion-asymmetric **Fe/GaAs (001) interface** acts as a momentum-dependent spin-orbit field (SOF). Combines Dresselhaus (BIA) and Bychkov-Rashba (SIA) contributions.
- **Method:** **First-principles DFT** on thin Fe/GaAs slabs (plane-wave / FLAPW-class electronic structure). A symmetry-based method extracts the SOF magnitude+direction for a generic Bloch state directly from the ab-initio band structure (not just fitting near Γ).
- **Headline claim 1:** SOFs depend not only on the interface electric field but **surprisingly strongly on the Fe magnetization orientation** — enabling *magnetic control* of the spin-orbit field.
- **Headline claim 2:** The SOF k-space patterns are **highly anisotropic** and change qualitatively with band/energy (consistent with bias-induced TAMR sign inversion); anisotropy axes can be flipped by rotating magnetization.
- **Replication target:** Reproduce the k-resolved SOF texture maps for Fe/GaAs and their dependence on magnetization direction.
- **Compute profile:** **DFT-heavy.** Requires full relativistic (SOC) DFT on interface slabs with fine k-meshes — plane-wave code (VASP/QE/WIEN2k-class). **Needs cluster dispatch.** In-process replication not feasible; a tight-binding toy of the symmetry analysis is possible but would not reproduce the actual material numbers. **Classed: DFT-heavy (need cluster).**
