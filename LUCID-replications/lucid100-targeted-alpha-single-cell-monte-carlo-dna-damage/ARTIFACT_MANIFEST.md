# Artifact Manifest

## Primary source
| Item | Location | Source | Date acquired | Notes |
|---|---|---|---|---|
| Paper PDF | `artifacts/paper.pdf` | https://link.springer.com/content/pdf/10.1007/s13246-025-01605-2.pdf | 2026-06-09 | Open access (Springer), 2.4 MB, 14 pages |
| Paper text | `artifacts/paper.txt` | local `pdftotext -layout` | 2026-06-09 | 659 lines, layout-preserved |

## Mirrors / alternative open-access locations
- PubMed Central: https://pmc.ncbi.nlm.nih.gov/articles/PMC12738655/
- QUT ePrints: https://eprints.qut.edu.au/262590/
- Semantic Scholar: https://www.semanticscholar.org/paper/4132b5f54db295eac77fdde67183a8e4a658c611

## Code / data availability (per paper)
- **NO public code repository.** Paper has no Code Availability / Data Availability statement.
- **NO supplementary materials / extended data files** referenced in the article.
- Funding: "no funds, grants, or other support were received."
- Compute: QUT eResearch Office (institutional HPC; no public cluster name or scheduler info).
- Software dependencies named in the paper:
  - **OpenTOPAS 3.9** — open source, https://github.com/OpenTOPAS/OpenTOPAS-public
  - **TOPAS-nBio** — open source extension, https://gitlab.com/topas-nbio/topas-nbio (registration required for binary releases of upstream TOPAS)
  - **Geant4 v11.1** — open source, https://geant4.web.cern.ch/
  - **Geant4-DNA** — bundled with Geant4 ≥ 10.1, https://geant4-dna.in2p3.fr/
  - **DBSCAN scorer** — bundled in TOPAS-nBio (`TsScoreClusteredDNADamage` / similar)

## Reference inputs we'd need to fully rerun
| Input | Status | Source if rerun |
|---|---|---|
| Decay scheme for ²²⁵Ac chain (4α, daughters Fr-221, At-217, Bi-213, Po-213/Tl-209, Pb-209, Bi-209) | Public | NNDC/ENSDF, ICRP-107 |
| Decay scheme for ²²³Ra chain (4α: Rn-219, Po-215, Bi-211, Pb-207) | Public | NNDC/ENSDF, ICRP-107 |
| Decay scheme for ²¹²Pb chain (β to ²¹²Bi; 36% via ²¹²Po α 8.78 MeV, 64% via ²⁰⁸Tl) | Public | NNDC/ENSDF |
| Decay scheme for ²¹¹At chain (58% α 5.87 MeV → ²⁰⁷Bi; 42% EC → ²¹¹Po → α 7.45 MeV) | Public | NNDC/ENSDF |
| G4_WATER density / composition | Public | Geant4 NIST manager |
| g4em-dna physics list defaults | Public | Geant4 11.1 source |
| DBSCAN parameters (5/37.5 eV ramp, 16% DNA frac, 3.2 nm cluster radius) | Public | Stated in paper |

## Authors / contact (no contact will be made by this subagent)
- Adam L. Jolly (QUT)
- **Andrew L. Fielding** (corresponding) — a.fielding@qut.edu.au
- School of Chemistry & Physics + Centre for Biomedical Technologies, Queensland University of Technology, Brisbane, Australia.

## Comparable / prior-art papers cited (for cross-check)
- Guerra Liberal et al. (TOPAS-nBio, α-only discrete sources, used as benchmark in Table 2)
- Berens et al. 2022 (TOPAS-nBio ⁶⁴Cu DSB benchmark)
- ICRP Publication 107 (radionuclide decay data)

## Replication blockers
1. **TOPAS-nBio + Geant4 v11.1 install** — not present on CherryRd; need uicgpu or Aurora.
2. **Compute** — 4 radionuclides × 4 locations × 2 physics lists × 20 repeats × 100 sources ≈ 12,800 independent TOPAS jobs (track-structure heavy in the nucleus). Estimated ~hours on a workstation per config, days serially.
3. **No reference output** — paper does not publish raw scorer dumps, so we can only cross-check the published summary tables/figures.
