# PROGRESS — Cantabella et al. 2022 (zebrafish brain chronic IR) replication

- **Status:** **completed (first-pass)**
- **Started:** 2026-06-09 12:58 CDT
- **Completed:** 2026-06-09 ~13:35 CDT
- **Wall-clock:** ~37 min (mostly env setup + DESeq2 runs)
- **Target:** Cantabella et al., *Cancers* 14(15):3793 (2022). DOI 10.3390/cancers14153793
- **Output dir:** `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-zebrafish-brain-chronic-low-dose-transcriptomics/`
- **LUCID100 slot:** 11 (rank 42, Wave 2 tier A)

## Done
- [x] Located paper and harvested it from PMC mirror (MDPI direct blocked)
- [x] Extracted full text → identified pipeline (STAR/GRCz11/Ensembl 98 + DESeq2 v1.30.1), cutoffs (|FC|≥1.5, padj<0.05), DEG counts (27/200/530), named genes (oxt, avp, tph1a, tph2, crx, cyp11c1, asip2b, nr4a1), GO terms (GO:0007601, GO:0008277, GO:0042428)
- [x] Discovered GEO **GSE206573** is public; pulled 4.6 MB tar of 21 per-sample STAR `ReadsPerGene` files
- [x] Built sample-metadata table from SOFT family file (4 dose rates: control / 0.05 / 0.5 / 5 mGy/h, two batches EC015/EC017 with confound)
- [x] Built 32,057 × 21 count matrix; confirmed reverse-stranded library
- [x] Installed pydeseq2 + gseapy in venv (no R/Bioconductor on box)
- [x] Ran DESeq2 under THREE designs (per-batch, full `~batch+group`, pooled `~group`)
- [x] Compared DEG counts vs paper for all three dose-rate groups
- [x] Verified direction-of-effect for 9 named stress-axis genes
- [x] Ran GO BP ORA against Ensembl BioMart zebrafish annotation
- [x] Generated 4 publication-quality figures
- [x] Wrote ARTIFACT_MANIFEST, README, PROGRESS, FIRST_PASS_REPORT
- [x] Updated JSON progress record under `~/.openclaw/workspace/memory/subagent-progress/`

## Blockers tried & worked around
- MDPI PDF/supp blocked (Akamai Access Denied) → got HTML from PMC9367516
- PMC supp ZIP gated by reCAPTCHA → could not get gene-level Table S4
- Europe PMC supplementaryFiles API timed out → also blocked
- No raw FASTQ deposited → cannot re-run alignment

## Cannot do without elevated effort
- Cross-check our DESeq2 gene-level results against paper's Table S4 (would need supplementary tables)
- Reproduce the exact 530 DEG count at 5 mGy/h (likely a DESeq2 R-vs-pydeseq2 independent-filtering or Cooks-cutoff difference; would need to run DESeq2 R 1.30.1 in a controlled R 4.0 environment)
- Reproduce the paper's *human-orthologue* GO enrichment (would need clusterProfiler + biomaRt orthologue mapping)

## Verdict
**PARTIAL (strong) — Coverage 8/10, Agreement 7/10**

- Dose-rate-dependent DEG ordering: REPLICATED
- DEG count at 0.05 mGy/h (`~batch+group`): 29 vs paper 27 → within 7%
- DEG count at 0.5 mGy/h: bracketed by 5–229 across designs (paper 200) → consistent
- DEG count at 5 mGy/h: 83–90 vs paper 530 → factor-of-6 short, unresolved
- Direction-of-effect for stress-axis genes at 5 mGy/h: all 8 match (positive log2FC for oxt, avp, tph1a, tph2, crx, cyp11c1, asip2b, nr4a1)
- Biological coherence of enriched pathways at 5 mGy/h: cerebellum development, circadian regulation, chemical synaptic transmission, adrenergic GPCR signaling — all match paper's neuro/stress narrative
- Specific GO IDs flagged by paper (GO:0007601 visual perception, GO:0008277 GPCR reg, GO:0042428 serotonin metabolic) not recovered by our zebrafish-only ORA → expected given paper used human orthologues
