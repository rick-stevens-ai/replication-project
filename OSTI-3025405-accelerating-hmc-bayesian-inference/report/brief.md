# brief.md — OSTI 3025405

**Paper.** Thiagarajan, Zaki, Shields (2025), "Accelerating Hamiltonian Monte Carlo
for Bayesian Inference in Neural Networks and Neural Operators"
(OSTI 3025405, arXiv:2507.14652v2, JHU / DE-SC0024162).

**What & why.** The paper proposes a *hybrid VI-HMC* method: run mean-field
variational inference on a Bayesian neural network to get a per-parameter
Gaussian, use its sigma² × grad² as a *sensitivity score*, freeze all
low-sensitivity parameters at their VI means, and run HMC only on the
high-sensitivity subset. The claim is that this reduced-dimension HMC has
higher acceptance rate at fixed step size, allows a larger step size at fixed
acceptance rate, and reaches the same posterior as full HMC — at a
fraction of the cost — while being tractable for real neural operators
(the paper's flagship: a hypersonic-cone DeepONet). We independently
re-implemented the sensitivity-ranking + reduced-HMC pipeline in PyTorch,
substituting MAP + diagonal Laplace for VI (VI collapsed on the small
overparameterized BNNs, matching the paper's own Section-5 limitation),
and reproduced the pipeline on the paper's Case I (6-param sinusoidal BNN)
and Case II (141-param tanh MLP).
