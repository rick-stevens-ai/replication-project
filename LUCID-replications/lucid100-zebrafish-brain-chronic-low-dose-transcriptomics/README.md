# LUCID100 slot 11 — Cantabella et al. 2022 zebrafish brain chronic low-dose transcriptomics

**Source paper**
Cantabella E, Camilleri V, Cavalie I, Dubourg N, Gagnaire B, Charlier TD,
Adam-Guillermin C, Cousin X, Armant O.
*Revealing the Increased Stress Response Behavior through Transcriptomic Analysis
of Adult Zebrafish Brain after Chronic Low to Moderate Dose Rates of Ionizing
Radiation.* **Cancers** 14(15):3793 (2022).
DOI: <https://doi.org/10.3390/cancers14153793> • PMID 35954455 • PMC9367516 • CC-BY 4.0

**LUCID100 record**: rank 42, Wave 2 (priority A, score 19) — `omics/signature replication`
themes: dose-rate / low-dose response, omics / biomarkers / signatures, immune / inflammation / senescence

## TL;DR
> **Verdict: PARTIAL (strong)** — dose-rate-dependent DEG ordering reproduces; full-design
> `~batch+group` matches the paper's 0.05 mGy/h DEG count to within 7 % (29 vs 27); the
> direction-of-effect for every named stress-axis gene (oxt, avp, tph1a, tph2, crx, cyp11c1,
> asip2b, nr4a1) matches the paper at 5 mGy/h; significant biological enrichment for
> neuro/chrono/stress pathways (cerebellum development, circadian regulation, chemical
> synaptic transmission, adrenergic GPCR signaling) recovered. **Coverage 8/10, Agreement 7/10.**
>
> Two unresolved gaps: (i) batch-vs-group confound at 0.5 mGy/h (only EC015) leaves DEG
> count between 5 (with batch term) and 229 (without) vs paper's 200, well-bracketed but
> design-sensitive; (ii) at 5 mGy/h we recover ~83-90 DEGs vs paper's 530, an unexplained
> factor of ~6 likely due to a normalization or model choice (independent filtering / Cooks
> handling) we could not exactly reproduce from the methods text. Pathway-level claims using
> *human orthologues* (paper's choice, GO:0007601 / GO:0008277 / GO:0042428) are not
> matched directly by our zebrafish-only ORA; pathways at the *biological-process level*
> are coherent.

## What we did
- Pulled GEO GSE206573 (processed STAR `ReadsPerGene` counts for 21 samples)
- Built 32 057 × 21 reverse-stranded count matrix (confirmed: ~36× more assigned reads on rev vs fwd)
- Ran DESeq2 (pydeseq2 0.5.x) under three designs that bracket the unstated paper choice:
  1. per-batch (most conservative; faithful to confound structure)
  2. full design `~ batch + group` on all 21 samples (batch-adjusted single model)
  3. pooled controls `~ group` (matches paper number at 0.05 / 0.5 mGy/h closely)
- Looked up named genes (oxt, avp, tph1a, tph2, crx, cyp11c1, asip2b, nr4a1) via Ensembl REST
- Ran GO BP ORA (Fisher right-tail + BH-FDR) against cached Ensembl BioMart annotations

## What we couldn't do (and why)
- **Supplementary Tables S1–S5**: MDPI CDN blocks scripted download; PMC mirror gated by reCAPTCHA → cannot cross-check gene-level DE table or pathway p-values directly against author-provided tables
- **Raw FASTQ → STAR pipeline**: no SRA/ENA accession; raw reads were not deposited
- **Human-orthologue GO enrichment**: paper used `clusterProfiler` + biomaRt-orthologue lookup; we used zebrafish-direct annotation. Not a faithful one-to-one for the specific terms they list

## Directory contents
```
README.md                       ← this file
PROGRESS.md                     ← session/work log
FIRST_PASS_REPORT.md            ← detailed replication report with verdict
ARTIFACT_MANIFEST.md            ← what was harvested, what was generated, what was blocked
data/
  sample_metadata.tsv           ← gsm, batch, group, dose-rate (21 rows)
  GSE206573_RAW.tar             ← original GEO supplementary
  GSE206573_family.soft.gz      ← per-sample metadata from GEO
  filelist.txt                  ← inventory
  counts/GSM62570{33..53}_*.gz  ← 21 per-sample STAR count files
code/
  00_build_count_matrix.py      ← strand-aware count matrix builder
  01_deseq2_de.py               ← per-batch DESeq2
  02_deseq2_pooled.py           ← pooled-control DESeq2 (two designs)
  03_ora.py                     ← Fisher right-tail GO BP ORA
  04_figures.py                 ← bar chart, dose-response, PCA, volcano
results/
  counts_matrix.tsv.gz          ← 32,057 × 21
  library_qc.tsv                ← per-sample STAR QC
  deseq2_*.tsv.gz               ← 8 result tables (different designs)
  deg_count_comparison*.tsv/json
  ora_*.tsv                     ← GO BP enrichment per contrast
  go_bp_drerio.tsv.gz           ← cached BioMart annotation
figures/
  fig1_deg_counts_vs_paper.png  ← paper vs our two designs
  fig2_stress_axis_doserate.png ← log2FC of 8 stress-axis genes across dose rates
  fig3_pca_samples.png          ← PCA; batch effect on PC1
  fig4_volcano_d5.png           ← volcano for 5 mGy/h vs control
paper/
  cantabella-2022-pmc.html      ← PMC open-access mirror
  cantabella-2022.txt           ← extracted plain text
```

## How to reproduce
```bash
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-zebrafish-brain-chronic-low-dose-transcriptomics
python3 -m venv .venv && source .venv/bin/activate
pip install pandas numpy scipy statsmodels matplotlib pydeseq2 gseapy matplotlib-venn scikit-learn
python code/00_build_count_matrix.py
python code/01_deseq2_de.py
python code/02_deseq2_pooled.py
python code/03_ora.py        # fetches Ensembl BioMart on first run
python code/04_figures.py
```
Total wall-clock: ~10 min on a laptop CPU; no GPU; ~15 MB output (excluding `.venv/`).

## License
- This replication code: same as parent LUCID-replications repo
- Cantabella et al. 2022 paper text and figures: CC-BY 4.0
- GSE206573 data: public domain (NCBI)
