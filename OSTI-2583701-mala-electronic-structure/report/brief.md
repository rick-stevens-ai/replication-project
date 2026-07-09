# OSTI-2583701 (MALA) — Brief

**Paper:** Cangi A, Fiedler L, Brzoza B, Shah K, Callow TJ, Kotik D, Schmerler S, Barry MC, Goff JM, Rohskopf A, Vogel DJ, Modine N, Thompson AP, Rajamanickam S. *Materials Learning Algorithms (MALA): Scalable machine learning for electronic structure calculations in large-scale atomistic simulations.* Computer Physics Communications 314:109654 (2025). DOI: [10.1016/j.cpc.2025.109654](https://doi.org/10.1016/j.cpc.2025.109654). CC BY 4.0 open access.

**License:** MALA source BSD-3-Clause. GitHub: <https://github.com/mala-project/mala>. Test data + pretrained demo models: <https://github.com/mala-project/test-data> (tag 2.0.0). Companion CPC library entry: <https://doi.org/10.17632/vbrxhnrvf2.1>.

## Core claims
1. MALA replaces expensive DFT with an ML surrogate: neural networks map local bispectrum descriptors of atomic environments to the local density of states (LDOS), from which band energy, total free energy, DOS, and electronic density are derived.
2. **Accuracy:** production MALA models achieve total-free-energy MAE below 10 meV/atom (paper's strict threshold) and always within chemical accuracy 43.4 meV/atom for boron 144 atoms, aluminum 256 atoms across the solid-liquid phase boundary and 100–933 K temperature range, and beryllium 256 atoms; electronic density MAPE ~1%.
3. **Transferability across length scales:** Be model trained on 256 atoms extrapolates to 512, 1024, 2048, and 131,072 atoms with density MAPE ~1% and total-energy MAE below 10 meV/atom (Fig. 14–15).
4. **Computational scaling:** MALA inference is linear in system size, vs cubic/quadratic for standard DFT. Up to 2 orders of magnitude cheaper than DFT at target sizes.
5. Framework is open-source, packaged, integrates with Quantum ESPRESSO + LAMMPS + PyTorch + ASE, and ships pretrained demo models + reference DFT data for reproducible tutorials.

## Replication scope
Real end-to-end replication of the MALA framework's inference pipeline (Claim 1) on the authors' own shipped DFT reference data for beryllium (2-atom Be cell, 4 snapshots, PBE + Quantum ESPRESSO reference). MALA 1.4.0 installed from GitHub master into a fresh Python 3.10 conda env on uicgpu (8×A100). Pretrained `Be_model` loaded from the test-data repo (BSD-3), inference run via `mala.Tester.test_all_snapshots()` on all four snapshots, band-energy and density errors computed against the DFT reference stored in the same repo.

Claims 3–4 (production-scale transferability and speedup) are out of scope for this pass — they require the paper's production models + Rodare-hosted training/inference datasets and thousands of GPU-hours of DFT reference generation, both far beyond a wave-brief budget.
