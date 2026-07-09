# Brief — Jin et al. 2020/2022 (PNN)

**Paper.** Pengzhan Jin, Zhen Zhang, Ioannis G. Kevrekidis, George Em Karniadakis — *Learning Poisson systems and trajectories of autonomous systems via Poisson neural networks* — arXiv:2012.03133 (2020) / IEEE TNNLS 2022, DOI 10.1109/TNNLS.2022.3148734.

**What.** PNN parameterizes the phase flow of an arbitrary Poisson system as `Φ = INN ∘ SympNet ∘ INN⁻¹` (a Darboux–Lie coordinate transform composed with a symplectic map), giving *structural* preservation of the Poisson bracket by construction.

**Why we care.** Long-time trajectory prediction of Hamiltonian/Poisson systems is a canonical test bed for physics-informed neural ODE-style learners; the paper's central empirical claim is that PNNs give stable rollouts and near-machine-precision invariant conservation where plain neural baselines drift.

**What we did.** Cloned the authors' public reference implementation (`github.com/jpzxshi/pnn` + `learner`), reran the Section IV-A Lotka–Volterra experiment on 1× NVIDIA A100 (uicgpu), at a reduced 30,000 iteration budget (vs. paper's 200,000), and compared PNN long-time rollout MSE and Hamiltonian-invariant drift against a plain residual MLP baseline (hidden=64, depth=4, tanh) trained on the identical one-step data. LLM-judge scoring via Argo Claude Opus 4.7 (free endpoint).
