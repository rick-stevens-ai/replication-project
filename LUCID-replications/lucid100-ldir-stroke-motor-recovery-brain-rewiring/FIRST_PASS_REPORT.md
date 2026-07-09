# FIRST_PASS_REPORT — LUCID100 slot 52

- **DOI:** 10.1016/j.bbi.2023.09.015
- **PubMed:** 37774892
- **Paper:** Au NPB, Wu T, Kumar G, Jin Y, Li YYT, Chan SL, Lai JHC, Chan KWY, Yu KN, Wang X, Ma CHE. *Low-dose ionizing radiation promotes motor recovery and brain rewiring by resolving inflammatory response after brain injury and stroke.* Brain Behav Immun 115:43–63 (Jan 2024; epub 27 Sep 2023).
- **Senior author:** Chi Him Eddie Ma, Dept of Neuroscience, City University of Hong Kong.
- **Run date:** 2026-06-09 (CherryRd, local; no heavy compute).

## VERDICT: PARTIAL-SUCCESS GO — replication-plausible at the omics pillar; non-replicable at the wet-lab pillars

Public bulk-RNA-seq data (**GSE244016**) for the central transcriptomic claim is fully available, downloads cleanly, and produces a 55,273-gene × 24-sample raw-count matrix on first try. The wet-lab pillars (rotarod, MRI infarct volume, EEG, microglia depletion rescue, axonal tracing) have **no public deposit** and are not replicable from public data under the no-author-contact constraint.

The smoke baseline (Welch t-test on log2(CPM+1), n=3 vs n=3) returns nominal-p hit lists of 8–47 genes per per-day stroke contrast with no BH-FDR-significant hits and essentially null curated-pathway enrichment. That is the **expected** behavior of an n=3 Welch on noisy mouse cortex bulk-RNA-seq; it neither confirms nor refutes the paper's claims and is not a critique of the published analysis. A full GO replication of pillar #1 requires DESeq2 (Bioconductor R sidecar) + MSigDB/REACTOME preranked GSEA, which is the recommended next step.

## What was confirmed

1. **Paper exists, is closed-access**, no Unpaywall OA copy. Abstract + PubMed metadata + GEO record + sample sheet harvested.
2. **GSE244016 is the only deposited dataset**, contains exactly what the paper claims:
   - mouse, cerebral cortex (ipsilateral after stroke), polyA bulk RNA-seq;
   - 2 conditions (sham X-ray vs 300 mGy whole-body X-ray) × 4 timepoints (uninjured naive, D1, D3, D7 post-photothrombotic stroke), n=3 per group;
   - NovaSeq 6000, STAR 2.7.8a, RawCount + TPM tables per sample;
   - GEO metadata field says "UCSC human GRCh38" — confirmed to be a curator typo (gene symbols are mouse: Xkr4, mt-*, Gm26206, etc.);
3. **Smoke replication runs end-to-end in <10 s on CherryRd** (Python stdlib + pandas/numpy/scipy/statsmodels, no R), produces reproducible artifacts (`counts_matrix.tsv`, `cpm_log2.tsv`, `de_*.tsv`, `smoke_summary.{md,json}`).
4. **No paid endpoints used; no author contact; no heavy compute.**

## What could not be confirmed / requires a stronger pipeline

- **FDR-significant DE genes per timepoint:** none with n=3 Welch (min BH FDR 0.78). Authors almost certainly used DESeq2 with empirical Bayes shrinkage; recommend re-running with DESeq2 + LRT across timepoints (sidecar required).
- **Microglia-state enrichment (homeostatic → DAM/phagocytic shift, pro-inflammatory cytokine down-regulation, anti-inflammatory up-regulation) at D3:** essentially null in our nominal-p hit lists. This is sensitive to (a) DE method, (b) pathway library (we used 5 hand-curated panels; paper likely used Reactome / KEGG / GO terms involving "inflammatory response", "microglia activation", "phagocytosis"). Replicating with gseapy preranked + Reactome Mm GMT is the right next step.
- **Behavior, MRI, EEG, histology, depletion rescue, 8-h-delayed-dosing efficacy:** not deposited; non-replicable from public data.
- **Statistical claims in figures/tables:** supplementary file not retrieved (closed-access). Could be retrieved via institutional access if needed.

## QA-retag recommendation

Curator row tags `worktype = omics/signature replication`. **Recommend refining to:**

> `wet-lab animal study + omics component (GSE244016)` — keep this entry in LUCID100; the omics pillar (24-sample bulk RNA-seq, 300 mGy whole-body LDIR in C57BL/6 ipsi cortex at D1/D3/D7 post-photothrombotic stroke) is a legitimate stand-alone signature-replication target. Six other pillars (behavior/MRI/EEG/histology/depletion/delayed-dosing) are out of replication scope and should be marked as such.

**Verdict label for QA TSV update:** `KEEP — partial replication-plausible (omics only); 6 of 7 pillars are wet-lab and out of scope`.

**No-go?** No. This slot is a **GO** for the omics pillar and explicit **NO-GO** for the wet-lab pillars; a single combined NO_GO_REPORT is not appropriate.

## Reproducibility recipe (minimal)

```bash
# 1. Get GEO supplementary (one-shot, 7.5 MB)
curl -sSL -o GSE244016_RAW.tar \
  "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE244016&format=file"
mkdir -p GSE244016_RAW && tar -xf GSE244016_RAW.tar -C GSE244016_RAW

# 2. Build counts + smoke DE (pandas/numpy/scipy preinstalled on CherryRd)
python3 scripts/smoke_replication.py

# 3. Inspect verdict
cat results/smoke_summary.md
```

## Reproducibility recipe (full, recommended for upgrade)

```bash
# In an R sidecar (uicgpu has BiocManager already available)
Rscript - <<'EOF'
library(DESeq2); library(tximport)
counts <- read.delim("results/counts_matrix.tsv", row.names=1)
meta   <- read.delim("results/sample_meta.tsv", row.names=1)
meta$timepoint <- factor(meta$timepoint, levels=c("naive","D1","D3","D7"))
meta$dose      <- factor(ifelse(meta$dose_mGy>0, "LDIR","Sham"), levels=c("Sham","LDIR"))
dds <- DESeqDataSetFromMatrix(counts, meta, ~ timepoint + dose + timepoint:dose)
dds <- DESeq(dds, test="LRT", reduced=~timepoint + dose)
res <- results(dds, name="timepointD3.doseLDIR")
res <- lfcShrink(dds, coef="timepointD3.doseLDIR", type="apeglm", res=res)
write.csv(as.data.frame(res), "results/deseq2_D3_LDIR_interaction.csv")
EOF

# Preranked GSEA with Reactome Mm GMT
python3 -c "import gseapy as gp; gp.prerank(rnk='results/deseq2_D3_LDIR_interaction.rnk', \
  gene_sets='Reactome_2022', outdir='results/gsea_D3')"
```

## Blockers / external dependencies

- No author contact (per policy).
- No paid PDF / supplement retrieval (per policy).
- DESeq2 + gseapy not installed on CherryRd; lightweight to bootstrap on `uicgpu` if upgrade approved.

## Files produced (relative to this directory)

- `README.md` — narrative + folder map + headline result
- `PROGRESS.md` — timestamped run log
- `FIRST_PASS_REPORT.md` — this file
- `MANIFEST.json` — machine-readable artifact list
- `artifacts/GSE244016_RAW.tar` + extracted `artifacts/GSE244016_RAW/` (24 GSM*.txt.gz)
- `scripts/smoke_replication.py`
- `results/counts_matrix.tsv` (55,273 × 24)
- `results/cpm_log2.tsv`
- `results/sample_meta.tsv`
- `results/de_{D1,D3,D7,naive}_LDIR_vs_Sham.tsv`
- `results/smoke_summary.json`
- `results/smoke_summary.md`
