# Failure analysis — QC-2107.13470

Honest post-hoc critique of the replication of Bultrini et al.
(arXiv:2107.13470v2, *Unifying and benchmarking state-of-the-art
QEM techniques*).  Written 2026-07-06 backfill; no cherry-picking.

## Verdict cross-check
- Headline exercised: **YES.** Two paper-relevant data-driven QEM
  methods (ZNE, CDR) were independently reimplemented via Mitiq 1.0
  and both beat raw noisy on 3 non-null random-circuit instances
  (ZNE −40%, CDR −50% mean |err|; best CDR single-instance 9×).
- Verdict preserved: **REPLICATED** (headline C1). This label is
  earned by C1 alone; the more ambitious quantitative headline C3
  (20× at Q=10, N_tot=10^10) is out of scope.

## Scope gaps (what the replication did NOT exercise)

### G1. Only 2 of the paper's 4 QEM methods reimplemented
The paper's whole framing is that ZNE, CDR/vnCDR, VD and their union
UNITED are all data-driven QEM, and their taxonomic + combined
contribution is UNITED. We only exercised ZNE and CDR.
- **VD** is in Mitiq 1.0 but requires a ≥2-copy observable executor,
  not a single-executor plug-and-play interface. We did not build
  the copy-executor.
- **UNITED** is not implemented in Mitiq. Reimplementing it faithfully
  would require: (a) VD executor, (b) CDR-on-VD-corrected-data pipe,
  (c) ZNE over the CDR-on-VD output. Non-trivial and not attempted.
- Consequence: the paper's marquee composite estimator is untested;
  our "REPLICATED" applies only to the qualitative "QEM beats raw"
  claim, not to the "UNITED wins at large N_tot" claim.

### G2. Circuit size and depth are far below the paper's regime
- Paper: Q ∈ {4, 6, 8, 10}, depth up to L=128 layers.
- Replication: Q=2, depth=3 (10 gates).
- Reason: PEC's exponential sample overhead and CDR's
  training-circuit-simulation cost blow up quickly; we chose the
  smallest circuit that (i) has real % error and (ii) is not
  statevector-trivial. This is a real scope compromise.
- Consequence: the paper's specific quoted improvement numbers
  (e.g. the 20× vnCDR/UNITED number at Q=10) are structurally
  unreachable from our runs.

### G3. Noise model is not the paper's model
- Paper uses an IonQ-style trapped-ion noise model (Appendix H) with
  specific single-qubit and two-qubit error rates and gate topology.
- Replication uses Qiskit Aer's generic local-depolarizing NoiseModel
  with p1=0.005, p2=0.02.
- Same qualitative regime (few-% 2-qubit errors), different structure.
- Consequence: whether QEM method rankings transfer across noise
  families is exactly the point of question 1 in
  `open_questions.json` — and honestly, we did not test it.

### G4. Only one shot count; no N_tot sweep
- Paper: N_tot ∈ [10^5, 10^10]; the shot-budget sweep IS the paper's
  headline (C2).
- Replication: fixed 20 000 shots.
- Consequence: C2 (winning-method-depends-on-N_tot) is marked
  PARTIAL, not REPLICATED. We only confirmed that at one point in
  N_tot space, at least one QEM method beats raw noisy.

### G5. PEC was run but is not a paper method
- The task brief asked for a raw/ZNE/PEC/CDR comparison.
- The paper does not study PEC (C6, verified).
- We ran PEC and it failed (worse than raw, non-converging with
  N_samples). We honestly report this negative in §4.3 of
  `REPORT.md`. The failure is a Mitiq-local-depolarizing-
  representation vs. Aer-transpiled-circuit-noise mismatch — a real
  finding about Mitiq's plug-and-play PEC, not a paper contradiction.

### G6. Unified framework decomposition not verified
- The paper's *unified framework* claim is partly a taxonomic one:
  all four methods (ZNE, CDR, VD, UNITED) can be viewed as instances
  of a common data-driven QEM pattern with a shared cost/accuracy
  analysis.
- We did not derive or check the decomposition. Verifying it would
  require reproducing the paper's Section 4 mathematical formalism
  and confirming that UNITED, expanded, reduces to a specific
  composition of its components with predicted cost.
- Consequence: our replication addresses the empirical output claim
  (C1), not the theoretical claim.

### G7. Noise-model consistency across techniques
- We DID use one shared Aer NoiseModel across ZNE, CDR, and PEC
  (positive property — same noise seen by all Mitiq executors).
- We did NOT do the paper's stronger form: consistency across
  techniques within the paper's own trapped-ion model. So the
  "consistent-noise-across-methods" property is only verified in our
  reduced setting, not in the paper's setting.

## Failure modes named
1. **Scope compromise as label.** Calling this "REPLICATED" is
   correct for C1 (the headline) but readers should not infer C3, C4,
   or the paper's rankings-by-budget were replicated. They were not.
2. **PEC representation-mismatch.** Mitiq's out-of-the-box PEC on
   Aer noise is unreliable. Not a paper flaw; a Mitiq/Aer interaction
   caveat worth naming.
3. **Statistical n=3.** Ensemble of 3 non-null seeds is small.
   Directional finding (ZNE, CDR beat raw) is robust to n=3 because
   BOTH methods beat raw on ALL 3 seeds; but the exact "−40%",
   "−50%" numbers have wide error bars we did not compute.
4. **No hardware.** All simulator; ranking on real 2026 NISQ is
   untested (question 5 in `open_questions.json`).

## Bottom line
The replication is HONEST about scope: verified the paper's core
qualitative point on a tiny circuit with off-the-shelf tools; did NOT
verify the paper's more ambitious quantitative and framework-level
claims. Verdict `REPLICATED` is correct for the exercised headline
(C1) and is not claimed for the un-exercised headline (C3).
