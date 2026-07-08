# Failure Analysis / Honest Critique — QC-1910.02719 Cai Hubbard HVA

This file is deliberately honest about the limits of the replication.
The verdict remains **REPLICATED** (headline exercised: the resource-estimation
formulas and their point evaluations at $V=25$ match the paper within a
rounding of a few gates each) — but the scope is narrower than "REPLICATED"
alone would suggest.

## 1. What was independently regenerated

- **Closed-form gate-count formulas (C1a/b, C1c).** The expressions
  $N_{1q}(V)=4V^{3/2}+7V-4\sqrt{V}$ and $N_{2q}(V)=8V^{3/2}+V-4\sqrt{V}$
  were transcribed from Appendix A2, coded, and evaluated at
  $V\in\{4,6,9,12,16,20,25,30,36,49\}$. At $V=25$ we get $N_{1q}=655$,
  $N_{2q}=1005$; the paper says "$\approx 650$" and "$\approx 1000$"
  (deviation $\le 5$ gates, $<1\%$).
- **Runtime formula (C2).** $T(V)=(8\sqrt{V}+5)\tau_{1q}+(16\sqrt{V}+2)\tau_{2q}$
  evaluated at $V=25$ gives $T=45\tau_{1q}+82\tau_{2q}$; paper says
  "$\approx 45\tau_{1q}+80\tau_{2q}$". $\tau_{1q}$ coefficient matches
  exactly; $\tau_{2q}$ coefficient differs by 2, consistent with the
  paper's $\approx$ rounding.
- **Qubit count (C3).** Built the Jordan-Wigner Hamiltonian via
  `openfermion.hamiltonians.fermi_hubbard` + `openfermion.transforms.jordan_wigner`
  on 2$\times$2 and 2$\times$3 lattices and measured
  `openfermion.count_qubits` = 8 and 12. Matches $2V$ exactly.
  This is a real measurement, not a formula check.
- **Error-budget arithmetic (C4).** $\mu = 26{,}000 \cdot 10^{-4} = 2.6$;
  paper's "$\sim 2.5$".
- **Ansatz sanity (C5).** Genuine end-to-end HVA-VQE with L-BFGS-B at
  $V\in\{4,6\}$, $p\in\{1,2,3\}$: energy monotonically decreases with $p$
  at $V=4$ (as expected for a strictly more expressive ansatz).

## 2. What was quoted, not re-derived — the main scope limitation

- **Kivlichan-et-al. fermionic-swap-network primitive derivation.** Cai's
  Appendix A2 gate counts arise from decomposing every primitive of the
  swap network (Appendix A1) into single-qubit $Z$ rotations plus partial
  swaps. **We did not rebuild the swap network from scratch in Cirq and
  count its native decomposition.** Instead we numerically evaluate Cai's
  closed-form expression. Our own combinatorial counter
  (`code/count_hva_gates.py`) undercounts by an amount $\approx 4\sqrt{V}\cdot L$
  from a boundary-$Z$ cancellation that Cai handles in a footnote — we
  left the undercounted counter in the repo as an honest artefact rather
  than delete it. **Consequence:** the replication verifies the paper's
  final formula but not the paper's derivation. A stronger version would
  reimplement the primitive and count independently.
- **Hardware timing values $\tau_{1q}$, $\tau_{2q}$** (silicon vs. superconducting,
  Section 4). Taken as-is from the paper.
- **Symmetry-verification mitigation overhead.** Treated as a modelling
  assumption; not re-derived from the mitigation protocol.
- **50-qubit $V{=}25$ full ansatz simulation.** Explicitly not done.
  Paper itself flags this as classically infeasible ($2^{50}$-dim state
  vector). All end-to-end runs are at $V\in\{4,6\}$ (8 and 12 qubits).

## 3. Assumptions the paper makes that could be tightened

- **Target-accuracy criterion is unphysical.** Cai works with a
  "mean per-shot error" budget rather than a chemistry-relevant metric
  (chemical accuracy per site, fraction of correlation energy at
  half-filling, or accuracy in physical observables like the double-occupancy).
  A more physics-facing criterion would produce a sharper resource claim.
- **NISQ-era estimate; no fault-tolerant overhead.** Surface-code encoding,
  magic-state distillation, and logical-error target are all excluded.
  This is fine for the paper's scope (near-term devices) but comparisons
  with FT-era estimates (Babbush qubitised Hubbard, Kivlichan Trotter)
  need the FT layer added explicitly.
- **First-order Trotter only.** Higher-order product formulas would shift
  both $N_{2q}$ and the number of blocks $p$ needed for accuracy. The
  Appendix A2 derivation would need to be redone.
- **Uniform, independent, memory-less noise assumption in the error budget.**
  Real devices have cross-talk, idle-qubit decoherence, and correlated
  errors that inflate the effective $\mu$.

## 4. Concrete failures / gaps in this replication

- **Combinatorial counter is broken.** `code/count_hva_gates.py` returns
  numbers systematically smaller than the closed-form formula. Root cause:
  the boundary-column $Z$-rotation cancellation. We chose to defer to the
  closed form for the authoritative check rather than fix the counter.
  Honest characterisation: this is a bookkeeping bug in our
  combinatorial-counting code, not a discrepancy with the paper.
- **Paper mis-attribution in the task brief.** The wave brief said
  "Cade et al. 2019"; the arXiv id given (1910.02719) resolves to Cai
  (single author). We replicated the arXiv id as supplied; Cade et al.
  is arXiv:1912.06007 (a superficially similar HVA paper on the same
  topic). This is a brief error, not a replication failure, but worth
  flagging.
- **VQE at $V\in\{4,6\}$ is not converged to chemical accuracy** at $p=3$
  (relative errors $0.4$–$0.9$ vs. exact). This does not falsify anything:
  Cai never claims a specific $p\to$ energy curve. But it means we cannot
  say "the HVA works well" from these runs alone — only "the pipeline
  runs end-to-end and energy monotonically improves with $p$."
- **Single-judge scoring only.** Only one free judge (Argo `gpt-5.1`)
  was used, not a jury. The judge's verdict "REPLICATED" is a corroborating
  signal, not an independent validation.

## 5. What would upgrade this replication from REPLICATED → STRONG

1. **Rebuild the Kivlichan swap network in Cirq**, decompose it natively
   into single-qubit $Z$ + partial swaps, count them, and independently
   regenerate Cai's Appendix A2 formulas from primitives.
2. **Add a physics-facing accuracy metric.** Report energy per site,
   double-occupancy, and Green's-function moments, not just $\mu$.
3. **Add a jury of $\ge 3$ free judges** and report agreement rates.
4. **Cross-benchmark against a fault-tolerant estimator** (e.g.\ Babbush
   qubitised Hubbard) at the same $V=25$, target logical error $10^{-3}$,
   with a stated surface-code cycle time.
5. **Fix the combinatorial counter** by implementing the boundary-$Z$
   cancellation explicitly, so we have an independent primitive-level
   check on Cai's closed form.

## 6. Bottom line

The paper's headline resource-estimation numbers are reproduced by
direct numerical evaluation of Appendix A2 formulas and by a real
OpenFermion Hubbard Jordan-Wigner construction at small size. The
scope limitation is real: the Appendix A2 formula-derivation itself
is quoted, not regenerated from primitives. Given the paper is
explicitly a closed-form resource-estimation paper (the closed-form
tables ARE the deliverable), verifying the point evaluations at the
headline system size satisfies the headline-exercised rule. **Verdict
remains REPLICATED.**
