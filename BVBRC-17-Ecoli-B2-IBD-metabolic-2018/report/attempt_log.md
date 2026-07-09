# BVBRC-17 — Attempt Log (2026-06-16/17)

| Step | Command / Action | Result |
|---|---|---|
| 1 | Europe PMC `search?query=DOI:10.1186/s12918-018-0587-5` | 1 hit, OA=Y, PMCID PMC5996543, full abstract. |
| 2 | BV-BRC: `genome/?and(eq(species,Escherichia coli),eq(genome_status,Complete))` count | **5,737** complete E. coli genomes available — comfortably exceeds the paper's 110-strain pan-genome. |
| 3 | BV-BRC: `genome/?and(eq(species,Escherichia coli),eq(strain,UTI89))` | 5 hits (Complete + WGS + plasmid). ✅ |
| 4 | BV-BRC: `genome/?and(eq(species,Escherichia coli),eq(strain,LF82))` | 3 hits, including GCA_000284495.1 Complete (4.77 Mb). ✅ |
| 5 | BV-BRC: `genome/?and(eq(species,Escherichia coli),eq(strain,NRG857c))` | 2 hits, including GCA_000183345.1 Complete (4.89 Mb). ✅ |
| 6 | Skipped: pulling the paper's per-strain GEMs from BiGG / running FBA on mucin-glycan substrates. | Out of scope for short pass; well documented and feasible separately. |

All API responses captured in `evidence/bvbrc_ecoli_B2_strain_probes.json`.
