# Workflow: LUCID-100 Casero 2017 Replication

## Pipeline overview

Independent end-to-end 16S amplicon re-analysis. All scripts in `scripts/`, all outputs in `work/` and `results/`. Free tools only (Homebrew vsearch, Python venv with scikit-bio/pandas/scipy).

```
Paper (Casero 2017)                        Our replication
────────────────────                        ─────────────────────
raw HiSeq 2×101 V4                          ↓ (identical raw data)
   SRA SRP098151 (80 libs)  ─────────────►  ENA mirror pull (curl 160 fastq.gz, 2.0 GB)
                                            │
                                            ▼
QIIME1 demultiplex + join                   vsearch --fastq_mergepairs
   (paper: default params)                    minovlen 20 maxdiffs 10
                                            │
                                            ▼
QIIME1 QC: minQ30, len 150                  vsearch --fastq_filter
                                              maxee 1.0 minlen 200 maxlen 300
                                            │
                                            ▼
GG_13_8 closed-ref @97%                     vsearch --cluster_size @97%  (de novo)
                                              + --uchime3_denovo
                                            │
                                            ▼
low-abund filter (<0.0005%)                 (skipped — retain all 2291 OTUs)
   → 1260 OTUs                              → 2291 OTUs
                                            │
                                            ▼
GG_13_8 taxonomy                            SILVA 138 NR99 (DADA2 train set)
                                              via vsearch --usearch_global blast6
                                            │
                                            ▼
Rarefaction to 60k                          Rarefaction to 30k (retains 79/80)
Faith PD alpha                              Shannon + observed OTUs (no phylo tree)
UniFrac beta                                Bray-Curtis + Jaccard
ANOSIM / PERMANOVA                          PERMANOVA (skbio)
DESeq2/LEfSe/MBCluster                      Targeted Mann-Whitney on paper-named taxa
                                            │
                                            ▼
                                            ✅ Headline: Akkermansia 17.28% vs 0.50%
                                            ✅ 10/12 quantitative claims verified
                                            ❌ PICRUSt/FishTaco arm: not run
                                            ❌ LC-MS metabolomics arm: not run (no Dryad DOI)
```

## Script execution order

| Order | Script | Purpose | Runtime |
|---|---|---|---|
| 1 | `scripts/01_make_metadata.py` | Parse ENA filereport → 80-row sample metadata (run ↔ dose ↔ time ↔ mouse ID) | <10 s |
| 2 | `scripts/02_download_fastqs.sh` | curl all 160 fastq.gz from ENA mirror | ~15 min |
| 3 | `scripts/03_prep_reference.py` | SILVA seed v138.1 → ungapped V4-extracted FASTA | ~1 min |
| 4 | `scripts/04_process_samples.sh` | Per-sample vsearch mergepairs + maxee-1.0 filter | ~25 min (8-thread) |
| 5 | `scripts/05_cluster_otus.sh` | Dereplicate → cluster_size 97% → uchime3_denovo → OTU table → blast6 taxa | ~5 min |
| 6 | `scripts/06_diversity_and_taxa.py` | Rarefy 30k → alpha/beta/PCoA/PERMANOVA/phylum-family-genus rollup/targeted MWU | <1 min |
| 7 | `scripts/07_reassign_with_nr99.py` | Retax OTUs against SILVA 138 NR99 DADA2 train_set | <1 min |

**Total wall-clock: ~45 min on CherryRd (Darwin, 8-thread).**

## Justified methods substitutions

| What we changed | Why | Impact on conclusions |
|---|---|---|
| QIIME1 → vsearch | QIIME1 unavailable / deprecated | None — same algorithm class, 97% cluster identity preserved |
| Closed-ref GG_13_8 → de novo vsearch | Avoids brittle GG_13_8 install | Richer OTU table (2291 vs 1260); dominant taxa unchanged |
| GG_13_8 taxonomy → SILVA 138 NR99 | Modern best practice | Different genus names in tail; Akkermansiaceae / Verrucomicrobiota still resolve correctly |
| UniFrac → Bray-Curtis + Jaccard | No phylogeny tree built | Different distances, same PERMANOVA significance pattern |
| Faith PD → Shannon + richness | No phylogeny tree | Different metric, same qualitative direction, magnitudes not directly comparable |
| DESeq2/LEfSe/MBCluster → targeted MWU | Scope: replicate headline, not every classification detail | Claim #11 (496 OTUs FDR<0.01) marked "not tested" |
| PICRUSt/FishTaco | Would need GG_13_8 closed-ref OTUs + PICRUSt v1 install | Fig. 4 / Table S6 unverified |
| LC-MS + Matlab CMP | No Dryad DOI in paper text | Fig. 5-6 / Tables S7-S10 unverified (data-availability blocker) |

## Reproducibility

- All code and outputs committed under this directory. Re-execute in order 01→07; requires `vsearch`, Python venv with `scikit-bio pandas scipy numpy`.
- Raw data recoverable from ENA / SRA SRP098151 with the supplied download script.
- Runtime dominated by fastq download; the analysis itself is <10 min on a modern laptop.
