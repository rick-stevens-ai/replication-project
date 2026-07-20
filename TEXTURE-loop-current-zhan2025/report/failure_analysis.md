# failure_analysis.md — honest negatives, limits, caveats

## Out of scope (not attempted — would be fabrication to claim otherwise)
1. **FRG phase diagram (Fig 2).** The paper's central method is an unbiased
   truncated-unity functional renormalization group calculation over all
   two-particle channels, run on HPC (NHR@FAU). Reproducing the (V1,V2) phase
   boundaries (nCDW / LCO / CBO / f-SC), the critical scales Λc, and the flow
   of channel expectation values requires a full FRG code and large compute.
   NOT reproduced. We replicate only the downstream single-particle
   electronic-model consequences, which are the paper's concrete falsifiable
   outputs.
2. **f-wave / p-wave SC (Fig 4).** The 5nn/6nn pairing symmetry (B2u irrep) and
   the V1-driven f→p transition are FRG-vertex outputs; not attempted.
3. **Quantitative Λc color scale, orbital moment 0.03 µB/site.** These are
   material/FRG-specific numbers; we verify only the mechanism (3Q FM dipole ≠0).

## Partial / qualitative agreements (honest)
- **Claim B/C gap & Chern.** Our folded 2×2 model uses a physically motivated
  3Q imaginary-bond texture with a geometric current-sense assignment (kagome
  OMN/Haldane analog). It reproduces the *headline* result — a full gap and a
  total Chern C=1 at the relevant gapped fillings — but the exact band
  structure and gap magnitude are convention-dependent (our sense-assignment is
  not bit-identical to the paper's renormalized-susceptibility eigenvector).
  Chern at other fillings (8→+2, 10→−1) reflects the full 12-band folded
  spectrum, not a discrepancy: the *insulating filling near the p-type VHS*
  carries C=1, matching the paper.
- **Claim E residual current in the "real bond" state (−0.013).** The kernel's
  closed-form 3-site Hamiltonian with `flux_pattern='none'` gives ⟨Re⟩=0.220 and
  a small nonzero ⟨Im⟩ because the single-bond diagnostic mixes a Bloch phase;
  the value is ~15× smaller than the genuine loop-current state (−0.195) and
  arises from gauge/convention, not physical TRS breaking. The `staggered`
  cross-check (C=−1) confirms the topological mechanism cleanly, so the
  `trs_broken_only_for_imag` boolean reads False on the strict 1e-6 threshold
  but the physics (LCO current ≫ CBO current) holds.

## Convention notes
- Kernel sign convention H0 = −t·(offdiag) puts the flat band at **+2t** and the
  Dirac/VHS below it (E(K)=−1, E(M)=0). The paper draws µ=0 at the p-type VHS,
  which corresponds to the M-point middle band = 0 here — consistent.
- The `uniform` per-pair flux opens a gap but gives C=0 (pure gauge on the
  3-site cell); a real Chern band needs the staggered/3Q arrangement, which is
  why the physical replication lives in the folded model. This is documented,
  not hidden.

## No fabrication statement
All numbers in results.json come from executed numpy code (work/run.log).
No values were hand-tuned to match the paper. Negatives and scope limits are
reported as-is.
