# Failure Analysis — Honest Critique

## What this document is
An honest, uncharitable inventory of what this replication did NOT accomplish, where the evidence is weaker than the REPLICATED verdict might suggest, and what a hostile reviewer could legitimately object to. This is a companion to REPORT.md / REPORT.tex, not a replacement for them.

## 1. No real quantum hardware was used
The single biggest gap. LaRose et al. (2022) Fig. 3 is fundamentally a **hardware panel** — IBMQ London and Rigetti Aspen-8 traces are what make it compelling, because those devices have coherent errors, drift, readout asymmetry, and crosstalk that no toy noise model captures.

Our replication used only:
- Qiskit-Aer `NoiseModel` with symmetric depolarizing channels (p1=0.01, p2=0.04).
- Cirq `DensityMatrixSimulator` with per-moment `cirq.depolarize(p=0.02)`.

A hostile reviewer is fully justified in saying: "you reproduced the *toy version* of the paper's headline. The hardware-runtime aspect — which is 60% of what makes Mitiq interesting — is entirely unverified." We flag this in REPORT.md §4c but the flag is understated. **The exact mitigated-vs-raw error ratios in the paper's Fig. 3 (which drive the ~2–3× reductions on real hardware) were NOT independently verified.** What we verified is that on *our* noise model, ZNE reduces error by ~40% and CDR by essentially 100%. Those numbers should not be conflated with the paper's.

## 2. Only two of three headline techniques exercised (PEC skipped)
The paper's §5 (PEC) is a first-class technique. We did not run `execute_with_pec` at all. Our justification in REPORT.md §4c ("PEC example is a template rather than a headline numerical claim") is defensible but partial — Mitiq v1.0.0 has real PEC infrastructure and the paper explicitly frames PEC as one of the three core methods. Skipping PEC means claim C6-analogue for PEC is unverified.

## 3. No head-to-head comparison across techniques on identical circuits
We ran three ZNE variants on the ZNE test circuits and CDR on a different circuit with a different observable and a different simulator. We did not:
- Run ZNE, PEC, and CDR on the *same* circuit with the *same* observable and the *same* noise model to see which method wins.
- Repeat CDR on the 10 depth-8 ZNE circuits.
- Repeat ZNE on the 7-op Clifford-dominant CDR circuit.

The paper (§3.1) itself declines to declare a winner, so we don't owe a winner. But a rigorous replication would still put the methods on equal footing so that *any future reader* can point to one number and say "on circuit X under noise Y, method Z wins." We did not produce that number.

## 4. Single circuit depth, single noise level, single random-circuit family
- ZNE was tested at depth=8 only. No depth sweep.
- ZNE noise was fixed at (p1=0.01, p2=0.04). No noise sweep.
- CDR was tested on ONE circuit (not a family of seeds). n=1.
- CDR noise was fixed at p=0.02 depolarizing. No sweep.

The CDR n=1 is particularly weak. A single float value showing CDR → truth is not statistically distinguishable from a fluke on a Clifford-dominant circuit where CDR is *expected* to work perfectly (that's basically the definition of CDR's inductive bias). A more honest replication would repeat the CDR experiment on ≥10 seeds with varying non-Clifford fractions and report a distribution.

## 5. `fold_gates_at_random` — stochastic noise scaling, no seed control reported
Our ZNE runs use `scale_noise=fold_gates_at_random`. This is a randomized folding strategy, and we did not lock a RNG seed for it in the executor. The `report/evidence/zne_results.json` values are therefore not bit-exactly reproducible on re-run. Reproducibility would improve by using `fold_gates_from_left` or by threading `numpy.random.default_rng(seed)` through the folding call.

## 6. Nougat OCR not actually run
The `extraction/nougat.mmd` file added in this backfill is a stub, not a real Nougat conversion. For this paper the stub is defensible (`pdftotext` on a clean arXiv PDF was sufficient for claim extraction) but the QC-100 wave standard artifact list expects a real Nougat output. Documented as a deferral rather than delivered.

## 7. What we did NOT check about Mitiq's own correctness
- Did not verify that `RichardsonFactory` extrapolation matches a hand-computed polynomial through the three (scale, value) points.
- Did not verify that `fold_gates_at_random` actually preserves the ideal unitary (the folded circuit should still give ⟨00⟩=1 in the noise-free simulator; we did not spot-check this).
- Did not verify that `execute_with_cdr`'s internal training-circuit generation actually respects the `fraction_non_clifford=0.2` parameter.

These are unit-test-level checks that would strengthen "Mitiq works as advertised" from a black-box "it improved the number" to a white-box "and here is *why* it improved the number, at each stage."

## 8. Framework coverage (C8) is thin
We tested Cirq and Qiskit. We did NOT test pyQuil or Braket adapters. C8 in REPORT.md is marked "Partially" but the verdict language in §5 does not weaken the overall REPLICATED to reflect this gap. If a reader interpreted REPLICATED as "all 8 claims tested" they would be misled.

## 9. Verdict-substance check
- REPORT.md verdict = **REPLICATED**.
- Substance of what was actually exercised:
  - C1 (installable): ✅ direct.
  - C2 (API surface): ✅ direct.
  - C3 (ZNE Fig. 3 capability): ✅ on toy noise, NOT on real hardware.
  - C4 (multiple ZNE methods): ✅ direct.
  - C5 (CDR §6 capability): ✅ on n=1 circuit.
  - C6 (folding preserves ideal): ✅ implicit only, not spot-checked.
  - C7 (H2 VQE Fig. 4): ❌ not attempted.
  - C8 (framework-agnostic): ⚠️ partial (Cirq + Qiskit only).

Headline (both ZNE and CDR one-line calls reduce error vs raw on canonical toy circuits) IS exercised. Fig. 4 (H2 VQE) is not, and hardware runtime is not. Verdict = **REPLICATED** for a software-tool paper is defensible on this evidence, but the reader must understand it means "the software does what the API says" not "we reproduced the paper's specific hardware numbers."

## 10. What a "REPLICATED (strong)" would require
1. Real hardware runs on a modern IBM/IonQ/Quantinuum device via free tier.
2. PEC exercised on the same circuits.
3. Head-to-head comparison of ZNE / PEC / CDR on identical circuits + observables.
4. Depth and noise sweeps.
5. Statistical CDR (n≥10 seeds, varying fraction_non_clifford).
6. Fig. 4 (H2 VQE) reproduced.
7. pyQuil / Braket adapters at least smoke-tested.

None of these were done. This is a "REPLICATED (baseline)" and REPORT.md should probably read that way if we tighten the wording in a future revision.
