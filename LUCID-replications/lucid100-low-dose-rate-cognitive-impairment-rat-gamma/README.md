# LUCID100 — Ma et al. 2024, Front. Public Health — Low-dose-rate vs High-dose-rate Cognitive Impairment in Rats

**Paper:** Ma T, Liu K, Sun W, Li X, Li Q, Pan Y, Wang M, Lu X, Feng J, Wang H, Wang T, Zuo C.
"Low-dose-rate induces more severe cognitive impairment than high-dose-rate in rats exposed to chronic low-dose γ-radiation."
*Frontiers in Public Health* 12:1387330 (2024).
**DOI:** [10.3389/fpubh.2024.1387330](https://doi.org/10.3389/fpubh.2024.1387330)
**License:** Frontiers OA, CC-BY
**LUCID100 slot:** Wave 6 rank 86 (max-rate backfill slot 55)

## Study at a glance

| | |
|---|---|
| Species | Sprague-Dawley rats, female, 6–8 weeks, n=36 (12/group) |
| Exposure | Whole-body chronic ⁶⁰Co γ-irradiation, 5 h/day × 30 days |
| LDR arm | 6 mGy/h → cumulative **0.9 Gy** |
| HDR arm | 20 mGy/h → cumulative **3.0 Gy** |
| Control | Sham, same environment |
| Endpoints | 2 weeks / 2 months / 4 months post-irradiation |
| Behavioral | NOR (DI), Y-maze (discrim ratio), SAB (alt %), OFT (center time); n=8/group |
| Functional imaging | ¹⁸F-FDG PET/MR (SUVmax, n=4); ⁹⁹ᵐTc-NaTcO₄ SPECT/CT (BBB, n=3) |
| Histology | Nissl (neuron count, hippocampus CA1/CA3a/b/c, n=5); FJB (glial activation) |
| Immunofluorescence | SYP, Iba-1/CD86 (M1 microglia), GFAP/C3 (A1 astrocytes) |
| Omics | Bulk hippocampal **RNA-seq** (Illumina NovaSeq 6000), Majorbio Bio-pharm; fold change >1.5 & p<0.05 |
| Stats | One-way ANOVA + LSD (parametric); Kruskal-Wallis (non-parametric, n=8 behavior) |

## Headline claim

Chronic low-dose γ at **low dose rate (LDR, 6 mGy/h, 0.9 Gy total)** causes **more severe and persistent cognitive impairment** than the same chronic low-dose at a **high dose rate (HDR, 20 mGy/h, 3 Gy total)**:

* HDR cognitive dysfunction recovers by 4 months; LDR does not.
* HDR causes hippocampal neuron loss (Nissl) + M1 microglia activation.
* LDR causes M1 microglia **and** A1 astrocyte activation, no neuron loss, but persistent chronic inflammation.
* RNA-seq shows **329 DEGs in HDR vs control**, **210 DEGs in LDR vs control**; KEGG enrichment top hit is **PI3K–Akt** in both arms (HDR upregulated, LDR downregulated).

## Worktype assessment — QA retag recommended

The master QA tagged this as `omics/signature replication`. After examining the actual study:

* The paper is primarily a **wet-lab animal in vivo behavioral + neuroinflammation study** (12 of 14 methods sections are wet-lab).
* RNA-seq is **one of many** endpoints, used to nominate the PI3K–Akt mechanism. Raw FASTQ is **not deposited** in GEO/SRA/ENA (search confirmed; data availability statement only points to article + supplementary materials, no accession).
* Differential-expression summary tables and KEGG annotations **are** provided as supplementary xlsx.

**Recommended retag:** `wet-lab in vivo (behavior + IHC + WB) + partial omics summary tables (no public FASTQ)`
→ This is a **mixed wet-lab/partial-omics** study, **not** a pure omics/signature replication candidate. Smoke replication is feasible at the **supplementary-table level**, not at the read-realignment level.

## Replication feasibility — **GO (qualitative + table-level)**

* **OA + supplementary materials fully open** (3 zip files, ~58 MB total) — Frontiers public-pages CDN, no auth needed.
* Supplementary contains **per-figure raw data xlsx** for Figures 1–8 (every quantified endpoint).
* SPSS .sav, GraphPad .pzfx, and SPSS output .spv files included → exact statistical workflow auditable.
* Original IF / Nissl / WB / PET-MR / SPECT-CT images included.
* DEG list (459 unique genes, Ensembl rat IDs) with per-condition direction calls included.
* KEGG enrichment tables (98 pathways HDR, 100 pathways LDR) included.
* **Smoke replication PASSES 9/9 anchors** (see `scripts/smoke_replicate.py`):
  * NOR DI at 2w/2m/4m, Y-maze at 4m, SAB at 2w → Kruskal-Wallis re-derived from the n=8 raw rows
  * HDR DEG count = 329 ✔, LDR DEG count = 210 ✔ (exact match to paper text)
  * PI3K-Akt pathway present in both HDR and LDR KEGG annotations ✔

**Block:** raw RNA-seq FASTQ is not publicly deposited. Re-running the bioinformatics pipeline (HISAT2 → DEGseq) would require contacting authors. Not pursued (per task: no author contact). Summary-level replication is already complete.

## Folder layout

```
.
├── README.md              # this file
├── PROGRESS.md            # turn-by-turn progress log
├── REPORT.md              # first-pass report + verdict
├── MANIFEST.md            # artifact manifest
├── scripts/
│   └── smoke_replicate.py # 9-anchor qualitative + table-level smoke (passes 9/9)
├── artifacts/
│   ├── paper.pdf                  # full open-access PDF
│   ├── article.html               # landing-page HTML (for SM URL discovery)
│   ├── Data_Sheet_{1,2,3}.zip     # original Frontiers supplementary zips
│   ├── Data_Sheet_{1,2,3}/        # extracted (per-figure raw data)
│   └── figures_pub/               # fig1–fig9 publication JPGs
├── data/                  # (empty: no external public dataset to mirror)
├── figures/               # (empty: smoke produces stats only, no plots)
└── notes/                 # (empty: reserved for future deep-dive)
```

## Reproducing the smoke

```bash
cd lucid100-low-dose-rate-cognitive-impairment-rat-gamma
python3 -m pip install --user openpyxl scipy   # if needed
python3 scripts/smoke_replicate.py             # exits 0 on full pass
```

Last verified: 2026-06-09. Runtime <2 s. Pure CPU, no GPU, no network.

## Next actions (if a second pass were budgeted)

1. **Plot replication:** redraw Figures 1–6 from the xlsx data using matplotlib/seaborn and overlay paper values for visual diff. (~30 min, deterministic.)
2. **DEG cross-check:** import `Statistical table of DEGs.xlsx` (459 genes) into a Python/R session, recompute KEGG enrichment using the same gene list against rno KEGG annotation, compare top-10 against paper Figure 8A. (~1 h, no FASTQ needed.)
3. **WB densitometry:** re-quantify β-actin-normalized PI3K/p-PI3K/Akt/p-Akt ratios from the included WB.xlsx; verify the LDR/HDR-driven activation direction. (~15 min.)
4. **Author outreach (NOT in current task):** request GEO/SRA deposit for the FASTQ; this would unlock full transcriptome replication.

## Compute footprint

* Total artifact bytes: ~120 MB (3 zips × 58 MB + 9 JPGs × 3 MB + PDF 6 MB)
* Smoke runtime: <2 s on CPU; ~50 MB RAM peak
* No heavy compute, no HPC job plan needed.
