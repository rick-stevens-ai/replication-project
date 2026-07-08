# Failure analysis / honest critique — Mitiq (LaRose et al. 2020)

**Verdict: REPLICATED.** This document records what did NOT go perfectly, so future readers can size the strength of the claim honestly.

## Strengths (why the verdict is genuine, not inflated)

1. **Independent software install.** Mitiq 1.0.0 was pulled from PyPI into a fresh Python 3.12 venv, not imported from a pre-existing environment shared with the authors. Cirq 1.6.1 likewise fresh.
2. **Specific benchmark reproduced, not quoted.** The Fig 5 toy circuit `H;X;CNOT` was rebuilt from the paper's description, the depolarizing noise model was re-applied per-gate, and the observable `⟨00|ρ|00⟩` was re-derived. The unmitigated value came out at **0.062222 vs paper 0.0622 — matching to 4 significant figures**. This is not a "quoted" reproduction; it is a genuine re-derivation.
3. **No-mitigation baseline present in every result table.** PEC and ZNE numbers are always shown alongside the unmitigated baseline. Improvement factors (6.4× for PEC, 1.77× for ZNE) are computed explicitly.
4. **Monte-Carlo variance characterized.** PEC is a stochastic estimator; 10 seeds were run (paper reports one). Every seed beat unmitigated; the paper's exact 0.0071 lies within the seed distribution.

## Weaknesses (genuine limitations to acknowledge)

### 1. CDR primitive not benchmarked
Mitiq advertises **three** headline error-mitigation techniques: ZNE, PEC, **CDR** (Clifford data regression). This replication reproduced ZNE and PEC quantitatively; CDR was checked only for package presence. A stronger replication would add `execute_with_cdr` on the same benchmark and report accuracy/cost against ZNE and PEC. This is the single biggest gap.

### 2. H₂ VQE surface (Fig 4) not independently run
Claim C4 (ZNE reduces L2 error on H₂ VQE energy surface) was marked "covered qualitatively by C3" because it uses the same ZNE code path. This is a defensible shortcut but not equivalent to a positive reproduction — the H₂ chemistry surface has its own numerical signature (bond-length sweep, ~1 kcal/mol chemistry accuracy threshold, active-space choice) that a 20-circuit RB benchmark does not verify. If the H₂ energy at, say, R=0.74 Å came out wrong under ZNE, C3 would not have caught it.

### 3. Hardware runs (Fig 3) untested
Claim C5 (real IBM/Rigetti hardware) was skipped entirely — no QPU access. All numbers here are from a noise-model-plus-density-matrix simulator. Real-device effects (crosstalk, drift, T1/T2 decay, calibration age, queue latency) were not encountered. This is the standard hardware-access gap in academic replications but must be flagged: **the paper's hardware plots are unverified by this work.**

### 4. Only Cirq backend exercised
The paper advertises Qiskit / pyQuil / Braket / Cirq support (part of C5). Only the Cirq path was tested. The Mitiq → Qiskit converter is a separate code route that could silently regress without affecting Cirq numbers. A stronger replication would run the same Fig 5 benchmark through qiskit-aer.

### 5. PDF vision tooling unavailable
At replication time Anthropic PDF vision credits were exhausted. Paper numerical values were extracted from the ar5iv HTML rendering (verbatim excerpt saved in `report/evidence/`). This is a reliable secondary source but one step removed from the PDF of record. If the ar5iv rendering had a transcription error in a numeric value, this replication would inherit it.

### 6. LLM judge is single-model, not consensus
The primary judge model `argo:claude-opus-4.8` hit a proxy response-parse bug; the run fell back to `argo:gpt-5.2`. The REPLICATED verdict is therefore based on one model's judgment, not multi-model consensus. Judge transcript in `report/evidence/evidence_llm_judge.txt`.

### 7. Toy-scale compute only
All simulations ran on CherryRd's CPU in ~2 minutes total. The mitigation code paths were exercised but not stress-tested at circuit sizes where PEC's exponential sample overhead or ZNE's extrapolation instability would become numerically dominant. Whether Mitiq's primitives remain accurate at, say, 6-qubit deep circuits is not addressed here.

## Not weaknesses (things that look bad but are fine)

- **Seed averaging PEC over 10 runs.** The paper reports one realization; averaging over seeds is a strictly stronger check because it verifies the estimator's distribution contains the paper's value, not just that a single lucky seed matched.
- **Free Argo proxy for the judge.** Standing project policy is free endpoints only; not a limitation, an intentional cost constraint.
- **~2 minute runtime.** Fig 5 is a 3-gate circuit; there is no room for the runtime to be shorter without losing the mitigation code exercise.

## Bottom line
REPLICATED is honest for the ZNE + PEC quantitative core of the paper. It is **not** a claim that the entire paper — CDR, all backends, all hardware plots, H₂ VQE surface — has been verified. The unverified portions are named above so downstream consumers can decide whether the replication answers their question.
