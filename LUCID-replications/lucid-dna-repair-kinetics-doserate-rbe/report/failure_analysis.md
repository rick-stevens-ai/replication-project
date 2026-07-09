# Failure Analysis — Honest Critique

Replication of Liew et al., IJMS 23, 6268 (2022) — LUCID DNA-repair kinetics
× dose-rate × RBE.

Verdict: **PARTIAL**. This file records where the replication succeeds, where
it fails, and where it silently avoids the question.

## 1. Where the paper's headline was exercised — partially

The paper's headline mechanism is *the addition of time-resolved DSB repair
kinetics to UNIVERSE, producing a dose-rate-dependent correction to the
photon reference channel, which then propagates into ion-beam RBE
predictions against in-vivo rat-spinal-cord TD50 data*.

We exercised:
- The photon-side repair-kinetics survival model (Eq. 5, Sec. 5.2).
- The R_TD50 dose-rate correction against the paper's Table 3 col 4 /
  Fig 4 left, quantitatively (MAD 0.83% across 14 conditions).
- The Table 2 saturation-gain trend vs dose at the LET → 0 photon-only limit.

We did **not** exercise:
- The ion track-structure sub-model (Kiefer–Chatterjee RDD, Eqs. 6–10).
- The Friedrich-2015 LET-dependent DSB-yield enhancement.
- The FLUKA Monte-Carlo simulation of the HIT scanned SOBP fields.
- The RBE-weighted absorbed-dose calculation itself (which is *the* clinical
  quantity of interest, and *the* thing the paper actually plots in Figs 1,
  2, 4 mid/right, 5).
- Any independent parameter fit — Table 1 parameters were used verbatim.

So the sub-model that generates the paper's *mechanistic novelty* is
reproduced. The showcase clinical curves — the pictures a reader would point
to and say "this is what the paper shows" — are not.

## 2. Specific gaps against the paper's headline

### 2a. DNA-repair ODE model
The paper describes the kinetics as a stochastic per-DSB Poisson-lifetime
process, not an ODE. We implemented it as written (MC per-DSB). If a
reviewer wanted a mean-field ODE comparison, that would be a genuine
extension — not part of the paper as written and not part of this
replication.

### 2b. Cell-line-specific parameter fits
The paper reports Table 1 values for DU145 (in vitro) and RSC (in vivo)
without a supplemental posterior or chi-square. We used the point estimates
verbatim; we did *not* refit them against Karger 2003 + Karger 2006 +
Saager 2018 + Hintz 2022 primary data. Consequently we cannot say whether
the paper's fit is uniquely determined or one of many indistinguishable
optima. This is a real gap for calling the parameter identification
"replicated" — it isn't.

### 2c. Cell-survival predictions
Photon-only cell survival at DU145 and RSC parameters is reproduced
(sanity check §3.3 of REPORT.md, 2.8% agreement with LQ at 2 Gy 2 Gy/min).
Ion-beam cell survival (which is where UNIVERSE's added value actually
lives) is not — the ion track-structure sub-model is absent.

### 2d. Dose-rate RBE curves
We produce a photon-side R_TD50(rate) curve. We do not produce the
Fig 1/Fig 2 ion RBE-vs-dose-rate curves. That's a fundamental gap: the
paper is *about* ion RBE and we replicated only the photon reference
denominator.

## 3. Honest assessment of PARTIAL verdict

PARTIAL is the right verdict. Arguments for stronger and weaker:

**Arguments for upgrading to REPLICATED (rejected).** The photon-side
sub-model is the piece the paper introduces as new physics. R_TD50 is the
paper's numerical headline for that new physics, and we hit it to <1.3%
across all 14 published conditions. If the paper's *contribution* is
"here is a repair-kinetics-derived R_TD50 factor", we replicated that.

Reason for rejection: the paper's *conclusion* is not "here's R_TD50", it's
"here's the ion-beam RBE prediction that agrees with in-vivo data once
R_TD50 is folded in". We touched none of the ion-beam RBE prediction.
Calling that REPLICATED would be dishonest.

**Arguments for downgrading to SPOT-CHECK (rejected).** We only touched
the photon side; the ion side is absent; the FLUKA MC and beamline geometry
are proprietary.

Reason for rejection: we did more than spot-check. We reimplemented the
photon-side MC engine end-to-end, ran 14 quantitative comparisons that
match the paper's numeric tables, and reproduced the Table 2 trend across
four doses. SPOT-CHECK would understate that.

**PARTIAL** captures both truths: the achievable subset is done well; the
unachievable subset is untouched.

## 4. What a future full replication would need

1. Public release of the FLUKA HIT scanned-SOBP geometry and per-spill
   timing files (proprietary today; would require HIT institutional
   agreement).
2. Numerical values for the Kiefer–Chatterjee K_p, nucleus radius, and
   saturation-energy constants used in the paper's runs (not printed).
3. Full form of the Friedrich-2015 LET-dependent DSB-yield boost
   (cited ref [62], not written out).
4. Primary TD50 data from Saager 2018 and Hintz 2022 in machine-readable
   form for an independent parameter fit.
5. Ideally, source code of the UNIVERSE GPU implementation — the paper's
   Data Availability Statement is "Not applicable", so this is unlikely.

None of these are within the free-endpoints-only scope of the LUCID
replication set.

## 5. Ambiguities where we made a choice that biased results

- **N_dom = 3200** (not printed; canonical LEM lineage value).
- **cDSB reclassification policy on partial repair**: no downgrade
  (strict Sec 5.2 reading). Estimated <1% impact on R_TD50.
- **Reference photon dose rate**: 3.75 Gy/min for the RSC R_TD50 (Table 3
  normalization), not 2 Gy/min (Figs 1–3 normalization). Consequential;
  we adopted the one that matches the table we're comparing against.

All three would need to be re-tested for robustness in a fuller
reproduction. None were.
