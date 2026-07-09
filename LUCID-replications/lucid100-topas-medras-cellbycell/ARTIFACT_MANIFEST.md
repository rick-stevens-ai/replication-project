# Artifact Manifest — LUCID100 slot 25

All paths relative to `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-topas-medras-cellbycell/`.

## Paper artifacts
| Path | Source | Size | Notes |
|------|--------|------|-------|
| `artifacts/paper.pdf` | `https://iopscience.iop.org/article/10.1088/1361-6560/ae6d6d/pdf` (CC-BY 4.0) | 3.10 MB | 19 pp; XeLaTeX/iText; published 2026-06-03. |
| `artifacts/paper.txt` | `pdftotext` of `paper.pdf` | 1014 lines | Searchable full text. |
| `artifacts/paper_landing.html` | `https://iopscience.iop.org/article/10.1088/1361-6560/ae6d6d` | 336 lines | Metadata (authors, ORCIDs, figure URLs, dates). |
| ❌ `artifacts/supplementary_data1.zip` | `https://doi.org/10.1088/1361-6560/ae6d6d/data1` | n/a | **Blocked by Radware bot challenge** from CherryRd CLI. Fetch via browser session (5-second manual step). |

## Code (author, cloned 2026-06-09)
Repo: `https://github.com/ahlim3/SPT-SDD-Framework` (no upstream LICENSE file; explicit "open-source" statement in paper §Data availability).

| Path | Bytes | Purpose |
|------|------:|---------|
| `code/SPT-SDD-Framework/README.md` | 4260 | Author's own README; mirrors the 3-step pipeline. |
| `code/SPT-SDD-Framework/main_assembler.py` | 2885 | End-to-end entry point. |
| `code/SPT-SDD-Framework/modules/core_utils.py` | — | Energy grid, PDF/CDF, config loader. |
| `code/SPT-SDD-Framework/modules/dose_engine.py` | — | Poisson (high-LET) and dose-matching (low-LET) sampling. |
| `code/SPT-SDD-Framework/modules/sdd_io.py` | — | SDDv2.0 writer, PID reindex, timestamp injector. |
| `code/SPT-SDD-Framework/alpha_config.json` | 451 | High-LET demo (²³⁸Pu α, PDG 1000020040, 0.75 Gy, 10 cells). |
| `code/SPT-SDD-Framework/proton_config.json` | 428 | Low-LET demo (p, PDG 2212, 1.0 Gy, 10 cells). |
| `code/SPT-SDD-Framework/electron_config_time.json` | 463 | Low-LET demo with dose-rate (e⁻, PDG 11, 1.0 Gy @ 0.55 Gy/min). |
| `code/SPT-SDD-Framework/{Alpha,Proton,Electron}_Dummy/Dose/` | 59 MB+19 MB+25 MB | Per-energy `<E>MeV.csv` dose deposition tables. |
| `code/SPT-SDD-Framework/{Alpha,Proton,Electron}_Dummy/SDD/` | (in same dirs) | Per-energy `<E>MeV.txt` single-track damage fragments. |
| `code/SPT-SDD-Framework/Ex_PHASE_SPACE/*.phsp` | 324 KB | Author-trimmed energy spectra (alpha 0.05–7 MeV, proton 0.05–100 MeV, electron 0.001–1 MeV). |
| `code/SPT-SDD-Framework/Average_Dose/*.csv` | 16 KB | Mean-dose-per-particle lookup for Poisson rate in high-LET case. |

**Not in repo (author-excluded; needed for paper-quality reproduction):**
- Full pre-computed SPT-SDD libraries (estimated >50 GB).
- TOPAS-nBio input decks for library generation.
- HPC submission scripts (ORNL CADES).

## Our code
| Path | Purpose |
|------|---------|
| `code/summarize_smoke.py` | Parses SDDv2.0 headers from `*/cell_*.sdd`, writes `results/smoke_summary.csv`. |

## Smoke-test outputs (regenerated 2026-06-09)
| Path | Cells | Notes |
|------|------:|-------|
| `code/SPT-SDD-Framework/Alpha_Simulation/cell_{0..9}.sdd` | 10 | Mean dose 1.05 Gy, mean 2.8 tracks, mean 1033 damages. |
| `code/SPT-SDD-Framework/Proton_Simulation/cell_{0..9}.sdd` | 10 | Mean dose 1.04 Gy, mean 14.4 tracks, mean 2002 damages. |
| `code/SPT-SDD-Framework/Electron_Sim/cell_{0..9}.sdd` | 10 | Mean dose 0.99 Gy, mean 367 tracks, mean 2447 damages; timestamps appended. |
| `results/smoke_summary.csv` | 30 rows | Per-cell `(particle, dose_Gy, primary_tracks, damage_count)`. |

## Upstream references already in the LUCID workspace
| Slot | Path | Relevance |
|------|------|-----------|
| 16 | `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-medras-mc/` | Downstream consumer of these SDD files; already replicated 2026-05-28. |
| 19 (Wave 2 #16) | `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-topas-proton-cellular-response/` | Earlier TOPAS-nBio + MEDRAS application (proton-only); supplies HPC cost baseline. |
