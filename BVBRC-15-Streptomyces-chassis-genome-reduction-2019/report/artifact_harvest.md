# BVBRC-15 — Artifact Harvest

## Bibliographic / OA
- Europe PMC core JSON: `evidence/europepmc_bu2019.json` (isOpenAccess=Y, PMC6348691).
- License: BMC open access (CC BY 4.0 per BMC default).

## Strain / genome metadata
- BV-BRC genus/species probe for *Streptomyces chattanoogensis*: 5 genomes indexed (NPDC001124, NPDC001300, NPDC001496, NPDC040912, NRRL ISP-5002). Lengths 8.32–9.13 Mb. See `evidence/bvbrc_chattanoogensis_species.json`.
- Strict strain query for **L10** in BV-BRC: 0 hits across three formulations (name, species+strain, keyword). See `evidence/bvbrc_L10_lookup.json`.
- L10 reference genome (historical): NCBI BioProject **PRJNA208758**, assembly under `NZ_AGSW00000000` (Liu Y. et al., 2013, Genome Announc.). Engineered derivatives L320/L321 are not deposited in BV-BRC under their construction names.

## Supplementary materials available from the paper
- Additional file 1 (PDF) — supplementary figures.
- Additional file 2 (table) — list of large non-essential regions identified.
- Cre/loxP plasmid maps in the body of the paper.

## Wet-lab artifacts NOT available without authors
- *S. chattanoogensis* L10/L320/L321 strains (Zhejiang University collection).
- Suicide plasmids with loxP/loxP-mutant cassettes.
- Heterologous expression cassettes for polyketide products tested.

## Tool stack from the paper
- Genome comparison: MAUVE / Mummer / Mauve-derived synteny.
- Essential gene prediction: DEG (Database of Essential Genes), Geptop, OGEE.
- Cre/loxP recombination system; PCR-targeted gene replacement.
- Phenotypic assays: HPLC for natamycin titer, ATP/NADPH bioluminescence kits.
