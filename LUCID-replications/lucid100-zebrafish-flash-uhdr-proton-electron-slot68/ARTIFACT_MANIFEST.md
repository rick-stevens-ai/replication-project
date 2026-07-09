# Artifact manifest — slot 68

All artifacts in this folder were collected on 2026-06-09 by the LUCID100 backfill subagent. Provenance is recorded for every file.

## Primary target
| File | Status | Source / URL | Notes |
|---|---|---|---|
| `artifacts/paper.pdf` (target) | **NOT OBTAINED** | https://doi.org/10.1016/j.radonc.2024.110197 (Elsevier ScienceDirect; CC-BY-NC) | Captcha wall on every fetch path (curl + OpenClaw browser). Title returned: "Are you a robot?" Reference number `a092b8e1bab93e5d` (ScienceDirect). |
| `artifacts/landing_blocked.html` | captured 835 KB | https://www.sciencedirect.com/science/article/pii/S0167814024001191/pdfft | ScienceDirect captcha page (proof of block). |
| `artifacts/hzdr_landing.html` | captured 18 KB | https://www.hzdr.de/publications/Publ-37761-1 | HZDR institutional record. Marked Open Access, but exposes no file/download URL. |
| `artifacts/oai_record.xml` | captured 5 KB | https://www.hzdr.de/publications/OAI-PMH/OpenAIRE?verb=GetRecord&identifier=HZDR:PUBLDB:37761&metadataPrefix=oai_datacite | DataCite metadata. `<datacite:rights>open access</datacite:rights>` but no oaire:file entry. |

## Bibliographic / structured metadata pulled
| Source | Endpoint | Stored in |
|---|---|---|
| Semantic Scholar | `graph/v1/paper/DOI:10.1016/j.radonc.2024.110197?fields=...` | (in `FIRST_PASS_REPORT.md` §Metadata snapshot) |
| Europe PMC core | `webservices/rest/search?query=DOI:10.1016/j.radonc.2024.110197&resultType=core` | (in `FIRST_PASS_REPORT.md`) |
| Unpaywall | `api.unpaywall.org/v2/10.1016/j.radonc.2024.110197` | (in `FIRST_PASS_REPORT.md`) |
| OpenAIRE | `api.openaire.eu/search/publications?doi=10.1016/j.radonc.2024.110197` | (in `FIRST_PASS_REPORT.md`) |

## Context PDFs (obtained, OA)
| File | Size | DOI / URL | Why it matters |
|---|---|---|---|
| `artifacts/flash_meta.pdf` | 3.4 MB | 10.1177/15330338241289990 (Wu et al. 2024, *TCRT* 23) via Europe PMC PDF render (PMC11544673) | Systematic review + meta-analysis of FLASH in animal models incl. zebrafish embryos. Table 2 tabulates the 3 precursor ZFE papers (Beyreuther 2019, Karsch 2022, Saade 2023) with dose / dose-rate / sparing flag. Search cutoff March 2023 — predates target, so target is not in the table, but it's the cleanest external anchor for the FMF plausibility plot. |
| `artifacts/frontiers_phys_sobp_2023.pdf` | 2.0 MB | 10.3389/fphy.2023.1213779 (Frontiers in Physics, OA) | Same Dresden/HZDR group's description of the **passive SOBP generation rig** used for the proton SOBP arm of Horst 2024 — methodological grounding for the beam quality (LET) part of the smoke replication. |

## Extracted text
| File | Source PDF | Lines |
|---|---|---|
| `notes/flash_meta_text.txt` | `flash_meta.pdf` | 654 |
| `notes/frontiers_sobp_text.txt` | `frontiers_phys_sobp_2023.pdf` | 687 |

## Code / data on this paper (replication-relevant)
| Resource | Found? | Notes |
|---|---|---|
| GitHub / GitLab | NO | No code link in paper metadata; group's prior ZFE FLASH papers also publish no code. |
| Zenodo / OSF / Figshare | NO | None advertised. |
| Supplementary tables (publisher) | NOT OBTAINED | Hosted on the same Elsevier endpoint that captcha-blocks. `hasSuppl=N` per Europe PMC. |
| Author public dataset | NO | Not advertised. |
| Meta-analytic table | YES (proxy) | Wu et al. 2024 Table 2 covers 3 sister ZFE studies; usable as external FMF anchor. |

## Negative-result records (so we don't redo these)
- `bioRxiv api.biorxiv.org/details/biorxiv/10.1016/j.radonc.2024.110197` → no preprint.
- `medRxiv` search for Horst+zebrafish+FLASH → no hits.
- `CORE.ac.uk` v3 search by DOI → 0 hits.
- `Europe PMC supplementaryFiles` for PMID 38447870 → no supp files.
- HZDR OAI-PMH `oai_datacite` record carries no `oaire:file` element → repository has no deposited fulltext file, only metadata.

## Reproducibility verdict (one-liner)
> "Target paper is functionally a paywalled CC-BY-NC text with no public dataset, no public code, and no preprint. Replication is artifact-limited, not compute-limited."
