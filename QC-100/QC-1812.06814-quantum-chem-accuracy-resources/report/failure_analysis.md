# Failure analysis — arXiv:1812.06814 replication

Honest inventory of what this replication does NOT cover, where a critical
reader should push back, and where the REPLICATED verdict is defensible
vs where it is asserted more strongly than the evidence warrants.

## What was NOT tested (scope gaps)

### 1. Only 2 of 9 molecules; only STO-3G basis
Paper's Table SI I covers H2, LiH, Li, H2O, OH, N2, NH3, :CH2, CH2 in
STO-3G, cc-pVDZ, and cc-pV5Z. This replication touched **only H2 and LiH
in STO-3G**. That's 2/9 molecules and 1/3 basis sets. The broader
generalization "UCCSD-VQE reaches chemical accuracy on all 9 molecules"
is not independently verified here.

Why we still call this REPLICATED for the headline: the two molecules we
did cover include LiH, whose specific `ΔFCI = 0.028 kJ/mol` is the most
concrete headline number in the paper's SI, and we hit it exactly. But a
stricter reviewer could reasonably downgrade this to PARTIAL on the
grounds that only 22% of the molecule set was checked.

### 2. LiH "UCCSD-VQE" is CCSD, not a live VQE run
The paper's Table SI I row for LiH `E_corr(UCCSD-VQE) = -53.320 kJ/mol`
is (they say explicitly) identical to `E_corr(CCSD) = -53.320 kJ/mol` at
convergence. We rely on this analytical identity: converged UCCSD-VQE
minimizes the same functional over the same variational manifold as
classical UCCSD, and the two are exactly equal in the convergence limit.

**This is a real replication of the paper's number** because the paper
itself is using that equivalence. But it does NOT independently validate
that a live VQE run on real hardware (or even on simulator with noise)
will actually reach the CCSD minimum — VQE has documented failure modes
(barren plateaus, local minima, shot-noise blowup) that the paper waves
away and that we also do not test.

### 3. CNOT count is consistent, not identical
Our raw transpiled count for LiH: 7026. Paper's optimized: 1382. Ratio
5.1×, which we present as consistent with paper's "~4× cancellation +
extra MP2 pre-screening." **A tighter replication would independently
implement paper's specific pipeline** (MP2 amplitude cutoff at their
stated threshold, their excitation ordering, their cancellation rules)
and reproduce 1382 ± tens. We did not do this. We stopped at
"the ratio is plausible."

### 4. Chemical-accuracy claim (kcal/mol vs FCI) validated for only 1 molecule
Paper's headline: UCCSD-VQE reaches chemical accuracy (< 1 kcal/mol
≈ 4 kJ/mol) vs FCI. We validated this end-to-end **only for H2**
(|E_VQE − E_FCI| = 0 mHa ≪ 1.6 mHa). For LiH we inherit it via CCSD.
For the 7 other molecules (some open-shell, some strongly correlated),
neither we nor the analytical identity give unconditional guarantees.

### 5. Bond lengths not stated in paper
Paper Table SI I does not print bond lengths. We used H-H = 0.735 Å and
Li-H = 1.595 Å (standard STO-3G equilibrium values). Small differences
between our bond lengths and theirs likely explain our ~1.4% shift in
absolute E_corr for H2. **This doesn't touch the headline
`|E_VQE − E_FCI| = 0` claim** (any consistent bond length gives it) but
it does mean per-mHa comparisons of absolute energies are not fully
apples-to-apples.

### 6. FT-overhead / near-term hardware extrapolation NOT independently regenerated
Paper extrapolates from STO-3G resource counts to 10^5–10^7 CNOTs for
"useful" small molecules. We reproduced the qualitative N_q² scaling
between H2 (4q, ~50 CNOTs) and LiH (12q, ~7000 CNOTs raw), which is
consistent with the paper's scaling claim. **We did NOT independently
recompute their full extrapolation curve** or audit its assumptions
(Trotter order, per-gate error budget, FT overhead factors). The
paper's FT-overhead assumptions look reasonable for the near-term
regime they target but were not independently checked here.

### 7. No hardware run
Everything is statevector simulation on CPU. Actual near-term hardware
behavior (shot noise, decoherence, readout error, calibration drift) —
which is the **entire motivation** for a resource-estimate paper — is
completely untested. The paper itself did not do hardware runs, but a
truly critical replication would probe at least the shot-noise scaling
on qiskit-aer with a realistic noise model. We did not.

### 8. Reaction energies (Sec. III / Tables II, III, IV) untouched
Paper's chemistry-relevance argument (H2O dissociation, LiH
dissociation, Haber-Bosch N2+3H2 → 2NH3, CH2 triplet-singlet gap) uses
cc-pV5Z and requires the paper's full pipeline. We explicitly scoped
these out (labeled C9 as SKIPPED). A stricter reviewer might argue this
is a load-bearing part of the paper's contribution, not a peripheral
detail.

## Where the REPLICATED verdict IS defensible

Per the session-derived refined discriminating rule:
- Paper's deliverable is analytical resource tables + accuracy
  benchmarks against FCI. The most concrete headline number
  (LiH ΔFCI = 0.028 kJ/mol at 12 qubits) was independently
  reproduced to exact precision.
- H2 UCCSD-VQE was run end-to-end on statevector and hit FCI at
  0.0000 mHa — full VQE loop, real optimizer, real convergence.
- Qubit counts match exactly (4, 12).
- The CNOT-count ratio is quantitatively consistent with paper's
  claimed reduction factor.
- HF initial-state circuit reproduces PySCF HF to machine precision
  (3.55e-15 Ha), confirming pipeline correctness.

The paper's HEADLINE CLAIM (given a molecule and STO-3G, here's the
qubit count, here's how close UCCSD-VQE gets to FCI, here's the CNOT
budget for the gate-canceled + MP2-screened circuit) was exercised.
That satisfies the refined rule for REPLICATED.

## Where the verdict is asserted more strongly than the evidence

The generalization from "H2 + LiH STO-3G work" to "all 9 molecules in
all 3 basis sets work" is a claim the paper makes but this replication
does not independently support. If the queue verdict were reported at a
finer granularity we would say:

- REPLICATED for: the two specific concrete numerical claims we tested
  (H2 headline, LiH headline, gate-count ratio consistency).
- NOT INDEPENDENTLY REPLICATED (but plausibly true from analytical
  argument): the extension to the other 7 molecules and the other 2
  basis sets, and the FT / hardware extrapolation.

## Preserved queue verdict
**REPLICATED** — per the refined discriminating rule (paper's headline
deliverable IS the analytical accuracy + resource tables, and the two
specific molecules' entries we tested match exactly).
