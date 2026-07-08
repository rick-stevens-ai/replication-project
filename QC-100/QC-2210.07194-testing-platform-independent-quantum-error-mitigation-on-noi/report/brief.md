# Brief — QC-2210.07194 Independent Replication

**Paper:** Russo, Mari, Shammah, LaRose, Zeng — *"Testing platform-independent quantum error mitigation on noisy quantum computers"* (arXiv 2210.07194, Unitary Fund).

**What we did:** Reproduced the paper's core simulator-only claim — that Zero-Noise Extrapolation (ZNE) with global unitary folding at scale factors {1, 2, 3} produces an "improvement factor" μ > 1 on 3-qubit randomized-benchmarking circuits under 1% two-qubit depolarizing noise — using **Mitiq 1.0.0 + Qiskit 2.5.0 + Qiskit Aer 0.17.2** built from scratch by us (no notebook copy).

**Why:** Verify that the paper's headline "1×–7× improvement from quantum error mitigation" is honestly reproducible with the exact software stack the paper cites, on our own randomly-generated Clifford circuits, without any per-experiment tuning.

**Result:** At depth d=1 the paper's regime is confirmed cleanly — mu_ZNE(Richardson) ≈ 3.4 and mu_ZNE(Linear) ≈ 6.0 under 1% depol noise (paper claim: μ up to 7×). At larger depths the noise saturates (A₀ → 1/2ⁿ), and ZNE μ ≈ 1 — this too matches the paper's own observation that mitigation is problem-and-noise-regime dependent.
