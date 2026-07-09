# Artifacts Summary — LUCID-100 slot 67

## Paper identity
- **Title:** Stochastic modelling of DSB repair after photon and ion irradiation
- **Authors:** Friedland, W.; Kundrát, P.; Jacob, P.
- **Venue:** *Int. J. Radiat. Biol.* 88(1–2):129–136 (2012)
- **DOI:** 10.3109/09553002.2011.611404
- **PMID:** 21823824
- **Institution:** Helmholtz Zentrum München
- **PDF status:** closed access (T&F IJRB); no preprint; S2 abstract field elided by publisher

## In-slot files
| Path | Purpose | Notes |
|---|---|---|
| `REPORT.md` | primary human-readable audit (2026-06-22, re-tiered 2026-06-25) | ~16 KB, canonical narrative |
| `FIRST_PASS_REPORT.md` | 2026-06-09 AMBER-KEEP first pass | ~7 KB |
| `MANIFEST.md` | artefact manifest with sha256 | ~2 KB |
| `PROGRESS.md` | progress log | ~2 KB |
| `README.md` | slot-level overview | ~6 KB |
| `report/REPORT.tex` | this backfill LaTeX audit | new 2026-07-06 |
| `report/open_questions.json` | 5 open questions (Q1–Q5) with basis + next_steps | new 2026-07-06 |
| `report/open_questions_section.tex` | LaTeX version of Q1–Q5 | new 2026-07-06 |
| `report/workflow.md` | tools, versions, effort estimate | new 2026-07-06 |
| `report/artifacts_summary.md` | this file | new 2026-07-06 |
| `report/failure_analysis.md` | honest failure analysis + queue-mismatch flag | new 2026-07-06 |
| `extraction/nougat.mmd` | stub — paper PDF unavailable, so no parse | new 2026-07-06 |
| `code/smoke_friedland2012.py` | analytical biexp-plus-labile fit | in-slot |
| `code/let_sweep_friedland2012.py` | Hill-saturation LET sweep | in-slot |
| `results/smoke_fit_results.json` | fit parameters + 6/6 checks PASS | in-slot |
| `results/let_sweep_results.json` | 8-LET table + 4/6 checks PARTIAL | in-slot |
| `figures/smoke_rejoining.png` | log-log data+fit overlay | in-slot |
| `figures/let_sweep.png` | LET-dependence of complex frac / residual / slow t½ | in-slot |
| `source/openalex_metadata.json` | 14-reference graph | in-slot |
| `source/unpaywall_metadata.json` | confirms is_oa=false, oa_locations=[] | in-slot |
| `source/s2_metadata.json` | TLDR + abstract-elision notice | in-slot |
| `source/references_table.md` | 14 refs w/ OA status | in-slot |

## External accessions / IDs
- **DOI:** 10.3109/09553002.2011.611404
- **PMID:** 21823824
- **OpenAlex ID:** in `source/openalex_metadata.json`
- **Semantic Scholar paper ID:** in `source/s2_metadata.json`

## Missing / not-obtained artifacts
- `paper.pdf` — **not obtained** (closed access). No sha256 possible.
- PARTRAC source — **not obtained** (proprietary, no public mirror).
- Precursor Friedland 2010 (RR1965) parameter tables — **not obtained** (closed access).
- Stenerlöw 2000 measured rejoining kinetics — **not obtained** (closed access).
- Nougat `.mmd` parse — **not possible** (no PDF).
- Marker `.md` parse — **not possible** (no PDF).

## Reproducibility
- Both in-slot scripts are deterministic (no RNG); rerunning produces bit-identical JSON to 8 decimals.
- No external data dependencies; the scripts embed literature-typical reference curves.
- Compute time: sub-second each on CherryRd.
