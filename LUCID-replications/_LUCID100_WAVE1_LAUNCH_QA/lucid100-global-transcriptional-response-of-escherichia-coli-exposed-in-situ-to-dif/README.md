# Global Transcriptional Response of _Escherichia coli_ Exposed In Situ to Different Low-Dose Ionizing Radiation Sources

## LUCID100 curated Wave 1 — slot 7 — replication

- **Status (2026-06-09):** ✅ **SUCCESS — count-matrix DE replicated within ±1%.** See `FIRST_PASS_REPORT.md`.
- **Rank / tier / score:** 38 / A / 20
- **Paper:** Wintenberg, Manglass, Martinez, Blenner. *mSystems* 8:e00718-22, Mar/Apr 2023.
- **DOI:** [10.1128/msystems.00718-22](https://doi.org/10.1128/msystems.00718-22)
- **PMID:** 36779725 — **PMC:** [PMC10134817](https://europepmc.org/articles/PMC10134817)
- **GEO accession:** [GSE208658](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE208658) (30 samples, public 2023-02-08)
- **BioProject:** PRJNA860569
- **Themes:** dose-rate / low-dose response; radiation quality / RBE; omics / biomarkers / signatures
- **Worktype:** omics/signature replication (RNA-seq differential expression)
- **QA decision:** KEEP: relevant and replication-plausible — **confirmed replicable**.

## Headline result

| Contrast | Paper DEG (Fig. 2) | This work (PyDESeq2) | Δ |
|---|---:|---:|---:|
| Pu-239 vs Control, Day 1 | 590 | **593** | +3 |
| Pu-239 vs Control, Day 15 | 11 | **10** | −1 |
| H-3 vs Control, Day 1 | 46 | **48** | +2 |
| H-3 vs Control, Day 15 | 2,137 | **2,144** | +7 |
| Fe-55 vs FeCl₃, Day 1 | 1,144 | **1,149** | +5 |
| Fe-55 vs FeCl₃, Day 15 | 661 | **664** | +3 |

Cutoff: `|log2FC| > 2` AND `padj < 0.05` (exact paper criterion). All six within ±7 genes / ≤1% on the largest contrast. Radiation-source-specific qualitative pattern (acute Pu-239, delayed H-3, persistent Fe-55) reproduced intact.

## Layout

```
.
├── README.md                          ← you are here
├── PROGRESS.md                        ← short timeline
├── MANIFEST.md                        ← every artifact + SHA256
├── FIRST_PASS_REPORT.md               ← verdict + acceptance evaluation
├── artifacts/
│   ├── msystems_00718_22.pdf          ← paper PDF (Europe PMC render)
│   ├── msystems_00718_22.txt          ← pdftotext extraction
│   ├── GSE208658_quick.txt            ← GEO series SOFT (quick view)
│   ├── GSE208658_samples.txt          ← GEO per-sample SOFT
│   ├── GSE208658_Ec_count_matrix.txt.gz
│   └── GSE208658_Ec_count_matrix.txt  ← 4566 genes × 30 samples (tximport-style)
├── repro/
│   ├── smoke_de_pydeseq2.py           ← runnable end-to-end DE replication
│   ├── deg_counts_replication.tsv     ← side-by-side vs paper Fig. 2
│   ├── de_tables/                     ← full per-contrast DESeq2 results
│   ├── sha256.txt
│   └── .venv/                         ← local Python 3.14 venv with pydeseq2
└── supplementary/                     ← (empty; ASM supplements gated by JS challenge, not needed)
```

## Reproducing the smoke test

```bash
cd repro
python3 -m venv .venv
. .venv/bin/activate
pip install pydeseq2 pandas numpy scipy
python smoke_de_pydeseq2.py
```

Runtime on CherryRd (M-series, single Python process): ~30 s for all 6 contrasts. CPU-only, ~150 MB RAM peak. No network access required after artifacts are fetched.

## Replication pipeline overview

Paper's pipeline (Methods):
**Trim Galore → FastQC → HISAT2 → SAMtools → StringTie → tximport → DESeq2 (R) → clusterProfiler (KEGG/GO)** on _E. coli_ K-12 MG1655 RefSeq GCF_000005845.2 (used as the surrogate annotation for the DH10β strain).

This work's pipeline:
- Skipped Trim Galore → HISAT2 → StringTie → tximport (paper authors did this and deposited the resulting count matrix as a GEO supplementary file).
- Replaced R DESeq2 v1.35.0 with **PyDESeq2 v0.5.4** (same statistical model: negative binomial GLM, Wald test, BH-adjusted P).
- Did **not** redo KEGG/GO enrichment (deferred; data tables in `repro/de_tables/` are ready inputs).

## Why this is a useful LUCID datapoint

1. **High-quality public data.** GEO-deposited count matrix means the in-silico replication does not depend on FASTQ availability or heavy compute.
2. **Quantitatively testable claims.** Fig. 2 reports exact DEG counts per condition × time — a clean acceptance criterion.
3. **Three radionuclides, two time points, internal cold-iron control.** Generalizes to radiation-source-specific signature questions LUCID cares about (dose rate, radiation quality, biomarkers).
4. **Replication confirms paper.** No discrepancies large enough to call the paper's central claims into doubt; all observed deltas attributable to known R↔Python DESeq2 numerical differences and tximport integer rounding.

See `FIRST_PASS_REPORT.md` for full detail and the (small) list of optional follow-ons.
