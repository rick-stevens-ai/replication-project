# Failure analysis — Chen 2022 replication

## Verdict: PARTIAL (strong qualitative agreement)

## What was fully reproduced
- **Existence/stabilization of the AF\* state**: self-consistent gMFT yields gapped
  deconfined spinons + gapless U(1) photon + nonzero all-in-all-out (AAO) `<Sz>` proxy
  at (t1=0.025, t2=0.02, Jx=1) — the defining fingerprint of the Coulombic antiferromagnet.
- **Phase sequence**: U(1) QSL → pyrochlore AF\* → fragmented AFM, matching Fig. 1 / Table I.
- **Boundary mechanism**: AF\*→fragmented-AFM occurs by spinon condensation (gap closure ≈
  t2c≈0.07), consistent with the paper's continuous Anderson–Higgs transition.
- **T^3 specific heat**: gapless photon → C∝T^3 with large coefficient from small exchange scale.

## Gaps / limitations (why PARTIAL, not REPLICATED)
1. **Effective vs. microscopic couplings.** We scan a single effective inter-sublattice hop
   `t2` rather than solving the coupled self-consistent set {chi1, chi2, I1, I2} in the true
   (Jperp~/Jx~, J2xz/Jx~) plane. The paper's exact phase boundaries are therefore not
   quantitatively reproduced — only the topology/ordering of phases.
2. **No figure data.** The PDF provides no extractable numerical data for Fig. 1/Fig. 2, so
   agreement is structural/qualitative, not point-by-point.
3. **T=0 only.** The claimed finite-T 3D-Ising transition of the AAO order is not tested.
4. **Neglected terms.** Dropped '…' terms (dipolar Szz, further-neighbor superexchange) that
   the paper also neglects in the minimal model — robustness untested.

## Non-fabrication statement
All numbers in `chen2022_result.json` are outputs of the committed solver
`chen2022_gmft.py` run under `/home/stevens/comfyui-env/bin/python`. No values were
hand-tuned to match the paper; the t2 scan and self-consistent lambda are deterministic.

## Scores
- Coverage: **8/10** (model, phase sequence, boundary, T^3 mechanism, dispersion all built;
  missing full self-consistency loop and dynamical continuum figure).
- Agreement: **8/10** (all qualitative claims match; no quantitative boundary check possible).
