# Artifact manifest — LUCID100 #63

Paper: Guerra Liberal, Parsons & McMahon, *Med Phys* 51(1):591–600 (2024), doi:10.1002/mp.16764.

Collected 2026-06-09 by Ollie (LUCID100 backfill slot 32, Wave 4).

| Path | Bytes | SHA-256 | Source URL | Notes |
| --- | ---: | --- | --- | --- |
| `paper_birmingham_submitted.pdf` | 865 818 | `30315f7764...79e5a` | https://pure-oai.bham.ac.uk/ws/files/207466192/mp.16764.pdf | OA mirror at University of Birmingham (publishedVersion per OpenAlex; cover page added by Birmingham). 10 pages of paper + 1 cover. |
| `paper_birmingham.txt` | 61 332 | (text extract) | (from above PDF via `pdftotext -layout`) | Used for digitizing reported RBE / SER values into `../data/`. |
| `crossref.json` | 11 148 | `ce4a9a0a03...8cb2a` | https://api.crossref.org/works/10.1002/mp.16764 | Crossref full record. CC-BY 4.0 license confirmed. |
| `openalex.json` | 31 220 | `9b17fbc2a4...26030` | https://api.openalex.org/works/doi:10.1002/mp.16764 | OpenAlex full record; lists OA locations, has_fulltext=True. |
| `rbemodels_upstream/RBEModels.py` | 4 249 | `22bf7d2074...85de0` | https://raw.githubusercontent.com/sjmcmahon/RBEModels/master/RBEModels.py | Library of 13 phenomenological proton RBE/LET models by paper's senior author. No LICENSE in upstream repo; treated as "code by same author, fair-use for replication verification". |
| `rbemodels_upstream/rbeAnalysis.py` | 6 523 | `f90892fa36...35ce0` | https://raw.githubusercontent.com/sjmcmahon/RBEModels/master/rbeAnalysis.py | Driver script for RBEModels.py. |

## Items requested but NOT retrieved

| Item | URL | Reason |
| --- | --- | --- |
| Wiley final PDF (`paper.pdf`) | https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/mp.16764 | Cloudflare bot-detection returns 5 KB HTML stub for `curl`. Browser-driven retrieval needed if a byte-identical archive of the published version is required. The Birmingham OA mirror was confirmed equivalent in content. |
| Wiley Supporting Information PDF | (link only visible on JS-rendered landing page) | Same Cloudflare gate. **This is the critical missing artifact** — it holds the per-dose clonogenic survival tables and the Supplementary Table 1 (% DSB repair for the complete set of cell lines). Without it, refitting the LQ parameters is impossible without first digitizing Figure 1 from the PDF. |
| QUB Pure mirror | https://pure.qub.ac.uk/files/525825381/Most_DNA_repair_defects.pdf | Cookies required; alternate Birmingham mirror succeeded so this was not pursued. |

## Code/data availability summary

- **Authors' Data Availability Statement (verbatim):** "All data generated or analyzed during this study are included in this published article and its supplementary information file."
- **No** GitHub, Zenodo, OSF, figshare, or Dryad accession is given.
- **No** statistical analysis code released (GraphPad Prism 9.0 used for LQ fits and ANOVA).
- The senior author has multiple related public repositories that are topically aligned but **not cited as the analysis code for this paper**: `sjmcmahon/RBEModels`, `sjmcmahon/Medras-MC`, `sjmcmahon/MEDRAS`, `sjmcmahon/FLASH-OER`.
