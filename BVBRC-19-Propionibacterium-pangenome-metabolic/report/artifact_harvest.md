# BVBRC-19 — Artifact Harvest

## Bibliographic / OA
- Europe PMC core JSON: `evidence/europepmc_mccubbin2020.json` (isOpenAccess=Y, PMC7650540).
- License: MDPI open access (CC BY 4.0).

## Strain / genome metadata (BV-BRC)
File: `evidence/bvbrc_propionibacterium.json`.

- Total *Propionibacterium* genomes in BV-BRC: **275**.
- Total *Cutibacterium acnes* genomes (formerly *P. acnes*) in BV-BRC: **600**.
- Sample *P. freudenreichii* (type species) complete genomes:
  - `1744.104` — PFRJS25 — GCA_900097245.1 — 2.70 Mb.
  - `1744.105` — PFRJS12-1 — GCA_900095075.1 — 2.62 Mb.
  - `1744.106` — PFRJS22 — GCA_900092755.1 — 2.63 Mb.
  - `1744.107` — PFRJS14 — GCA_900087655.1 — 2.51 Mb.
  - `1744.108` — PFRJS12 — GCA_900087375.1 — 2.61 Mb.

## Reclassification context
- Since 2016, the old genus *Propionibacterium* has been split (Scholz & Kilian 2016) into *Propionibacterium* (sensu stricto, dairy / industrial — incl. *P. freudenreichii*, *P. acidipropionici*), *Cutibacterium* (skin — incl. C. acnes, C. avidum, C. granulosum), *Acidipropionibacterium* (e.g., *A. jensenii*), and *Pseudopropionibacterium* (e.g., *Ps. propionicum*).
- The paper covers all five splits under their pre-split names.

## Models / supplementary
- Paper deposits the *P. freudenreichii* GEM and pan-metabolic model openly (Supplementary files / GitHub link in the Genes article); not downloaded in this pass but openly accessible.

## Tool stack from the paper
- Annotation: RAST / RASTtk.
- Pan-genome: GET_HOMOLOGUES, OrthoMCL.
- GEM reconstruction: ModelSEED + manual curation.
- BLAST for cross-species ortholog mapping.
