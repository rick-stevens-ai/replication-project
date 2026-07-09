# Failure / Limitation Analysis — Poisson Neural Networks (Jin 2022)

Verdict: **REPLICATED** on the focal Sec IV-A Lotka–Volterra experiment.
This document records what the "REPLICATED" verdict does **not** cover, so
that no downstream reader over-interprets the headline.

## 1. Deviations from the paper (transparent)

### 1.1 Reduced training budget (30k vs 200k iterations, 15%)
- **What.** The paper trains PNN for 200 000 iterations on LV. We used 30 000
  for wall-time reasons (single A100, single subagent run).
- **Impact.** Absolute PNN error may be higher than the paper’s original level;
  we cannot claim numeric identity with the paper’s Fig. 2 curves.
- **Why the qualitative verdict still stands.** PNN step-1000 rollout MSE
  (3.61e-3) is *smaller* than step-100 (4.89e-3) — clear evidence of a stable
  regime, not an under-trained one. C2 and C3 hold at 15% of the budget.
- **Residual risk.** Direction: mild under-statement of PNN quality.
  Would not flip verdict.

### 1.2 Baseline is a residual MLP, not the paper’s bare-SympNet counter-example
- **What.** We compared PNN to a residual MLP with ~16× more parameters
  (12 802 vs 816). The paper motivates PNN partly by showing that a bare
  SympNet fails on multi-trajectory *non-canonical* LV data.
- **Impact.** We demonstrated PNN > unstructured baseline, not PNN > SympNet.
  These are different (though compatible) claims.
- **Residual risk.** The paper’s specific counter-example (bare SympNet
  failing on non-canonical LV) remains **unreplicated** here.

### 1.3 Single seed, single run
- **What.** No confidence bands over multiple seeds.
- **Impact.** The reported 45× MSE gap and 5–20× drift gap are point estimates.
- **Mitigation.** The gap is roughly two orders of magnitude — very unlikely
  to close under seed variance. But formally we cannot cite a variance.

### 1.4 Ground truth is symplectic-integrator, not analytic
- **What.** LV has no elementary closed-form flow; SV integrator (drift ~5e-7)
  is the reference.
- **Impact.** Errors are relative to SV. Since SV drift is ~4 orders below
  PNN error, this is a not a practical concern.

## 2. Sub-claim scope: what was **not attempted**
| ID | Claim | Status here | Why unattempted |
|---|---|---|---|
| C1 | Poisson preservation by construction (Darboux–Lie). | **OUT-OF-SCOPE** (indirect via rollouts only) | Structural property; would need bracket / Jacobian probe, not rollouts. |
| C4 | Extended pendulum (odd-dim Poisson).            | **NOT ATTEMPTED** | LV was the assigned focal experiment. |
| C5 | Charged particle in EM potential, NLS, two-body pixel. | **NOT ATTEMPTED** | Out of scope for a single subagent run. |
| C6 | Single non-Hamiltonian trajectory (Thm 3).      | **NOT ATTEMPTED** | Requires a different data setup and metrics. |

These are **claims-in-good-standing**, not refuted claims. Independent
replications would be needed to close them.

## 3. Structural-preservation caveat (C1 is the softest sub-claim)
- PNN’s construction `Φ = INN ∘ SympNet ∘ INN⁻¹` guarantees Poisson
  preservation for the *exact* θ; the trained INN is only an approximate θ.
- Observed PNN invariant drift (max 5.81e-3, final 1.41e-3) is 5–20× better
  than MLP but ~4 orders looser than the SV symplectic-integrator reference
  (4.77e-7).
- This is *consistent* with structural preservation up to approximation error
  in θ, but does not prove the property. A direct bracket-preservation probe
  is future work (see `open_questions.json` Q1).

## 4. Generalisation gap not tested
- Rollouts start at the three training endpoints, which lie ON the trained
  level curves. Off-basin initial conditions on nearby level curves are
  untested — the strongest test of the Poisson-structure story.
- See `open_questions.json` Q5.

## 5. What would flip the verdict
- Systematic 5-seed rerun where PNN vs MLP gaps collapse to statistical
  noise → would downgrade to PARTIAL.
- Discovery that the authors’ INN + G-SympNet stack, run unchanged, produces
  materially worse MSE than reported here (i.e. reveals a code-level bug in
  the reference implementation) → would require reissue.
- Off-basin ICs where PNN degrades to MLP-level → would downgrade C1/C2 to
  in-basin only.

None of these are currently in evidence.

## 6. Summary
- Headline verdict **REPLICATED** is honest for the Sec IV-A LV experiment
  with the caveats above.
- The most important open questions concern **C1 architectural test**,
  **budget sensitivity**, **HNN / bare-SympNet A/B**, **non-separable
  Hamiltonians**, and **off-basin generalisation** — all captured in
  `open_questions.json`.
