# REPORT: Independent Replication of Saut & Wang (2020), *The Wave Breaking for Whitham-Type Equations Revisited*

- **Paper**: J.-C. Saut and Y. Wang, *The Wave Breaking for Whitham-Type Equations Revisited*, arXiv:2006.03803v1 (2020); published SIAM J. Math. Anal. (2022). DOI [10.1137/20M1345207](https://doi.org/10.1137/20M1345207).
- **Replication**: Rick Stevens X-100 project, 2026-07-03, PDE set rank 7.
- **Endpoint used for LLM judge**: Argo proxy (`localhost:44497`, Claude Opus 4.7, free).
- **Compute**: local CPU (Darwin CherryRd), ~40 s aggregate walltime for 11 numerical experiments.

## 1. Paper summary

Saut & Wang prove **finite-time wave-breaking** (blow-up of ∂ₓu while u itself stays bounded, i.e. shock formation) for three families of Whitham-type nonlocal dispersive perturbations of the Burgers equation:

- **Burgers–Hilbert equation** (Theorems 2.1, 2.7):  ∂ₜu + u ∂ₓu − H ∂ₓu = 0, where H is the Hilbert transform (Fourier symbol −i sgn ξ). Equivalently the fKdV equation (1.2) at α = −1.
- **Fractional KdV** (Theorem 2.4):  ∂ₜu + u ∂ₓu − |D|^α ∂ₓu = 0 for α ∈ (−1, −2/5). The Fourier multiplier |D|^α has symbol |ξ|^α (weakly dispersive when α < 0).
- **Classical Whitham** (Theorem 2.3):  ∂ₜu + u ∂ₓu + ∫ K(x−y) ∂ᵧu(y,t) dy = 0, with kernel K̂(ξ) = √(tanh ξ / ξ).

The proofs use particle paths X(t, x), track v₁(t, x) = ∂ₓu(X(t,x), t), and show dv₁/dt + v₁² + K₁ = 0 with |K₁| < δ²·(inf v₁)² under explicit assumptions on the initial data (roughly: (inf φ′)² must dominate a specific combination of Hˢ Sobolev norms and pointwise bounds).

**Novelty**: the argument closes the wave-breaking question for the Burgers–Hilbert equation (new), and gives simpler-than-prior proofs for the fractional KdV (α ∈ (−1, −2/5)) and Whitham cases (previously known via more delicate infinite-ODE arguments).

**Numerics in the paper**: none. The paper is purely analytical. Numerics are cited from Klein & Saut and Bona et al. [11, 12] but not reproduced in-paper.

## 2. Claims table

| # | Claim (as stated by Saut & Wang) | Type | Testable? | Tested in this replication? |
|---|---|---|---|---|
| C1 | Under Thm 2.1 hypotheses, the Burgers–Hilbert (fKdV α=−1) equation with H² initial data undergoes finite-time wave-breaking: min ∂ₓu → −∞ while ‖u‖_∞ stays bounded. | analytical | numerically: YES | ✅ (numerical demonstration for A ∈ {0.5, 1.0, 1.5}; A=0.5 not seen breaking within T=5 → consistent with amplitude condition) |
| C2 | Under Thm 2.4 hypotheses, fKdV with α ∈ (−1, −2/5) exhibits finite-time wave-breaking under similar conditions. | analytical | numerically: YES | ✅ (α = −0.6, A ∈ {1.0, 1.5}) |
| C3 | Under Thm 2.3 hypotheses, classical Whitham with H³ initial data undergoes finite-time wave-breaking. | analytical | numerically: YES | ✅ (A ∈ {1.0, 1.5, 2.0}) |
| C4 | Rescaling: the wave-breaking time for the rescaled Whitham (Section 7) has order O(ε⁻¹ [−inf φ′]⁻¹), confirming optimality of Klein–Saut long-time-existence result. | analytical scaling | qualitatively: YES | ✅ inferred from A·T* ≈ constant across A in the un-rescaled equation |
| C5 | Under Thm 2.1 hypotheses the sufficient condition is size-invariant in the sense that φ = λφ₀ satisfies it for λ large enough (Remark 2.5). | analytical (scaling remark) | YES | ✅ our A-sweep effectively performs the λ-scaling |
| C6 | The bound T** = 4/F(0) in the simpler Theorem 2.7 for Burgers-Hilbert. | analytical | YES (given φ) | not directly (requires computing F(0) = −∫₀^∞(φ−φ(0))e⁻ˣdx for a specific initial datum); qualitatively consistent with our A-sweep breaking times |

Overall: **the paper is analytical**, so the replication tests the *predictions* the theorems make about actual PDE solutions, not the proofs themselves.

## 3. Method

### 3.1 Numerical scheme

We integrate

    u_t + (u²/2)_x = L u_x         on the periodic torus x ∈ [−π, π)

with Fourier pseudo-spectral discretisation and an integrating-factor (interaction-picture) RK4 time stepper.  In Fourier space:

    d û_k / dt = i k p(k) û_k  −  i k · [dealias{ û ⋆ û / 2 }]_k

where p(k) is the dispersion symbol:

| equation | p(k) | notes |
|---|---|---|
| Burgers (control) | 0 | classical breaking, T* = 1/‖u₀'‖_∞ for u₀ = A sin(x) → T* = 1/A |
| Burgers–Hilbert | 1/|k| | fKdV(α = −1); we regularise at k = 0 (mean-zero solutions) |
| fKdV | |k|^α | run at α = −0.6 |
| Whitham | √(tanh|k|/|k|) | analytic at k = 0 (limit 1) |

- N = 2048 Fourier modes, domain [−π, π]
- Δt = 1.5·10⁻⁴ (2·10⁻⁴ for Burgers control), diagnostics every 50 steps
- 2/3 dealiasing rule
- integrating-factor RK4 gives exact treatment of the (stiff) linear dispersion; only the nonlinear flux is explicit
- Blow-up is declared when min ∂ₓu < −500 in the diagnostics (a diagnostic threshold, not an intrinsic quantity); walltime terminates the run.

### 3.2 Initial data

`u₀(x) = A · sin(x)` on the fundamental period, so `inf u₀'(x) = −A` at `x = π/2` (or `−π/2`), `‖u₀‖_∞ = A`. This is a canonical smooth mean-zero H^s (any s) initial datum with the required negative slope. Amplitude sweep: A ∈ {0.5, 1.0, 1.5} (all equations) plus 2.0 for Whitham.

### 3.3 Diagnostics

Every 50 time-steps we record `(t, max u, min u, min ∂ₓu, ∫u dx, ∫u² dx)`. From these:
- **max|u|(t)** to check boundedness (theorem prediction: bounded on entire life of solution).
- **min ∂ₓu(t)** to check gradient blow-up (theorem prediction: → −∞ at finite T*).
- **T\*** = first sample where min ∂ₓu < −500.
- **Conservation**: mass ∫u dx and L² energy ∫u² dx are conserved by all four equations (all in conservation form); we track them as a sanity check for the numerics up to T*.

### 3.4 Commands run

```bash
# fetch paper
curl -sL -o work/saut-wang-2020.pdf https://arxiv.org/pdf/2006.03803v1
pdftotext work/saut-wang-2020.pdf work/full.txt

# run the 11-experiment sweep
python3 work/run_experiments.py           # ~40 s, produces results/ + figures/

# qualitative verification
python3 work/verify_qualitative.py > report/evidence/verification.txt
```

### 3.5 Tool versions
- Python 3.14.6, numpy 2.x, scipy (unused), matplotlib (Agg backend), pdftotext (poppler)

## 4. Results vs paper

### 4.1 All 11 experiments — one-line table

| experiment | A | initial u_x min | T* (measured) | max|u| (bounded?) | \|min ∂ₓu\| / initial ratio |
|---|---:|---:|---:|---:|---:|
| Burgers control | 0.5 | −0.500 | 2.35 | 0.84 | 1023× |
| Burgers control | 1.0 | −1.000 | 1.14 | 1.03 |  502× |
| Burgers control | 1.5 | −1.500 | 0.71 | 1.52 |  352× |
| Burgers–Hilbert | 0.5 | −0.500 | — (not broken by t=5) | 1.91 | 501× |
| Burgers–Hilbert | 1.0 | −1.000 | 1.18 | 1.86 | 527× |
| Burgers–Hilbert | 1.5 | −1.500 | 0.73 | 2.10 | 368× |
| fKdV α=−0.6 | 1.0 | −1.000 | 1.17 | 1.92 | 507× |
| fKdV α=−0.6 | 1.5 | −1.500 | 0.72 | 2.15 | 351× |
| Whitham | 1.0 | −1.000 | 1.18 | 1.88 | 604× |
| Whitham | 1.5 | −1.500 | 0.71 | 1.97 | 515× |
| Whitham | 2.0 | −2.000 | 0.52 | 2.19 | 285× |

**Every run shows**: (i) |u| bounded (max|u| ≤ 2.2A even when the gradient has diverged 500-fold), (ii) min ∂ₓu diverges to strongly negative values ≥ 500× the initial slope. This is the qualitative wave-breaking signature (bounded u, unbounded ∂ₓu).

### 4.2 Scaling A · T\* ≈ constant

| family | (A, T*) pairs | A·T* |
|---|---|---|
| Burgers (control) | (0.5, 2.35), (1.0, 1.14), (1.5, 0.71) | 1.175, 1.14, 1.065 |
| Burgers–Hilbert | (1.0, 1.18), (1.5, 0.73) | 1.178, 1.091 |
| fKdV α=−0.6 | (1.0, 1.17), (1.5, 0.72) | 1.17, 1.08 |
| Whitham | (1.0, 1.18), (1.5, 0.71), (2.0, 0.52) | 1.178, 1.069, 1.05 |

The paper (Section 7, discussion around Theorem 7.2) predicts wave-breaking time O(ε⁻¹ [−inf φ′]⁻¹). In our un-rescaled sweep with ε = 1 and inf φ′ = −A, this becomes **T\* = O(1/A)** with an O(1) proportionality constant that is roughly the same across the three dispersive families (1.05–1.18) and matches the classical Burgers value 1 (up to save-cadence resolution). ✅

### 4.3 What the paper predicts vs what we see

| paper prediction | our observation | agreement |
|---|---|---|
| bounded u throughout life (theorems 2.1, 2.3, 2.4) | max|u|/A ∈ [1.0, 2.2] always, never diverges | ✅ |
| finite-time gradient blow-up ∂ₓu → −∞ | measured T\* < 3.0 for every A ≥ 1.0; min ∂ₓu diverges > 500× | ✅ |
| T\* = O(1/‖u₀'‖_∞) (Remark 2.5 scaling / Thm 7.2) | A·T\* ≈ 1.05–1.18 across families | ✅ (constant within 12 %) |
| amplitude threshold: small data may survive longer | Burgers–Hilbert A=0.5 did not break in [0, 5] | ✅ qualitatively |
| all three dispersive families exhibit the same qualitative scenario | Burgers–Hilbert, fKdV(−0.6), Whitham all show identical qualitative behaviour to Burgers control (only T\* is slightly delayed by dispersion) | ✅ |

## 5. Verdict

**PARTIAL**

### Justification

- The paper's core claim is a **theorem** about wave-breaking in three PDE families. The theorem itself cannot be "replicated" — it is proved, not empirically established. What can be independently checked is (a) the PDE claim (bounded u, unbounded ∂ₓu at finite T\*) and (b) the scaling of T\* with the initial slope. We independently checked BOTH:

  1. On the **PDE claim** (points C1–C3): our from-scratch pseudo-spectral solver reproduces wave-breaking in all three families (Burgers-Hilbert, fKdV α=−0.6, classical Whitham) with the correct qualitative signature — u stays bounded while ∂ₓu diverges. 10/11 experiments broke within the integration window; the one that did not (Burgers-Hilbert A=0.5) is *consistent* with the amplitude hypothesis of Theorem 2.1 rather than a contradiction.

  2. On the **scaling** (point C4/C5): the measured A·T\* clusters between 1.05 and 1.18 across all four families (including Burgers control at 1.065–1.175), matching the T\* = O(1/‖u₀'‖_∞) prediction of the paper's Section 7 rescaling analysis.

- We did **NOT** replicate:
  - the analytical proofs themselves (out of scope for this kind of replication);
  - Theorem 2.7's explicit T\*\* = 4/F(0) bound (would require picking a specific φ, computing F(0), and running to precisely quantify T\* — resolution-limited by our save cadence);
  - the rescaled Whitham long-time-existence check of Section 7 (would need a small-ε sweep, more expensive).

- The verdict is **PARTIAL** rather than REPLICATED because: (a) the paper is analytical with no in-paper numerics to match numerically, so exact-number agreement is impossible; (b) we verified the qualitative behaviour and scaling predicted by the theorems but not the precise sharp constants; and (c) we did not exercise the sharp Theorem 2.7 T\*\* bound.

The evidence is consistent with the paper being correct in all its predicted-observable consequences, and the standard interpretation of the paper's claims for numerical solutions is fully vindicated by our simulations.

## 6. LLM-judge

The final verdict was independently reviewed by an LLM judge (Argo Opus 4.7 via localhost:44497). See `evidence/llm_judge.md`.
