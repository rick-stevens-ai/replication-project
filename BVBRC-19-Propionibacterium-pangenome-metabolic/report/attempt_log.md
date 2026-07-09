# BVBRC-19 — Attempt Log (2026-06-16/17)

| Step | Command / Action | Result |
|---|---|---|
| 1 | Europe PMC `search?query=DOI:10.3390/genes11101115` | 1 hit, OA=Y, PMCID PMC7650540, full abstract present. |
| 2 | BV-BRC: `genome/?eq(genus,Propionibacterium)` count | 275 genomes (any status). |
| 3 | BV-BRC: `genome/?eq(genus,Cutibacterium)` (proxy for reclassified P. acnes via `species,Cutibacterium acnes`) | 600 C. acnes genomes. |
| 4 | BV-BRC: `genome/?eq(species,Propionibacterium freudenreichii)` | 5+ complete genomes returned (PFRJS series), all 2.51–2.70 Mb. ✅ |
| 5 | Sanity check: typical *P. freudenreichii* genome size | 2.5–2.7 Mb, ~67% GC — matches BV-BRC values, supports the paper's "high-GC, small-genome" framing. ✅ |
| 6 | Skipped: GET_HOMOLOGUES pan-genome rerun, ModelSEED GEM rebuild, FBA of the ferredoxin-linked pathway. | Out of scope for short metadata pass. |

All API responses captured in `evidence/bvbrc_propionibacterium.json`.
