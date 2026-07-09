# Failure Analysis — s100-017 (Jonak et al. 2016 ATM/p53/NF-κB ODE)

**Verdict on disk:** REPLICATED (Coverage 8/10, Agreement 8/10).
**Queue verdict:** REPLICATED. **Cross-check:** MATCH — no verdict mismatch.

This file is the mandatory honest post-mortem per Rick's 2026-07-05 rule.
It records what we did not test, what we could not test, and where the paper
itself has limitations that the replication inherits.

## 1. What we did NOT reproduce (out-of-scope by choice)

| Claim family | Why not | Data blocker? |
|---|---|---|
| Apoptotic-fraction % (Fig 4b/c, 1000-cell Gillespie stats) | Requires Haseltine–Rawlings hybrid simulator implementation (~1–2 dev-days). | No — algorithm in MOESM2. |
| Clonogenic-survival % (Fig 4a) | Same as above **plus** Kracikova threshold values not printed in supplements. | **Yes** — Fig 4a training-set numerical table is genuinely absent from all 10 supp files (bar-graph readoff only, ±1 pp). |
| Sensitivity-analysis numerics (MOESM8) | Only in plot form. Paper's claim is qualitative. | No — model is available; can re-derive on demand. |

## 2. Quantitative vs qualitative fit — HONEST assessment

### p53 pulse: period and amplitude
- **Paper claim:** damped oscillations, peak ~2 h post-IR, decay back to
  baseline by ~24 h.
- **Our result:** peak P53pn at 2.25 h (Ctr) / 2.55 h (Wip1-RNAi), decay
  back to low band by 24 h. **Matches paper's specification.**
- **What we did NOT do:** we did not fit the pulse period or amplitude
  against Geva-Zatorsky-style single-cell live-imaging data (100-min pulse
  period in MCF-7). The paper itself does not attempt this — its pulse claim
  is essentially "one damped pulse in the deterministic limit," and our
  numbers satisfy that specification. But this is a **qualitative** match on
  pulse structure, not a **quantitative** period/amplitude fit.
- **Verdict:** QUALITATIVE MATCH on pulse structure. NO QUANTITATIVE
  PERIOD/AMPLITUDE FIT.

### NF-κB oscillation timescale
- **Paper claim:** NF-κB activation by TNFα is much stronger than by ATM/IR
  (implicit in Fig 1 connectivity, verified numerically in Fig 4c).
- **Our result:** peak NFKBn 88 493 (TNF) vs 9 245 (IR-only) → ~10×. **Matches
  paper's implicit prediction.**
- **What we did NOT do:** we did not fit the NF-κB oscillation period
  (~100 min in Hoffmann/Nelson data). The IκBα/A20 negative-feedback loop is
  in the model and *can* support oscillations, but a period sweep versus
  experimental data was not run. Our TNF trajectories saturate rather than
  oscillate at the resolution shown.
- **Verdict:** MAGNITUDE-RANKING MATCH. NO OSCILLATION-PERIOD FIT.

### p53 ↔ NF-κB crosstalk
- **Paper claim:** TNFα 3 h pre-IR reduces p53 pulse amplitude
  (radio-protective, mediated via NF-κB → apoptosis-inhibitor upregulation).
- **Our result:** peak P53pn 111 480 (TNF+IR) vs 188 011 (IR-only) → −41%.
  **Matches paper's directional claim; not quantitatively fit to a target
  number because none is published.**
- **Reciprocal probes NOT tested:** Wip1-KO effect on NF-κB (does removing
  the DDR switch-off alter NF-κB kinetics?); NF-κB inhibitor effect on p53
  (does IKK-KD change the IR p53 response?). Both are model-testable in
  ~1 h of extra work.
- **Verdict:** ONE ARM OF CROSSTALK TESTED, RECIPROCAL ARMS UNTESTED.

## 3. Parameter identifiability — the elephant in the room

The model has **~110 rate constants** against experimental readouts consisting
of a handful of Western-blot time courses (Figs 2, 3) plus one clonogenic
survival curve (Fig 4a). This is textbook non-identifiability territory
(Raue et al. 2009 Bioinformatics; Villaverde 2019 review).

- The paper reports **local sensitivity plots** (MOESM8) but no
  **profile likelihoods**, no **Fisher-information analysis**, no
  **structural identifiability** analysis (COMBOS, StrikePy, etc.).
- Our replication reproduces the trajectories. This does **not** prove the
  mechanism (it only proves that *one* parameter set produces the observed
  behaviour — many others might too).
- **Concrete concern:** the paper's headline conclusion "Wip1 is the
  dominant DDR switch-off" would be undermined if a compensating change in
  Mdm2 kinetics reproduces the Wip1-RNAi phenotype. We have not tested this.
- **Verdict:** IDENTIFIABILITY IS UNADDRESSED BY THE PAPER, INHERITED
  UNADDRESSED BY OUR REPLICATION.

## 4. Mean-field DSB gap (claim #13)

- Paper: 24 DSBs @ 4 Gy (from fit to stochastic scheme).
- Our mean-field: 2.3 DSBs @ 4 Gy.
- This is **not** a disagreement — the mean-field limit collapses Poisson
  DSB events into a continuous quantity, and downstream Michaelis–Menten
  kinetics saturate at DSB ≳ mm2 = mm3 = 1, so p53/Mdm2/Wip1 dynamics are
  correct. But at LOW doses (<0.5 Gy) this gap becomes qualitative — the
  mean-field model likely **underestimates low-dose hypersensitivity (LDHS)**.
- The paper does not sweep below 2 Gy. Our replication inherits this gap.
- **Verdict:** DOCUMENTED MEAN-FIELD ARTIFACT AT HIGH DOSE; QUALITATIVE
  FAILURE MODE AT LOW DOSE (UNTESTED).

## 5. Broader limitations of the paper (which we now inherit)

1. **Single cell line.** Validated on Ctr-RNAi vs Wip1-RNAi in one
   MCF-7-like background. Generalization to p53-mutant, ATM-null,
   MDM2-amplified backgrounds is untested (Open Question #5).
2. **G1/G0 only.** No ATR/CHK1; not applicable to replication-stress
   agents combined with IR (Open Question #2).
3. **Missing training data.** Fig 4a clonogenic training set never
   printed anywhere in the paper or its 10 supplements. This is the
   **only true data blocker** we hit.
4. **Homogeneous 1000-cell population.** All 1000 simulated cells drawn
   from identical parameters → artificial synchrony (Open Question #1).

## 6. What would flip the verdict

The replication would move from REPLICATED → PARTIAL if any of the following
were shown:
- Independent parameter identifiability analysis reveals that the Wip1
  or TNFα headline claims are not identifiable from the training data.
- Stochastic hybrid simulation shows apoptotic-fraction % disagreeing
  with paper's Fig 4b/c beyond the ±5 pp typical Kracikova-fit slop.
- Extension to p53-null / ATM-null backgrounds fails to reproduce published
  radio-sensitivity rankings (indicating the model is over-fit to one
  cell line).

None of these have been done. The current REPLICATED verdict rests on the
**deterministic ODE core** matching all the paper's ODE-level qualitative
and semi-quantitative predictions. It does **not** vouch for the paper's
population-statistics or clinical-generalization claims.

## 7. Free-endpoint / reproducibility compliance

- All replication runs local CPU (no LLM inference, no GPU).
- All backfill artifacts authored offline, no paid API calls.
- Bit-for-bit reproducible on any platform with the same NumPy/SciPy.
