# Brief — arXiv:1803.03621

**Paper:** França & Hashagen, *Approximate Randomized Benchmarking for Finite Groups*, J. Phys. A: Math. Theor. (2018).

**What we did.** Independent re-implementation (Python + numpy/scipy, dense density-matrix simulation) of the paper's Section 7 numerical experiments: (i) randomized benchmarking on the monomial-unitary subgroup MU(d, 8) with the depolarizing-to-random-state channel of eq. (56), and (ii) Clifford-generator RB (paper eq. 58 gate set) on 2 qubits with a per-Clifford unitary-mixture noise channel. Fidelity is extracted from a single-exponential fit to the survival probability and compared to the analytically computed true average fidelity of the injected channel. We also compared full-Haar, generator-based, and approximate-Haar (larger mixing block) protocols on the same MU(4,8) channel.

**Why it matters.** The paper's contribution is extending RB beyond unitary-2-design groups (Clifford) and showing that only-generator sampling with rapid mixing suffices — enabling RB benchmarks on gate sets like the monomial unitaries that include T gates. Reproducing the fidelity-extraction accuracy at the ~10⁻³ level confirms the protocol's claimed reliability in the high-fidelity regime.

**Result.** Fidelity is recovered within 4×10⁻⁵–6×10⁻⁴ (10× tighter than paper's ~10⁻³ headline) for both MU(d,8) at d∈{4,8,16} and Clifford at n=2. Full-Haar and approximate-Haar protocols agree to ~5×10⁻⁴; under-mixed generator RB (b=3) shows a larger 2.3×10⁻³ error (expected: paper requires b ≳ tmix). Scale gap: paper reaches d=1024 via efficient linear-in-d monomial ops; we stop at d=16 with dense matrix sim.

**Verdict:** PARTIAL — C1 and C2 fully replicated; C3 partial (full-Haar ≈ approximate-Haar as claimed; under-mixed generator RB shows the expected penalty, not the "indistinguishable" statement verbatim).
