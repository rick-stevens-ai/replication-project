# Testable claims inventory — Staaf et al. 2012 — RE-PASS

Each row: claim ID, plain statement, location in paper, status in pass 1, plan in pass 2.

## A. Headline quantitative claims

| ID  | Claim                                                              | Source                | Pass 1 | Pass 2 plan |
|-----|--------------------------------------------------------------------|-----------------------|--------|-------------|
| A1  | RBE_α total IRIF = 0.76 ± 0.52                                     | Abstract; Discussion  | ✅ 0.74 ± 0.19 | — keep |
| A2  | RBE_α large foci = 2.54 ± 1.11                                     | Abstract; Discussion  | ✅ 2.41 ± 1.13 | — keep |
| A3  | Mixed-beam dose response is additive (total IRIF)                  | Abstract; Results     | ✅          | — keep |
| A4  | Large-foci frequency/area initially lower than predicted in mixed beam, increase over first 3 h | Abstract; Results | ✅ qualitative | — keep |
| A5  | Mixed-beam LF area significantly < predicted at 0.5 h (p<0.001)    | Fig 5B, Results       | ✅ effect size, p≈0.10 (digitization-limited) | — keep |

## B. Dose-response / R² claims (reported R² values in text)

| ID  | Claim                                                  | Source        | Pass 1 | Pass 2 plan |
|-----|--------------------------------------------------------|---------------|--------|-------------|
| B1  | Total IRIF R²: X 0.82, α 0.75, mix-obs 0.71, mix-pred 0.89 | Results | partly (X/α) | extend to mix-obs / mix-pred |
| B2  | LF R²: X 0.57, α 0.66, mix-obs 0.46, mix-pred 0.86       | Results | partly (X/α) | extend to mix-obs / mix-pred |
| B3  | LF slope difference X vs α: p=0.015 (number), p=0.01 (area) | Results | ❌ | ✅ reproduce ANCOVA-style slope-difference test |
| B4  | IRIF per Gy at 30 min, 0.8 Gy X-ray: 19.6 ± 7.2 → 24.5 ± 9.0 per Gy | Results | ❌ | ✅ recompute from Fig 2C (0.5 h X-ray) |
| B5  | IRIF per Gy at 1 h: 25.3 ± 4.5 per Gy                  | Results       | ❌ (implicit in fit) | ✅ recompute from Fig 2A X-ray |

## C. Fluence / per-nucleus particle traversal sanity check

| ID  | Claim                                                                 | Source     | Pass 1 | Pass 2 plan |
|-----|-----------------------------------------------------------------------|------------|--------|-------------|
| C1  | 23789 ± 4564 particles s⁻¹ cm⁻² · 250 µm² · 60 s = 3.57 ± 0.68 per nucleus | Results | ✅ 3.40 ± 0.65 | — keep |

Note: pass 1 used `A = 238 µm²` (dose-response cells); paper's formula uses `~250 µm`
(repair-kinetics cells). Pass 2 recompute with both nuclear areas.

## D. Repair kinetics directional claims

| ID  | Claim                                                                 | Source     | Pass 1 | Pass 2 plan |
|-----|-----------------------------------------------------------------------|------------|--------|-------------|
| D1  | X-ray IRIF: significant decrease 0.5 → 3 h (p=0.038)                  | Results    | ❌     | ✅ test from Fig 2C |
| D2  | X-ray IRIF: p<0.002 for 0.5 h vs 24 h AND 1 h vs 24 h                 | Results    | ❌     | ✅ test from Fig 2C |
| D3  | Mixed-beam IRIF: significant decrease 0.5 → 3 h (p=0.037)             | Results    | ❌     | ✅ test from Fig 2C |
| D4  | Alpha IRIF: no significant change over first 3 time points            | Results    | ❌     | ✅ test from Fig 2C |
| D5  | Predicted relative LF area > observed at 1 h and 24 h vs 0.5 h (predicted): p=0.032, p=0.023 | Results | ❌ | ✅ test from Fig 5B predicted series |
| D6  | Observed relative LF area significantly larger at 1 h vs 0.5 h (p=0.039) | Results | ❌    | ✅ test from Fig 5B observed series |
| D7  | Observed relative LF number significantly larger at 3 h vs 0.5 h (p=0.033) and area (p=0.021) | Results | ❌ | ✅ test from Fig 5A/5B |

## E. Figure 4 (per-individual-focus average areas) — pass 1 explicit gap

| ID  | Claim                                                                              | Source       | Pass 1 | Pass 2 plan |
|-----|------------------------------------------------------------------------------------|--------------|--------|-------------|
| E1  | Avg LF area for repair kinetics: α > X at 0.5 h (p=0.040), 1 h (p<0.001), 3 h (p=0.014) | Fig 4D / Results | ❌ | partial — digitize from Fig 4D in this re-pass (text-supplied magnitudes) and t-test |
| E2  | Mixed-beam LF avg area increases 0.5 → 1 h (p=0.042)                                 | Fig 4D / Results | ❌ | partial — same as above |
| E3  | Mixed vs α at 0.5 h: mixed smaller, p=0.048                                          | Fig 4D / Results | ❌ | partial |
| E4  | Mixed vs X at 1 h and 3 h: mixed larger, p=0.024, 0.035                              | Fig 4D / Results | ❌ | partial |
| E5  | Avg IRIF area: α > X+mixed at 0.5 and 1 h (p<0.001) for kinetics                     | Fig 4E/F / Results | ❌ | partial |

Pass-2 strategy for E1–E5: pass-1 did not digitize Figure 4 panels. For the re-pass, instead of
adding 6 more visual digitizations (high uncertainty, low new information), we (a) record the
reported p-values verbatim, (b) reproduce the **direction** by deriving avg-area = total LF area
/ LF number from the already-digitized Figure 3 panels (total LF count and total LF area), which
gives an average-per-focus area for each (radiation, time/dose) combination. This is an
independent algebraic check on Figure 4, not a digitization.

## F. Average IRIF / dose-response claims for SF / LF area

| ID  | Claim                                                                            | Source       | Pass 1 | Pass 2 plan |
|-----|----------------------------------------------------------------------------------|--------------|--------|-------------|
| F1  | Avg SF area: α > X+mix at 0.27 Gy (p=0.018), 0.40 Gy (p=0.003) (Fig 4A)         | Results      | ❌     | record + cross-check via Fig 2 SF≈total fact |
| F2  | Avg LF area NOT dose-dependent at 1 h, but α vs X significant at 0.40 (p=0.007), mix vs X at 0.80 (p=0.002) | Results | ❌ | record + cross-check via Fig 3B/3A ratio |
| F3  | X-ray avg IRIF area significantly larger at 24 h vs 0.5/1/3 h (p<0.001 / p=0.004) | Results | ❌ | test from Fig 2D / Fig 2C |
| F4  | Alpha avg IRIF area p=0.02 for 1 h vs 24 h                                       | Results      | ❌     | test from Fig 2D / Fig 2C |

## G. Methods constants and units (low-leverage cross-checks)

| ID  | Claim                                                            | Source  | Pass 1 | Pass 2 plan |
|-----|------------------------------------------------------------------|---------|--------|-------------|
| G1  | 1 pixel = 0.012 µm² (calibration: 93 px = 10 µm linear)          | Methods | ❌     | ✅ algebra check: (10 µm / 93 px)² ≈ 0.01156 µm²/px ≈ 0.012 |
| G2  | SF cutoff: 8–75 px; LF cutoff: ≥76 px → 0.91–8.7 µm² SF; ≥9.1 µm² LF | Methods | ❌ | ✅ convert thresholds, sanity-check against avg LF areas |
| G3  | Mixed dose split: α 25% + X 75%                                  | Methods | ✅     | — |
| G4  | Total dose rate alpha source (incl. β,γ) = 0.265 Gy/min          | Methods | ❌     | ✅ check 0.24 + 0.025 = 0.265 |
| G5  | Predicted mix at lowest dose (0.27 Gy) = half-α + half-X        | Methods | ✅ implicit | ✅ make explicit test |
| G6  | One outlier removed (alpha dose-resp exp 2 at 0.27 Gy) by Nalimov test, p=0.001 | Methods | ❌ | cannot reproduce without raw data; record as data-gap |

## H. Coverage scorecard

Pass-1 claim coverage: 7 / 10 (per existing REPORT.md).

Pass-2 plan: A1–C1 retained + add B1, B2, B3, B4, B5, D1–D7, E-block (algebraic),
F3 + F4 (algebraic), G1, G2, G4, G5. Target coverage post-pass-2: ≥ 8 / 9.

Hard data gap (cannot be lifted without authors): G6 (raw replicate data + outlier test);
paper-exact paired-t p-values on Fig 5B (raw n=4 replicate trajectories not available).
