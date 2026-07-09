# LUCID100 slot 22 — *D. radiodurans* irradiation proteomics

**Paper:** Chen C, Zhang Y. *Proteomic Profiling of Deinococcus radiodurans Reveals Irradiation-Induced Proteins and Their Associated Functional Pathways.* **J. Phys.: Conf. Ser. 3109 (2025) 012098.**
**DOI:** [10.1088/1742-6596/3109/1/012098](https://doi.org/10.1088/1742-6596/3109/1/012098)
**License:** CC BY 4.0 (Gold OA via IOP / Unpaywall).
**Citation count (S2, 2026-06-09):** 0 (conference proceedings; The Second International Conference on Space Science and Technology).
**LUCID100 row:** rank 53, Wave 3, slot 22, tier A, priority_score 17, status `candidate_curated`, worktype `omics/signature replication`.
**Folder convention:** `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-deinococcus-proteomics-irradiation/`.

## TL;DR verdict

**FIRST PASS: PASS-low ✅ (all 7 smoke criteria green).** The paper, the
reference proteome it depended on (UniProt **UP000002524**, *D. radiodurans*
R1, 3,085 proteins), and the three named irradiation-induced DNA-repair
proteins (RuvC `Q9RX75`, DdrA `Q9RX92`, DdrB `Q9RY80`) all resolve, and the
authors' Figure 2b Venn arithmetic is internally consistent
(2,034 + 142 + 62 = 2,238 detected, ~72% of the reference proteome — well
within the plausible LC-MS/MS coverage band).

**PASS-mid / PASS-full: NO-GO unless authors deposit raw data or release a
supplement.** See [`FIRST_PASS_REPORT.md`](./FIRST_PASS_REPORT.md) for full
reasoning. Key blockers (single-paragraph form): the paper does **not**
publish the 62 irradiation-induced protein list, does **not** publish the
142 control-only list, and lists **no** ProteomeXchange / PRIDE / MassIVE /
jPOST accession for the raw `Q Exactive HF-X` LC-MS/MS files. The same
lab (Yongqian Zhang at Beijing Institute of Technology) routinely
deposits in PRIDE for other studies (PXD035309, PXD062500) but did not
do so for this conference paper. Without raw spectra **or** a supplement
table, neither the protein identifications nor the GO enrichment can be
re-run from public data.

## Directory layout

```
.
├── README.md                  ← this file
├── PROGRESS.md                ← timeline log
├── FIRST_PASS_REPORT.md       ← verdict + evidence
├── ARTIFACT_MANIFEST.tsv      ← every file with bytes / sha256-16 / source / notes
├── artifacts/
│   ├── paper.pdf              ← full 10-page Gold OA PDF (IOP /pdf endpoint)
│   ├── paper.txt              ← pdftotext -layout
│   ├── paper_raw.txt          ← pdftotext -raw
│   ├── iop_landing.html       ← 14 KB Radware bot challenge (provenance only)
│   ├── figures_extracted/     ← 6 PNGs from pdfimages (workflow + Venn + bars)
│   ├── unpaywall.json         ← oa_status=gold, no PDF URL surfaced
│   ├── s2.json                ← Semantic Scholar metadata
│   ├── europepmc.json         ← 0 hits (paper not indexed in Europe PMC)
│   └── pxd062500.json         ← related (different) PRIDE deposit by same lab
├── code/
│   └── smoke_test.py          ← 3-step smoke (proteome / GO / Venn)
├── data/
│   └── UP000002524.json       ← UniProt D. radiodurans R1 reference proteome
├── figures/                   ← (empty — no replicated figures this pass)
└── results/
    └── smoke_test_report.json ← 7/7 criteria pass
```

## How to reproduce the smoke

```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-deinococcus-proteomics-irradiation
python3 code/smoke_test.py
# → writes results/smoke_test_report.json, exits 0 on PASS-low
```

Only stdlib + network access to `rest.uniprot.org`. No paid endpoints,
no heavy compute, no GPU. Runs in <5 s on CherryRd.

## Key methods (as published)

- **Strain.** *Deinococcus radiodurans* CGMCC 1.633 (= R1, ATCC 13939).
- **Irradiation.** ⁶⁰Co γ-source, **6 kGy**, dose rate **30 Gy/min**, at Peking University. Early stationary phase (OD₆₀₀ ≈ 1.5), TGY broth.
- **Recovery sampling.** 0, 1, **3 h** post-irradiation (also 6, 12 h sampled but not analyzed in this paper). 3 biological replicates.
- **MS pipeline.** Lysis in 8 M urea + EDTA + PMSF, probe sonication; trypsin digest (1:50 → 1:100); desalted on Monospin C18; Easy-nLC 1000 + **Q Exactive HFX** in DDA mode, top-20 MS/MS, m/z 350–1500; 90-min gradient.
- **Identification.** **pFind3 v3.2.2** against **UniProtKB UP000002524** (D. radiodurans R1, snapshot 2019-10-02); 20 ppm precursor + fragment; ≤ 3 missed cleavages; Open Search ON; carbamidomethyl-C fixed, oxidation-M variable.
- **Enrichment.** **DAVID Bioinformatics Resources 6.8**, GO_BP / GO_CC / GO_MF, EASE ≤ 0.05, min count 2.
- **Figures.** Python + BioRender.

## Quantitative claims extracted from the paper

| Quantity                                                       | Value          |
|----------------------------------------------------------------|----------------|
| Dose                                                            | 6 kGy γ        |
| Recovery time points analyzed                                  | 0, 1, 3 h      |
| Detected proteins (per group, each time point)                 | ≈ 2,000        |
| Shared between control + radiation                              | **2,034**      |
| Control-only proteins                                          | **142**        |
| Radiation-only proteins (irradiation-induced)                  | **62**         |
| Reference proteome size (UP000002524)                          | **3,085**      |
| Named DDR proteins exclusive to irradiated group               | RuvC, DdrA, DdrB |
| DdrA trend                                                     | monotonic increase 0 h → 3 h |

## Replication-feasibility verdict (per LUCID100 rubric)

| Pass tier | Status | Reason |
|-----------|--------|--------|
| **PASS-low** (artifact harvest + sanity smoke) | ✅ PASS | PDF + UniProt + GO all verifiable |
| **PASS-mid** (regenerate the 62-protein list + GO enrichment) | ⛔ **NO-GO** | Raw `.raw` files not deposited; protein list not published |
| **PASS-full** (rebuild quant pipeline + replicate Figure 4 PSM trajectories) | ⛔ **NO-GO** | Same blocker; PSM-count tables absent |

**QA retag recommendation:** keep `candidate_curated` for the artifact-harvest
tier; flag as `replication_blocked_no_data` for PASS-mid and PASS-full
unless/until (a) the authors deposit raw spectra in PRIDE (their other
work shows they know how) or (b) a supplement appears. The paper itself
is legitimate (real venue, real lab with a track record, real OA Gold
PDF), the *replication* is what's blocked.
