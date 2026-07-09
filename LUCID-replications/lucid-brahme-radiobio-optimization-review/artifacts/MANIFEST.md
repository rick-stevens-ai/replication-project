# Artifact Manifest — Brahme 2024, DOI 10.29011/2574-7754.101625

## Source artifacts harvested
| Path | Size | SHA-style note | Origin |
|---|---|---|---|
| `paper.pdf` | 4,693,885 B | PDF 1.7 | gavinpublishers.com OA PDF |
| `paper.txt` | 2,159 lines | `pdftotext -layout paper.pdf paper.txt` | local |

## Figures / tables in the paper
- **38 figures**, no numbered tables (a tabular insert appears in Figure 15).
- All figures are conceptual diagrams, replots, or schematic illustrations sourced from the author's earlier work or cited clinical series.
- Notable items:
  - Fig 1, 4: BIOART / TP53-driven response schematics.
  - Fig 6, 7, 8: Cell-survival model evolution (Ln → LQ → RCR → RHR).
  - Fig 10–12: PET-CT IVPA / BIOART illustration on one lung cancer case.
  - Fig 13–18: TCP / NTCP / P+ / γC vs LET (microdosimetric heterogeneity).
  - Fig 15 (tabular insert): γC, σD/D̄, RBE per modality.
  - Fig 16: Lionel Cohen neutron-vs-photon DRR; chordoma 5-yr local control.
  - Fig 19, 20: Low-dose repair initiation; weekly fractionation optimization (Friday/weekend).
  - Fig 22, 25–30: Hypoxia, depth-dose / LET for He–Ne ions.
  - Fig 33: PRIMA-1 / APR-246 TP53 reactivation, U1690 SCLC, 60Co γ-rays.
  - Fig 37, 38: Prostate cancer biochemical relapse-free control: conformal → IMRT → IMPT.

## Data sets
- None deposited. No supplementary archive; no GitHub/Zenodo/Dryad URL in the paper.
- Lionel Cohen neutron/photon DRR data and NIRS chordoma 5-yr LC are clinical/historical and not redistributed by this paper.

## Code
- None.

## Equations of interest (verbatim)
- **Eq (1):** `P+ = PB − PI + δ(1 − PB) PI`, with δ on the order of 0.2 (text near l. 693, l. 1028).
- Poisson eradication `~ e^{-N}` (l. 656).
- `γC ≈ ln(N)/e` low-LET asymptotic slope (l. 1218).
- LQ / RCR / RHR survival forms referenced via Figures 7–8 (parameters not given numerically in this paper; see Brahme refs [1-3, 45]).

## Generated artifacts (this work)
| Path | Type | What |
|---|---|---|
| `smoke/p_plus_smoke.py` | python | Toy reproduction of Eq (1) on sigmoid PB / PI, sweeps δ and γC. |
| `figs/p_plus_smoke.png` | png | 4-panel plot: PB/PI, P+ vs dose for δ ∈ {0, 0.2, 1}, optimum-dose shift, γC effect. |
| `figs/p_plus_smoke.csv` | csv | Raw dose grid with PB, PI, P+(δ=0), P+(δ=0.2), P+(δ=1). |

## What is **not** harvestable
- No raw patient images, no per-voxel D0,eff maps.
- No quantitative LDHS / LDA cell-survival data points (these live in Brahme refs [1-3, 23, 34, 45]).
- No RHR-model parameter table.
