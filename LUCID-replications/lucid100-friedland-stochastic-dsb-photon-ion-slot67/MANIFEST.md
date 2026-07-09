# Artefact manifest — slot 67 Friedland 2012 DSB stochastic

Generated 2026-06-09 by subagent run.

| Path (relative)                                              |     bytes | sha256-12   |
|--------------------------------------------------------------|----------:|-------------|
| README.md                                                    |      5656 | 51fd2f46aee5 |
| PROGRESS.md                                                  |      2008 | 6ccf5347397a |
| MANIFEST.md                                                  |    (this) | —           |
| FIRST_PASS_REPORT.md                                         |   (see f) | —           |
| code/smoke_friedland2012.py                                  |      8651 | eb5749597f3b |
| figures/smoke_rejoining.png                                  |     62523 | 7ece18dd9315 |
| results/smoke_fit_results.json                               |      1751 | 4345d2e9d2bc |
| source/openalex_metadata.json                                |     21597 | b39466ee1a8e |
| source/references_table.md                                   |      3737 | 139aaafd8e19 |
| source/s2_metadata.json                                      |      1344 | 9e43ec2410e6 |
| source/unpaywall_metadata.json                               |      1318 | 4239a51bc0c4 |
| logs/                                                        |     empty | —           |

## Provenance
- `source/openalex_metadata.json` — `GET api.openalex.org/works/doi:10.3109/09553002.2011.611404` 2026-06-09
- `source/unpaywall_metadata.json` — `GET api.unpaywall.org/v2/...` 2026-06-09
- `source/s2_metadata.json` — `GET api.semanticscholar.org/graph/v1/paper/DOI:10.3109/09553002.2011.611404` with `x-api-key` from macOS keychain `semantic-scholar-api-key` 2026-06-09
- `code/smoke_friedland2012.py` — written by subagent; uses literature-typical reference rejoining curves (digitisation-quality), not measured data
- `results/smoke_fit_results.json` — produced by running `python3 code/smoke_friedland2012.py` on CherryRd
- `figures/smoke_rejoining.png` — matplotlib output of same run

## What is NOT here
- Full paper PDF (closed-access, not redistributable).
- PARTRAC source code (proprietary, not publicly released as of 2026-06-09).
- Tabulated model parameters from the paper / its 2010 RR1965 precursor.
- Original Stenerlöw 2000 N-ion vs ⁶⁰Co γ rejoining-kinetics digitisations.
