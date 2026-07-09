# Artifact harvest — BVBRC-76 (Carpi 2021)

## Public artifacts fetched

| Source | URL | Local path | Size | Notes |
|---|---|---|---:|---|
| Paper (OA PDF) | https://europepmc.org/articles/PMC9290807?pdf=render | work/paper.pdf | 1.2 MB | 6-page CC-BY PDF; text extracted with `pdftotext` → `~/.openclaw/workspace/tmp_carpi_paper.txt` (2,912 lines) |
| S2 metadata | https://api.semanticscholar.org/graph/v1/paper/PMID:34216519 | work/paper_meta.json | 2 KB | title, authors, DOI, PMC, TL;DR |
| Cohort census (all L. plantarum complete) | https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/taxon/lactiplantibacillus%20plantarum/dataset_report?filters.assembly_level=complete_genome&filters.exclude_atypical=true&page_size=500 | work/ncbi_lp_complete.json + work/ncbi_lp_all.json | 760 KB | 865 assemblies (2026-07 snapshot); paged via `next_page_token` |
| Paper-era subset (release ≤ 2020-07-31) | (filter of the above) | work/ncbi_lp_paper_era.json + work/lp_refseq_paper_era.{json,tsv} | 470 KB | 251 GCA+GCF; 125 GCF; 124 unique strains |
| 124 FASTA assemblies (RefSeq GCF, ≤2020-07-31) | https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/download (dehydrated + rehydrate) | uicgpu:/gpustor/stevens/bvbrc76-lp/work/lp124_pkg/ | 399 MB | 124 `<acc>_<asm>_genomic.fna` files |
| Wiley supplement Table S5 (probiotic marker genes) | https://onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1111/jam.15199&file=jam15199-sup-0001-Tables.zip | — | — | **BLOCKED** — Cloudflare CAPTCHA HTML returned instead of ZIP |
| PMC OAI supplement package | https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/4e/7f/PMC9290807.tar.gz | — | — | **404** (Object not found) |

## Derived / produced artifacts

| Path | Bytes | Provenance |
|---|---:|---|
| `report/evidence/summary_statistics.txt` | 206 | Roary 3.13.0 output |
| `report/evidence/rarefaction_summary.txt` | 2,038 | Python analysis of Roary Rtabs (see `work/rarefaction_analysis embedded in judge3.py`) |
| `report/evidence/number_of_conserved_genes.Rtab` | 6,200 | Roary rarefaction (10 perms × 124 genomes) |
| `report/evidence/number_of_genes_in_pan_genome.Rtab` | 7,107 | Roary rarefaction (10 perms × 124 genomes) |
| `report/evidence/number_of_new_genes.Rtab` | 4,064 | Roary rarefaction (10 perms × 124 genomes) |
| `report/evidence/number_of_unique_genes.Rtab` | 6,199 | Roary rarefaction (10 perms × 124 genomes) |
| `report/evidence/blast_identity_frequency.Rtab` | 55 | Roary all-vs-all BLASTP identity histogram |
| `report/evidence/gene_presence_absence.csv` | 14,812,417 | Roary per-cluster full annotation (16,522 gene families × 124 strains + header) |
| `report/evidence/judge_results.json` | ~5 KB | Three independent Argo LLM-judge responses (gpt-5.2, gpt-5.4, gemini-2.5-pro), 3/3 PARTIAL |
| `work/lp_all124_accessions.txt` | 124 lines | Deduped RefSeq accession list actually annotated |
| `work/lp_all124_meta.tsv` | 125 lines (incl. header) | accession, strain, release_date |
| `work/prokka_run.sh` | 1.2 KB | 24-way parallel Prokka wrapper |
| `work/roary_run.sh` | 786 B | Roary launcher with paper's thresholds |
| `work/judge3.py` | 3.8 KB | LLM-judge harness (final version) |
| `work/paper.pdf` | 1.2 MB | Cached copy of the paper |
| uicgpu `/gpustor/stevens/bvbrc76-lp/prokka/` | ~1.8 GB | 124 × Prokka annotation dirs (GFF/FAA/FNA/GBK/TSV/TXT/ERR/SQN/LOG each) |
| uicgpu `/gpustor/stevens/bvbrc76-lp/roary/` | ~300 MB | Full Roary tree — includes MCL groups, accessory FASTA + newick, pan-genome reference FASTA, gene-presence CSV |

## Free-endpoint compute

- **uicgpu.tail2cbb22.ts.net** (Tailscale) — 8 × NVIDIA A100 (unused for this task; CPU-only pipeline), 255 CPUs (used up to 32 in parallel), 2 TB RAM (peak ~15 GB). No egress costs. Standard `~/env.sh` sourced for HTTP proxy through <lan-host>:3128.
- **CherryRd (this driver)** — Mac Studio, local, 0 external cost.
- **Argo LLM proxy** at `http://127.0.0.1:44497/v1` — free per standing policy; only free models used (gpt-5.2, gpt-5.4, gemini-2.5-pro).

No paid API calls of any kind were made.
