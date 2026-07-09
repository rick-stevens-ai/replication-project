# Failure analysis — Matsuya 2018 IMK replication

## What "REPLICATED" actually means here
We reproduced the **mathematical structure and the qualitative biology**
of the IMK model against the paper's own **digitised figures and printed
parameters**. We did NOT independently verify the paper's biology against
the primary experimental sources it cites (Lyng, Han, Marples, Edin,
Mothersill, Liu, Ojima, Chalmers). Read the REPLICATED verdict as
"the paper's math is internally consistent with itself" — not as
"the biology is confirmed against the wet-lab literature."

## Concrete failures / limitations

### 1. Digitised-only comparison (biggest weakness)
All 10 claim-comparisons use hand-digitised points from paper figures at
±5–10 % precision. This limits how confidently we can call anything
"REPLICATED" quantitatively; several claims are effectively
"the curve shape looks right." A serious replication would refit IMK
against the primary raw data. We did not do that.

### 2. Bystander-signal dynamics NOT replicated
The paper claims IMK is an "integrated" DTE + NTE model. We reproduced
the DTE side (LQ + biphasic DSB repair) rigorously and the NTE side
**only as a scalar hit-fraction f_h(D) folded into the survival
equation**. We did NOT simulate:
- A spatial cell population (2D monolayer, cell-cell distances).
- Explicit paracrine signalling (secretion, diffusion, receptor
  binding).
- Emergent NTE from local signal concentration crossing a threshold.

So "bystander effect" here is a phenomenological fit term, not a
mechanistic simulation. Any claim about "cell-cell signaling scope"
from this replication is unearned.

### 3. Only one radiation quality (photon LQ, ~0.05–2 Gy)
The model was tested only against low-LET photon data in the
0.05–2 Gy window. High-LET (α, proton, C-ion) is not covered.
IMK's HRS mechanism should predict LET-dependent HRS shifts (see
open question #5) but this is untested here.

### 4. Cell-line coverage limited
- V79-379A: SPOT-CHECK
- T-47D: PARTIAL (β₀ typo suspect)
- HPV-G / E48: PARTIAL (MTBE only)
- CHO-K1: REPLICATED for PARP-inhibition ordering + derived c_b
- MRC-5: REPLICATED for DSB kinetics ratio

No independent-cell-line generalisation was attempted. The 65× NTE:TE
repair ratio is from MRC-5 only.

### 5. Low-dose hyper-radiosensitivity claim is MODEL-ONLY
We reproduced the model's HRS shoulder and its response to a c_b scan.
We did NOT demonstrate that HRS in real V79 or T-47D data
**requires** IMK's NTE mechanism, as opposed to competing frameworks
(induced-repair, PLD-repair, threshold LQ). The paper does not run a
formal model comparison against these alternatives and neither did we.

### 6. Parameter non-identifiability
Our independent NLS refit for V79-379A landed in a very different
parameter basin (α₀=0.51 vs. paper 0.016; α_b=0.10 vs. paper 1.46;
δ=1.50 vs. paper 0.26) while achieving R²(log SF) = 0.9996. This is
classical practical non-identifiability. No profile-likelihood or
Bayesian posterior was computed. Every biological interpretation of
individual parameter values (including "c_b = 0.155 h⁻¹") is
therefore weakly supported.

### 7. No MCMC / no credible intervals
Paper: 10⁷ MC samples. Us: bounded-NLS. Neither provides posterior
uncertainty in the modern sense (profile likelihoods, Sobol indices).

### 8. Paper-internal inconsistencies detected but not resolved
- Claim 1: `1/√β_b` V79 text (5.03 Gy) vs. Table 2 β_b (0.396 Gy⁻²
  ⇒ 1.59 Gy). Off by 10× in β_b or by 3× in the text.
- Claim 5: T-47D printed β₀=0.029 gives S(2 Gy)≈0.67 vs. Fig 2(D)
  ≈0.1. Suspected typo.
- Claim 10: T-47D max LLs/nucleus = 0.23 in Fig. 5A vs. Eq. 15
  theoretical max δ/4 = 0.043 with printed δ=0.172. Suspected
  legend swap V79/HPV-G/T-47D.

We flagged these but did NOT contact the authors, file a corrigendum
request, or resolve them via correspondence. A proper replication
ecosystem would.

### 9. Nougat / structured extraction deferred
`extraction/nougat.mmd` is a stub. Real structured extraction (with
LaTeX equation preservation) was deferred pending GPU allocation.
This limits downstream reuse (equation graph, cross-paper claim
mining) but does not affect the numeric replication itself.

### 10. Scope narrower than IMK literature
IMK-family models are claimed to address chromosome aberrations,
micronuclei, apoptosis, and transformation. We only touched
clonogenic survival + DSB kinetics + MTBE.

## Honest self-summary
This replication supports the **model** more than it supports the
**biology**. The IMK equations do what the paper says they do; the
question of whether IMK's NTE mechanism is the *right* explanation
for HRS + MTBE + biphasic DSB repair in real cells remains genuinely
open (see open_questions.json). No falsification, but also no strong
independent confirmation of the paper's headline biological claim.
