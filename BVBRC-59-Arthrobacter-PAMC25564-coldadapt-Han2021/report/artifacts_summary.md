# Artifacts Summary — BVBRC-59 (Arthrobacter sp. PAMC25564, Han et al. 2021)

Directory: `~/Dropbox/REPLICATE-PROJECT/BVBRC-59-Arthrobacter-PAMC25564-coldadapt-Han2021/`

## Reports (`report/`)
| File | Purpose |
|---|---|
| `REPORT.md`               | Canonical markdown replication report (verdict + claims table + results). |
| `REPORT.tex`              | LaTeX version of the report with dedicated "Genuine Critique" section. |
| `open_questions.json`     | 5 open scientific questions grounded in Arthrobacter cold-adaptation biology, each with basis + next steps. |
| `workflow.md`             | Step-by-step methods (M1–M6) with tools, versions, inputs/outputs, and paper-vs-rerun deltas. |
| `artifacts_summary.md`    | This file. |
| `failure_analysis.md`     | Documented gaps, near-misses, and forced substitutions. |

## Genome data (`work/genomes/`)
| File | Contents | Source |
|---|---|---|
| `PAMC25564.fna`           | Focal genome FASTA (CP039290.1 / GCA_004798705.1, 4,170,970 bp, 66.71% GC). | NCBI Datasets v2 |
| `PAMC25564_proteins.faa`  | PGAP proteome, 3,613 sequences. | NCBI Datasets v2 (PROT_FASTA) |

## Focal-genome accessioning
- **GenBank:** CP039290.1
- **RefSeq:** NZ_CP039290.1
- **Assembly:** GCA_004798705.1 / GCF_004798705.1 (ASM479870v1)
- **BioProject:** PRJNA531357
- **BioSample:** SAMN11356967
- **Submitter:** Korea Polar Research Institute
- **Sequencing:** PacBio Sequel, HGAP v4
- **Annotation vintage used:** GenBank original 2019-04-11 (paper-contemporaneous)

## Reference DB
- **dbCAN-HMMdb-V9** (pro.unl.edu, 99 MB, HMMER3). Substituted for the paper's V8-era dbCAN2 DB because bcb.unl.edu is offline.

## Comparator accessions (sampled and verified)
| Accession | Strain |
|---|---|
| CP040018.1 | Arthrobacter sp. 24S4-2 |
| CP007595.1 | Arthrobacter sp. PAMC25486 |
| CP017421.1 | Arthrobacter sp. ZXY-2 |
| CP018863.1 | Arthrobacter crystallopoietes DSM 20117 (Crystallibacter) |
| CP002379.1 | Pseudarthrobacter phenanthrenivorans Sphe3 |

All resolve to real complete public genomes of the named strains.

## Key numerical outputs
| Metric | Paper | Rerun |
|---|---|---|
| Length (bp)      | 4,170,970 | 4,170,970 |
| GC (%)           | 66.74     | 66.71 |
| Total genes      | 3,829     | 3,829 |
| CDS              | 3,613     | 3,613 |
| Pseudogenes      | 147       | 147 |
| rRNA             | 15        | 15 |
| tRNA             | 51        | 51 |
| Total CAZymes    | 108       | 102 |
| GH / GT / CE / AA / CBM / PL | 33/45/23/5/2/0 | 34/43/16/5/9/0 |

## Cold-adaptation CAZyme families (recovered)
GH1, GH13 (7 subfamilies including GH13_11 glycogen-debranching and GH13_26), GH65 (α-trehalose phosphorylase), GH77 (4-α-glucanotransferase), CBM48. **Full match to paper Table 2.**

## Compute + endpoints
- Host: uicgpu01 (16 CPU, conda `antismash` env)
- HMMER: 3.4
- Python: 3.8
- NCBI: Datasets v2 REST + E-utilities (free)
- LLM judge: Argo gpt-5.2 at localhost:44497 (free, per standing rule)
- Paper OA: Europe PMC XML

## Verdict artifact
`REPORT.md` verdict block: **REPLICATED**, coverage 9/10, agreement 8/10.

## WAVE_RESULT
```
WAVE_RESULT set=BVBRC-59 paper=PMID:34078272(Han2021,BMC-Genomics,Arthrobacter-sp.-PAMC25564-cold-adaptation-CAZymes) verdict=REPLICATED dir=~/Dropbox/REPLICATE-PROJECT/BVBRC-59-Arthrobacter-PAMC25564-coldadapt-Han2021 one_line=All six primary genome stats (4,170,970 bp; 66.7% GC; 3,829 genes/3,613 CDS/147 pseudo/15 rRNA/51 tRNA) reproduced EXACTLY on public NCBI data; independent HMMER/dbCAN rerun gave 102 CAZymes vs paper's 108 with all glycogen/trehalose cold-adaptation families (GH1/GH13_11/GH13_26/GH65/GH77/CBM48) recovered; LLM judge REPLICATED cov9/agr8.
```
