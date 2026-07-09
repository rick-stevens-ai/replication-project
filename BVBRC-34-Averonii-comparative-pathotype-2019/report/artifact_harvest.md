# Artifact Harvest — BVBRC-34

## Paper
| Artifact | URL | Size |
|---|---|---|
| PLoS ONE PDF | https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0221018&type=printable | 5.9 MB (work/paper.pdf) |
| Europe PMC full-text XML | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6715197/fullTextXML | 256 KB (work/paper_fulltext.xml) |

## Genomes — 41 A. veronii assemblies (NCBI Datasets, free, no auth)
Downloaded as one package `av41.zip` (91,946,078 bytes) via
`datasets download genome accession --inputfile acc_list.txt --include genome,protein`.
Full Table1→assembly map in `evidence/resolved.tsv` and `evidence/acc2strain.json`. All 41/41 resolved; sizes match Table 1.

| Strain | Table1 accession (2018) | Resolved assembly | Length (bp) |
|---|---|---|---:|
| VBF557 | LXJN00000000.1 | GCF_001696435.1 | 4,696,503 |
| CIP107763 | NZ_CDDU00000000.1 | GCF_000820285.1 | 4,430,813 |
| pamvotica | NZ_MRUI00000000.1 | GCF_001921885.1 | 4,919,147 |
| TTU2014-140ASC..108ASC (17 dairy-cattle) | NZ_LKJ*/LKK* | GCF_00144xxxx.1 | ~4.53–4.68 M |
| CECT4486 | NZ_CDBU00000000.1 | GCF_000820365.1 | 4,410,797 |
| CCM7244 | NZ_MRZQ00000000.1 | GCF_001908555.1 | 4,422,254 |
| CB51 | CP015448 | GCF_001634345.1 | 4,584,103 |
| Hm21 | NZ_ATFB00000000.1 | GCF_000464515.2 | 4,766,880 |
| X11 | NZ_CP024930 | GCA_002803925.1 | 4,283,286 |
| A29 | NJGB00000000.1 | GCF_002214865.1 | 4,481,700 |
| X12 | NZ_CP024933 | GCF_002803945.1 | 4,773,186 |
| AER39 | NZ_AGWT00000000.1 | GCF_000297975.1 | 4,420,590 |
| LMG13067 | NZ_CDBQ00000000.1 | GCF_000820385.1 | 4,735,607 |
| AVNIH2 | NZ_LRBO00000000.1 | GCF_001647435.1 | 4,523,432 |
| AVNIH1 | NZ_CP014774.1 | GCF_001634325.1 | 4,955,058 |
| AMC35 | NZ_AGWW00000000.1 | GCF_000298035.1 | 4,565,607 |
| CECT4257 | NZ_CDDK00000000.1 | GCF_000820225.1 | 4,516,420 |
| CCM4359 | NZ_MRZR00000000.1 | GCF_001908535.1 | 4,511,265 |
| B565 | NC_015424 | GCF_000204115.1 | 4,551,783 |
| AER397 | NZ_AGWV00000000.1 | GCF_000297995.1 | 4,496,658 |
| RU31B | NZ_FTMU00000000.1 | GCF_900156085.1 | 4,534,419 |
| Ae52 | BDGY00000000.1 | GCF_001748325.1 | 4,564,863 |
| ARB3 | NZ_JRBE00000000.1 | GCF_000754905.1 | 4,542,657 |
| **ML09-123** | **PPUW01000001** | **GCF_002906945.1** | **4,754,017** |
| **TH0426** | **NZ_CP012504.1** | **GCF_001593245.1** | **4,923,009** |

(Full 41-row table with GC%/contigs/proteins in `evidence/genome_stats.json`.)

## Reference databases
| DB | Source | Content |
|---|---|---|
| VFDB (Virulence Factors DB) | abricate 1.4.0 bundled db (`vfdb`, 4592 seqs, identical to mgc.ac.cn setB scope) | virulence-factor profiling |
| NCBI A. veronii taxon index | `datasets summary genome taxon "Aeromonas veronii"` | 1927 genomes (corpus check) |

## Compute artifacts (uicgpu:/data/stevens/bvbrc34)
- `genomes/av41.zip` + unpacked `av41/ncbi_dataset/data/GC*/` (fna + protein.faa)
- `work/ani_all.tsv` (fastANI), `work/mash_dist.tsv`, `work/pan/clusters70.clstr` (CD-HIT), `work/vfdb_out/*.tab` (41 abricate reports)
- All driver scripts + result JSONs (synced to `report/evidence/`).

## Checksums (evidence)
Run `shasum evidence/*.tsv evidence/*.json` to verify; ani_all.tsv = 1681 lines, mash_dist.tsv = 1681 lines, genome_stats.json = 41 records.
