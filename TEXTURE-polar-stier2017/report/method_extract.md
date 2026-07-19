# Method Extract — Stier et al. 2017 (arXiv:1701.07256)
**Title:** Skyrmion-Antiskyrmion pair creation by in-plane currents
**Texture class:** polar (magnetic skyrmion/antiskyrmion spin textures; "polar" per project taxonomy)

- **Core physics:** In-plane spin-polarized currents create **skyrmion–antiskyrmion (Sk–ASk) pairs** from magnetization fluctuations without violating topological charge conservation (Sk and ASk carry opposite topological charge). Applied current separates them; the ASk then decays via Gilbert damping, changing the net skyrmion number Q.
- **Headline claim (replication target):** A derived **skyrmion equation of motion** reveals the two-step mechanism (pair creation → current-driven separation → dissipative ASk annihilation), predicting net change of topological charge Q under in-plane current — beyond the standard Thiele approximation. Confirmed by micromagnetic simulation.
- **Key equations:** Extended **Landau-Lifshitz-Gilbert (LLG)** for n = M/|M|:
  ∂ₜn = −n×B_eff + α n×∂ₜn + (v_s·∇)n − β n×(v_s·∇)n,  with B_eff = −∂H/∂n; spin-current velocity v_s = p a³ j_c /(2e). Hamiltonian includes exchange + DMI + Zeeman (lattice model, their Eq. 8). A generalized Thiele/EOM for the skyrmion collective coordinate is derived.
- **DFT-heavy or theory?** **THEORY / MICROMAGNETICS — tractable in-process.** Pure LLG + DMI 2D lattice simulation (mumax-style) plus analytic EOM. No DFT. Excellent replication candidate: reproduce Sk-ASk pair creation and ΔQ from a 2D LLG solver.
