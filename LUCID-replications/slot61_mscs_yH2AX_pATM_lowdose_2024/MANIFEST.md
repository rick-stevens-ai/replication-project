# Artifact Manifest — slot 61

Generated 2026-06-09. All paths relative to this folder.

| Path | sha256 | bytes | source | license / notes |
|---|---|---|---|---|
| `artifacts/paper.pdf` | `8eda57940b86110c7add4f6d54d3a21254503981c40134acbc9e416af1032ab3` | 609395 | https://medradiol.fmbafmbc.ru/journal_medradiol/abstracts/2024/1/15-19.pdf (HTTP 200, application/pdf, 5 pages) | Journal open-access PDF; respect publisher copyright; use for replication study only. |
| `artifacts/paper.txt` | `0f2d851d84e154fba5d1fadda5e67dc7b8458fafdc48dc7027a2d483d4f1134a` | 46153 | `pdftotext -layout paper.pdf` | Full-text Russian + English abstract; used for narrative numerical extraction. |
| `artifacts/fig-000.png` | `1a4819b765a7b130199d2d70a65c6848aaa01bb59829c44ac7de9966841b66b6` | 246718 | `pdfimages -all paper.pdf fig` | Figure 1 raster (4 panels: γH2AX, pATM, colocalization across doses). Awaits manual digitization. |
| `scripts/smoke_replicate.py` | `c50cdf7545c090318b1e7a9079d3b7f8b03e5100cd0710c87cd9d73cdb72651c` | 11099 | this work | Qualitative claim-consistency check + replot template. Numpy + matplotlib only. |
| `outputs/claim_check.csv` | `eb3f4508e1755a3571e304097070ad1ee941bf43e8eb67bb5aeac17776b05105` | 751 | smoke script | Per-claim PASS/FAIL table. |
| `outputs/fig1_qualitative_replication.png` | `a0ae229614a443efd0c4e519ee96fe5c944a55f91ad2411e24f6e9257076607e` | 98141 | smoke script | Two-panel qualitative kinetic plot anchored to verbal numbers. |
| `outputs/summary.txt` | `af7da6763c69c0bcdc67556ed73e6ffca2fbc71d249d4215125a3c0e9eac12fd` | 468 | smoke script | One-line + per-check summary; current run 6/6 PASS. |

## Things NOT in this folder (and why)
- No supplementary data file from publisher — the paper has none.
- No code/repository from authors — none cited.
- No digitized CSV of Figure 1 — environment lacks a working image-vision tool and no GUI digitizer is available; this is the documented blocker (see `FIRST_PASS_REPORT.md`).
- No wet-lab data — out of scope for a desk replication.

## Provenance command log
```
curl -sSL https://medradiol.fmbafmbc.ru/journal_medradiol/abstracts/2024/1/15-19.pdf -o artifacts/paper.pdf
pdftotext -layout artifacts/paper.pdf artifacts/paper.txt
pdfimages -all artifacts/paper.pdf artifacts/fig
python3 scripts/smoke_replicate.py
```
