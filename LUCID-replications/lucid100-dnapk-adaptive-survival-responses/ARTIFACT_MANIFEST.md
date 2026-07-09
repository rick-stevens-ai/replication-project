# Artifact Manifest — LUCID100 Slot 29

## Successfully retrieved
| Artifact | Source | Local path | Size | License |
|---|---|---|---|---|
| Full paper PDF | EuropePMC `https://europepmc.org/articles/pmc1533273?pdf=render` | `paper/main.pdf` | 1.0 MB, 5 pp | Public domain (US Govt work / EHP supplement) |
| Text dump | `pdftotext -layout paper/main.pdf` | `paper/main.txt` | 411 lines | derived |
| Table 1 transcription | Manually keyed from PDF | `data/table1_extracted.tsv` | 7 rows | derived |

## Searched but unavailable (no-paid-endpoint policy honored)
| Artifact class | Sources tried | Outcome |
|---|---|---|
| Raw clonogenic counts / colony images | EuropePMC supplementary tab | None present (1998 EHP supplement, no SI section) |
| Flow-cytometry FCS files for Fig 1/2 | Implicit; no FlowRepository entry expected for 1998 | Not deposited; pre-dates FlowRepository (founded ~2012) and ImmPort |
| DNA-PK Western / kinase activity raw blots | Referenced as "Yang et al., in preparation" within paper | Never published as a standalone dataset (followup paper not located via S2 free search) |
| Cell line provenance | Referenced as "provided by M. Brown (Stanford), ref 10 (Kirchgessner 1995, Science 267:1178)" | Cell lines exist (CB-17 and CB-17/scid fibroblasts) — commercial/MTAs only, not redistributable |

## Public databases checked
- **EuropePMC PMC1533273** — paper retrieved; no associated dataset records.
- **GEO / SRA / ArrayExpress** — N/A (no high-throughput data in paper).
- **FlowRepository** — N/A (paper predates platform; figures only show summary curves).
- **Figshare / Zenodo** — no matching records under DOI or PMC search (and not expected for a 1998 EHP supplement).
- **Wayback** — paper text is preserved at the EHP NIEHS URL referenced in the abstract footer; no extra artifacts.

## Closely related upstream artifact (NOT replicated, but cited)
- Kirchgessner et al. 1995, Science 267:1178 — original SCID/CB-17 complementation paper. Cited as ref 10. Available via DOI 10.1126/science.7855601 (paid, not retrieved per policy).

## Summary
The paper itself is the only public artifact. All quantitative content lives in **Table 1** (6 rows × 2 cell lines × mean+SD) and two cell-cycle time-course figures (**Fig 1 panels A–E for CB-17, Fig 2 panels A–E for SCID**, each panel = 4 traces × 8 time points). Everything else is qualitative narrative or Western-blot allusion to unpublished follow-up work.
