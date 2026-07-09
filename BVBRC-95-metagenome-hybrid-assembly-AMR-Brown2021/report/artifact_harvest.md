# Artifact harvest — BVBRC-95

## Publications
- Brown CL et al. 2021, Scientific Reports 11:3753. DOI 10.1038/s41598-021-83081-8. PMC7881036.
- Full text XML pulled from NCBI eutils efetch: `work/pmc_fulltext.xml` (105 KB); cleaned text `work/pmc_fulltext.txt` (53 KB).

## Sequence data (NCBI BioProject PRJNA527877 → ENA mirror)
Bulk index: `work/ena_run.tsv` (123 runs, all metadata columns).

Pulled to uicgpu (`/data/stevens/BVBRC-95/work/assemblies/`), 7 assemblies of USA-1-influent:

| Accession | Assembler | fastq.gz size | contigs | total bp | N50 |
|---|---|---:|---:|---:|---:|
| SRR12664619 | Megahit | 16 MB | 98,668 | 48 Mbp | 469 |
| SRR13105837 | metaSpades | 85 MB | 649,361 | 249 Mbp | 372 |
| SRR12664620 | IDBA-UD | 44 MB | 173,704 | 136 Mbp | 907 |
| SRR12664586 | HybridSpades | 86 MB | 597,391 | 256 Mbp | 430 |
| SRR12664608 | Canu | 4 MB | 2,125 | 15 Mbp | 19,298 |
| SRR12664575 | Flye | 9 MB | 971 | 30 Mbp | 45,101 |
| SRR12664597 | OPERA-MS | 18 MB | 85,623 | 55 Mbp | 544 |

Download URLs of form `https://ftp.sra.ebi.ac.uk/vol1/fastq/<3-letter-prefix>/<3-digit last-3>/<accession>/<accession>.fastq.gz` — resolved via ENA REST `filereport?fields=fastq_ftp`.

## Reference DB
- NCBI AMRFinder+ database `2024-07-22.1` at `/home/stevens/micromamba/envs/amr/share/amrfinderplus/data/latest`. Bundled by the `amr` micromamba env.

## Code
All in `report/evidence/`:
- `filter_and_amr.sh` — filter each assembly to contigs ≥1kb then run AMRFinder+
- `analyze_amr.sh` — cross-assembler ARG analysis + Jaccard
- All also in `work/` in original form (`pull_batch2.sh`, `stats_all.sh`, `assembly_stats.sh`).

## Not pulled (scope limit)
- Raw Illumina fastqs for USA-1-influent (SRR10059217, SRR8749023 + variants) — would enable de-novo reassembly but scope was verification not re-assembly.
- Raw Nanopore for USA-1-influent (SRR12664564 = USA-1-inf-Nanopore, SRR11626801 = USAIN) — same reason.
- Assemblies for the other 9 metagenomes (CHE-inf/as, HKG-inf/as, IND-inf/as, SWE-inf/as, USA-as) — scope limit.
- MetaCompare pipeline + ACLAME + PATRIC (for MGE/host contextualization) — scope limit.
