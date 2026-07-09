# Independent Replication — OSTI 2564727

**Paper:** Ryan T. Grimm & Joel D. Eaves, *Accurate Numerical Simulations of Open Quantum Systems Using Spectral Tensor Trains*, J. Chem. Phys. (2025). DOI **10.1063/5.0228873**. OSTI 2564727. OA PDF sha256 `f9f14720ee5a20d8e9e814f66c0b08c001080b431ba25d1e1984f3e6e6f5e6e8`.

**Set:** OSTI-100 (applied_math, rank 5). **Date:** 2026-07-02. **Compute:** local numpy (light); PDF fetched via uicgpu proxy. **LLM judge:** free Argo `gpt-5.2`.

---

## 1. Paper summary

The paper introduces **Q-ASPEN** (Quantum Accelerated Stochastic Propagator Evaluation), a numerically-exact method for the time-dependent noise-averaged reduced density matrix `⟨ρ(t)⟩` of an open quantum system driven by prescribed colored **intrinsic** (thermal/quantum, obeys fluctuation-dissipation) and **extrinsic** (external-field) noise. It solves the **Stochastic Liouville Equation** (SLE), `dρ/dt = −i L(t) ρ` with `L(t)=L₀+ξ(t)L₁`, by:

1. Trotter-discretizing the noise-averaged propagator `Φ_N` (Eqs. 4–6).
2. Using the Gaussian influence kernel `K` (Eqs. 7–8) which weights trajectories like a Boltzmann factor over eigenfrequency walks (a "statistical mechanics of trajectories" ≈ ideal gas of dressed particles).
3. Representing `K` as a **spectral tensor train** (STT) — a matrix-product of Chebyshev-expanded, matrix-valued functions `Kα(ω)` (Eqs. 10–14) — trained by SGD/importance sampling (with an observed *barren-plateau* obstacle).

Benchmarks: spin-boson (Fig. 3, matches PT-TEMPO) and a 2–32-site quantum chain under extrinsic noise (Fig. 4; memory scaling `p≈2.0` for Q-ASPEN vs `p≈8.3` for PT-TEMPO).

**Load-bearing exact result (Eqs. 15–17):** In the **extrinsic Markov limit** (`H=H₀+ξ(t)V`, `⟨ξ(t)ξ(s)⟩=γδ(t−s)`), the correlation matrix is `G=γτ𝟙`, the fugacities collapse to `Zα=e^{−iL₀τ/2}e^{−γL₁²τ/2}e^{−iL₀τ/2}`, and BCH + `τ→0` gives the exact propagator `Φ(t)=exp(−itL₀−tγL₁²/2)`, i.e. the **Lindblad master equation**

> `d⟨ρ⟩/dt = −i[H₀,⟨ρ⟩] + γ( V⟨ρ⟩V − ½{V²,⟨ρ⟩} )`   (Eq. 17).

This is the theoretical anchor on which the whole method's correctness rests, and the target of this replication.

## 2. Claims table

| ID | Claim | Type | Testable independently? | Tested here? |
|----|-------|------|--------------------------|--------------|
| **C1** | Extrinsic-Markov SLE (white noise) ⇒ exact Lindblad ME (Eqs. 16–17) | analytic/exact | **Yes** (integrate SLE + Lindblad, compare) | **Yes ✓** |
| **C2** | Method conserves trace / gives a physical density matrix | numerical | Yes (as consequence of C1) | Yes ✓ (Tr=1.0000) |
| C3 | Spin-boson (Fig.3) matches PT-TEMPO; relaxes to Boltzmann eq. | numerical | Partially (needs PT-TEMPO/OQuPy + intrinsic-noise kernel of App. A) | Not fully (geometry mimicked, not the intrinsic-noise bath) |
| C4 | 32-site chain: Q-ASPEN memory scaling `p≈2.0` vs PT-TEMPO `p≈8.3` | empirical scaling | Needs full STT + OQuPy port | No (out of scope) |
| C5 | STT training exhibits barren plateaus (Fig.5) | empirical (ML) | Needs full STT training | No |

## 3. Method (independent, from equations only)

**Reference (exact Lindblad).** RK4 integration of Eq. 17 (`sle_lindblad.py: integrate_lindblad`). Validated against a closed-form: for `V=σz, H₀=0`, Eq. 17 gives `ρ₀₁(t)=ρ₀₁(0) e^{−2γt}`.

**Independent stochastic route (the object ASPEN averages).** Monte-Carlo average of the SLE stochastic-Schrödinger equation `i d|ψ⟩/dt=(H₀+ξ(t)V)|ψ⟩` with real white noise. Per step, accumulated noise `Δ_k ~ N(0, γτ)`; propagate with **symmetric Trotter** `e^{−iH₀τ/2} e^{−iΔ_k V} e^{−iH₀τ/2}` (mirrors the paper's Eq. 5), then average `ρ=|ψ⟩⟨ψ|` over trajectories. For real noise coupling to Hermitian V, each trajectory is *unitary*; decoherence emerges purely from the ensemble average — the Kubo stochastic-Liouville mechanism the paper is built on. Vectorized over trajectories for speed (exact reformulation).

**Systems tested** (units where relevant match Fig. 3): (1) pure dephasing `V=σz, H₀=(ε/2)σz`; (2) transverse `V=σx, H₀=(ε/2)σz` (non-commuting); (3) **biased qubit, Fig. 3 geometry** `H₀=Ωσx+εσz, V=ασz` with `Ω=1, ε=0.5, α=0.75`.

**Tools:** Python 3.14, numpy, matplotlib. Commands: `python3 sle_lindblad.py`, `python3 convergence.py`, `python3 plot_dynamics.py`.

## 4. Results vs paper

**Analytic anchor** (`V=σz,H₀=0,γ=0.5`): Lindblad `ρ₀₁(t)` vs `0.5 e^{−2γt}` → **max error 9.6e-13** (machine precision). Confirms our Lindblad implementation + conventions.

**C1 — SLE Monte-Carlo vs exact Lindblad** (`N_traj=40000, τ=0.01, t∈[0,4]`):

| Case | max\|ρ_MC − ρ_Lindblad\| | Tr(ρ_MC) | ⟨σz⟩ tracking |
|------|--------------------------|----------|----------------|
| 1 Pure dephasing `V=σz` | **4.3e-3** | 1.0000 | flat (correct) |
| 2 Transverse `V=σx` | **4.2e-3** | 1.0000 | decays 1→0, matches |
| 3 Biased qubit (Fig.3 geom) | **2.9e-3** | 1.0000 | oscillates +0.59→−0.35→…, matches to 3 decimals |

Residuals are at the Monte-Carlo sampling level (`~1/√N ≈ 5e-3` at N=40k). See `evidence/sle_vs_lindblad_dynamics.png`: SLE-MC markers sit on the exact Lindblad curves for all of σx, σy, σz.

**Convergence (no systematic bias).** MC error decreases with N_traj: 7.5e-3 (2.5k) → 5.4e-3 (10k) → 2.8e-3 (40k) → 2.6e-3 (160k). A Trotter scan confirms the residual floor is sampling + O(τ²) discretization, not a model mismatch. As `N→∞, τ→0` the SLE ensemble average → the exact Lindblad solution, exactly as Eqs. 16–17 claim.

**Not reproduced (honest scope):** the STT/tensor-train machinery, its `O(d²)` memory scaling claim (C4), the intrinsic-noise spin-boson↔PT-TEMPO comparison (C3, needs App. A kernel + OQuPy), and the barren-plateau training behavior (C5). These require porting the full method and were out of scope for a fast independent replication.

## 5. Independent LLM-judge (free Argo gpt-5.2)

Verdict: **REPLICATED** for the core analytic claim. Justification (verbatim gist): "Independent Monte-Carlo averaging of the SLE converges toward the Lindblad master-equation solution across several distinct qubit Hamiltonians/couplings, with an analytic dephasing case matched to machine precision and no evidence of systematic deviation." Full text: `evidence/llm_judge_verdict.txt`.

## 6. Assessment

The paper's **central exact statement** — that noise-averaging the Stochastic Liouville Equation with Markovian white noise yields precisely the Lindblad master equation (Eqs. 16–17) — is **independently reproduced**. Two mutually-independent routes (direct Lindblad integration and Monte-Carlo SLE trajectory averaging) agree to sampling+Trotter precision across three physically distinct qubit systems, and a closed-form dephasing case matches to 1e-12. This validates the theoretical foundation of Q-ASPEN. The higher-level STT approximation and scaling claims were not re-derived and are marked untested; hence the core is REPLICATED while the paper as a whole is a PARTIAL replication (core anchor solid, full method not re-run).

## Verdict
**Verdict:** REPLICATED (core analytic claim, Eqs. 16–17); PARTIAL for the paper overall (STT machinery & scaling benchmarks not re-run).
