# Artifacts summary — BVBRC-34 (Tekedar et al. 2019, A. veronii pathotype)

**Verdict:** PARTIAL REPLICATION (strong). Independent LLM judge (`argo:gpt-5.2`, free): PARTIAL, coverage 5/5, agreement 5/5.

## Report bundle (`report/`)
| File | Purpose |
|---|---|
| `REPORT.md` | Canonical human-readable replication report (15 KB). |
| `REPORT.tex` | LaTeX version + dedicated "Genuine critique" section. |
| `brief.md` | Original replication brief. |
| `attempt_log.md` | Session-by-session narrative log. |
| `artifact_harvest.md` | Notes on paper artifact discovery + Table 1 extraction. |
| `open_questions.json` | 5 truly-open scientific questions grounded in the paper. |
| `workflow.md` | End-to-end pipeline in 9 stages. |
| `failure_analysis.md` | Honest accounting of what did NOT replicate cleanly. |
| `artifacts_summary.md` | This file. |

## Evidence bundle (`report/evidence/`)
| File | Content | Ties to claim |
|---|---|---|
| `genome_stats.json` | Per-assembly length, GC%, contigs, protein count for all 41 genomes (all match Table 1). | C2 |
| `ani_all.tsv` | fastANI all-vs-all: 1,681 pairs. | C1, C2 |
| `ani_pan_results.json` | ANI summary (ML09-123 rank, species-wide distribution) + pan/core counts. | C1, C2, C3 |
| `mash_dist.tsv` | mash all-vs-all k-mer distances (sketch s=100000). | C1 |
| `mash_ml_nearest.json` | ML09-123 nearest neighbours (TH0426 d=0.00171; Hm21 d=0.03151). | C1 |
| `vfdb_results.json` | VF matrix summary + secretion-system tallies + ML09-123/TH0426 overlap (Jaccard 1.000). | C4, C5 |
| `acc2strain.json` | Accession ↔ strain-name map. | provenance |
| `resolved.tsv` | Table 1 → current NCBI assembly (41/41 resolved). | provenance |
| `ani_heatmap.png` | 41×41 ANI heatmap figure. | C1, C2 |
| `phylo_dendrogram.png` | mash-distance NJ-style dendrogram (ML/TH clade visible). | C1 |
| `vf_counts.png` | Per-genome VF-load bar chart. | C5 |
| `llm_judge_verdict.txt` | Free-endpoint (`argo:gpt-5.2`) independent judge output. | overall verdict |

## Work directory (`work/`, on `uicgpu:/data/stevens/bvbrc34/`)
Not synced back (92 MB genome data).
| File | Role |
|---|---|
| `accessions.tsv` | Table 1 accession list. |
| `match_accessions.py` | 2018-accession → current-NCBI-assembly resolver (41/41). |
| `setup_and_stats.py` | Genome statistics (C2). |
| `run_ani.sh` | fastANI driver. |
| `run_pangenome.sh` | CD-HIT ortholog clustering driver. |
| `run_phylo.sh` | mash sketch + all-vs-all distance driver. |
| `run_vfdb.sh` | 41-genome abricate/VFDB driver. |
| `analyze_ani_pan.py` | ANI + pan/core analysis. |
| `analyze_vfdb.py` | Virulence matrix + secretion-system analysis. |
| `make_figures.py` | Heatmap, dendrogram, VF-count figures. |
| `judge.py` | Free-endpoint LLM-judge driver. |
| `paper.pdf`, `paper_fulltext.xml` | Source paper (Europe PMC OA). |
| `av41.zip` (92 MB) | 41 genome + protein assemblies (NCBI Datasets). |

## Headline numbers reproduced
- 41/41 Table-1 strains resolved to current NCBI assemblies.
- 41/41 genome sizes + GC% match Table 1 (all deltas within noise).
- fastANI: ML09-123 × TH0426 = **99.927%** (essentially clonal); 2nd-nearest = 96.484%.
- mash: ML09-123 nearest = TH0426 (d=0.00171); ~18× closer than the next strain.
- VFDB: ML09-123 (136) ∩ TH0426 (136) = 136, Jaccard **1.000**.
- Core genome 2834 (paper 2855; delta 0.7%). Core fraction 29.3% (paper 30.9%).
- Pan genome 9664 (paper 8710; delta +11%, algorithm-driven).
- 41/41 conserved: T1SS, T2SS, T4P, flagellum. Variable: T3SS 31/41, T6SS 28/41, TAD 12/41.
- 5/5 claims covered, 5/5 agree in direction (magnitude match for C1, C2, C3-core, C4), 0 contradicted.
