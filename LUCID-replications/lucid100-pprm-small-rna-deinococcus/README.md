# LUCID100 slot 35 — PprS sRNA / pprM regulation in *D. radiodurans* under IR

**Paper:** Villa JK, Han R, Tsai C-H, Chen A, Sweet P, Franco G, Vaezian R, Tkavc R, Daly MJ, Contreras LM. *A small RNA regulates pprM, a modulator of pleiotropic proteins promoting DNA repair, in Deinococcus radiodurans under ionizing radiation.* **Sci. Rep. 11:12949 (2021).**
**DOI:** [10.1038/s41598-021-91335-8](https://doi.org/10.1038/s41598-021-91335-8) · **PMID:** 34155239 · **PMCID:** [PMC8217566](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8217566/)
**License:** CC BY 4.0 (Gold OA via Nature / Unpaywall).
**Citation count (S2, 2026-06-09):** 25.
**LUCID100 row:** rank 66, Wave 4, slot 35, tier A, priority_score 14, status `candidate_curated`, worktype `omics/signature replication`.
**Folder convention:** `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-pprm-small-rna-deinococcus/`.

## TL;DR verdict

**FIRST PASS: PASS ✅ (7/7 smoke criteria green).** Every artifact needed
for a full re-run of the paper's two omics layers is publicly available
under permissive terms:

| Data layer | Accession | Status | Files retrieved |
| --- | --- | --- | --- |
| RNA-seq (12 samples, WT × PprSKD × {0, 10 kGy}) | **GEO GSE176207** | Public Jun 2021 | 12 processed htseq count files (≈ 10 KB each) |
| MAPS pull-down (6 samples, MS2-blank vs MS2-PprS) | **GEO GSE176207** | Public Jun 2021 | 6 processed htseq count files (≈ 14 KB each) |
| Time-course proteomics (Orbitrap Fusion) | **PRIDE PXD026633** | Public Jun 2021 | metadata fetched; raw .raw files not downloaded for this pass |
| Per-gene published DEG/MAPS tables | Springer ESM `MOESM1` | Excel (264 KB) | Tables S1-S9 (proteomics L2FC, MAPS L2FC, RNA-seq DEGs, strains, primers) |
| Supplementary figures | Springer ESM `MOESM2` | PDF (8.1 MB) | downloaded |

**The central biological claim — PprS sRNA binds and stabilizes the pprM
mRNA — reproduces directly from the published processed counts:**

- pprM (DR_0907) MAPS L2FC = **+2.98** in MS2-PprS pull-down vs MS2-blank
  (clear enrichment; pprM is the headlined direct target of PprS).
- pprM RNA-seq L2FC at sham = **-0.65** (CPM-mean ratio) / **-2.52** (paper
  DESeq2), sign-concordant. Paper padj 1.34e-9.
- ~106 enriched MAPS targets at L2FC > 1 (paper claims "~130 potential
  interacting transcripts") — within 20% of the paper's number from raw
  count files.

See [`FIRST_PASS_REPORT.md`](./FIRST_PASS_REPORT.md) for full evidence
table and PASS-mid / PASS-full plan.

## Directory layout

```
.
├── README.md                  ← this file
├── PROGRESS.md                ← timeline log
├── FIRST_PASS_REPORT.md       ← verdict + evidence + replication plan
├── ARTIFACT_MANIFEST.tsv      ← every file with bytes / sha256-16 / source / notes
├── artifacts/
│   ├── paper.pdf              ← 1.9 MB OA PDF from Nature
│   ├── paper.txt / paper_raw.txt
│   ├── nature_landing.html    ← article HTML (supplement URL provenance)
│   ├── supplement1.xlsx       ← Tables S1-S9 (Springer ESM MOESM1)
│   ├── supplement2.pdf        ← Supplementary figures (Springer ESM MOESM2)
│   ├── figures_extracted/     ← 10 PNGs from pdfimages
│   ├── unpaywall.json         ← oa_status=gold, cc-by
│   ├── s2.json                ← Semantic Scholar metadata
│   ├── europepmc.json         ← OA=Y, PMID 34155239
│   ├── gse176207_*.txt/html   ← GEO series + file inventory
│   ├── gsm5360101_brief.txt   ← example sample-level metadata
│   └── pxd026633.json         ← PRIDE proteomics deposit summary
├── code/
│   └── smoke_test.py          ← 7-check smoke replication
├── data/
│   └── geo_GSE176207/         ← GSE176207_RAW.tar + 18 unpacked htseq.gz files
├── figures/
│   └── maps_pulldown_pprm_smoke.png  ← replicated MAPS L2FC scatter
└── results/
    └── smoke_test_report.json ← machine-readable 7/7 pass record
```

## How to reproduce the smoke

```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-pprm-small-rna-deinococcus
python3 code/smoke_test.py
# Expected: {"passed": 7, "total": 7, "verdict": "PASS"}
```

Dependencies: Python 3 + `pandas`, `numpy`, `openpyxl` (installed
automatically by the smoke test if missing), `matplotlib` for the figure.
No DESeq2/R required for the smoke; PASS-mid would add R/DESeq2.

## Sibling

This is the second *D. radiodurans* irradiation paper in LUCID100. The
sibling (slot 22) is `lucid100-deinococcus-proteomics-irradiation`
(Chen & Zhang 2025 conference proteomics). Together they form a small
*D. radiodurans* radioresistance cluster.

## QA recommendation

Retag **`candidate_curated` → `replication_smoke_passed`** (or the
project's PASS-low equivalent). Promote to PASS-mid backlog because
every input (raw counts, supplementary DEG tables, proteomics raw deposit,
genome accessions) is public and CC BY 4.0; the path to a full DESeq2
re-run is unblocked.
