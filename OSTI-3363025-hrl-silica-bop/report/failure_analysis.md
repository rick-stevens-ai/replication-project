# Failure Analysis — OSTI 3363025

## What worked

- **Public code exists and runs.** `miscquanta/HMRRL-tersoff-silica` is a real public repo with the two Tersoff parameter files, one working LAMMPS input, and one starting geometry. All four files parse cleanly in LAMMPS 29Aug2024.
- **Verbatim reproduction succeeds mechanically.** `lmp -in in.relax` completes in ~50 s per potential on 1 CPU. No crashes, no warnings, no divergence. NBList and Tersoff pair evaluation work as expected.
- **α-quartz seed is correct.** `quartz.data` describes proper P3_121 hex α-quartz with a=4.916 Å, c=5.405 Å, ρ=2.648 g/cm³ (exp).
- **Timing claim (C3) is plausible.** ML-Tersoff and Q-Tersoff both hit 213 timesteps/s = 0.24 M atom-step/s/core, consistent with a short-range Tersoff pair style. Paper's ≥100× speedup vs. GAP is physically expected.
- **Small tetrahedral-preservation claim (C6) partially holds.** Q-Tersoff keeps 97.6% of Si 4-coordinated at 298 K NPT and O-Si-O = 108.22° (1.25° off tetrahedral) — this is close to the paper's ≤ 2° claim.
- **Free-endpoint LLM judge worked.** Two independent judges (argo:gpt-5.1, argo:gemini-2.5-pro) returned identical CONTRADICTED verdicts with matching numerical citations. Confidence in the negative verdict is high.

## What didn't work (per claim)

### C2 — α-Quartz density and Si-O-Si angle: CONTRADICTED
- Paper: Q-Tersoff density err ~0%, ML-Tersoff 9.2%.
- Ours: 20.7-34.5% (Q-Tersoff) and 26.4-39.9% (ML-Tersoff) across 3 protocols.
- No protocol we tried produces the paper's density numbers.
- Possible causes (see open_questions.json):
  1. Silent post-publication update to the .tersoff files on GitHub.
  2. Paper's evaluation used a fixed-symmetry constrained cell for property evaluation, hiding the true global-minimum structure.
  3. Different LAMMPS Tersoff parsing convention across versions.
  4. The parameter values in Table 1 of the paper don't exactly match the .tersoff files (Table 1 is truncated to ~4 sig figs, .tersoff files are 15 sig figs — this is unlikely to explain 20% density error).

### C2 (angles) — CONTRADICTED for ML-Tersoff, PARTIAL for Q-Tersoff
- Q-Tersoff Si-O-Si: paper 1.7°, ours 3.85° (2.3×). O-Si-O: paper 0.3°, ours 1.25° (4×). Both are within noise band but consistently larger. PARTIAL disagreement.
- ML-Tersoff Si-O-Si: paper +7°, ours **−15°** (wrong sign, 2× magnitude). Clearly CONTRADICTED.
- ML-Tersoff O-Si-O: paper 0.4°, ours 3.52°. 9× larger.

### C6 (coordination) — CONTRADICTED for ML-Tersoff
- Paper implies all polymorphs preserve 4-fold Si.
- ML-Tersoff at 298 K NPT: only 77% of Si is 4-fold. 11% is 3-fold, 9% is 5-fold. 8% of O atoms are dangling (1-fold).
- Q-Tersoff at 298 K NPT: 97.6% of Si is 4-fold (matches paper implication).

### C1 (21-polymorph energetic ordering) — NOT TESTED (BLOCKED)
- The 20 non-quartz IZA structures are not in the released repo.
- Would need to fetch IZA CIFs, convert to LAMMPS data, run the same protocol for each.
- Estimated additional effort: 4-6 hours for a competent user with the IZA CIF export tools.

### C4 (elastic constants) — NOT TESTED
- Paper acknowledges 66-6013% error on elastic constants.
- We did not run the finite-strain protocol.
- Would take ~30 min per potential.

### C5 (amorphous S(q)) — NOT TESTED
- Requires the full melt-quench protocol described in Methods: 4000-SiO₂ β-cristobalite, heat to 2500 K with ML-BKS over 1 ns, quench to 300 K, equilibrate with Tersoff for 3 ns, extract S(q) from last 1 ns.
- Estimated: 12-24 h of MD on 1 GPU.

## Root-cause hypothesis for the CONTRADICTED verdict

The **single most parsimonious explanation** is that the paper's Fig. 4 α-quartz numbers were computed with a *different structural evaluation protocol* than a straightforward "relax cell and measure" — most likely: (a) the properties were evaluated at fixed experimental cell parameters (a=4.913, c=5.405), sampling only atomic degrees of freedom, and (b) the density reported is then trivially "0% error" because the cell was fixed at exp. This would also explain why the ML-Tersoff Si-O-Si "error" of 7° is reported as positive: with a fixed cell, the potential is forced into a compressed α-quartz frame and Si-O-Si would still be within the vicinity of exp values.

If this hypothesis is correct, then:
- The paper's density claim is essentially "when you constrain the cell to the experimental values, the atoms don't want to move" — which is a much weaker statement than "the potential correctly predicts density."
- Our finding that the potentials do NOT have α-quartz at their global minimum is not a contradiction of the paper's claim per se, but it is a very important caveat that would meaningfully change how one uses these potentials in practice (any free-cell MD will drift away from α-quartz).

## Recommendation for the authors

Release, alongside the .tersoff files:
1. Whether property evaluation was at fixed-cell or free-cell.
2. The exact LAMMPS input used to evaluate each property in Table 1/Fig 4 (currently only the "relax" script is public).
3. The 21 IZA polymorph starting geometries (Zenodo dump would be ideal).
4. A commit hash / SHA-256 of the .tersoff files at the time of publication.

Without these, the paper's α-quartz claims cannot be independently reproduced from the released artifacts using the natural default protocol. This is an actionable-repo hygiene gap, not necessarily a scientific error in the paper.
