# Failure Analysis: feng2021 replication

**Verdict: PARTIAL** — qualitative claim replicated, quantitative energetics not matched.

## What matched (successes)
| Claim | Paper | This work | Status |
|---|---|---|---|
| CFP is lowest-energy 2×2 order at λ=0.3 | yes | yes (E=−2.6770 t/cell, lowest) | ✅ MATCH |
| CFP breaks time-reversal symmetry | yes (Fig.1c) | yes (only order with complex H) | ✅ MATCH |
| vCDW & CBO preserve T | yes (Fig.1c) | yes (real H both) | ✅ MATCH |
| CFP current conservation at each site | required | max net current ~8e-16 | ✅ MATCH |
| CFP is loop-current (imaginary bond) order | yes (Eq.9) | mean \|bond current\| = 0.0158 ≠ 0 | ✅ MATCH |

## What did not match (discrepancies)
| Quantity | Paper | This work | Ratio |
|---|---|---|---|
| E_CBO − E_CFP | 0.195 t | 0.0130 t | ~15× smaller |
| E_vCDW − E_CFP | 0.435 t | 0.0073 t | ~60× smaller |
| vCDW vs CBO ordering | CBO below vCDW | vCDW below CBO | reversed |

## Root-cause hypotheses
1. **Order-parameter normalization / amplitude convention.** The paper writes all three
   orders with the same λ but they enter the Hamiltonian through very different operators
   (onsite density vs. hopping bond vs. imaginary hopping). The relative *effective*
   coupling of an onsite λ vs a bond λ depends on coordination and the M-point Bloch
   weights; the 5-page Rapid Communication does not pin this down. A different bond-vs-onsite
   scaling would both enlarge the splittings and could flip the vCDW/CBO order — exactly the
   two discrepancies we see.
2. **Current-restoring hoppings for CFP.** The paper states "the current must conserve at
   each lattice site" and adds "the remaining terms due to current constraint" to build the
   full CFP Hamiltonian. Our construction achieves current conservation numerically
   (~1e-16) via the symmetric cos(Q·r) pattern, but the paper's explicit extra terms may
   deepen the CFP energy relative to ours, widening the gap toward 0.195 t.
3. **2×2 phase origin / folding convention.** We evaluate cos(Q·r_ij) at the bond midpoint;
   the paper uses a 4-sublabel (1,2,3,4) sub-cell convention (Fig.1a). A different origin
   redistributes the modulation among the four sub-cells and can change absolute energies
   (though a physical order parameter should be gauge-invariant — flagged as open question 4).
4. **Chemical potential at 5/4 filling.** We fix filling by counting occupied states
   (5/12·N, μ implicit). The paper tunes μ to the van Hove point; a slightly different μ
   shifts how much each order gains at the M-point saddle, affecting absolute splittings.

## Not attempted (scope-limited)
- Chern number / σ_xy of the folded CFP bands (QAH claim) — needs k-space 2×2 Bloch folding
  + FHS; deferred to next steps (open_questions.json).
- Self-consistent extended-Hubbard (U,V) derivation of λ — the paper itself defers this to
  future work.
- Real-space charge pattern (Fig.3a) and site-resolved LDOS (Fig.3b).

## Honesty note
No numbers were fabricated. All energies come from direct diagonalization in
`work/feng2021_replication.py`; raw output is in `work/feng2021_result.json` and copied to
`report/evidence/`. The qualitative winner and symmetry classification are robust; the
absolute energetics are model-convention-dependent and only partially reproduced.
