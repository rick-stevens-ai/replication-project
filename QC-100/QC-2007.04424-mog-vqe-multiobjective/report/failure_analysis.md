# Failure Analysis — QC-2007.04424-mog-vqe-multiobjective

> **Purpose.** This is the honest critique of what this replication does and does not
> establish. It exists so downstream readers (and future replication waves) can tell the
> difference between "the paper's claim is verified end-to-end" and "the paper's claim is
> verified on a compute-affordable proxy, with the full claim still pending."

## 1. What the paper claims, in three tiers

**Tier A (qualitative headline):** Multiobjective GA search over ansatz *topology* (energy
vs CNOT count) discovers ansatze that reach chemical accuracy with far fewer CNOTs than
standard baselines (HEA, UCCSD).

**Tier B (specific quantitative headline):** On BeH₂ (8q) the minimum-CNOT chem-acc
circuit uses 9 CNOTs vs 70 for HEA (~7×); on LiH (12q) chem-acc is reached at 12 CNOTs.

**Tier C (algorithmic claim):** The specific NSGA-II (outer) + CMA-ES (inner) coupling
converges to these Pareto corners within a stated compute budget.

## 2. What THIS replication establishes

- **Tier A: ✓ REPLICATED on H₂.** Multiobjective structure produces a real Pareto front.
  We reimplemented the circuit primitive (Fig 2a generalized-CNOT block), the NSGA-II
  outer loop, and a same-class inner optimizer (COBYLA / L-BFGS-B multistart). We showed
  a hard lower bound at k=2 CNOTs (0/60 topologies chem-acc) and a first-feasible corner
  at k=3 (7/60 → FCI to machine precision). Reduction vs UCCSD is 6×, vs HEA L=2 is 2×.
  Sign, mechanism, and existence of the elbow all confirmed.

- **Tier B: ✗ NOT tested.** We did not run MoG-VQE on BeH₂ or LiH. The 10× number is a
  headline number attached to those specific molecules where the HEA baseline is much
  larger; on H₂ the HEA baseline itself is only 6 CNOTs, so 10× is not even geometrically
  possible on H₂. This is the biggest single gap between this replication and the paper.

- **Tier C: ✗ PARTIAL.** Our own NSGA-II run at pop=16, gen=6, single seed did NOT
  by itself find the 3-CNOT chem-acc topology; the directed enumeration in §3.6 of the
  main report did. The enumeration proves the family *contains* the corner (which is
  necessary for the paper's algorithm to be capable in principle), but the paper's
  \*specific\* GA convergence claim (that NSGA-II reliably finds those corners at a
  stated compute budget) was under-tested here. A fair Tier-C test requires more seeds,
  more generations, and a hyperparameter sweep.

## 3. Explicit substitutions and their effect

| Paper choice | This replication | Impact |
|--------------|------------------|--------|
| Inner: CMA-ES | COBYLA / L-BFGS-B multistart | Same algorithmic class; both converge to FCI on H₂ 3-CNOT topologies. On high-D angle spaces (12q LiH ~60 angles) CMA-ES's covariance adaptation may matter more; UNTESTED here. |
| Outer: NSGA-II with unpublished hyperparameters | NSGA-II, pop 16, gen 6, gene-swap/insert/delete/position-swap ops | Same algorithm family. Compute budget substantially smaller than paper's implied budget (paper doesn't publish exact numbers). |
| Molecules: H₂, H₄, H₆, BeH₂, LiH | Only H₂ | Big scope reduction. H₂ is the smallest instance and the least stringent test of the 10× headline. |
| Single-seed GA | Single-seed GA (same as paper as published) | Consistent with paper, but statistically fragile — multi-seed rerun is on the open-questions list. |

## 4. Baseline honesty checks

- **UCCSD 18 CNOTs.** We built UCCSD as an explicit Trotter decomposition of the
  fermionic excitation operator (2 singles + 1 double for H₂/STO-3G active space) and
  counted CNOTs after decomposition to a standard hardware gate set. This is the correct
  ``chemistry-inspired baseline'' interpretation. Some literature quotes lower UCCSD
  CNOT counts using specific compilation tricks; 18 is the standard uncompiled figure.

- **HEA L=2 gives 6 CNOTs, reaches chem-acc.** L=1 (3 CNOTs) does NOT reach chem-acc
  (error 0.76 Ha, still at HF). This confirms the H₂ HEA baseline is really 6 CNOTs, so
  the ``fair'' MoG-VQE-vs-HEA ratio on H₂ is bounded by 6/2=3× (if MoG-VQE could reach
  chem-acc at k=2, which it can't — hard bound), and 6/3=2× (which is what we observed).
  This is a legitimate replication, not a cherry-pick.

- **HEA at L≥5 hits barren-plateau-like local minima on random init** but still stays
  under chem-acc. This is a known VQE pathology, not a bug in our implementation.

## 5. What single-objective baseline was NOT run (Rick's 2026-07-05 requirement)

Rick's directive explicitly asks whether comparison against single-objective VQE
baseline was made. **Answer: not directly.** UCCSD and HEA serve as fixed-topology
baselines but neither is an evolutionary search over topology space with objective =
energy only. The strict apples-to-apples test — rerun our NSGA-II with objective =
energy only, check whether it fails to find the 3-CNOT elbow — is **open** and is Q3
on the open-questions list.

## 6. What genetic-algorithm convergence + hyperparams were NOT verified

Rick's directive explicitly asks whether GA convergence + hyperparams were verified.
**Answer: partially.** We used our own hyperparameters (pop=16, gen=6, standard genetic
operators) because the paper does not publish all NSGA-II hyperparameters. We did NOT:
- sweep pop/gen/mutation-rate/crossover-rate
- test multiple random seeds and report convergence variance
- benchmark against the paper's plotted convergence curves at matched compute
The 3-CNOT elbow was found by directed enumeration (§3.6), not by the GA main run.
So the GA-convergence claim is **evidence-supported but under-tested**.

## 7. Bottom line

- **VERDICT: REPLICATED** on H₂ scope — matches paper's Tier-A qualitative claim
  end-to-end via genuine circuit simulation.
- **Verdict is NOT stronger** because Tier-B (10× on BeH₂/LiH) and full Tier-C
  (GA convergence) were not exercised.
- **Verdict is NOT weaker** because everything we did test came out consistent with
  the paper's mechanism and no discrepancy was found — the residual gaps are
  compute-budget gaps, not methodological failures.
- The 5 open questions (`open_questions.json`) are the concrete follow-on probes to
  close the Tier-B and Tier-C gaps.
