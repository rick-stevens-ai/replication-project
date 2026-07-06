# Artifacts Summary — Sivakumar et al. 2023 Replication

Inventory of every file produced or pulled for this replication, plus URLs and
accessions traced through it.

## Paper / Source

| File | Size | Notes |
|---|---|---|
| `paper.pdf` | 5,101,724 B | Fetched 2026-07-05 from `https://bmcgenomics.biomedcentral.com/counter/pdf/10.1186/s12864-022-09090-7.pdf`. **sha256:** `e8ff50da7e228d69c2f1fab9b277fbddeae939ebd5580108d8ed94bfdf40dde9`. |
| `paper/paper.html` | ~ 500 KB | BMC article HTML pulled 2026-05-05. |
| `paper/paper_text.txt` | 62 KB (2109 lines) | Text extraction from HTML — was the primary paper-reading substrate for both passes. |
| `extraction/marker.md` | 1.6 KB | Header + provenance note (Marker not run; pdftotext fallback). |
| `extraction/marker.raw.txt` | 73 KB | pdftotext -layout dump of paper.pdf. |
| `extraction/nougat.mmd` | 1.0 KB | Pending-stub with sha256 pinned for later corpus sweep. |

## Paper metadata

- **Title:** Genome sequencing and comparative genomic analysis of bovine mastitis-associated *Staphylococcus aureus* strains from India
- **Authors:** Sivakumar R., Pranav P.S., Annamanedi M., Chandrapriya S., Isloor S., Rajendhran J.*, Hegde N.R.*
- **Journal:** BMC Genomics 24, 44 (2023)
- **DOI:** [10.1186/s12864-022-09090-7](https://doi.org/10.1186/s12864-022-09090-7)
- **Received:** 2022-09-19 · **Accepted:** 2022-12-19 · **Published:** 2023-01-25
- **License:** CC-BY 4.0 (open access)

## Data (BV-BRC pulls)

| File | Size (approx.) | Content |
|---|---|---|
| `data/accessions.txt` | 700 B | 41 NCBI GenBank WGS accessions from the paper's Data Availability paragraph |
| `data/bvbrc_genomes.json` | ~ 20 KB | BV-BRC `genome_id` per accession (all 41 hit) |
| `data/bvbrc_genomes_detail.json` | ~ 250 KB | Full genome metadata (length, GC, contigs, MLST) |
| `data/bvbrc_amr.json` | ~ 100 KB | AMR phenotype records |
| `data/bvbrc_amr_genes.json` | ~ 300 KB | AMR-annotated specialty genes |
| `data/bvbrc_specialty_genes.json` | ~ 2 MB | All specialty genes (AMR + VF + transporters) |
| `data/pangenome_plfam.json` | ~ 30 KB | PLFam per-strain family counts, core/soft/shell/cloud partition |

**BV-BRC endpoint used:** `https://p3.theseed.org/services/data_api/{genome, sp_gene, ...}`

## Analysis outputs

| File | Shape | Content |
|---|---|---|
| `analysis/amr_gene_matrix.tsv` | 41 × 37 | Presence/absence, columns are AMR gene names (CARD + NDARO from BV-BRC) |
| `analysis/vf_gene_matrix.tsv` | 41 × 131 | Presence/absence, columns are VFDB gene names/descriptions |
| `analysis/distance_matrix.tsv` | 41 × 41 | Jaccard distance on PLFam presence vectors |
| `analysis/phylo_tree.nwk` | 41 leaves | UPGMA tree in Newick from the Jaccard matrix; visually recovers 6 major clusters matching paper's Fig. 2 topology (proxy) |

## Report artifacts (8-artifact standard)

| # | File | Present |
|---|---|---|
| 1 | `paper.pdf` | ✅ |
| 2 | `extraction/marker.md` | ✅ (pdftotext fallback; central Marker parse pending) |
| 3 | `extraction/nougat.mmd` | ✅ (pending stub; sha256 pinned) |
| 4 | `report/REPORT.tex` (+ `report/REPORT.md` legacy) | ✅ (LaTeX; pdflatex not attempted in this backfill) |
| 5 | `report/open_questions.json` | ✅ (5 questions, each with basis + next_steps) |
| 6 | `report/workflow.md` | ✅ |
| 7 | `report/artifacts_summary.md` | ✅ (this file) |
| 8 | `report/failure_analysis.md` | ✅ |

## Traces / logs

| Item | Location |
|---|---|
| Checkpoint log (original pass) | `report/PROGRESS.md` (CP1–CP7 with wall-clock stamps) |
| Legacy markdown report | `report/REPORT.md` |
| Empty replication dir | `replication/` (no artifacts placed here in either pass) |

## External accessions traced through this replication

All 41 NCBI GenBank WGS accessions (Sivakumar et al. Data Availability):

```
JAHSUU000000000  JAHSUV000000000  JAHSUK000000000  JAHSUR000000000
JAHSUQ000000000  JAHSUJ000000000  JAHRIE000000000  JAHNVJ000000000
JAHNVI000000000  JAHNVH000000000  JAHNVG000000000  JAHNVE000000000
JAHNVF000000000  JAHNVA000000000  JAHNVC000000000  JAHNVD000000000
JAHNVB000000000  JAHNUY000000000  JAHNUZ000000000  JAHNUW000000000
JAHNUX000000000  JAHNUS000000000  JAHNUT000000000  JAHNUQ000000000
JAHMIQ000000000  JAHMIP000000000  JAHMIR000000000  JAHMIO000000000
JAHLZV000000000  JAHLZT000000000  JAHLZU000000000  JAHLZO000000000
JAHLZM000000000  JAHLZK000000000  JAHLZL000000000  JAHLZJ000000000
JAHLZI000000000  JAHLZS000000000  JAHLZR000000000  JAHLZQ000000000
JAHLZP000000000
```

Reference genome cited by paper (not remapped here): **NZ_CP020656.1** (*S. aureus* K5).
