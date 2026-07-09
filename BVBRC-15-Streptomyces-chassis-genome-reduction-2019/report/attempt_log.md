# BVBRC-15 — Attempt Log (2026-06-16/17)

| Step | Command / Action | Result |
|---|---|---|
| 1 | Europe PMC `search?query=DOI:10.1186/s12934-019-1055-7` | 1 hit, full abstract + PMCID PMC6348691, OA=Y. |
| 2 | BV-BRC: `genome/?eq(genome_name,Streptomyces chattanoogensis L10)` | 0 hits. |
| 3 | BV-BRC: `genome/?and(eq(species,Streptomyces chattanoogensis),eq(strain,L10))` | 0 hits. |
| 4 | BV-BRC: `genome/?keyword(L10 chattanoogensis)` | 0 hits. |
| 5 | BV-BRC: `genome/?eq(species,Streptomyces chattanoogensis)` | 5 hits, lengths 8.32–9.13 Mb (other isolates only). |
| 6 | Cross-ref against published L10 reference genome | Located in NCBI as BioProject **PRJNA208758** / NZ_AGSW00000000 (Liu et al. 2013) — not yet ingested into BV-BRC under the L10 strain label. |
| 7 | Genome-size sanity check for the 1.3 Mb (L320) and 0.7 Mb (L321) deletions | 1.3 Mb / 8.7 Mb ≈ **15%** of the genome and 0.7 Mb / 8.7 Mb ≈ **8%** — both within the published range for streamlined-genome *Streptomyces* hosts (M145 → M1146/M1152 series deleted ~1.4 Mb). Biologically plausible. |
| 8 | Skipped: Cre/loxP wet-lab replication (out of scope and requires the authors' plasmids + strains). |

No commands required interactive auth. All API responses captured in `evidence/`.
