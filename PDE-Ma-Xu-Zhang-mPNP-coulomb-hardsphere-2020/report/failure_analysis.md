# Failure Analysis — Ma-Xu-Zhang mPNP replication

An honest inventory of what went wrong, what stayed unresolved, and what the workflow should have caught earlier.

## 1. Duplicate work (workflow failure)

**What happened.** After completing this replication I discovered a prior independent replication of the *same paper* by "Ollie" from 2026-05-28, at `~/Dropbox/REPLICATE-PROJECT/PDE-replications/modified-pnp/`. The earlier work covers all four sub-models (MF/SC/LC/LS), including the WKB Coulomb self-energy of Eq. 3.22, and reports 8/10 claims confirmed.

**Why the ABORT check missed it.** The brief's ABORT check ran `ls ~/Dropbox/REPLICATE-PROJECT/ | grep -i ...` — a match against *direct children* of the project root. The prior replication lives two levels deep (`PDE-replications/modified-pnp/`) and did not surface.

**Impact.** ~30 minutes of duplicated compute; no lost information (both dirs preserved). The new dir sits at the top level and does not overwrite the earlier work.

**Fix for next time.** Recursive DOI-based check before starting: `grep -R "10.1137/19M1310098" ~/Dropbox/REPLICATE-PROJECT/ -l` would have caught this. The wave-integration layer should de-duplicate at the paper level (DOI).

## 2. LC/LS not implemented (scope limitation, deliberate but material)

**What happened.** The WKB Coulomb self-energy analytic solution of Eq. 3.22 is a semi-infinite integral of Bessel-function combinations. I judged it not feasible inside a 30-minute session and deferred it.

**Impact.** The paper's headline scientific claims (C5–C7 in REPORT.md §2) — that the *full LS* model quantitatively matches MC/MD data at c_0 = 90 mM, L = 5 nm, high HS packing a = 0.35 — remain untested by this replication. The REPLICATED verdict certifies only the MFMT + MF + SC prerequisites.

**Fix for next time.** Explicitly flag in the pre-flight that the paper's key physical claims require the LC/LS ingredients and either (a) budget the multi-hour effort to implement Eq. 3.22, or (b) reuse Ollie's earlier LC/LS implementation and layer only the fresh cross-check on top.

## 3. Units gap I could not close (partial failure)

**What happened.** The paper's Fig. 4.1(a) inset shows the bulk-fluid μ_hs around 0.9, while our analytic Carnahan–Starling target at the same packing fraction η = 0.028274 is 0.239. The paper's dimensionless prefactor ν = 1/(8π q ε^2) rescales weighted densities in the free-energy density with additional prefactors, but I could not fully reconcile the ~3.8× gap without the paper's supplementary material.

**Impact.** The C1 convergence-rate test is scale-invariant and unaffected, but the "I fully understand the paper's non-dimensionalisation" story has a real hole. A reader who expects the absolute μ_hs values to line up will be confused.

**Fix for next time.** Track down the paper's supplementary discussion of the ν prefactor, or contact the authors, or reproduce the exact form of Eq. 2.26–2.30 in the paper's normalisation before comparing absolute values.

## 4. Opus 4.7 fallback (infrastructure hiccup, gracefully handled)

**What happened.** The primary LLM-judge model `argo:claude-opus-4.7` returned HTTP 502 during this run. The fallback chain triggered and `argo:claude-sonnet-4.6` delivered the final verdict (recorded in `evidence/llm_judge_model.txt`).

**Impact.** Verdict is single-model, single-shot from Sonnet 4.6 rather than the intended Opus 4.7. The numerical evidence is strong enough that I stand behind the REPLICATED label, but the meta-observation that "one LLM call became the arbitrator" is a workflow weakness.

**Fix for next time.** Either re-run the judge on Opus 4.7 after transient 502s clear, or default to a two-model consensus (Opus + Sonnet) whose disagreement escalates to a human.

## 5. Time-dependent scheme untested (scope, honest)

**What happened.** The paper's Eq. 3.27 is a time-dependent discretisation whose mass conservation (C8) I could have tested but did not — the pre-flight plan targeted only the equilibrium C1/C2/C3 claims.

**Impact.** The paper's *transient* mPNP behaviour and the mass-conservation guarantee remain unreplicated here. Ollie's earlier replication may or may not cover this.

**Fix for next time.** Add C8 to the second-tier claim list. Mass conservation is a mechanical but non-trivial test: run the Eq. 3.27 update from a symmetric IC, integrate ∫ c_+ dx and ∫ c_- dx per step, and confirm drift below 10^-10 over 10^4 steps.

## 6. Stress-regime coverage (not attempted)

**What happened.** All numerical tests use the paper's moderate parameters (ε, q, a, γ, V) = (0.2, 0.3, 0.15, 1, 1). Regimes where the paper hints at numerical difficulty (large γ near 1 with strong surface charge 0.02 C/m² and small L ~ 2 nm) were not exercised.

**Impact.** No stress-test of the Newton solver's robustness or the SC nested Picard's convergence rate in stiff regimes. Reported residuals |R| = 3.5×10^-12 (MF) and μ_rel_diff = 8.7×10^-10 (SC) are for the friendly parameters.

**Fix for next time.** Parameter sweep over (γ, V, L) ∈ {(0.95, 2, 0.5), (0.99, 3, 0.3)} with iteration-count-to-fixed-residual and peak-c_+ error vs a fine-grid reference. See `open_questions.json` question 4 for a proposed benchmark.

## 7. Summary

| # | Issue | Category | Severity | Corrective action |
|---|-------|----------|----------|-------------------|
| 1 | Duplicate-work ABORT check missed prior Ollie replication | workflow | high | recursive DOI grep in pre-flight |
| 2 | LC/LS not implemented (WKB integral) | scope | high | budget multi-hour effort or reuse Ollie's LC/LS |
| 3 | Units gap between paper's Fig 4.1(a) inset and CS analytic | correctness/understanding | medium | reconcile ν prefactor from supplementary |
| 4 | Opus 4.7 fell back to Sonnet 4.6 for verdict | infra | low | two-model consensus |
| 5 | Time-dependent Eq. 3.27 and mass conservation untested | scope | medium | add C8 to second-tier claim list |
| 6 | Stress-regime coverage (large γ, high V, small L) not attempted | scope | medium | parameter sweep with fine-grid reference |

Nothing in this list changes the REPLICATED verdict for the three tested claims (C1, C2, C3), but all of it should inform the next mPNP replication or the wave-integration layer's handling of this paper.
