# Artifact Manifest — LUCID100 Wave 1 Slot 6

Paper: Cahill et al. 2023, *Sci. Rep.* 13:918. DOI 10.1038/s41598-022-26976-4.

## Files in this folder

```
README.md                                                   # Replication brief, claims, acceptance criteria
PROGRESS.md                                                 # Running progress log
FIRST_PASS_REPORT.md                                        # Verdict + evidence + T2 HPC job plan
MANIFEST.md                                                 # This file
artifacts/
  cameron2023_scirep.pdf                                    # Publisher OA PDF, 2.9 MB
                                                            # Source: nature.com/articles/s41598-022-26976-4.pdf
                                                            # Downloaded 2026-06-09 via curl
  cameron2023_scirep.txt                                    # pdftotext -layout extraction, 1163 lines
  geo/
    GSE200212_series.soft                                   # GEO series metadata
    GSE200212_samples.soft                                  # GEO per-sample metadata (12 GSM)
    GSE200212_Torpor_vs_control_zebrafish_IDs.txt.gz        # Full DESeq2 result (~32.5k rows)
    GSE200212_Radiation_vs_control_zebrafish_IDs.txt.gz     # Full DESeq2 result (~32.5k rows)
    GSE200212_Torpor_Radiation_vs_control_zebrafish_IDs.txt.gz  # Full DESeq2 result (~32.5k rows)
    GSE200212_DEG_torpor_group_zebrafish_human_IDs.txt.gz       # Human-ortholog subset (~9.4k rows)
    GSE200212_DEG_radiation_group_zebrafish_human_IDs.txt.gz    # Human-ortholog subset (~9.4k rows)
    GSE200212_DEG_torpor_with_radiation_zebrafish_human_IDs.txt.gz  # Human-ortholog subset (~9.4k rows)
repro/
  deg_count_smoke.py                                        # T0 smoke test: re-derives paper's DEG counts
  sha256.txt                                                # SHA-256 of every artifact above
```

## File provenance

| Path | Source | Notes |
|---|---|---|
| `artifacts/cameron2023_scirep.pdf` | `https://www.nature.com/articles/s41598-022-26976-4.pdf` | Open access PDF, retrieved with `curl -sL -A Mozilla/5.0` |
| `artifacts/cameron2023_scirep.txt` | `pdftotext -layout artifacts/cameron2023_scirep.pdf` | macOS / Homebrew poppler |
| `artifacts/geo/GSE200212_*.txt.gz` | `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE200nnn/GSE200212/suppl/` | 6 published DESeq2 output tables |
| `artifacts/geo/GSE200212_series.soft` | `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE200212&targ=self&form=text&view=brief` | GEO series description |
| `artifacts/geo/GSE200212_samples.soft` | `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE200212&targ=gsm&form=text&view=brief` | Per-sample (12 GSMs) metadata |

## Key accessions

| Resource | ID | Use |
|---|---|---|
| GEO Series (primary RNA-seq) | **GSE200212** | 12 liver-RNA samples, 5 conditions × ~2-3 replicates |
| BioProject | **PRJNA823689** | Same study, raw-FASTQ side |
| SRA experiments | **SRX14748159 – SRX14748170** | Per-sample FASTQ download for T2 re-analysis |
| BioProject (validation: bear hibernation) | **PRJNA413091** | Cross-species meta-analysis vs. zebrafish torpor |
| NASA GeneLab (validation: spaceflown mice) | **GLDS-47** | Cross-species meta-analysis vs. zebrafish radiation |
| Reference assembly | **GRCz11** (Danio rerio) | Used by authors; Ensembl 105 GTF a reasonable choice for re-run |

## What is *not* in this folder (and why)

- **Raw FASTQs.** ~120 GB; pulling them is wasted bytes on CherryRd. They are addressable on demand via SRA accessions for a T2 HPC re-run (see job plan in `FIRST_PASS_REPORT.md`).
- **STAR genome index for GRCz11.** ~30 GB. Build on the compute node, not on CherryRd.
- **Bear / spaceflown-mouse cross-validation FASTQs (PRJNA413091, GLDS-47).** Deferred — T3 scope. Same reasoning: large FASTQs only useful on HPC.
- **Author code repository.** The paper does not cite a code repository. The pipeline is described prose-only in §2.4 of the methods (FastQC → Cutadapt → STAR/GRCz11 → HTSeq → DESeq2), with version numbers given for each tool. No GitHub URL, no Snakefile, no `requirements.txt`. The T2 job plan re-creates the pipeline from the published prose.
- **Advaita iPathwayGuide outputs / database snapshot.** Proprietary, paid service. The authors' ORA / pathway results from this tool are not exactly re-creatable. The paper's `Supplementary Tables S5–S33` contain the resulting gene lists; if needed those should be harvested separately from the Nature SOM (not done in this pass).
- **Supplementary tables S1–S33.** The Nature SOM ships these as Excel files; not pulled in this first pass because the T0 reproducibility result is already conclusive without them. If a future deeper audit (T4) is needed, harvest them from `https://static-content.springer.com/esm/art%3A10.1038%2Fs41598-022-26976-4/MediaObjects/41598_2022_26976_MOESM*.xlsx`.

## Mirror under workspace

None this pass — artifacts live only in the Dropbox replication folder. If the workspace mirror at `/Users/stevens/.openclaw/workspace/lucid-replications/slot6-zebrafish-hypothermic/` is needed by a downstream LUCID consumer, it is a single `cp -r` away.
