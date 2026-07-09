# Artifact manifest — Cantabella et al. 2022 (zebrafish brain chronic low-dose IR)

Paper: Cantabella E, Camilleri V, Cavalie I, Dubourg N, Gagnaire B, Charlier TD,
Adam-Guillermin C, Cousin X, Armant O.
**Revealing the Increased Stress Response Behavior through Transcriptomic Analysis
of Adult Zebrafish Brain after Chronic Low to Moderate Dose Rates of Ionizing
Radiation.** *Cancers* 14(15):3793 (2022).
DOI: <https://doi.org/10.3390/cancers14153793> | PMID: 35954455 | PMC: PMC9367516
License: CC-BY 4.0

## Public artifacts harvested

| Artifact | Source | Local path | Size | Notes |
|---|---|---|---|---|
| Full text (HTML) | PMC PMC9367516 | `paper/cantabella-2022-pmc.html` | ~320 KB | open-access mirror; MDPI PDF blocked |
| Full text (plain) | converted | `paper/cantabella-2022.txt` | ~95 KB | regex-stripped HTML, used for fact extraction |
| GEO supplementary (RAW tar) | GEO FTP, GSE206573 | `data/GSE206573_RAW.tar` | 4.6 MB | 21× STAR `ReadsPerGene` files |
| Per-sample STAR counts | extracted from tar | `data/counts/GSM62570{33..53}_*.counts.txt.gz` | 21 files, ~230 KB each | gene_id, unstranded, fwd, rev |
| GEO SOFT family file | GEO FTP, GSE206573 | `data/GSE206573_family.soft.gz` | 2.9 KB | per-sample metadata |
| GEO file list | GEO FTP | `data/filelist.txt` | 1.8 KB | inventory of the RAW tar |
| Sample metadata table | derived | `data/sample_metadata.tsv` | 21 rows | gsm, label, batch, group, dose_rate, replicate |

## Artifacts NOT obtainable (blockers)

| Artifact | Why blocked | Mitigation |
|---|---|---|
| MDPI supplementary `cancers-14-03793-s001.zip` (Tables S1-S5) | MDPI/CDN serves Akamai "Access Denied" to scripted UA; PMC mirror gated by reCAPTCHA | Could not validate gene-level DEG lists in Table S4 or pathway p-values in Table S3 against paper-provided tables; replication relies on numeric claims in the paper body |
| Raw FASTQ | Not deposited in SRA/ENA (only processed counts in GEO) | Cannot re-run STAR/quantification from raw reads; we accept the authors' STAR/GRCz11/Ensembl-98 counts as ground truth for our analysis |

## Generated artifacts (this replication)

### Code (`code/`)
- `00_build_count_matrix.py` — parse STAR `ReadsPerGene` files, pick strand (reverse, confirmed by ~36× more assigned reads vs forward), build 32k×21 count matrix
- `01_deseq2_de.py` — per-batch DESeq2 (initial, conservative design)
- `02_deseq2_pooled.py` — pooled-control DESeq2 (`~group` and `~batch+group`)
- `03_ora.py` — GO BP over-representation (Fisher right-tail, BH-FDR) using Ensembl BioMart zebrafish BP annotations (16,734 gene-term pairs cached)
- `04_figures.py` — DEG count comparison bar chart, stress-axis dose-response, sample PCA, d5 volcano

### Results (`results/`)
- `counts_matrix.tsv.gz` — 32,057 genes × 21 samples, reverse-stranded counts
- `library_qc.tsv` — per-sample STAR QC (assigned %, library size)
- `deseq2_*.tsv.gz` — 8 DESeq2 result tables under different designs (per-batch, pooled, full ~batch+group)
- `deg_count_comparison.tsv` / `.json` — per-batch DEG count comparison vs paper
- `deg_count_comparison_alt_designs.tsv` — pooled designs vs paper
- `ora_*.tsv` — ORA results per contrast (top 10 BP terms each)
- `go_bp_drerio.tsv.gz` — cached Ensembl BioMart GO BP annotation for *D. rerio*

### Figures (`figures/`)
- `fig1_deg_counts_vs_paper.png` — DEG counts: paper vs ~batch+group vs ~group (pooled)
- `fig2_stress_axis_doserate.png` — log2FC of oxt, avp, tph1a, tph2, crx, cyp11c1, asip2b, nr4a1 across dose rates
- `fig3_pca_samples.png` — PCA on top-2000 variable genes (shows EC015 vs EC017 batch effect on PC1)
- `fig4_volcano_d5.png` — volcano plot for 5 mGy/h vs control with named stress-axis genes annotated

## Environment
- `.venv/` (Python 3.x): pandas 3.0.2, numpy 2.4.3, scipy 1.17.1, statsmodels, pydeseq2, gseapy 1.2.1, matplotlib 3.10.8, matplotlib-venn, scikit-learn
- Heavy compute: none required — entire pipeline runs in &lt; 10 min on CherryRd CPU; total disk &lt; 15 MB excluding venv

## Reproducibility checklist
1. `tar -xf data/GSE206573_RAW.tar -C data/counts/`
2. `python code/00_build_count_matrix.py` → `results/counts_matrix.tsv.gz`
3. `python code/01_deseq2_de.py` and/or `python code/02_deseq2_pooled.py`
4. `python code/03_ora.py` (fetches GO annotation from Ensembl BioMart on first run; cached after)
5. `python code/04_figures.py`
