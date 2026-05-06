# Progress Log — 26392213 Outer Mucus Niche Replication

## 2026-05-05 10:58 CDT — Started
- Created project directory structure
- Beginning paper download and SRA data identification

## 2026-05-05 11:00 CDT — Paper analyzed, data located
- Read full paper from Nature Comms / PMC
- Key finding: 16S data deposited on Figshare (doi:10.6084/m9.figshare.1499145), NOT SRA
- SRA data (PRJEB8805) = whole-genome isolate sequences only
- Methods: 16S V5-V6, Ion Torrent PGM, QIIME 1.8.0, UCLUST 97%, Greengenes, weighted UniFrac

## 2026-05-05 11:01 CDT — Data downloaded
- Downloaded mapping files — sample structure confirmed
- SPF: 6 mice, Colon/Cecum/Ileum × Mucus/Content, 2 Ion Torrent chips
- sDMDMm2: multiple gnotobiotic mice, similar design
- Downloaded 3 FASTQ files (1.15 GB total), all MD5 checksums verified

## 2026-05-05 11:03 CDT — Environment setup
- Created conda env "microbiome" with Python 3.10
- Installed scikit-bio, biom-format, matplotlib, seaborn, scipy, pandas

## 2026-05-05 11:05 CDT — v1 analysis (bug: shared barcodes across chips)
- Demultiplexing + OTU clustering + diversity analysis completed
- Found significant PERMANOVA p=0.009 (SPF), p=0.004 (sDMDMm2)
- Discovered bug: barcodes reused across chips, need chip-specific mapping

## 2026-05-05 11:08 CDT — v2 analysis (corrected)
- Fixed chip-mapping pairing (chip_1→map1, chip_2→map2)
- 101 SPF samples (vs 54 in v1), 60 sDMDMm2 samples
- PERMANOVA: SPF F=3.03, p=0.001; sDMDMm2 F=4.21, p=0.003
- Effect sizes small: R²=3.0% (SPF), R²=6.8% (sDMDMm2)
- ANOSIM R near zero (0.05-0.06)
- Generated PCoA, alpha diversity, and heatmap figures

## 2026-05-05 11:15 CDT — Report complete
- Wrote comprehensive REPORT.md
- Overall score: 6/10 — Partially Replicated
- Statistical significance replicates, but "distinct niche" is overstated
- Communities largely overlap with subtle compositional shifts
- Gut location explains more variance than mucus-content distinction

## STATUS: COMPLETE ✓
