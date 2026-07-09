# Failure Analysis

Honest accounting of what broke, what almost broke, and what's still not covered.

## What was NOT re-implemented from the paper
- **Proposition 2 numerical Fourier-coefficient bounds in the appendix.** The paper's appendix gives numerical bounds on the tail weight |α_ρ|² using an analytic Dirichlet-kernel argument. We independently *reproduced* the values (see C3 in `REPORT.tex`) but by numerical maximisation over 4000 random θ ∈ [0,1) at N=2¹⁰, not by re-deriving the analytic bound. The paper's numerical values (0.099, 0.067, 0.050) matched our numerical values (0.0994, 0.0669, 0.0504) to three decimals, which strongly indicates their derivation is correct, but we did not re-derive it.

- **Explicit Qiskit-Aer circuit compilation of the modified Hadamards / the U^j operator.** The paper's Section 3.2 describes a specific implementation (per-qubit Hadamard replaced by a single-qubit gate |0> → (|0> + e^{2πi 2^{n-ℓ}λ}|1>)/√2). We treat the input state to C as already prepared in the ideal λ-shifted form. This is a *mathematical* equivalence to what the modified-Hadamard circuit produces, not a physical circuit-level demonstration. For a full replication targeting hardware fidelity, the circuit should be compiled and simulated with realistic gate infidelities.

- **Amplitude estimation (Section 4.2).** We tested Section 4.1 (period-finding) but not Section 4.2 (amplitude estimation). The paper says AE requires the Section 3.3 "general θ" analysis rather than the tighter n-bit-θ Section 3.2 result, so a full AE test would exercise the tighter tolerable-η regime (η ≤ 0.041 rather than η < 1/2). We accept this gap and flag it as a natural next-round test.

## Bugs discovered during the reproduction

### Bug 1: post-QFT Z-dephasing is invisible to the paper's η metric
- **Symptom**: our initial "dephasing" channel (per-qubit random Z rotations *after* the ideal iQFT) reported ground-truth η = 0 across all noise strengths p ∈ {0.05, 0.10, 0.15, 0.20}, and the Theorem-1 estimator agreed with η = 0.
- **Root cause**: diagonal unitaries in the computational basis (Z rotations) do not change |ψ|² for any state ψ, so the paper's outcome-distribution-based η is identically 0 for these channels. This is *not* a bug in the paper — it's an inherent feature of measuring "does the correct k appear?" — but it's a notable metric blind spot we did not anticipate.
- **Fix**: replaced the noise channel with per-qubit random RY over/under-rotation, which produces genuine computational-basis measurement errors.
- **Feeds Q1** in `open_questions.json`.

### Bug 2: period-finding "good outcome" criterion was too strict
- **Symptom**: initial C4 runs reported shifted success rate ~0.4 vs paper bound 0.78 → apparent CONTRADICTION.
- **Root cause 1**: initial `good` criterion was `|j/N - c/r| < 1/N` which for N=32, r=5 gives only c=0..4 with 1/N=1/32 tolerance, missing floor/ceil choices when N/r is not an integer.
- **Root cause 2**: initial C4 fed `F_N|π_s>` directly into channel C, but the actual PE circuit produces on the first register a *mixed state* Σ_j |α_j|² F_N|j><j|F_N† (obtained by tracing out the second register after V acts). The correct Monte-Carlo is: sample j ~ |α_j|², prepare F_N|j> (a Fourier basis state), apply C, measure.
- **Fix**: both criteria corrected. New good_js = {floor(cN/r), ceil(cN/r) : c=0..r-1}. New protocol samples j ~ |α_j|² per trial. Shifted success rate then jumped to ~0.86, comfortably above the paper's (1-η)·8/π² ≈ 0.78 bound.
- **Lesson**: when reproducing PE, do not conflate the first-register state *at the end of V* with the state you feed the inverse QFT for measurement — they are related by the partial trace on the second register.

### Bug 3: pure-Python inner loop O(N · n) per channel call was slow
- **Symptom**: initial run of C1 was stuck for >5 min just on channel 1 of 5.
- **Root cause**: nested Python for-loops assembling the diagonal phase vector for the dephasing channel.
- **Fix**: precomputed bit masks and used numpy vector ops. Speedup ≈ 20×.

## Where our numbers are noisier than they could be
- **C1 empirical failure rate = 0/60 in every cell.** With Chernoff constant c=3 and Chernoff success rate at (ε=0.02, δ=0.10) predicting one failure every ~10 trials, our 0/60 suggests our c=3 is generously above the tight constant. This is *fine* for validating the O-bound but does not tightly pin the constant. A dedicated run with c=1 (approximating the naive Chernoff bound) would sharpen this.
- **C2 Monte-Carlo noise (2000 shots per config)**: shifted failure rate has ~1% standard error, which is not tiny compared to the differences we're measuring (0.096 vs 0.093 for gt_eta on ryerr-n3-p0.20). All three cases where naive > shifted are consistent with the paper, but a rigorous statistical test would need ~10x more shots.
- **C3 sampling of θ**: 4000 random θ finds |α_ρ|² tails to ~1% precision. To match the paper's numerical values to 3 decimals we may have slightly under-estimated the true worst case; a dense grid over θ ∈ [0, 1/N) (the fundamental region) would be more rigorous.
- **C4 shifted success rate at 1500 trials**: ~1.3% standard error on rates near 0.87.

## Residual gaps we consciously accept
- **Marker/Nougat fallback**: we used pdftotext as a fallback. Both `extraction/marker.md` and `extraction/nougat.mmd` bear an explicit header disclosing this. For a 6-page paper with a clean text layer, we judged installing the ~5.5 GB of ML dependencies disproportionate. Documented in `workflow.md`.
- **No LLM-judge verdict**: the wave brief allows an optional 3-judge Argo panel "only if time remains". Given that all four claims are quantitatively self-verifying against the paper's stated numbers (η ≤ 0.041, tolerable η < 1/2, (1-η)·8/π² ≈ 0.78), we opted for a self-verdict grounded in the numerical evidence rather than an LLM panel. If Rick wants the panel we can add it in a follow-up.
- **No hardware run**: the paper's motivation is verifying *real* hardware QFTs, but we simulated with numpy statevector only. Running on IBM Quantum / IonQ would test the practical protocol at O(n) qubits — this is a natural follow-up but out of scope for a first-cut QC-200 replication.
- **n ≤ 6 only**: paper's bounds are asymptotic in n but paper-scale numerics are typically at N=2¹⁰. We tested C3 at N=2¹⁰ (only 1D scan over θ, not exhaustive) but C1/C2/C4 at n ≤ 5 to keep runtime reasonable. Given the closed-form nature of the theorems, scaling to larger n changes constants but not correctness.
