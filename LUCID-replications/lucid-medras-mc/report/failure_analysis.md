# Failure Analysis — lucid-medras-mc

## Verdict: PARTIAL

## What was successfully done (75% weight)
- **The Medras-MC binary WAS re-run from scratch.** This is unusual for LUCID
  MC replications, which historically stop at "code exists / documentation
  read" without ever executing the simulator (the "MC-never-rerun" pattern).
  Here, `basicXandIon(runs=20)` + `repairSimulation(Fidelity)` executed
  end-to-end in ~5 min on 1 CPU thread with real MC noise reported.
- **All 7 mechanistic claims (C1–C7) qualitatively reproduced** from the
  shipped code:
  1. 35 DSB/Gy quality-independence — quantitative match (33 vs 35).
  2. p_complex = 0.43 ± 0.02 — quantitative match (0.426 mean).
  3. Misrepair rises with LET (RBE peak mechanism) — shape match.
  4. Inter-chromosome misrepair falls with LET — shape match.
  5. Sub-linear misrepair vs dose (Eq 9 η'·N scaling) — shape match.
  6. Bi-exponential kinetics (fast NHEJ + slow HR/complex) — shape match.
  7. LET-driven unrepaired-lesion tail — shape match.
- **Three publication-quality figures reproduced** (Fig 5, 2C, 3A shapes).
- **Openness verified:** BSD-2 per-file, FOSS deps, open data (SDD v1.0).

## What was NOT done (25% weight — the reason for PARTIAL, not REPLICATED)

### Headline application layer skipped
The paper's *stated* contribution is not the MC backbone (which pre-existed
in earlier MEDRAS papers). It is the **coupling** of that MC to
cell-survival datasets to produce:
- **Fig 4** — MID (mean inactivation dose) scatter across cell lines from
  the Paganetti proton compilation. Requires the Paganetti dataset. **Not
  attempted.**
- **Fig 5** — RBE-vs-LET overlays for proton + carbon against PIDE ion
  survival points. Requires PIDE 3.4. **Not attempted; PIDE behind
  registration wall (GSI institutional email verification).**
- **Fig 6** — Dose-rate sparing curves vs Lehmann/Newman experimental data.
  **Not attempted.**
- **Fig 7** — Dose-rate MID predictions across cell lines. **Not attempted.**

The MC ingredients that *feed* these figures (misrepair-vs-LET shape,
dose scaling, kinetics shape) were reproduced, but the actual
data-overlaid, chi-square-able comparison plots that make the paper
publishable were not reconstructed.

### PIDE dataset access
- PIDE 3.4 (Particle Irradiation Data Ensemble, GSI) is the reference
  dataset for RBE studies. Not anonymously downloadable.
- Registration URL:
  `gsi.de/work/forschung/biophysik/forschungsfelder/radiobiological_modelling/pide_registration`
- Requires institutional email; maintainers email `.xls` + `.dat` files.
- Cached: NASA THREE PIDE overview + GSI page snapshot. Sufficient to
  document schema, not to fit.

### Coverage estimate
- Mechanistic MC claims: 100% (7/7 qualitatively; 2/2 quantitatively where
  paper reports numbers).
- Full paper scope (including data-overlaid application figures): ~35%.
- Gap: 65% depends on external cell-survival datasets not sourced.

## Why the PARTIAL verdict is preserved (not upgraded to REPLICATED)
The LUCID convention tags a run **REPLICATED** only when the paper's
headline results (the figures the paper's abstract points to) are
reconstructed. Here the abstract emphasizes the survival/RBE/dose-rate
predictions across cell lines, not the underlying misrepair distribution.
Without touching Paganetti/PIDE/Lehmann-Newman data, we cannot claim the
headline was exercised.

**PARTIAL is the honest tag.** It is a *softer* PARTIAL than the classic
LUCID pattern (where the MC binary itself was never executed) because here
we did rerun the simulator; only the downstream data-fit overlays were
skipped. Recommend future work either (a) source PIDE via GSI registration
and complete Fig 5 overlays, or (b) explicitly redefine the replication
scope to "mechanistic MC only" and re-tag REPLICATED with a scope caveat.

## Friction tags encountered
- `license-without-LICENSE-file`
- `no-pinned-deps`
- `deterministic-seed-not-exposed`
- `kinetics-column-not-self-described`
- `non-deterministic-output-order`
- `registration-required-dataset` (PIDE 3.4)

## No blockers
Code ran first try. Zero debugging. Zero patches needed to the shipped source.
