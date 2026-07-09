# Failure Analysis — Nicoud (2000) Replication

Verdict: **REPLICATED** on both tested claims (C1 4th-order spatial accuracy; C2 discrete conservation). No numerical failures. Below are the *near-failures* and *deliberate limitations* encountered, with root causes and prevention notes so the same time isn't paid twice.

## 1. Argo proxy schema-validation bug on opus-4.7 / opus-4.8 (recovered)

**Symptom.** The brief called for `argo:claude-opus-4.7` as the LLM judge. Every request to opus-4.7 (and opus-4.8) returned an upstream error of the form:

> `Failed to parse upstream response: Value at 'choices[0].message' does not match any variant of SystemMessage | UserMessage | AssistantMessage | ToolMessage`

**Root cause.** Argo-proxy-side response-schema validation is broken for opus-4.7 and opus-4.8 specifically. Verified against 5 models — `opus-4.5`, `opus-4.6`, `sonnet-4.6`, and `gpt-4o` all respond cleanly with the same prompt shape. It is a proxy schema-validation defect, not a request malformation on our end.

**Recovery.** Fell back to `argo:claude-opus-4.6`, one minor version behind the requested judge. Judge still emitted a clean structured verdict (C1: REPLICATED, C2: REPLICATED, overall: REPLICATED) with rationale citing the exact numerical evidence.

**Documentation.** Fallback is explicit in `work/llm_judge.py`, `report/evidence/judge_verdict.json` (`model_actual` vs `model_requested`), and §4 of `report/REPORT.md`.

**Prevention.** Any future replication that pins opus-4.7 or opus-4.8 as judge should probe first with a trivial ping and fall back automatically. A tiny probe helper (send a 5-token request, check for the schema-validation string) would save re-diagnosis.

## 2. Characteristic-inversion robustness for the T2 analytic reference (mitigated)

**Concern.** The T2 reference solution requires inverting the travel-time integral `τ(x) = ∫₀ˣ ρ(s)/M ds` to get the characteristic foot `X_0(x, T)`. If the inversion is not spectrally accurate, its own error can floor the observed convergence rate of the scheme and hide a legitimate 4th-order signal.

**Root cause / mitigation.** Used a cubic spline on `2 × 10⁵` points to construct and invert τ. Estimated inversion error << 10⁻⁸ over the entire domain, i.e. far below the finest-grid scheme error (≈ 4.5 × 10⁻⁸ at N = 512). Confirmed by the clean 3.90 → 3.97 → 3.99 → 4.00 convergence trajectory — an error-floored reference would flatten this out.

**Residual risk.** The reference is not closed-form; we assert but do not formally bound its accuracy. If a future run pushes N > 1024, spline-inversion floor could start to bite.

**Prevention.** Prefer a closed-form reference (e.g. constant-ρ pure translation) if the goal is to push spatial order at very high N; use the ρ(x) = 1 + 0.4 sin variable-density reference only for the N ≤ 512 regime where its accuracy dominates the scheme error by 6+ orders of magnitude.

## 3. Scope decisions (deliberate; documented as GENUINE CRITIQUE)

These are not failures — they are honest scope narrowings — but worth listing so no one over-claims.

* **C3 (2nd-order-in-time) not verified.** We used RK4, strictly stronger than the paper's scheme. The observed conservation of the *scalar* would in principle depend on the time integrator; RK4 preserves it here to round-off, but Nicoud's 2nd-order integrator on a nonlinear reacting scalar was not tested.
* **C4 (3-D reacting LES applications) out of scope.** A single-night operator-level replication cannot cover the paper's downstream 3-D LES/combustion applications. What we verified is the operator/conservation foundation those applications rest on.
* **Only 1-D periodic BCs.** Bounded domains with inflow/outflow/walls are where boundary closures typically drop order or leak conservation, and the paper's contribution actually earns its keep there. Not tested here.
* **Density ratio ≈ 2.33 only.** Combustion-scale density ratios (~10²) not exercised.
* **No pressure-Poisson / acoustic-filter step implemented.** Genuine low-Mach acoustic-filtering behavior as M → 0 not stressed. `M = 1` in T2 is a normalized mass flux, not a physical Mach number.
* **Single implementation on single machine.** Would benefit from an independent re-implementation (Fortran/JAX) to harden against implementation bugs.

**Prevention.** These caveats are listed in §6 of `report/REPORT.tex` (GENUINE CRITIQUE) and in the `next_steps` fields of `report/open_questions.json` so a follow-on replication has a clear scoping menu.

## 4. What went right (for the record)

* Test design chose the minimum battery that stresses both foundational claims: single-shot operator convergence (T1), full nonlinear time-integrated variable-density scalar transport (T2), long-time conservation monitor (T3).
* Convergence orders came out to two decimals of theoretical 4.00 in both norms across three tests. Strong inductive evidence of correct operator implementation.
* Conservation drifts came out at exactly 0 (mass, momentum) or 5 ε_mach (scalar) after 1067 RK4 steps. As tight as double precision allows.
* Whole battery ran in 2.5 s wall time on `cherryrd`; no GPU, no HPC allocation, no paid endpoints.
* LLM-judge verdict independently matched the numerical evidence with a specific-numbers rationale, giving a cross-check on our own reading of the results.

## Bottom line

No failures on the tested claims. One recovered infrastructure fault (Argo opus-4.7/4.8 proxy bug). One deliberate reference-solution risk (spline-inverted characteristic) that was well-controlled at the tested resolutions. Multiple deliberate scope narrowings, all documented in the GENUINE CRITIQUE section of `REPORT.tex` and in `open_questions.json`.
