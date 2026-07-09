# Workflow — Acheva et al. 2017 Replication

## Provenance
- **Paper:** Acheva A, Schettino G, Prise KM. *Pro-inflammatory Signaling in a 3D Organotypic Skin Model after Low LET Irradiation.* Front Immunol 8:82 (2017). doi:10.3389/fimmu.2017.00082
- **Set:** LUCID
- **Verdict:** PARTIAL (5/10 coverage, 7/10 agreement)
- **Backfill date:** 2026-07-05
- **Replicator:** LUCID replication subagent

## Data Flow

```
paper.pdf  (in-repo, archived)
    │
    ├── PDF-text extraction ──► deposit-scan (68,135 chars → 0 hits)
    │                          → confirms 6/22 missing-artifact rule
    │
    ├── Bar-chart digitization (multimodal-LLM read of PDF page rasters
    │       via Argo Claude Sonnet 4.6, free endpoint)
    │
    │       ├── code/digitized_figures.py         (Fig 1, 2, 7A)
    │       └── code/digitized_figures_extra.py   (Fig 3, 4B, 5, 6, 7B)
    │
    ├── Statistical re-analysis
    │       ├── code/replicate_stats.py           (Fig 1, 2A, 2B, 7A Tukey HSDs)
    │       ├── code/replicate_extended.py        (2^-ΔΔCT identity + deposit scan)
    │       └── code/replicate_promo2.py          (Fig 3, 4B, 5B/C, 6, 7B trends + Tukey)
    │
    ├── Machine-readable outputs
    │       ├── results/spotcheck_results.json
    │       ├── results/extended_results.json
    │       └── results/promo2_results.json
    │
    └── Figure regeneration
            └── code/make_figures.py              (produces PNGs from same inputs)
```

## Endpoints Used
- **PDF text extraction:** local (pdftotext / PyMuPDF, no network)
- **Bar-chart digitization:** Argo Claude Sonnet 4.6 (free, `argo:claude-sonnet-4.6`)
- **Statistical routines:** scipy.stats (Tukey HSD), scipy.optimize.curve_fit (4PL)
- No paid APIs, no author contact, no closed data sources, no nested subagents.

## Reproduction (Single Command)
```bash
python3 code/replicate_stats.py && \
python3 code/replicate_extended.py && \
python3 code/replicate_promo2.py && \
python3 code/make_figures.py
```

## Deposits Searched (All Zero Hits)
- **Sequence:** GEO (GSE, GDS, GPL), SRA (SRX/SRP/SRR), ArrayExpress (E-MTAB-*, E-GEOD-*), ENA (ERR*, PRJEB*), BioProject (PRJNA*)
- **Proteomics:** PRIDE (PXD*)
- **General:** Zenodo DOIs, Dryad DOIs, FigShare, Mendeley Data
- **Code:** GitHub, GitLab, Bitbucket URLs
- **Scan scope:** 68,135 chars of PDF text via `code/replicate_extended.py::run_e8`

## Scope Boundary
This is a **computational audit** of the paper's printed summary statistics and identities. It is NOT:
- an independent wet-lab re-execution (would require N/TERT-1 3D organotypic culture facility);
- an independent qPCR/Western/IHC/ELISA re-quantification (raw data not deposited);
- an independent signaling-network model (paper does not present one; this replication does not build one either).

See `report/failure_analysis.md` for the honest what-worked / what-broke summary.
