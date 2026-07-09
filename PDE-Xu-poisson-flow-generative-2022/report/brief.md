# Brief — Poisson Flow Generative Models (Xu et al., NeurIPS 2022)

**What:** PFGM is a continuous normalizing flow that interprets image pixels as electric charges in an augmented (N+1)-dim space, learns the (normalized) Poisson field of the data, and generates samples by integrating a backward ODE anchored on the extra "z" dimension. Central claim: PFGM matches state-of-the-art SDE diffusion FID on CIFAR-10 (FID 2.35–2.48) while using 10–20× fewer neural-network evaluations at inference (NFE ≈ 104–110 vs 1,000–2,000 for VE/VP-SDE).

**Why replicate:** PFGM is a foundational PDE-flavored generative modeling paper — it reframes diffusion as electrostatics, making the ODE physically anchored. Independent verification of (a) the pretrained checkpoint loading and running end-to-end, (b) the reported NFE efficiency, and (c) the step-size-robustness claim, is a natural PDE-set entry.
