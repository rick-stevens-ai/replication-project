# Artifact Manifest — LUCID100 slot 80 (Wave 5)

**Paper:** Nair S et al. (2019). *The Impact of Dose Rate on DNA Double-Strand Break Formation and Repair in Human Lymphocytes Exposed to Fast Neutron Irradiation.* Int. J. Mol. Sci. 20(21): 5350.
**DOI:** 10.3390/ijms20215350
**PMID:** 31661782 | **PMCID:** PMC6862539
**OA status:** Open Access (CC-BY 4.0), in EPMC + PMC, `hasSuppl: N`

## Files harvested

| File | Source | HTTP | Size | Notes |
|---|---|---|---|---|
| `paper.pdf` | europepmc.org/articles/PMC6862539?pdf=render | 200 | 1.2 MB | Full rendered PDF (13 pages) |
| `paper.txt` | local `pdftotext -layout paper.pdf` | — | 49 KB | 1043 lines, OCR-quality good; some duplicated lines from layout |
| `paper_fulltext.xml` | EPMC `/PMC6862539/fullTextXML` | 200 | 119 KB | JATS structured full text — best source for clean table extraction |
| `epmc_search.json` | EPMC search API | 200 | — | Metadata + OA flags |

## Source-of-truth row (LUCID100_SOLID_MASTER_QA.tsv)

- rank=80, wave=Wave 5, tier=B, priority_score=13, status=candidate_curated
- declared worktype: `simulation/model replication`
- **assessed actual worktype:** wet-lab radiobiology assay (γ-H2AX foci) + reduced table-curve replication (2nd-order polynomial + single-exponential repair)
- **retag recommendation:** `wet-lab assay / radiobiology table replication`

## Data attempted but not available

- MDPI direct PDF + landing page → HTTP 403 (anti-bot, expected; OA route worked)
- No supplementary material declared by journal or EPMC
- No deposited code / GraphPad project file / raw foci-count CSV
- No public repository linked (NCBI / Zenodo / Figshare / GitHub) — confirmed via paper end matter
- Authors used Microsoft Excel 2013 + GraphPad Prism v5 for fits — no scripts to release

## Extracted numerical artifacts (digitized from PDF text, Tables 1–3)

Stored in `../data/`:
- `table1_induction.csv` — mean γ-H2AX foci per cell, 5 doses × 2 dose rates (n=4 donors)
- `table2_hdr_lq_ratio.csv` — HDR/LDR ratio per dose
- `table3_repair_kinetics.csv` — mean foci vs time post-irradiation, 6 time points × 2 dose rates (1 Gy)
- `paper_key_numbers.json` — abstract-level quantitative claims for smoke checks
