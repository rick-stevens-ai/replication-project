# Brief — OSTI-2561245 (Istas et al. 2024/2025, H2 LLPT)

Istas, Jensen, Yang, Holzmann, Pierleoni & Ceperley (arXiv:2412.14953, Phys.
Rev. E 111, 045307) use an E(3)-equivariant NequIP machine-learned interatomic
potential trained on public PBE-DFT hydrogen configurations (96-atom cells,
qmc-hamm database) to run 200-2048 atom NPT MD trajectories of ≥200 ps and
apply finite-size scaling to locate the liquid-liquid phase transition
critical point of PBE-hydrogen at T = 1250 K ± 50 K, P ≈ 155-160 GPa,
substantially lower than the Morales et al. 2010 PBE estimate of ~2000 K near
120 GPa. Independent PARTIAL replication (Ollie, 2026-07-02): the qmc-hamm
public dataset was pulled and quantitatively verified to match paper claims
(96 H atoms/cell, PBE energies -14.4 to -15.5 eV/atom, rs range 1.44-1.78
bohr covering the paper's 1.43-1.52 LLPT window, monotone rs(P) at every
sampled isotherm); NequIP is a real actively-maintained open-source E(3)
equivariant NN potential (PyPI, mir-group/nequip); the prior-work
positioning claim (Morales 2010 gave ~2000 K) is triangulation-verified
against the actual Morales et al. PNAS paper abstract. The novel scientific
claim — a lower LLPT critical point at 1250 K from finite-size-scaling
analysis on 200-2048-atom NequIP trajectories — was not rerun end-to-end
here (that requires training a NequIP model + O(100) GPU-hours of NPT MD at
4+ system sizes, well beyond a single subagent turn).
