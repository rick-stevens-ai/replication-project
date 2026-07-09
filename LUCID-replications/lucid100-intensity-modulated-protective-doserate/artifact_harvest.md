# Artifact Harvest — Matsuya et al. 2019

## Files in `evidence/`
| File | Size | Description |
|---|---|---|
| `europepmc.json` | 7.9 KB | EuropePMC core record with full abstract. Confirms title, authors, *Sci Rep* 2019, DOI 10.1038/s41598-019-45960-z, open access. |
| `fullText.xml` | 179 KB | EuropePMC full-text XML (open-access body, methods, Table 1, figures captions). |

## Files in `code/`
| File | Size | Description |
|---|---|---|
| `lq_spotcheck.py` | 3.3 KB | Computes acute LQ survival S(D)=exp(-(α₀D+β₀D²)) for D=0..6 Gy from Table 1 (AGO1522 MF/UF, DU145 MF/UF) and the SLDR half-time t½=ln2/(a+c) from each (a+c). Writes `results/lq_spotcheck.json`. |

## Files in `results/`
| File | Source | Description |
|---|---|---|
| `lq_spotcheck.json` | written by `lq_spotcheck.py` 2026-06-16 21:19 CDT | All numeric outputs (Table 1 parameters echoed; LQ survival vectors; SLDR t½; pass/fail booleans for headline claims i and ii). |
| `lq_spotcheck.txt` | stdout capture 2026-06-16 21:19 CDT | Same as JSON, plus diagnostic prints. |

## Table 1 parameters (transcribed by `lq_spotcheck.py`)
| Condition | α₀ (Gy⁻¹) | β₀ (Gy⁻²) | a+c (h⁻¹) |
|---|---|---|---|
| AGO1522, MF | 0.363 | 0.011 | 0.034 |
| AGO1522, UF | 0.388 | 0.081 | 1.684 |
| DU145, MF   | 0.032 | 0.039 | 2.509 |
| DU145, UF   | 0.022 | 0.041 | 1.506 |

## What is NOT here
- No fit of split-dose / fractionated survival data (would need Eq. 1 of the paper with explicit dose-rate convolution).
- No intercellular-communication branch evaluation (α_b, β_b, δ parameters not in Table 1 transcription).
- No raw clonogenic survival CSV from the authors (paper does not deposit data; figure-digitised values would be needed).
- No replication of the cell-cycle (G1 arrest at 6 h) finding from claim §iii — that requires the wet-lab flow data the paper used.

## Conclusion of harvest
Evidence cleanly supports a SPOT-CHECK of qualitative claims (i) and (ii) from Table 1 in the acute limit. Full IMK and intercellular-communication replication is out of scope for this batch.
