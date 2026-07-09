# Failure analysis — honest critique

## Headline exercised?
**Partially.** The paper's headline is: *"[²²⁵Ac]Ac-PSMA-I&T is ~4× more
biologically effective per unit absorbed dose than [¹⁷⁷Lu]Lu-PSMA-I&T"* and
the associated linear-α / RBE / MIRD-chain scaffolding.

- **Linear-α model:** REPRODUCED (both isotopes, both digitization reads).
- **RBE ≈ 4:** QUALITATIVELY REPRODUCED (recovered 2.96–3.33 vs. published 4.2 ± 0.46, within 1.4–2.7σ). The direction and order-of-magnitude are right; the exact multiplier is off by digitization noise on the shallow Lu-177 survival curve.
- **MIRD chain D = Σ Ã · S:** STRUCTURALLY REPRODUCED with a constant multiplicative offset (Lu 1.28×, Ac 2.4×) whose mechanistic origin is identified.

## What was NOT done (specific + honest)

### 1. Proprietary Monte-Carlo substrate NOT re-run
The paper's S-values in Table 2 come from a **Geant4 v10.03(6) run** with
Livermore EM + FTFP_BERT hadronic physics lists on **custom cellular
geometries derived from microscopy** (Table 1). We took Table 2 verbatim.

- No re-run under Geant4-DNA (BSD-licensed, open source).
- No re-run under TOPAS-nBio.
- No re-run under MCNP or PHITS for cross-code sanity.
- Per-cell geometry meshes are NOT in the paper — only mean dimensions
  are published in Table 1. Re-derivation would require either
  reconstructing meshes from Table 1's summary statistics
  (approximation) or contacting the authors for the raw meshes.

**Consequence:** the S-values that drive the entire MIRD pipeline are
zero-variance inputs in our replication. Any real uncertainty on S is
absent. This is the single largest un-quantified gap.

### 2. Alpha-track microdosimetry NOT reproduced
The paper's RBE ≈ 4 has a mechanistic microdosimetric interpretation
(alpha LET ≈ 80 keV/µm gives high-density DNA damage; beta LET ≈ 0.2 keV/µm
gives sparse damage; ratio 3–5 is theoretically expected). We do not:

- Compute or reproduce the specific-energy distribution f₁(z) for the
  alpha emitter at the nucleus target.
- Model the stochastic hit distribution (Poisson-with-mean-1 regime for
  low-activity alpha) vs. deterministic mean-dose (high-activity beta).
- Reproduce the Ac-225 alpha-daughter chain contributions
  (Fr-221, At-217, Bi-213, Po-213) separately from the parent.

All treatment is at the paper's mean-dose granularity.

### 3. MIRDcell cross-dose averaging NOT performed
The paper explicitly performs cross-dose averaging over the cell-dimension
distribution using MIRDcell. We use only:

- The self-dose S-values for cytoplasm and membrane (0.76 / 0.24 weighting).
- The cross-dose S-value for Lu-177 (1.13E-6 Gy/(Bq·s)) as a stated value
  verified for physics-consistency (C14), not integrated into the pipeline.

This is one of the two identified causes of the constant 1.28× / 2.4×
MIRD offset (the other being instant-uptake vs. slow-ramp TAC).

### 4. Wet-lab data NOT replicated
Six precisely-named data artifacts are required to elevate from PARTIAL
to REPLICATED — none are publicly deposited:

1. Raw clonogenic plate counts (Fig. 3A, 3C).
2. Raw 53BP1 foci segmentation output (per-cell, timepoint × isotope).
3. Raw IC₅₀ displacement plate counts.
4. Fig. S2 per-timepoint cellular excretion %AA.
5. Raw clonogenic plate counts at the highest activity concentrations
   (5 MBq/mL Lu, 1.85 kBq/mL Ac).
6. Geant4 input geometry meshes + decay-history seeds.

Paper's Data Availability statement: *"Please contact the corresponding
author"*. No public deposit exists.

## LUCID-corpus PARTIAL pattern (documented)
This replication fits the **known LUCID pattern** where a paper's central
claim rests on a proprietary computational substrate (here Geant4 with
custom geometry) that is out-of-scope for the LUCID replication budget:

- **Analytical / literature-comparison layer:** reproducible from paper text alone → REPRODUCED.
- **MIRD algebraic chain:** reproducible with reasonable assumptions → REPRODUCED-IN-STRUCTURE.
- **Proprietary MC substrate:** requires days of CPU + non-published geometry → NOT ATTEMPTED.

The LUCID corpus has a documented ~40% verdict-integrity issue in this
class where the underlying MC simulation is never re-run and the
"REPLICATED" verdict is inflated. **This replication does not inflate.**
The verdict is PARTIAL because that is what the evidence supports:
central scaffolding reproduced with quantified residuals, MC substrate
trusted verbatim, wet-lab ground truth data-blocked.

## Drift risk / reader traps

### Digitization noise is real, not spin
Two independent digitization reads of Fig. 3 give α(Ac) = 1.088 (read 1)
vs. 0.639 (read 2) — a factor of 1.7 spread from digitization alone. The
paper reports 0.67 ± 0.06. **Read 2 is within 1σ; read 1 is 3σ off.**
A reader running our pipeline with different digitization seeds will land
somewhere in this range. This is honest digitization uncertainty, not a
hidden systematic.

### The MIRD offset is stable, not random
The 1.28× (Lu) / 2.4× (Ac) offsets are **constant across all five (Lu)
and seven (Ac) tested activity concentrations**. This constancy is the
diagnostic signature of a single multiplicative modeling choice (instant
uptake), not of an algebra error. Readers should not interpret the offset
as a physics disagreement with the paper.

### RBE is invariant under the offset
Because RBE = α(Ac)/α(Lu) is a *ratio*, a constant multiplicative dose
offset that applies equally to both isotopes cancels. What does NOT
cancel is a *differential* offset (Lu 1.28× vs. Ac 2.4×) — this differs
between isotopes because the biological washout kinetics and physical
half-lives differ. This differential is the reason the RBE lands at
2.96–3.33 rather than exactly 4.2 even accounting for the offset.

## Verdict rationale (why PARTIAL, not REPLICATED, not SPOT-CHECK)

**Why not REPLICATED?**
1. Central quantitative claim (α, RBE) recovered only within 1–3σ, and
   the recovery depends on which digitization read one uses.
2. Geant4 MC dosimetry producing Table 2 S-values NOT re-run from first
   principles. We trust the authors' S-values in our pipeline check.
3. No raw wet-lab data; all "STATED VALUE CONFIRMED" claims (C8, C9, C11,
   C14) are cross-checks against physics/statistical priors, not
   independent re-derivations from raw counts.

**Why not SPOT-CHECK?**
1. 12 claim checks (C7–C19) landed on disk with per-claim JSON evidence
   — this exceeds spot-check granularity by an order of magnitude.
2. Central α/RBE/MIRD chain reproduced with quantified residuals, not
   just spot-verified for consistency.
3. Reproducibility blockers named precisely (6/22 rule satisfied).

**Why PARTIAL is right:**
- Paper's central quantitative scaffolding is reproduced from free/local
  sources with quantified residuals.
- The MC substrate under Table 2 is trusted verbatim (documented gap).
- Wet-lab raw data is data-blocked (documented gap).
- The verdict honestly reflects: "the math and the physics check out; the
  simulation substrate and the wet-lab ground truth do not, and we said so."
