# Brief — OSTI 3002455

**Paper:** Han & Cheng (2025), "Benchmarking universal machine learning interatomic potentials for rapid analysis of inelastic neutron scattering data", *Mach. Learn.: Sci. Technol.* 6, 030504 (ORNL). DOI 10.1088/2632-2153/adfa68. Code+data released (github.com/maplewen4/phonon_uMLIP, Zenodo 10.5281/zenodo.15298435).

**What:** The authors built a new DFT phonon reference database (4869 crystals ≤ 12 atoms from Materials Project) and benchmarked 12 universal ML interatomic potentials (uMLIPs) — ORB v3, SevenNet-MF-ompa, MatterSim 5M, MACE-MPA-0, GRACE-2L-OAM, eSEN-30M-OAM, ORB v1, SevenNet-0, MACE-MP-0, CHGNet, M3GNet, eqV2 M — on optimized-geometry deviation, phonon-frequency MAE vs DFT, PDOS Spearman correlation, plus experimental INS spectra for 4 crystals and 6 hydrogen-containing molecular crystals. Key qualitative claim: the *newest* uMLIPs (ORB v3, MatterSim, SevenNet-MF-ompa, GRACE-2L-OAM, MACE-MPA-0, eSEN-30M-OAM) approach near-DFT phonon accuracy, whereas older ones — **especially MACE-MP-0** — **systematically underestimate phonon frequencies** (soften high-frequency optical modes).

**Why:** Independently verify that (a) the released code + pretrained checkpoints actually reproduce the paper's methodology, and (b) the headline directional claim about MACE-MP-0 underestimation holds when we run the exact same recipe (ASE + FIRE relax → Phonopy finite-difference → uMLIP forces) on our own crystal selection.

**How:** On uicgpu, installed a fresh Python 3.11 env, `pip install mace-torch chgnet ase phonopy pymatgen`. Reproduced the paper's per-material workflow (their `mlff_phonon_0_8.py`) on 5 well-characterized crystals with experimentally known max phonon frequencies (Si, Ge, NaCl, MgO, diamond). Ran MACE-MP-0 and CHGNet — the two paper-index-0 and paper-index-1 baselines. Compared max phonon frequency (all q-points on 8×8×8 Γ-centered mesh) to experimental references.

**Result:** All 10 of 10 material×model combinations underestimate the reference max phonon frequency (MACE-MP-0 mean −21.6%, CHGNet mean −20.6%). Directly reproduces the paper's central qualitative claim of systematic softening for the older uMLIPs.

**Verdict:** PARTIAL (headline directional claim about MACE-MP-0 systematic underestimation is quantitatively reproduced; the 12-model 4869-crystal full benchmark and INS-spectra head-to-heads for the newer uMLIPs are out of scope for this small-subset independent rerun).
