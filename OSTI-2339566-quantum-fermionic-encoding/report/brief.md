# Brief — OSTI 2339566

**Paper:** Huang, Sheng, Govoni, Galli (2023), *Quantum Simulations of Fermionic Hamiltonians with Efficient Encoding and Ansatz Schemes*, J. Chem. Theory Comput. 19, 1487–1498. DOI 10.1021/acs.jctc.2c01119; arXiv 2212.01912.

**What/why:** The authors combine (i) a Qubit-Efficient Encoding (QEE) that maps only physically-allowed Slater determinants onto qubits, needing `Nq = ⌈log₂ Q⌉` instead of `2N`, with (ii) a modified Qubit Coupled-Cluster (QCC) ansatz that screens entanglers by first-derivative gradients, plus (iii) zero-noise extrapolation on IBM hardware, to make VQE simulations of spin defects (NV⁻, VV⁰, V⁻ₛᵢ in diamond/4H-SiC) practical beyond minimum models on NISQ devices.

**Replication scope:** Full download of the OSTI PDF + independent classical reimplementation of QEE (from OpenFermion/PySCF integrals) and QCC (all-Pauli screening + BFGS-VQE) on the small-molecule reference cases the paper cites (H₂, LiH, BeH₂, H₂O in STO-3G), plus H₄-linear. Spin-defect QDET/WEST runs and IBM ibmq_guadalupe hardware runs are not reproduced (external HPC + retired hardware).
