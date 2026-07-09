# BVBRC-17 — Artifact Harvest

## Bibliographic / OA
- Europe PMC core JSON: `evidence/europepmc_fang2018.json` (isOpenAccess=Y, PMC5996543).
- License: BMC open access (CC BY 4.0).

## Strain / genome metadata (BV-BRC)
File: `evidence/bvbrc_ecoli_B2_strain_probes.json`.

### Total complete E. coli genomes in BV-BRC
- **5,737** as of 2026-06-17 (well above the 110 strains the paper used in 2018).

### Canonical B2 / AIEC reference strains (used by Fang et al. and the broader IBD-E.-coli literature)
- **UTI89** (uropathogenic, B2):
  - `364106.8` — GCA_000013265.1, Complete, 5.18 Mb (canonical reference).
  - `364106.45`, `364106.46` — Complete reassemblies (5.07 Mb).
- **LF82** (AIEC isolated from a Crohn's disease patient, B2 — the AIEC reference):
  - `591946.4` — GCA_000284495.1, Complete, 4.77 Mb.
  - `591946.44` — GCA_021398935.1, Complete, 4.77 Mb (reassembly).
- **NRG857c** (AIEC O83:H1, B2):
  - `685038.3` — GCA_000183345.1, Complete, 4.89 Mb.

## Underlying GEM
- Paper builds on the **iJO1366** *E. coli* K-12 GEM (Orth et al. 2011) and per-strain GEMs from Monk et al. 2013/2016 (PNAS / Nature Biotech).
- Models available in the [BiGG Models database](http://bigg.ucsd.edu/) (not downloaded in this pass, but free and open).

## Tool stack from the paper
- Pan-genome: PanX / Roary / EDGAR-style.
- GEM reconstruction: COBRApy + ME-models extensions.
- Phylogrouping: ClermonTyping.
- Sugar-utilization simulations: FBA on glycan-derived carbon sources.
