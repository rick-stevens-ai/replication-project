# Artifact Harvest — BVBRC-39

## Paper
| Item | Value |
|---|---|
| Title | Pan-genome analysis of the genus *Finegoldia* identifies two distinct clades, strain-specific heterogeneity, and putative virulence factors |
| Authors | Brüggemann H, Jensen A, Nazipi S, Aslan H, Meyer RL, Poehlein A, Brzuszkiewicz E, Al-Zeer MA, Brinkmann V, Söderquist B |
| Journal | Scientific Reports 8:266 (2018) |
| DOI | 10.1038/s41598-017-18661-8 |
| PMC | PMC5762925 · PMID 29321635 |
| Open access | Yes (CC BY 4.0) |
| Full text | Europe PMC REST fullTextXML (free) → `work/fulltext.xml` (110,940 bytes), `work/fulltext.txt` |

## Genomes — the exact 17 from the paper (paper WGS accession → current NCBI GCA)
Downloaded via NCBI Datasets v2 REST/CLI (free, no auth). `work/fin17.zip` (17.4 MB), unpacked to `work/fin17/ncbi_dataset/data/`.

| Strain | Paper WGS acc | Current GCA | Group |
|---|---|---|---|
| 07T609 | NDYJ00000000 | GCA_002243235.1 | newly-seq (Sweden) |
| 08T492 | NDYI00000000 | GCA_002243075.1 | newly-seq |
| 09T408 | NDYH00000000 | GCA_002243155.1 | newly-seq |
| 09T494 | NDYG00000000 | GCA_002243215.1 | newly-seq |
| 12T272 | NDYF00000000 | GCA_002243175.1 | newly-seq |
| 12T273 | NDYE00000000 | GCA_002243195.1 | newly-seq |
| 12T306 | NDYD00000000 | GCA_002243135.1 | newly-seq |
| CCUG54800 | NDYC00000000 | GCA_002243095.1 | newly-seq |
| T151023 | NDYB00000000 | GCA_002243115.1 | newly-seq |
| T160124 | NDYA00000000 | GCA_002243035.1 | newly-seq |
| ACS-171-V-Col3 | AECM01 | GCA_000179495.1 | prev-published |
| ATCC 29328 | AP008971/AP008972 | GCA_000010185.1 | prev (complete) |
| ATCC 53516 | ACHM02 | GCA_000159695.1 | prev |
| GED7760A | LRPW01 | GCA_001546385.1 | prev |
| BVS033A4 | AEDP01 | GCA_000179695.1 | prev |
| SY403409CC001050417 | AFUI01 | GCA_000221585.2 | prev |
| ALB8 | JDVC01 | GCA_000582635.1 | prev |

**All 17 paper strains resolved 1:1 to public NCBI assemblies — the complete original dataset was recovered.**

## Reference virulence-factor proteins (UniProt REST, free)
- `work/refs/uniprot_vf.faa` (17 seqs: FAF/faf, SufA, sortases, CAMP factor)
- `work/refs/uniprot_vf2.faa` (10 seqs: PAB, protein L, albumin-binding homologs, pilin)
- Curated query set: `work/vf_query.faa` (7 representatives)

## NCBI corpus context
- NCBI Datasets now indexes **278 *Finegoldia* genome records (168 GCA primary)** vs 17 in 2018 — dataset fully available and greatly expanded.

## Tools (all free / local)
| Tool | Version/notes | Use |
|---|---|---|
| NCBI Datasets CLI | `datasets` /usr/local/bin | genome+protein download |
| fastANI | /usr/local/bin | all-vs-all ANI |
| CD-HIT | /usr/local/bin | pan/core proteome clustering |
| BLAST+ | makeblastdb, blastp | virulence-factor homology |
| Python3 + scipy/numpy | local | clustering, stats |
| Argo proxy | argo:gpt-5.2 (localhost:44497, free) | LLM-judge scoring |
