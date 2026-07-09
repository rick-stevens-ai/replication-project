# Workflow — BVBRC-13 (He 2018, *E. faecalis* environmental adaptation)

**Working dir:** `/Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-13-Efaecalis-envadapt-He2018`
**Replication style:** BV-BRC bacterial-genomics, free-tool only (no paid BV-BRC compute).
**Target:** He Q et al. 2018, *BMC Genomics* 19:527 (doi:10.1186/s12864-018-4887-3).

---

## Executed stages (present in-directory)

The pipeline below is inferred from staged outputs, since `scripts/` is empty and no runnable code was preserved (see `failure_analysis.md` Blocker #3).

### Stage 1 — Genome / proteome ingest
- **Input panel:** 78 *E. faecalis* strains: 15 newly-sequenced dairy isolates + 63 GenBank assemblies, matching the paper's panel.
- **Output:** `data/proteins/*.faa` (78 files) and `data/genome_stats.tsv` (79 rows: header + 78).
- **Verified:** strain count = 78 across every downstream table (C1); niche breakdown matches paper exactly (C2).

### Stage 2 — Genome QC / stats
- **Recomputed from `data/genome_stats.tsv`:** mean genome size = 2.937 ± 0.146 Mb (N=77, excluding Merz96 contaminant), mean GC = 37.40 % (range 36.99–38.03 %).
- **Match:** paper 2.94 ± 0.15 Mb and 37.0–38.0 % GC (C3, C4). Merz96 at 5.21 Mb / 41.2 % GC flagged as non-*E. faecalis*.

### Stage 3 — Pan-genome clustering
- **Tool used:** CD-HIT (produced `.clstr` file). **Exact command line not preserved.**
- **Output:** `results/pangenome/pan_clusters.clstr` (13,255 clusters), `core_clusters.txt` (1,382), `single_copy_core.txt` (1,374), `presence_absence.tsv` (78 × 13,255).
- **Discrepancy:** paper reports 10,573 pan / 1,361 core (SiLiX 80/80). Core matches within 1.5 % (C7 ✅). Pan-genome is +25 % over (C6 ❌).

### Stage 4 — Core-genome alignment
- **Output:** 1,374 per-gene MSAs in `results/phylogeny/alignments/`, plus concatenated `core_concat_full.fasta`, `core_concat_300.fasta`, `core_concat_100.fasta` (all 78 seqs).
- **Missing:** Gblocks-trimmed alignment not explicitly preserved (⚠️ unverifiable). Paper used Gblocks trimming.

### Stage 5 — Phylogeny (**broken**)
- **Tool intended:** FastTree (evident from log content in `core_tree.nwk`).
- **Failure:** `core_tree.nwk` (939 B) contains only FastTree's stderr banner + iteration timings — no Newick string, no terminal `;`. Whoever ran FastTree captured stderr instead of stdout.
- **Consequence:** paper claim C8 (4 branches A=19, B=22, C=16, D=21) is unverifiable in-directory.

### Stage 6 — AR (CARD) survey
- **Input DB:** CARD BLAST database, `data/databases/`.
- **Output:** `results/card/card_blast_raw.txt` (10.6 MB), `ar_per_strain.tsv`, `ar_summary.tsv`.
- **Recomputed:** mean Classic_AR = 7.359 (paper 7.5, C10 ✅); core AR gene set = {lsaA, emeA, efrA, efrB, dfrE} present in all 78 (matches paper exactly, C11 ✅); max Classic_AR = 18 in TX0104, S613, R712, DAPTO_516, DAPTO_512 (matches paper's 5 strains exactly, C12 ✅).

### Stage 7 — VF (VFDB) survey
- **Input DB:** `VFDB_setA_pro.fas` in `data/databases/` (**setA only — paper used setB**).
- **Output:** `results/vfdb/vfdb_blast_raw.txt` (20.6 MB), `vf_per_strain.tsv`, `vf_summary.tsv`.
- **Recomputed:** mean = 20.0 VFs/genome vs paper 23.8 (C13 low); 37 unique VF labels vs paper 60; V583 = 34 vs paper 52 (C14 undercount). Root cause: setA-only run misses predicted/hypothetical VFs in setB.

---

## Stages absent from the paper's methodology

| Stage | Purpose | Why missing |
|---|---|---|
| Scoary pan-GWAS | 293 niche-associated genes (paper's biological centerpiece) | Not attempted; presence/absence matrix exists, niche labels exist, just never joined + Scoary'd. |
| PHASTER prophage scan | 116 intact prophages in 65/78 genomes | Requires nucleotide assemblies (`data/genomes/*.fna`); only proteomes staged. |
| RAST 2.0 / COG functional annotation | Functional category enrichment | Not attempted. |
| Gubbins recombination filter | Recombination-corrected core MSA before phylogeny | Paper used Gubbins; not present here. |

---

## Runbook to close the gaps (1–2 day cleanup, free tools only)

Order is dependency-driven:

1. **Rebuild the tree.**
   `FastTree -gtr -nt results/phylogeny/core_concat_100.fasta > results/phylogeny/core_tree.nwk`
   → closes Blocker #1, unblocks C8 verification.

2. **Run Scoary on the existing matrix.**
   - Build traits TSV: strain × 6 niche one-hot columns from `ar_summary.tsv`.
   - `scoary -g presence_absence.tsv -t traits.tsv -n core_tree.nwk -p 0.05 --collapse -e 1000`
   → closes Blocker #2, tests C9 (293 niche-associated genes).

3. **Re-BLAST VFDB setB.**
   - Fetch `VFDB_setB_pro.fas`; `blastp -db VFDB_setB_pro -query ... -evalue 1e-15 -outfmt 6`; filter ≥95 % identity.
   → closes Blocker #4, tests C13–C14.

4. **Drop or replace Merz96 (N=77 run).**
   - Verify NCBI accession; if wrong, refetch. If genuinely unavailable, drop and rerun pangenome / core / AR / VF tabulations on N=77.
   → closes Blocker #6.

5. **Re-cluster with SiLiX-equivalent 80/80 parameters.**
   - Preferred: `silix -i 0.80 -r 0.80 all_proteins.faa all_vs_all.blast > pan.slx`
   - Fallback: `cd-hit -c 0.80 -aS 0.80 -aL 0.80 -n 5 -i all_proteins.faa -o pan80`
   → closes Blocker #3, tests C6 pan-genome count.

6. **Fetch nucleotide assemblies + PHASTER.**
   - `data/genomes/*.fna` via NCBI datasets (78 accessions).
   - PHASTER (free web) or PHASTEST for high-throughput; per-genome JSON in `results/phaster/`.
   → closes Blocker #5, tests C15.

7. **(Optional) Preserve pipeline as runnable scripts.**
   - Write `scripts/{01_ingest.sh, 02_qc.sh, 03_pangenome.sh, 04_align_tree.sh, 05_ar.sh, 06_vf.sh, 07_scoary.sh, 08_phaster.sh}` so the recorded command lines allow future re-execution without archaeology.

---

## Provenance notes

- No claim in this workflow was accepted from any prior `PROGRESS.md` — every number in the audit table (see `REPORT.md` / `REPORT.tex` §3) was recomputed directly from the staged TSV/FASTA artifacts.
- The absence of `scripts/` is itself a reproducibility hazard: exact command lines for CD-HIT, BLAST thresholds, MSA method, and FastTree invocation are all lost. Future replications should preserve the command lines with the outputs.
