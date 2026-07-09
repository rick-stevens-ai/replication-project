# Artifacts summary — BVBRC-81

Inventory of the concrete outputs of this replication, keyed to the claims
they support.

Repo root: `~/Dropbox/REPLICATE-PROJECT/BVBRC-81-lplantarum-PU3-nanopore/`

---

## Retrieved primary data

| Path | Size | Source | Supports |
|---|---|---|---|
| `paper.xml` | 200,906 B | Europe PMC full-text XML for PMC10609609 | Method / claim ground-truth |
| `genome/PU3_all.fasta` | 3,423,478 B | NCBI EUtils efetch, accessions CP120642–CP120651 (10 records) | C1, C2, C3 |
| `genome/PU3_all.gb` | 7,876,807 B | NCBI EUtils efetch (GenBank flat file) | C6, C7, C8 |
| `refs/M19.fna` (from GCA_018588605.2) | reference | NCBI Genomes FTP | C9, C12 |
| `refs/WCFS1.fna` (from GCF_000203855.3) | reference | NCBI Genomes FTP | C9, C12 (control) |

## Independent computation outputs

| Path | Purpose | Supports |
|---|---|---|
| `report/evidence/genome_metrics.tsv` | Per-record length + GC recomputed in Python from the deposited FASTA | C2, C3, C4, C5 |
| `report/evidence/genbank_feature_counts.txt` | Per-locus counts of `gene`/`CDS`/`tRNA`/`rRNA`/`ncRNA`/`tmRNA` parsed from `PU3_all.gb` | C7, C8 |
| `prokka_out/PU3.gff`, `PU3.gbk`, `PU3.faa`, `PU3.ffn`, `PU3.tsv` | Independent Prokka 1.14.6 annotation | C7, C8, C11 |
| `report/evidence/bacteriocin_window.gff` | Prokka GFF filtered to chromosome 1,561,101–1,586,810 (bacteriocin cluster) | C11 |
| `fastani_out.tsv` | FastANI PU3 vs {M19, WCFS1} | C9, C12 |
| `mash_dist.tsv` | Mash distances PU3 vs {M19, WCFS1} | C12 (species confirmation) |

## Screens

| Path | Tool + DB | Outcome | Supports |
|---|---|---|---|
| `report/evidence/abricate_card.tsv` | Abricate 0.5 + CARD | 1 raw hit (dfrE @ 67.6% cov / 75.5% id), 0 passing @ 80%/80% | C10 |
| `report/evidence/abricate_vfdb.tsv` | Abricate 0.5 + VFDB | 5 raw hits (clfA/clfB fragments @ 12–33% cov), 0 passing @ 80%/80% | C10 |
| `report/evidence/abricate_resfinder.tsv` | Abricate 0.5 + ResFinder | 0 hits | C10 |
| `report/evidence/abricate_argannot.tsv` | Abricate 0.5 + ARG-ANNOT | 0 hits | C10 |

## LLM-judge outputs

| Path | Judge | Verdict |
|---|---|---|
| `report/evidence/judge_output_gpt4o.txt` | `argo:gpt-4o` | REPLICATED |
| `report/evidence/judge_output_gpt5.txt`  | `argo:gpt-5` | REPLICATED |
| `report/evidence/judge_output_gemini25pro.txt` | `argo:gemini-2.5-pro` | PARTIAL (dissent on C8 gene-count divergence) |

**Consensus:** 2/3 REPLICATED, 1/3 PARTIAL → REPLICATED with acknowledged
annotation-pipeline caveat.

## Report artifacts

| Path | Content |
|---|---|
| `report/REPORT.md` | Canonical replication report (Markdown, 14 KB) |
| `report/REPORT.tex` | Typeset LaTeX version with dedicated GENUINE CRITIQUE section |
| `report/workflow.md` | Numbered workflow (this replication's actual command sequence) |
| `report/open_questions.json` | 5 truly-open scientific questions grounded in PU3 biology |
| `report/failure_analysis.md` | What went wrong, what almost went wrong, what wasn't attempted |
| `report/artifacts_summary.md` | This file |

## Cross-reference: claim → primary evidence artifact

| Claim | Primary evidence artifact(s) |
|---|---|
| C1  Ten accessions deposited | EUtils esummary loop + `genome/PU3_all.fasta` (10 records) |
| C2  Chromosome = 3,180,940 bp | `report/evidence/genome_metrics.tsv` |
| C3  9 plasmids, exact sizes | `report/evidence/genome_metrics.tsv` |
| C4  Chromosome GC = 44.65% | `report/evidence/genome_metrics.tsv` (measured 44.66%) |
| C5  Plasmid GC 35.22–41.08% | `report/evidence/genome_metrics.tsv` (measured 35.23–41.09%) |
| C6  Coverage 162×, MinION, Flye | NCBI Assembly record + BV-BRC `/api/genome/1590.5192` |
| C7  16 rRNA + 72 tRNA | `report/evidence/genbank_feature_counts.txt` + Prokka `PU3.tsv` |
| C8  2,962 genes (2,874 CDS) | Prokka `PU3.tsv` (3,617); PGAP re-annotation (3,273); BV-BRC (3,794) |
| C9  99.60% ANI vs M19 | `fastani_out.tsv` (measured 99.6132%) |
| C10 Zero VF/AMR hits | `report/evidence/abricate_{card,vfdb,resfinder,argannot}.tsv` |
| C11 Bacteriocin cluster @ 1.56–1.59 Mb | `report/evidence/bacteriocin_window.gff` |
| C12 Species = L. plantarum | `fastani_out.tsv` + `mash_dist.tsv` |

## BV-BRC references

- BV-BRC genome id: `1590.5192`
- BioProject: PRJNA946199
- Assembly: GCA_045010995.1
