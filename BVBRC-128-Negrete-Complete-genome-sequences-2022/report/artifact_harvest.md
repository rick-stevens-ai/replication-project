# Artifact Harvest — BVBRC-128 Negrete

Every public artifact pulled during this replication.

| # | URL / source | Local path | Size | Purpose |
|---|--------------|------------|-----:|---------|
| 1 | https://gutpathogens.biomedcentral.com/counter/pdf/10.1186/s13099-022-00500-5.pdf | paper.pdf | 2,220,111 B | Source paper (BMC OA) |
| 2 | NCBI EFetch nuccore CP078106 (fasta) | work/sequences/CP078106.fna | 4,425,011 B | GK1025B chromosome |
| 3 | NCBI EFetch nuccore CP078106 (ft) | work/sequences/CP078106.ft | 1,115,320 B | GK1025B chromosome features |
| 4 | NCBI EFetch nuccore CP078107 (fasta+gb) | work/sequences/CP078107.{fna,gb} | 103,316 + 240,068 B | pGK1025B_1 |
| 5 | NCBI EFetch nuccore CP078108 (fasta+gb) | work/sequences/CP078108.{fna,gb} | 121,992 + 266,535 B | pGK1025B_2 |
| 6 | NCBI EFetch nuccore CP078109 (fasta+gb) | work/sequences/CP078109.{fna,gb} | 47,286 + 115,920 B | pGK1025B_3 |
| 7 | NCBI EFetch nuccore CP078110 (fasta+ft) | work/sequences/CP078110.{fna,ft} | 4,412,846 + 1,121,066 B | H322 chromosome |
| 8 | NCBI EFetch nuccore CP078111 (fasta+gb) | work/sequences/CP078111.{fna,gb} | 102,268 + 242,004 B | pH322_1 |
| 9 | NCBI EFetch nuccore CP078112 (fasta+gb) | work/sequences/CP078112.{fna,gb} | 119,961 + 270,505 B | pH322_2 |
| 10 | NCBI EFetch nuccore NC_018843 (fasta) | work/SSU5_NC_018843.fna | 104,828 B | Salmonella phage SSU5 |
| 11 | https://bitbucket.org/genomicepidemiology/plasmidfinder_db/raw/HEAD/enterobacteriales.fsa | work/plasmidfinder_db/enterobacteriales.fsa | 133,145 B | CGE PlasmidFinder Enterobacteriales replicon DB |
| 12 | https://rest.pubmlst.org/db/pubmlst_cronobacter_seqdef/schemes/1/sequence (POST) | work/mlst_query/CP078110_result.json | ~2 KB | PubMLST live query — H322 |
| 13 | https://rest.pubmlst.org/db/pubmlst_cronobacter_seqdef/schemes/1/sequence (POST) | work/mlst_query/CP078106_result.json | ~2 KB | PubMLST live query — GK1025B |

Total network payload: ~14.5 MB.
Every fetch was to a free / open endpoint. No auth, no paid API, no rate-limit hit.
