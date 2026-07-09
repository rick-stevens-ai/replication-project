# LUCID100 Slot 52 — Low-dose ionizing radiation, stroke motor recovery, brain rewiring

**Paper:** Au NPB et al. "Low-dose ionizing radiation promotes motor recovery and brain rewiring by resolving inflammatory response after brain injury and stroke." *Brain, Behavior, and Immunity* 115:43–63, Jan 2024 (epub 2023-09-27). DOI: [10.1016/j.bbi.2023.09.015](https://doi.org/10.1016/j.bbi.2023.09.015) · PMID 37774892.

**Source of truth row:** `LUCID100_SOLID_MASTER_QA.tsv` rank 83 (Wave 6, Tier B, priority 13).
**Curator worktype tag:** `omics/signature replication`.
**Actual worktype (verified):** wet-lab mouse study (behavior + MRI + histology + live-cell + EEG) **with** an embedded bulk RNA-seq dataset. See QA-retag recommendation in the report.

## What the paper claims

In adult male C57BL/6 mice, a **single whole-body 300 mGy X-ray dose (LDIR)** delivered shortly after photothrombotic stroke (or controlled cortical impact TBI):

1. reduces infarct volume on MRI and reverses motor deficits (rotarod / grid walk),
2. shifts cortical microglia toward an anti-inflammatory / phagocytic state — transcriptomically and in live-cell chemotaxis/phagocytosis assays,
3. clears glial scar and promotes axonal projections (brain "rewiring") in motor cortex,
4. restores EEG activity months after stroke,
5. retains full motor-recovery efficacy when administration is **delayed by 8 h** post-injury,
6. microglia/macrophage depletion **completely abolishes** the LDIR benefit (causal demonstration).

## Public data inventory (what we actually have)

| Resource | Accession / URL | What it gives | Local copy |
|---|---|---|---|
| Bulk RNA-seq cortex | **GEO GSE244016** | 24 samples = 4 groups × n=3 (uninjured-sham, uninjured-LDIR, D1/D3/D7-stroke-ipsi-sham, D1/D3/D7-stroke-ipsi-LDIR); RawCount + TPM tables per sample (~55k mouse genes); STAR-aligned | `artifacts/GSE244016_RAW.tar` (7.5 MB) + `artifacts/GSE244016_RAW/` (24 .txt.gz) |
| SRA raw FASTQ | PRJNA1020901 / SRX21883864… | Re-quantification only | **not downloaded** (not needed for smoke; would need ~hundreds GB to STAR) |
| Behavior / MRI / EEG / histology data | — | **Not deposited publicly.** No Zenodo / Dryad / OSF / figshare / IDR record discoverable. | n/a |
| Code | — | **No GitHub repo cited.** No protocols.io DOI cited. | n/a |
| Supplementary tables/figures | Elsevier supplementary (paywalled host) | Stat results, DE tables, gene lists | **not retrieved** (closed-access PDF + supplements) |

The full PDF is closed-access (Elsevier ClinicalKey / ScienceDirect) and Unpaywall reports no OA copy as of fetch time. Abstract + GEO metadata are sufficient to scope the replication.

## What this replication delivers

A first-pass artifact harvest + a runnable **smoke replication** of the bulk-RNA-seq pillar (pillar #1 in the paper's causal chain):

- `scripts/smoke_replication.py` — 24-sample raw counts → log2(CPM+1) → per-timepoint Welch t-tests (LDIR vs Sham at D1/D3/D7 ipsi cortex + naive contrast) → Fisher-exact enrichment of LDIR-up and LDIR-down hit lists against five curated mouse gene panels (homeostatic microglia, DAM/phagocytic microglia, pro-inflammatory cytokines, anti-inflammatory/resolution, axonal projection / brain-rewiring).
- Results written to `results/` (smoke_summary.{md,json}, counts/CPM matrices, per-timepoint DE tables, sample metadata).

The smoke deliberately does **not** install DESeq2/edgeR (no R toolchain bootstrap); a Welch t-test on log2(CPM+1) with n=3 is the lightest sane baseline and is the best you can do with three biological replicates per arm before pulling in the full Bioconductor stack.

## Headline smoke result

Running on CherryRd in <10 s, peak memory <500 MB:

- 24 samples loaded cleanly, 55,273 mouse gene symbols, library sizes 18.3M–27.8M (well balanced).
- D1 LDIR-vs-Sham (ipsi): 8 up / 21 down at |logFC|>0.585, p<0.05.
- D3 LDIR-vs-Sham (ipsi): 47 up / 8 down.
- D7 LDIR-vs-Sham (ipsi): 29 up / 10 down.
- **No genes survive BH FDR < 0.1** in any single-timepoint contrast (min BH FDR ≈ 0.78–0.99). This is expected for n=3 vs n=3 Welch tests on noisy bulk cortex RNA — the paper's findings rely on DESeq2 shrinkage + larger curated pathway enrichment.
- Curated-set Fisher enrichment in the LDIR-up nominal hit list: essentially **null** at every timepoint with this minimal baseline (only one suggestive hit: `Slit1` ∈ axonal-projection set at D3, OR 19.0, p 0.055).

**Interpretation:** the GEO data is real, downloads correctly, parses to a usable matrix, and is suitable for a full DESeq2 + MSigDB/REACTOME enrichment + LRT-over-time replication (Wave-7 or upgrade candidate). The naive n=3 Welch baseline is too underpowered to recover the paper's microglial-phenotype-shift narrative on its own; that is a known property of the test, not evidence against the paper.

## Folder layout

```
lucid100-ldir-stroke-motor-recovery-brain-rewiring/
├── README.md                 ← this file
├── PROGRESS.md               ← timestamped run log
├── FIRST_PASS_REPORT.md      ← verdict + reproducibility recipe
├── MANIFEST.json             ← machine-readable artifact list
├── artifacts/
│   ├── GSE244016_RAW.tar
│   └── GSE244016_RAW/        (24 GSM*.txt.gz; RawCount + TPM)
├── scripts/
│   └── smoke_replication.py
├── results/
│   ├── counts_matrix.tsv (55,273 × 24)
│   ├── cpm_log2.tsv      (55,273 × 24)
│   ├── sample_meta.tsv
│   ├── de_{D1,D3,D7,naive}_LDIR_vs_Sham.tsv
│   ├── smoke_summary.json
│   └── smoke_summary.md
├── data/                     (reserved; nothing here)
└── notes/                    (reserved; nothing here)
```

## How to re-run

```bash
cd lucid100-ldir-stroke-motor-recovery-brain-rewiring
python3 scripts/smoke_replication.py
```

Needs only stdlib + pandas + numpy + scipy (preinstalled on CherryRd). Re-downloading the GEO TAR is one curl from `https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE244016&format=file`.

## What is NOT replicated and why

| Endpoint | Why it cannot be smoked from public data |
|---|---|
| Rotarod / grid-walk motor scores | No behavioral data / individual mouse records deposited |
| MRI infarct volume | No raw or processed MRI deposited |
| EEG recovery | No EEG traces deposited |
| Microglia chemotaxis / phagocytosis live-cell videos | Imaging data not deposited |
| Axonal tracing / glial scar histology | No imaging archive |
| Microglia/macrophage depletion rescue | Requires PLX5622 chow experiment in live mice — not a reanalysis target |
| 8-h delayed-dosing protective effect | Same — wet-lab only |

Authoritative replication of those pillars would require either (a) author-deposited supplementary tables of per-mouse measurements (not found), or (b) a wet-lab reproduction (out of scope, no author contact per policy).
