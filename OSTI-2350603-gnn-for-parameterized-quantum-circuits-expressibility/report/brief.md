# Brief — OSTI 2350603

**Paper:** Aktar et al., "Graph Neural Networks for Parameterized Quantum
Circuits Expressibility Estimation" (LA-UR-23-33850, arXiv:2405.08100, 2024).

**What:** A graph-transformer GNN predicts the expressibility (KL divergence to
Haar) of a parameterized quantum circuit directly from its structure, avoiding
the expensive fidelity-sampling estimation. Paper reports RMSE ≈ 0.05 on a
25,000-PQC noiseless dataset and validates on the 19 Sim et al. reference
circuits (RMSE 0.05).

**Why replicate:** the method is a plausible ML-shortcut for a well-defined
statistical quantity (Sim-et-al KL expressibility). Both the ground-truth
computation (fidelity sampling + Haar analytic PDF + histogram-KL) and the
GNN pipeline (TransformerConv × 3 + global-feature MLP + regressor) are
described in enough detail to reimplement independently. No public code
accompanies the paper, so a from-scratch reimplementation is the only route.

**Independent replication:** built the full pipeline from the paper text on
UICGPU (Qiskit 2.5 for statevector fidelity, PyG 2.8 TransformerConv for the
GNN). Validated our ground-truth expressibility calculation against Sim et
al.'s published Table VII values on 19 reference circuits at n=4 (agreement
within statistical noise on 5000 samples). Then trained the GNN on a 750-PQC
scale-down dataset (n ∈ {2..6}, 3000 samples per PQC) and evaluated on both
held-out random circuits and the Sim19 set.
