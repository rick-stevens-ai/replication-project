# Workflow — BVBRC-18 Marine *Streptomyces* BGC Replication

**Paper:** Xu et al. 2019 — *Comparative Genomic Insights into Secondary Metabolism Biosynthetic Gene Cluster Distributions of Marine Streptomyces* (Marine Drugs 17(9):498, DOI 10.3390/md17090498).
**Verdict:** PARTIAL.

## Pipeline (this pass)

```
[Europe PMC / PMC OA]                    [BV-BRC public API]
        |                                        |
        |  paper.pdf                             |  /genome/?keyword(marine)+Streptomyces
        v                                        v
[pdftotext extraction]                  [287-genome metadata snapshot]
        |                                        |
        v                                        v
[headline claims parsed]                [CheckM re-filter: completeness>95, contam<5]
                                                 |
                                                 v
                                        [141 QC-passing marine Streptomyces]
                                                 |
                                                 +----> corpus stats (size, GC, gene count, ecotype)
                                                 |
                                                 v
                                        [stratified 12-strain sample]
                                                 |
                                                 v
                                        [BV-BRC /genome_feature/ pulls (~150k CDS)]
                                                 |
                                                 v
                                        [BGC marker-keyword scan]
                                                 |     PKS-I/II, NRPS, terpene,
                                                 |     RiPP/lanti, siderophore,
                                                 |     bacteriocin, butyrolactone
                                                 v
                                        [class-specific divisors -> rough BGC count]
                                                 |
                                                 v
                                        [compare to paper claims C6-C10]

[Outgroup accession GCA_000269985.1] -----------> [BV-BRC query -> exists, 8.78 Mb, CheckM 98/0]
                                                          -> C11 verified
```

## Steps executed

| # | Step | Input | Output | Skill / Tool |
|---|------|-------|--------|--------------|
| 1 | Fetch paper | Europe PMC search on DOI | `work/paper.pdf` | curl + Europe PMC OA endpoint |
| 2 | Extract text | `paper.pdf` | Section-level headline numbers | `pdftotext` |
| 3 | Corpus probe | BV-BRC API: keyword(marine) + genus(Streptomyces) | `work/genomes/bvbrc_marine.json` (287 hits) | BV-BRC public REST |
| 4 | QC filter | 287 genomes + CheckM fields | 141 QC-passing subset | Python 3 stdlib |
| 5 | Corpus stats | 141-genome set | genome-size, GC, CDS, ecotype tallies | `work/corpus_stats.txt` |
| 6 | Sample selection | 141-genome set | 12 stratified genomes (`work/bgc_scan/sample.json`) | Python |
| 7 | Feature pulls | 12 genome_ids | ~150k CDS product strings | BV-BRC `/genome_feature/` |
| 8 | Marker scan | CDS products + keyword regex | `work/bgc_scan/results.json` | `work/bgc_scan/scan.py` |
| 9 | Rough BGC counts | Marker hits + class divisors | Per-strain BGC estimates, class fractions | `scan.py` |
| 10 | Correlation | Estimates vs genome_length | Pearson r = 0.24 | Python (`statistics`) |
| 11 | Outgroup check | `GCA_000269985.1` | BV-BRC record present (PRJNA19951, 8.78 Mb) | BV-BRC query |
| 12 | Report | All of the above | `report/REPORT.md`, `REPORT.tex` | Manual synthesis |

## Steps *not* executed (deliberate — flagged in `failure_analysis.md`)

| # | Step | Why not | Impact on verdict |
|---|------|---------|-------------------|
| A | antiSMASH v5/v6 install + run | Not installed; substituted with keyword-marker scan | PKS-I overcounted; density inflated; PARTIAL not FULL |
| B | Proteinortho V5.16b pan-genome | Requires ~7000 OC sets × 88 genome all-vs-all BLAST | C12 (123,302 OCs) untested |
| C | MAFFT + trimAl + IQ-Tree LG+F+R8 | Requires 888 single-copy OCs from step B | C13 (3-clade 23/38/22) untested |
| D | Kruskal-Wallis on clade × ecotype × BGC | Requires B + C + antiSMASH on full corpus | C14 (headline biology) untested |
| E | MDPI Table S1 (87-strain accession list) | HTTP 403 across all URL variants | Cannot bit-reproduce exact 87 |

## Determinism / reproducibility

- BV-BRC API queries are timestamped; snapshot preserved in `work/genomes/bvbrc_marine.json`. Rerunning against live BV-BRC will drift as new genomes are deposited.
- Marker-scan regex patterns are hard-coded in `work/bgc_scan/scan.py` — reproducible bit-for-bit given same JSON input.
- Class divisors (PKS/NRPS = 2, terpene/butyrolactone = 1) are heuristic; see `failure_analysis.md` for critique.
- Corpus stats and Pearson r are deterministic (no random seeds; no ML models).

## Provenance trail

- All raw pulls stored under `work/`.
- Original spot-check report preserved as `report/REPORT.md.bak-pre-promo`.
- Promotion pass log embedded in `report/REPORT.md` §§ 3–10.
- No secrets, credentials, or private data at any step.
