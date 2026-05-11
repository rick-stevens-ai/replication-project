# Progress Checkpoint — Kandasamy et al. 2022 Replication

## Paper: Probiogenomic In-Silico Analysis and Safety Assessment of L. plantarum DJF10
- DOI: 10.3390/ijms232214494
- PMID: 36430971
- Data: SRR14598288 (Illumina NovaSeq 6000, 14.8M PE reads)
- BioProject: PRJNA731289
- BioSample: SAMN19277818
- No assembled genome deposited; assembled de novo from raw reads

## Status: COMPLETE — PARTIAL REPLICATION

### Completed
- [x] Paper fetched and saved (paper/paper.pdf)
- [x] Quantitative claims extracted (28 claims identified)
- [x] Raw reads downloaded (SRR14598288: 14.8M PE reads)
- [x] FASTQ extraction complete
- [x] Quality trimming with fastp
- [x] Read subsampling (~2M reads, ~100x coverage)
- [x] Genome assembly with SPAdes v4.2 (--isolate --only-assembler)
- [x] Assembly QC with QUAST
- [x] Prokka structural annotation (--noanno; 3,169 CDS, 51 tRNA, 3 rRNA, 1 tmRNA)
- [x] Manual functional annotation (blastp vs SwissProt; 1,720/3,169 annotated)
- [x] ANI analysis with fastANI (7 reference strains; 98.3-99.1%)
- [x] AMR analysis (abricate: CARD + ResFinder + NCBI; all clean)
- [x] Virulence analysis (abricate: VFDB + ecoli_vf + Victors; all clean)
- [x] Plasmid analysis (abricate: PlasmidFinder; no plasmids)
- [x] CRISPR analysis (minced; 1 array, 14 spacers)
- [x] IS element analysis (blastp vs IS database; 19 hits)
- [x] Probiotic gene verification (stress response, BSH, antiporters, sortase, bacteriocin)
- [x] Cold shock protein count verified (5, matching paper exactly)
- [x] Hemolysin tlyA confirmed (41.8% identity)
- [x] COG category assignment (817 unique COGs)
- [x] REPORT.md written with full claim verification table
- [x] Final verdict: PARTIAL REPLICATION — Paper Supported

### Not Tested (web-only tools)
- [ ] PHASTER prophage analysis (web-only)
- [ ] RAST subsystem analysis (web-only)
- [ ] KEGG/BlastKOALA pathway analysis (web-only)
- [ ] dbCAN CAZyme analysis (not installed)
- [ ] IslandViewer genomic islands (web-only)
- [ ] BAGEL4 bacteriocin analysis (web-only)

### Key Results
- Genome: 3,382,068 bp (paper: 3,385,113; Δ=0.09%)
- GC: 44.29% (paper: 44.3%)
- CDS: 3,169 (paper: 3,168)
- ANI: 98.3-99.1% to reference L. plantarum strains
- AMR: 0 genes (3 databases)
- Virulence: 0 factors (3 databases)
- Plasmids: 0 replicons
- Safety: Confirmed safe (no AMR, no VF, no plasmids)
- Probiotic genes: All major categories confirmed

### Checkpoints
- 2026-05-10 08:36 — Started: paper fetched, reads downloaded
- 2026-05-10 08:47 — fastp trimming complete
- 2026-05-10 09:47 — SPAdes assembly started on full reads (killed at K=55)
- 2026-05-10 10:10 — Restarted: subsampled reads, MEGAHIT (segfault), switched to SPAdes --only-assembler
- 2026-05-10 10:21 — SPAdes assembly complete on subsampled reads
- 2026-05-10 10:22 — QUAST complete, assembly verified
- 2026-05-10 10:27 — Prokka annotation complete (--noanno)
- 2026-05-10 10:28 — ANI analysis complete (7 strains)
- 2026-05-10 10:29 — AMR/Virulence/Plasmid screens complete (all clean)
- 2026-05-10 10:30 — CRISPR, IS element analysis complete
- 2026-05-10 10:35 — Functional annotation (SwissProt blast) complete
- 2026-05-10 10:40 — Probiotic gene inventory verified
- 2026-05-10 10:45 — REPORT.md finalized with verdict
