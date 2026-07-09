# BVBRC-16 — Attempt Log (2026-06-16/17)

| Step | Command / Action | Result |
|---|---|---|
| 1 | Europe PMC `search?query=DOI:10.1186/s12864-018-5043-9` | 1 hit, OA=Y, PMCID PMC6122445, full abstract present. |
| 2 | BV-BRC: `genome/?and(eq(species,Enterococcus faecium),eq(strain,17OM39))` | 1 hit — `1352.1047`, GCF_001652715.1, 106 contigs, 2,840,201 bp, BioProject PRJNA318315. ✅ |
| 3 | BV-BRC: `genome/?and(eq(species,Enterococcus faecium),eq(strain,T110))` | 2 hits — `1344042.3` (Complete chromosome, 2,737,963 bp, GCA_000737555.1) + `1344042.14` (44,086 bp plasmid). ✅ |
| 4 | BV-BRC: `genome/?keyword(17OM39)` | Returns mostly unrelated noise (Norovirus, SARS-CoV-2 with similar codes); use the strain-field query instead. |
| 5 | Sanity check: typical *E. faecium* genome size | 2.7–3.1 Mb expected; both candidate (2.84 Mb) and comparator (2.74 Mb) are in range. ✅ |
| 6 | Skipped: pan-genome / phylogenetic reconstruction across all paper strains; AMR + virulence rescreen. | Out of scope for short pass. |

All API responses captured under `evidence/`.
