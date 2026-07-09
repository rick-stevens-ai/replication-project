# BVBRC-18 — Artifact Harvest

## Bibliographic / OA
- Europe PMC core JSON: `evidence/europepmc_xu2019.json` (isOpenAccess=Y, PMC6780079).
- License: MDPI open access (CC BY 4.0).

## Strain / genome metadata (BV-BRC)
File: `evidence/bvbrc_marine_streptomyces.json`.

- Total *Streptomyces* genomes in BV-BRC: **14,474** (any status).
- Marine-source examples confirmed by `isolation_source`:
  - `1690221.4` — *S. spongiicola* 531S — marine sponge — 6.91 Mb.
  - `1055352.3` — *Streptomyces* sp. W007 — Kiaochow Bay marine sediment — 9.06 Mb.
  - `909626.3` — *Streptomyces* sp. RV15 — marine sponge — 10.77 Mb.
  - `2250578.3` — *Streptomyces* sp. LHW50302 — marine sponge — 7.69 Mb.
  - `1857892.3` — *Streptomyces* sp. MP131-18 — marine sediment — 7.96 Mb.

## Genome-size context
- Marine *Streptomyces* observed range here: ~6.9–10.8 Mb.
- *Streptomyces* genomes typically encode 20–60 BGCs (one cluster per ~150 kb of "biosynthetic-rich" genome). The paper's 16–84 range fits this scaling.

## Tool stack from the paper
- Genome download from NCBI; comparative genomics with OrthoMCL / GET_HOMOLOGUES.
- Phylogenomics from concatenated single-copy core genes (likely RAxML / IQ-TREE).
- SMBGC mining with **antiSMASH** (v4 or v5 in 2019).
- Cluster classification by SMBGC type (PKS-I/II, NRPS, terpene, RiPP, hybrid, others).

## Notes
- The paper's 87-strain list (Supplementary Table S1 in *Marine Drugs* article) is not parsed in this pass but is openly accessible from MDPI.
- BV-BRC indexes the genus broadly; marine-source filtering currently requires `isolation_source` keyword matching, which is incomplete (some marine isolates are recorded without that field).
