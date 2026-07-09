# BVBRC-18 — Attempt Log (2026-06-16/17)

| Step | Command / Action | Result |
|---|---|---|
| 1 | Europe PMC `search?query=DOI:10.3390/md17090498` | 1 hit, OA=Y, PMCID PMC6780079, full abstract present (with all key numbers: 87 genomes, 123,302 OG clusters, 16–84 SMBGCs, three clades). |
| 2 | BV-BRC: `genome/?eq(genus,Streptomyces)` count | 14,474 genomes (any status). |
| 3 | BV-BRC: `genome/?and(eq(genus,Streptomyces),keyword(marine))` | 5 sample hits returned (sponge, sediment); confirmed marine-source strains are indexed. |
| 4 | Sanity check: genome size range of returned marine strains | 6.91–10.77 Mb — consistent with the typical Streptomyces size that supports antiSMASH counts of 16–84 BGCs (one BGC per ~150 kb). |
| 5 | Skipped: antiSMASH rerun, OrthoMCL pan-genome, phylogenomic tree. | Out of scope for short metadata pass. |

All API responses captured in `evidence/bvbrc_marine_streptomyces.json`.
