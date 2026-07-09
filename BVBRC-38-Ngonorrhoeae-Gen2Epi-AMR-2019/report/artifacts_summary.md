# Artifacts Summary — BVBRC-38 Gen2Epi *N. gonorrhoeae* AMR Replication

All artifacts produced during the replication of Sundaraj Suchindran et al. 2019 (DOI 10.1186/s12864-019-5542-3). Reproduction target: the 11 WHO 2016 reference strains. All inputs free and public.

## Directory layout

```
work/
├── fetch_genomes.py                              # ENA/NCBI Datasets fetch driver
├── genome_manifest.json                          # 11 WHO genomes provenance
├── genomes/
│   ├── WHO_F.fna, WHO_G.fna, WHO_K.fna,
│   ├── WHO_L.fna, WHO_M.fna, WHO_N.fna,
│   ├── WHO_O.fna, WHO_P.fna, WHO_X.fna,
│   ├── WHO_Y.fna, WHO_Z.fna                      # 11 PacBio finished refs (ENA PRJEB14020)
│   └── FA1090.fna                                # NCBI Datasets (GCA/GCF_000006845.1)
├── extract_refgenes.py                           # FA1090 → wild-type AMR/typing genes
├── refgenes/
│   ├── penA.fna, gyrA.fna, parC.fna,
│   ├── ponA.fna, mtrR.fna, porB.fna,
│   └── rrna23S.fna                               # 7 reference loci for BLAST-based detection
├── mlst_typing.py                                # NG-MLST driver (BLAST vs pubMLST alleles)
├── mlst_results.json                             # 11 strains × 7 loci → ST
├── amr_detect.py                                 # NG-STAR AMR determinant driver
├── amr_results.json                              # 11 strains × 7 loci codon reads
├── rrna23S_azithro.py                            # 23S rRNA operon counter
├── rrna23S_results.json                          # per-strain 23S copy count
├── genome_stats.py                               # Biopython assembly-stats calculator
├── genome_stats.json                             # 11-strain assembly stats + panel median
├── alleles/
│   ├── abcZ.fas, adk.fas, aroE.fas, fumC.fas,
│   ├── gdh.fas, pdhC.fas, pgm.fas                # pubMLST NG-MLST allele FASTAs
│   └── profiles_mlst.tsv                         # 18,488-row ST profile table
├── reads/
│   ├── ERR5860304_1.fastq.gz
│   └── ERR5860304_2.fastq.gz                     # WHO_F Illumina paired reads (ENA)
├── assembly/
│   ├── WHO_F_denovo.fna                          # SPAdes 4.3.0 --careful de-novo assembly
│   ├── spades.log                                # full SPAdes stdout/log
│   └── fastp.json                                # fastp Q15 trim report
├── denovo_type_amr.py                            # NG-MLST + penA on de-novo assembly
├── denovo_results.json                           # de-novo assembly typing + penA output
├── llm_judge.py                                  # Argo gpt-5.2 judge harness
└── gen2epi_fulltext.xml                          # paper full text (Europe PMC)
report/
├── REPORT.md                                     # canonical replication report
├── REPORT.tex                                    # detailed LaTeX + genuine critique
├── workflow.md                                   # stage-by-stage workflow
├── artifacts_summary.md                          # this file
├── failure_analysis.md                           # what didn't work + why
├── open_questions.json                           # 5 open research questions
└── evidence/                                     # curated evidence package
    ├── genome_stats.json
    ├── mlst_results.json
    ├── amr_results.json
    ├── rrna23S_results.json
    ├── denovo_results.json
    ├── llm_judge_verdict.txt
    └── gen2epi_fulltext.xml
```

## Key JSON artifacts

| File | Content | Backs claim |
|---|---|---|
| `genome_stats.json` | Per-strain assembly stats + panel median (contigs, total length, longest scaffold, GC%, N50). | C1a |
| `mlst_results.json` | 11 strains × 7 NG-MLST loci → ST. | C2 |
| `amr_results.json` | 11 strains × 7 NG-STAR loci codon reads + mosaic-penA calls. | C3a, C3b |
| `rrna23S_results.json` | Per-strain 23S rRNA operon count (all = 4). | C3a (azithromycin locus) |
| `denovo_results.json` | fastp+SPAdes de-novo assembly stats + NG-MLST + penA call on assembled scaffolds vs finished reference. | C1b, C4 |
| `llm_judge_verdict.txt` | Free-Argo `gpt-5.2` judge verdict + coverage + agreement (VERDICT REPLICATED, 8/10, 9/10). | Independent scoring |

## Headline numbers (from the artifacts)

### Assembly stats (WHO panel median vs Paper Table 1)
| Metric | Paper | Replication | Match |
|---|---|---|---|
| Longest / chromosome length | 2,167,463 bp | 2,172,826 bp | ✅ |
| GC% | 52.64% | 52.52% | ✅ |
| N50 | 2,167,463 | 2,172,826 (chromosome-level) | ✅ |

### End-to-end de-novo (WHO_F, ERR5860304)
| Metric | Value |
|---|---|
| Total assembly length | 2,197,379 bp |
| GC% | 52.30% |
| Genome fraction vs WHO_F ref (≥95% id) | **99.96%** |
| Contig N50 (pre-Ragout) | 64,607 bp |
| NG-MLST | ST 10934 (7/7 alleles identical to finished ref) |
| penA | non-mosaic (99.657%) — same as finished ref |

### NG-MLST typing
| Strain | ST | | Strain | ST |
|---|---|---|---|---|
| WHO F | ST10934 | | WHO O | ST1902 |
| WHO G | ST1903  | | WHO P | ST8127 |
| WHO K | ST7363  | | WHO X | ST7363 |
| WHO L | ST1590  | | WHO Y | ST1901 |
| WHO M | ST7367  | | WHO Z | ST7363 |
| WHO N | ST1583  | |        |         |

All 11 strains: full 7/7 profiles, exact allele calls (100% id / 100% length).

### NG-STAR AMR determinants — headline biology
- **penA mosaic** detected in exactly **WHO K, X, Y, Z** (X/Y/Z are the three known ceftriaxone-resistant XDR strains — H041, F89, A8806).
- **WHO F** (pan-susceptible reference): wild-type penA, no QRDR mutations, wild-type ponA 421 — ✅ phenotype-concordant.
- All 4 23S rRNA operons recovered in every genome.

### LLM-judge (free Argo gpt-5.2)
- Verdict: **REPLICATED**
- Coverage: **8/10**
- Agreement: **9/10**
- Comment: *"Independent reimplementation matches WHO-panel MLST and AMR genotypes; assembly size/GC align, with only Ragout/misassembly metrics not fully reproduced."*

## Provenance summary

| Resource | Source | Cost |
|---|---|---|
| Paper full text | Europe PMC (`fullTextXML`) | Free |
| 11 WHO genomes | ENA PRJEB14020 (browser FASTA API) | Free |
| FA1090 reference | NCBI Datasets v2alpha REST | Free |
| NG-MLST alleles + profiles | pubMLST `pubmlst_neisseria_seqdef` scheme 1 | Free |
| WHO_F Illumina reads | ENA fastq FTP (ERR5860304) | Free |
| BLAST+ 2.17 | conda-forge / bioconda | Free |
| SPAdes 4.3.0 | bioconda | Free |
| fastp 1.3.6 | bioconda | Free |
| Biopython 1.87 | conda-forge | Free |
| Argo proxy `argo:gpt-5.2` | free Argo (key=stevens) | Free |
| Compute | ~2 min BLAST (laptop) + ~5 min SPAdes (uicgpu 16-core) | Free |

## Verdict recorded in artifacts

**PARTIAL REPLICATION (strong; near-REPLICATED).** Free-Argo LLM judge scored the final evidence package REPLICATED (coverage 8/10, agreement 9/10); recorded conservatively as PARTIAL due to 11-strain (not 1484) scope and un-run Ragout scaffolding.
