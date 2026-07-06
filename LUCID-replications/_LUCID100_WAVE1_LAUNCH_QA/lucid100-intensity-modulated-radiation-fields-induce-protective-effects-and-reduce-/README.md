# Matsuya et al. 2019 — Intensity-Modulated Radiation Fields Induce Protective Effects

LUCID100 Wave 1 · Slot 3 · `simulation/model replication` · partial-scope verdict

## Full citation

> Matsuya, Y., McMahon, S. J., Ghita, M., Yoshii, Y., Sato, T., Date, H., & Prise, K. M.
> (2019). **Intensity Modulated Radiation Fields Induce Protective Effects and Reduce
> Importance of Dose-Rate Effects.** *Scientific Reports*, 9, 9483.
> https://doi.org/10.1038/s41598-019-45960-z

License: CC BY 4.0 (open access).

## Source links

| What | Where |
|---|---|
| Article landing | https://www.nature.com/articles/s41598-019-45960-z |
| Main PDF (mirror) | `paper.pdf` (sha256 `001ca939e425…`) |
| Supplementary PDF (MOESM1) | `supplement/41598_2019_45960_MOESM1_ESM.pdf` (sha256 `fcaefb6dbfba…`) |
| Original Dropbox copy | `/Users/stevens/Dropbox/XFER/LUCID-replication-targets/5f5b0d9df89a74d8abbe7143e9a2c9c1fb5e9cd3.pdf` |

## Code, data, supplement availability

| Resource | Status |
|---|---|
| Public code repo | **None published.** Model fully specified by Eqs (1)–(10) in main and (S1)–(S7) in supplement. |
| Public dataset | **None deposited.** No GitHub / Zenodo / figshare DOI in the paper. |
| Supplementary materials | ✓ One PDF (`MOESM1_ESM.pdf`) with sections I–VII. Downloaded and indexed locally. |
| Tabulated parameter set | ✓ **Table 1** (main paper) — full mean ± s.d. for both cell lines × both fields. |
| Microdosimetric inputs | ✓ Main text §"Monte Carlo simulation to calculate yD value": yD = 4.393 ± 0.007 keV/µm in-field, 4.769 ± 0.044 keV/µm out-of-field. |
| Raw experimental survival points | ✗ Embedded in Figs 2–6 as graphics only — would need WebPlotDigitizer for a numerical χ² replication. |
| Raw flow-cytometry / cell-cycle data | ✗ Not available. |

## Target claims and figures

The paper makes three central testable claims (Abstract, §Results, §Conclusion):

1. **C1 — Protective effect.** In-field cell survival under half-field (MF, A_IF=0.5) exposure is *higher* than under uniform-field (UF, A_IF=1.0) exposure for the same delivered in-field dose. Most pronounced in normal AGO1522 cells; weak in DU145.
2. **C2 — Reduced SLDR.** The sub-lethal damage repair rate (a+c) is much smaller in AGO1522 under MF (0.034 ± 0.062 h⁻¹) than under UF (1.684 ± 0.911 h⁻¹), making AGO MF survival approximately dose-rate-independent. DU145 keeps substantial SLDR in both fields.
3. **C3 — Reduced initial DNA-lesion yield.** The β₀ term is reduced under MF for both cell lines (AGO: 0.011 vs 0.081 Gy⁻²; DU145: 0.039 vs 0.041 Gy⁻²), pointing to fewer initial PLLs rather than enhanced repair as the mechanism of the protective effect.

Quantitative figure targets:

- **Fig 2** — split-dose recovery curves (4 Gy total = 2+2 Gy) at τ = 0…48 h, two cell lines × three exposure configurations (in-field MF, out-of-field MF, in-field UF).
- **Fig 3** — single-dose survival curves D = 0…10 Gy, same configurations.
- **Fig 4** — survival at total dose 4 Gy across four average dose-rates (0.59, 0.20, 0.10, 0.05 Gy/min).
- **Fig 5** — split-dose comparison vs Ghita et al. 2015 data.
- **Fig 6** — protective-effect mechanism toy models (migration vs reduced DNA yield).
- **Table 1** — IMK parameter set (α₀, β₀, a+c, αb, βb, δ) for AGO/DU145 × MF/UF.

## Acceptance criteria (this replication)

Forward-model reproduction is **PASS** if all of the following hold using only Table 1 parameters and Eqs (1)–(6):

| ID | Criterion | Result |
|---|---|---|
| A1 | S_in(MF) > S_in(UF) for AGO at every D ∈ {2, 4, 6, 8, 10} Gy | ✅ pass |
| A2 | S_in(MF) is invariant to dose-rate for AGO at 4 Gy total across 0.05–0.59 Gy/min (within ≤2% relative spread) | ✅ pass (S = 0.148 at all four rates) |
| A3 | S_in(UF) for AGO at 4 Gy total *rises* monotonically as rate falls 0.59 → 0.05 Gy/min | ✅ pass (0.010 → 0.011 → 0.013 → 0.017) |
| A4 | S_in(MF) ≈ S_in(UF) for DU145 across same dose-response grid (relative difference ≤ ~15% for D ≥ 4 Gy) | ✅ pass (within ~7%) |
| A5 | D₁₀ (dose for 10% survival, in-field) AGO MF > AGO UF, while DU145 D₁₀ MF ≈ UF | ✅ pass (AGO: 4.78 Gy vs 2.16 Gy; DU145: 5.17 Gy vs 5.01 Gy) |
| A6 | Out-of-field survival drops below 1 even at D = 0 because the in-field hit cells signal | ✅ pass |

Future / stretch criteria (Wave-2):

- **A7** — χ² agreement between regenerated curve and digitized Fig 3 points (WebPlotDigitizer pipeline).
- **A8** — independent MCMC refit recovers Table 1 parameters within stated uncertainty using only the digitized data.

## Artifact harvest checklist

- [x] Source PDF saved locally and hashed
- [x] Full main text extracted (`paper.txt`, 701 lines)
- [x] Supplementary PDF downloaded from Springer's `static-content` CDN
- [x] Supplement text extracted (`supplement/supplement.txt`, 420 lines)
- [x] No public code repository — confirmed (no GitHub/Zenodo/figshare URL in either PDF)
- [x] No public dataset — confirmed
- [x] Environment plan written (see `ARTIFACT_MANIFEST.md`)
- [x] Acceptance metrics defined (above)
- [x] Blockers listed explicitly (see REPORT.md)

## Execution checklist

- [x] Smoke test — `src/imk_model.py` self-test passes
- [x] Forward-model curves regenerated — `src/reproduce_figures.py` writes `figures/fig3_dose_response.png`, `figures/fig4_dose_rate.png` and CSVs in `data/`
- [x] Qualitative claims C1, C2, C3 numerically checked against published parameters
- [ ] Quantitative χ² against digitized data points — deferred (needs WebPlotDigitizer pass)
- [ ] Independent MCMC parameter refit — deferred (out of scope, also needs the same digitized data)
- [x] `REPORT.md` written
- [x] Progress JSON updated under `~/.openclaw/workspace/memory/subagent-progress/`

## Layout

```
.
├── README.md                        ← this file
├── PROGRESS.md
├── REPORT.md                        ← first-pass verdict + evidence
├── ARTIFACT_MANIFEST.md             ← provenance + hashes + reuse policy
├── paper.pdf, paper.txt             ← main paper
├── supplement/
│   ├── 41598_2019_45960_MOESM1_ESM.pdf
│   ├── supplement.txt
│   └── landing.html                 ← article landing snapshot
├── src/
│   ├── imk_model.py                 ← IMK forward model implementation
│   └── reproduce_figures.py         ← regenerate Figs 3 & 4 + landmarks
├── data/
│   ├── fig3_AGO1522.csv             ← predicted curve numerics
│   ├── fig3_DU145.csv
│   ├── fig4_AGO1522.csv
│   ├── fig4_DU145.csv
│   └── landmarks.csv                ← S(2), S(4), S(8), D10 per model
└── figures/
    ├── fig3_dose_response.png
    └── fig4_dose_rate.png
```

## Run

```
cd .../lucid100-intensity-modulated-radiation-fields-induce-protective-effects-and-reduce-
python3 src/imk_model.py            # smoke test
python3 src/reproduce_figures.py    # regenerate curves + CSVs
```

Requires Python 3, numpy, scipy, matplotlib — all already present on CherryRd
(verified: numpy 2.4.3, scipy 1.17.1, matplotlib 3.10.8).

## Initial abstract (paper)

In advanced radiotherapy, intensity modulated radiation fields and complex dose-delivery are utilized to prescribe higher doses to tumours. Here, we investigated the impact of modulated radiation fields on radio-sensitivity and cell recovery during dose delivery. We generated experimental survival data after single-dose, split-dose and fractionated irradiation in normal human skin fibroblast cells (AGO1522) and human prostate cancer cells (DU145). The dose was delivered to either 50% of the area of a T25 flask containing the cells (half-field) or 100% of the flask (uniform-field). We also modelled the impact of dose-rate effects and intercellular signalling on cell-killing. Applying the model to the survival data, it is found that (i) in-field cell survival under half-field exposure is higher than uniform-field exposure for the same delivered dose; (ii) the importance of sub-lethal damage repair (SLDR) in AGO1522 cells is reduced under half-field exposure; (iii) the yield of initial DNA lesions measured with half-field exposure is smaller than that with uniform-field exposure.
