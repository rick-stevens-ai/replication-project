# LUCID100 slot 58 — Soroko et al. 2024, A431 LDR vs HDR corpuscular dose-rate study

**DOI:** [10.3390/cimb46120828](https://doi.org/10.3390/cimb46120828) ·
**PMC:** [PMC11726848](https://pmc.ncbi.nlm.nih.gov/articles/PMC11726848/) ·
**License:** CC BY 4.0 · **Year:** 2024 · **Venue:** *Current Issues in Molecular Biology*

> Soroko SS, Skamnitskiy DV, Gorshkova EN, Kutova OM, Seriev IR, Maslennikova AV,
> Guryev EL, Gudkov SV, Vodeneev VA, Balalaeva IV, Shilyagina NY. *The Dose Rate
> of Corpuscular Ionizing Radiation Strongly Influences the Severity of DNA
> Damage, Cell Cycle Progression and Cellular Senescence in Human Epidermoid
> Carcinoma Cells.* Curr Issues Mol Biol. 2024 Dec 6;46(12):13860-13880.

## What this study actually is

A **wet-lab radiobiology** study, not a simulation. The LUCID100 master TSV
tags it as `simulation/model replication`, but the paper is a head-to-head
comparison of high-dose-rate (HDR, 600 Gy/h, 6 MeV electrons on a Novalis Tx
LINAC) and low-dose-rate (LDR, 0.25-3 Gy/h, ⁹⁰Sr+⁹⁰Y sealed beta sources,
24 h exposure) corpuscular irradiation of A431 human epidermoid carcinoma
cells, with MTT cell viability, fluorescence cell counting, clonogenic
assay, comet assay, flow-cytometry cell-cycle (PI), Annexin V/PI, SA-β-gal
senescence, DCFH₂DA ROS, and giant-cell counting as readouts.

**→ Recommend retag in `LUCID100_SOLID_MASTER_QA.tsv`:**
`worktype: simulation/model replication`  →
`worktype: wet-lab radiobiology assay (dose-rate effect study)`.

## Key headline numbers (from main text)

| Quantity                              | HDR (600 Gy/h, 6 MeV e⁻) | LDR (0.25–3 Gy/h, β) |
| ------------------------------------- | ------------------------ | -------------------- |
| LD₅₀ (Gy, MTT, 72 h)                 | **3.4**                 | **10.8** (≈3.2×)    |
| D₃₇ (Gy, MTT, 72 h)                  | ≈ 8                     | ≈ 20 (≈2.5×)        |
| % DNA in comet tail, 4 Gy             | 5                        | 3                    |
| % DNA in comet tail, 8 Gy             | 8                        | 4                    |
| G2/M arrest at 24 h (≥8 Gy)           | ≈ 100 %                  | none                 |
| 5× increase in giant cells (vs ctrl)  | 16 Gy                    | none                 |
| SA-β-gal fold-change (LD₅₀ / D₃₇)    | not significant          | 1.5 / 2.0            |
| ROS (DCF fluorescence) 40 min, fold   | 15 (8 Gy)                | 4 (≈18 Gy)           |

## Data / code availability

- **Code:** *Not released.* No GitHub / OSF / Zenodo / repository link given.
- **Data:** *Not released as tables.* The Data Availability Statement reads:
  *"The original contributions presented in the study are included in the
  article; further inquiries can be directed to the corresponding author."*
- **Supplementary materials** (downloaded; CC BY 4.0):
  - Figure S1 — representative giant cell after HDR 16 Gy, 72 h
  - Figure S2 — HyPer-sensor H₂O₂ time-course after LDR 0.125 Gy

## Replication scope chosen for this pass

Wet-lab repetition is out of scope (requires a clinical LINAC, sealed ⁹⁰Sr/⁹⁰Y
sources, biosafety facilities, A431 cells, flow cytometer, SA-β-gal kit, ...).
What is feasible from the public artifacts alone is a **light analytical
smoke** of the dose-rate-effect *biophysics*:

1. Fit a Linear-Quadratic (LQ) survival model
   `SF(D) = exp(-α D - G β D²)` to the two reported HDR anchor points
   (LD₅₀, D₃₇), with the Lea–Catcheside G-factor.
2. Solve for the protraction half-time `t½` that, under shared intrinsic
   `(α, β)`, predicts the observed LDR LD₅₀ and D₃₇.
3. Cross-check against the LDR/HDR comet-tail ratio (~0.55 at equal dose)
   using the end-of-exposure residual-break fraction
   `f_res = (1 − exp(−μ t)) / (μ t)` with `μ = ln 2 / t½`.

See `FIRST_PASS_REPORT.md` for the verdict (short version: the *empirical*
3× sparing factor reproduces trivially as a ratio, but a *single* shared
LQ + Lea–Catcheside biophysics cannot fit both the survival and the comet
data with one repair half-time, exposing a known limitation of MTT-as-survival).

## Layout

```
lucid100-corpuscular-doserate-dna-damage-senescence/
├── README.md                        ← this file
├── PROGRESS.md                      ← what was done, when, and by whom
├── FIRST_PASS_REPORT.md             ← verdict + analytic findings
├── artifacts/
│   ├── paper.pdf                    ← Europe PMC PDF
│   ├── paper.txt                    ← pdftotext -layout extraction
│   ├── paper.xml                    ← PMC JATS XML (eutils efetch)
│   ├── cimb-3305746-supplementary.pdf
│   ├── supplement.txt               ← pdftotext of the supplement
│   ├── supplement.zip               ← original MDPI supplement archive
│   ├── pmc_package.tar.gz           ← NCBI OA tarball
│   ├── pmc_package/PMC11726848/…    ← exploded tarball (figures + nxml)
│   └── artifact_manifest.json       ← per-file size + sha256
├── data/
│   └── digitized_values.json        ← all in-text numbers transcribed
├── figures/                         ← Figs 1–7 as JPEGs
├── scripts/
│   └── smoke_lq_doserate.py         ← analytical smoke; runs in <1 s
└── outputs/
    ├── fig_lq_survival.png
    ├── fig_drmf_vs_repair.png
    ├── fig_comet_ratio.png
    ├── fig_hill_mtt.png
    ├── smoke_summary.json
    └── smoke_run.log
```

## How to re-run

```bash
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-corpuscular-doserate-dna-damage-senescence
python3 scripts/smoke_lq_doserate.py     # CPU only, <1 s, no GPU/HPC
```

Dependencies: Python ≥3.9, `numpy`, `matplotlib`. CherryRd is fine.

## How the open-access artifacts were retrieved

`www.mdpi.com` is Akamai-gated against non-browser clients; `pmc.ncbi.nlm.nih.gov`
has an interstitial download page; `pmc.ncbi.nlm.nih.gov/articles/instance/.../bin/*.zip`
returns a reCAPTCHA challenge. Two routes that **did** work:

1. **PDF:** `https://europepmc.org/backend/ptpmcrender.fcgi?accid=PMC11726848&blobtype=pdf`
   (HTTP/1.1 only; HTTP/2 stream is closed mid-response. Curl `--http1.1`.)
2. **Everything else (XML, figures, supplement, JATS):**
   `ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/deprecated/oa_package/6c/f3/PMC11726848.tar.gz`
   listed by `https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id=PMC11726848`.

Worth memoizing for future MDPI/PMC retrievals.
