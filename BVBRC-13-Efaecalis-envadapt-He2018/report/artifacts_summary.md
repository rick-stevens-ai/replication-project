# Artifacts Summary — BVBRC-13 (He 2018, *E. faecalis*)

**Working dir:** `/Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-13-Efaecalis-envadapt-He2018`
**As of:** 2026-06-25

## Present artifacts

### Inputs
| Path | Size / count | Notes |
|---|---|---|
| `data/proteins/*.faa` | 78 files | One proteome per strain; matches the paper's 78-strain panel. |
| `data/genome_stats.tsv` | 79 lines (1 header + 78) | Size (Mb), contig count, GC (%). Merz96 flagged: 5.21 Mb / 41.2 % GC (not *E. faecalis*). |
| `data/databases/` | multiple | CARD (AR) and VFDB (VF) BLAST DBs. **VFDB is `setA_pro.fas` only.** |

### Pan-genome / core-genome
| Path | Size / count | Notes |
|---|---|---|
| `results/pangenome/pan_clusters.clstr` | 13,255 clusters | CD-HIT format; parameters not preserved. Paper reports 10,573 (SiLiX 80/80). |
| `results/pangenome/core_clusters.txt` | 1,382 | Paper 1,361 (match within 1.5 %). |
| `results/pangenome/single_copy_core.txt` | 1,374 | Used as concatenated-alignment input. |
| `results/pangenome/presence_absence.tsv` | 78 × 13,255 | Ready for Scoary pan-GWAS (Scoary not yet run — see Blocker #2). |

### Phylogeny
| Path | Size / count | Notes |
|---|---|---|
| `results/phylogeny/alignments/` | 1,374 per-gene MSAs | One MSA per single-copy core cluster. |
| `results/phylogeny/core_concat_full.fasta` | 78 seqs | Full concatenation. |
| `results/phylogeny/core_concat_300.fasta` | 78 seqs | 300-gene subset. |
| `results/phylogeny/core_concat_100.fasta` | 78 seqs | 100-gene subset (fastest tree input). |
| `results/phylogeny/core_tree.nwk` | 939 B | **CORRUPT — FastTree stderr log, not a Newick tree.** |

### CARD (AR)
| Path | Size | Notes |
|---|---|---|
| `results/card/card_blast_raw.txt` | 10.6 MB | Raw BLAST tabular output. |
| `results/card/ar_per_strain.tsv` | 78 rows | Per-strain hit list. |
| `results/card/ar_summary.tsv` | 78 rows | Includes `Classic_AR` column and niche label. |

**Key recomputed numbers:**
- Mean Classic_AR = **7.359** (paper 7.5 ✅).
- Core AR gene set (present in all 78) = {**lsaA, emeA, efrA, efrB, dfrE**} (exact match to paper ✅).
- Max Classic_AR = 18 in **TX0104, S613, R712, DAPTO_516, DAPTO_512** (exact match to paper ✅).

### VFDB (VF)
| Path | Size | Notes |
|---|---|---|
| `results/vfdb/vfdb_blast_raw.txt` | 20.6 MB | Raw BLAST tabular output vs setA. |
| `results/vfdb/vf_per_strain.tsv` | 78 rows | |
| `results/vfdb/vf_summary.tsv` | 78 rows | |

**Key recomputed numbers (all low vs paper — see Blocker #4):**
- Mean = **20.0** VFs/genome (paper 23.8).
- **37** unique VF labels (paper 60).
- V583 = **34** (paper 52); third behind TX2137=35 and TX0855/T2=34.

---

## Missing artifacts (would close the gap to full replication)

| Artifact | For claim | How to produce (free tools) |
|---|---|---|
| Valid `core_tree.nwk` (proper Newick, terminal `;`) | C8 (4 branches A/B/C/D) | `FastTree -gtr -nt core_concat_100.fasta > core_tree.nwk` — inputs already staged. |
| `results/pangwas/scoary_results.csv` + `traits.tsv` | C9 (293 niche-associated genes) | Scoary 1.6.16 on `presence_absence.tsv` with niche labels from `ar_summary.tsv`, BH p<0.05, 1000 perms. |
| Re-clustered pan-genome at SiLiX 80/80 | C6 (pan = 10,573) | `silix -i 0.80 -r 0.80 …` or `cd-hit -c 0.80 -aS 0.80 -aL 0.80`. |
| Re-BLASTed VF table vs `VFDB_setB_pro.fas` | C13, C14 (60 unique VFs, V583=52) | `blastp -db VFDB_setB_pro …`, E<1e-15, ≥95 % identity. |
| `data/genomes/*.fna` (78 nucleotide assemblies) | Prerequisite for C15 | NCBI datasets fetch per accession in `ar_summary.tsv`. |
| PHASTER per-genome output | C15 (116 intact prophages in 65/78 genomes) | PHASTER (free web) or PHASTEST batch mode. |
| Merz96 replacement (or drop + N=77 rerun) | Contaminant hygiene (Blocker #6) | Verify NCBI accession; refetch or drop. |
| `scripts/` with runnable pipeline | Reproducibility hygiene | Preserve exact CD-HIT, BLAST, MSA, FastTree, Scoary command lines. |
| RAST 2.0 / COG functional annotation | Paper's Fig. 4 functional category enrichment | RAST-tk (SEED), COGclassifier (both free). |
| Gubbins recombination filter | Paper's Methods (pre-phylogeny cleanup) | `run_gubbins.py core_concat_full.fasta`. |

---

## Directory footprint (staged raw data + intermediate)

- Total present output surface: ~35 MB of BLAST/TSV artifacts + 78 proteomes + 1,374 per-gene MSAs + 3 concatenated alignments.
- Missing footprint (estimated to close gap): +78 nucleotide assemblies (~200 MB), +Scoary output (<1 MB), +PHASTER output (~50 MB), +setB VFDB BLAST (~40 MB), +optional Gubbins output (~50 MB).

---

## One-line status per stage

- **Ingest / QC / core / AR:** ✅ replicated cleanly (numbers match).
- **Pan-genome:** ⚠️ present but over-fragmented (+25 %) — parameters lost.
- **Phylogeny:** ❌ input alignment present, tree file corrupt.
- **VF:** ⚠️ present but low-count (setA vs paper's setB).
- **Scoary / PHASTER / RAST / Gubbins:** ❌ not attempted.
