# Method Extract — Hayashi, Kato, Frigeri, Wakabayashi, Sigrist 2005 (arXiv:cond-mat/0510548)
**Title:** Basic properties of a vortex in a noncentrosymmetric superconductor
**Texture class:** polar (SC vortex core + radially-textured magnetic-moment density)

- **Core physics:** Microscopic (quasiclassical) study of a **single vortex core in a noncentrosymmetric superconductor** (CePt₃Si-type, no mirror symmetry about xy plane). Mixed **singlet–triplet (s+p-wave) Cooper pairing** enforced by Rashba spin-orbit coupling that splits the Fermi surface into two sheets (I, II).
- **Headline claim (replication target):** Spatial profiles around the vortex — **pair potential, local density of states (LDOS), supercurrent density, and a radially-textured magnetic-moment density** — computed in the clean limit. The **core magnetization / radial magnetic-moment texture** arising from broken inversion symmetry is the distinctive result.
- **Key equations:** Order parameter Δ_k = (Ψσ̂₀ + d_k·σ̂)iσ̂_y with d_k = Δ(−k̃_y, k̃_x, 0) (s+p mix); **Eilenberger quasiclassical equations** split into two FS sheets: iv·∇ǧ_{I,II} + [iω_n τ̌₃ − Δ̌_{I,II}, ǧ_{I,II}] = 0, solved self-consistently for Δ(r) with Riccati/quasiclassical Green's functions.
- **DFT-heavy or theory?** **THEORY / QUASICLASSICAL NUMERICS — tractable in-process.** No DFT. Requires an Eilenberger/Riccati vortex solver (2D self-consistent) — a moderately specialized but standard numerical method, runnable in-process. Reproducible outputs: LDOS map, core magnetization profile. Solid replication candidate.
