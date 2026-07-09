# Brief — OSTI 2976249

**Paper.** Toscano, Oommen, Varghese, Zou, Ahmadi Daryakenari, Wu, Karniadakis (Brown, 2025). *From PINNs to PIKANs: Recent Advances in Physics-Informed Machine Learning.* OA PDF (36 MB, 55 pp.) fetched from OSTI purl 2976249.

**Why spot-check, not full replication.** This is a comprehensive review/survey paper (algorithmic developments, applications, UQ, theory, software of PINNs and their Kolmogorov–Arnold Network variant PIKANs). It presents no original numerical experiment of its own — every quantitative comparison is cited from prior work (esp. ref [17] Shukla et al., CMAME 431:117290, 2024, the actual cPIKAN benchmark paper). Per the wave brief protocol, a pure review with no reproducible original experiment is a legitimate SPOT-CHECK target: verify data/code availability and method plausibility.

**What we did.** (1) Independently classified paper structure and confirmed no numbered reproducible experiment. (2) Verified public availability of every major framework the paper reviews (DeepXDE, PhysicsNeMo, NeuralPDE.jl) and the seminal cPIKAN reference. (3) Ran an independent canonical PINN benchmark — 1D viscous Burgers with ν=0.01/π, the exact problem the review itself uses as its running exemplar — on uicgpu with DeepXDE 1.10.1 / PyTorch. Achieved 5.8 % global L2 relative error with a short training budget (Adam 8k + L-BFGS 1k, 110 s wall), demonstrating the reviewed methodology is live and reproducible.

**Verdict (v1, spot-check phase):** SPOT-CHECK.

---

**Wave-3 deepening (2026-07-04).** Because the review's *headline narrative* claim (C2: cPIKANs comparable-or-better than MLP-PINNs with fewer parameters, per ref [17] Shukla 2024) IS testable via reimplementation of both models on the same canonical benchmark, we did exactly that. Implemented in pure PyTorch on uicgpu (1×A100): a matched-budget head-to-head where an MLP-PINN `[2,20,20,20,20,1]` (1341 params, tanh, Xavier) and a Chebyshev-KAN `[2,10,10,1]` deg=6 (910 params, per Shukla et al. 2024 Sec III) were trained with identical loss weights, collocation points, seed, optimizer schedule (Adam 20k @ lr=1e-3 grad-clip=1 + 3×L-BFGS 500), against the same Raissi spectral reference on 1D Burgers ν=0.01/π. **Result: MLP-PINN reaches 0.98 % global L2 (Raissi 2019 ballpark). The cPIKAN under matched budget reaches only 16.05 % global L2 despite 32 % fewer params, and fails to capture the shock past t ≈ 0.5.** This does NOT reproduce C2 out-of-the-box under matched-budget honest implementation — which is a real, testable finding about the review as a standalone artifact.

**Verdict:** PARTIAL (C6 + C7 reproduced, C2 tested and did not reproduce under matched-budget straightforward reimplementation; C1/C3/C4/C5 not testable or not tested here). Argo `argo:gpt-5.2` LLM judge concurs (PARTIAL, confidence 0.78).
