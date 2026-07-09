# LUCID100 — Slot 57 — Adaptive Response DDR Mechanistic Model

**Paper:** Piotrowski Ł., Krasowska J., Fornalski K.W. (2023). *Mechanistic Modelling of DNA Damage Repair by the Radiation Adaptive Response Mechanism and Its Significance.* **BioMedInformatics** 3(1), 150–163.
**DOI:** [10.3390/biomedinformatics3010011](https://doi.org/10.3390/biomedinformatics3010011)
**License:** CC BY 4.0 (open access)
**LUCID100 master row:** id 88, Wave 6, slot 57, B-tier, simulation/model replication
**Source of truth:** `/Users/stevens/.openclaw/workspace/lucid-replications/LUCID100_SOLID_MASTER_QA.tsv`
**Backfilled:** 2026-06-09 by Ollie (sub-agent task)

## What the paper does

Wraps an **analytical layer** around the authors' own simplified Monte Carlo
model of human-lymphocyte / X-ray irradiation (Fornalski et al., Dose-Response
2022, ref [1] in the paper) and asks: **once every other cellular biological
process is folded in, is the radiation adaptive response (AR) a *significant*
contributor to DNA-damage repair, or does it disappear into the noise?**
The answer is the latter: AR is significant in dedicated experimental designs
(priming-dose / Raper–Yonezawa) but at the whole-population / whole-organism
level its contribution falls to ~0.126 % of cells.

## Key equations & parameters (paper, §2–3)

| Quantity | Symbol | Value | Notes |
|----------|--------|-------|-------|
| Hit probability | `P_hit(D) = 1 - e^{-a D}` | `a = 1.3 Gy⁻¹` | Eq. (1), human lymphocyte / X-ray |
| Lesion-creation prob. | `P_RDEM = 1 - e^{-a₂ D}` | `a₂ = 2.4 Gy⁻¹` | |
| Metabolic damage | `P_M ≈ τ + a₃ K^n` | `τ = 0.001, a₃ = 6.8·10⁻¹² h⁻³, n = 3` | K = cell age (h) |
| AR probability (single dose) | `P_AR = α₀ D² k² e^{-α₁ D - α₂ k}` | `α₀=22.9 Gy⁻²h⁻³, α₁=79.4 Gy⁻¹, α₂=0.0832 h⁻¹` | Eq. (2) |
| AR probability (constant ḋ) | `P_C = μ₀ ḋ² e^{-μ₁ ḋ}` | HBRA: μ₀=882·10³ h²mGy⁻², μ₁=1025 h·mGy⁻¹; in-vitro: μ₀=38 h²mGy⁻², μ₁=11.5 h·mGy⁻¹ | Eq. (5) |
| Repair-fraction definition | `f(D) = Σ S_n / (N₀ P_hit)` | Eq. (3) |
| Recursive series | `S_n` per Eq. (4) | |
| Simulation size | N₀ = 493 000 cells, T₀ = 120 h | |

Two-dose Raper–Yonezawa scenarios (Figs 3–6) use `(D₁, Δt, D₂)`:
1. (25 mGy, 24 h, 1500 mGy)  2. (25 mGy, 24 h, 4000 mGy)
3. (25 mGy, 100 h, 1500 mGy) 4. (100 mGy, 24 h, 1500 mGy)
Each scenario: 64 000 cells × 50 MC runs (AR on / AR off).

Constant dose-rate scenarios (Figs 7–10):
- ḋ = 0.17 or 0.002 mGy/h, two parameter sets (HBRA / in-vitro).

## Repository contents

```
.
├── README.md                       (this file)
├── PROGRESS.md                     (per-step status log)
├── FIRST_PASS_REPORT.md            (verdict + summary)
├── artifacts/
│   ├── paper.pdf                   (9.2 MB, fetched from pub.mdpi-res.com)
│   ├── article_text.txt            (extracted article text)
│   ├── artifact_manifest.json      (catalog of harvested files)
│   └── figures/                    (fig001.jpg … fig012.jpg, 550-wide)
├── scripts/
│   └── smoke_adaptive_response.py  (analytical Eq. 1-4 reproduction)
└── outputs/
    ├── fig1_repair_fraction.png    (replica of paper Fig 1)
    ├── fig12_global_fraction.png   (replica of paper Fig 12)
    └── smoke_summary.json          (numeric checks)
```

## Reproducing

```sh
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-adaptive-response-ddr-model
python3 scripts/smoke_adaptive_response.py
```

Runtime ≈ 0.5 s on CherryRd. Uses only `numpy` + `matplotlib`.

## Verdict

**GO (light replication achieved; full MC out of scope here).** The analytical
core of the paper (Eqs 1–4) reproduces qualitatively and quantitatively:
in the 10–45 mGy dose band our replica gives f(D) = 97.5–99.9 % matching the
paper's quoted "≈100 %" claim; the analytical P_AR peak in (D, k) sits at
(25.2 mGy, 24.0 h), which is exactly the priming-dose / Δt combo the authors
calibrated and used in their first two-dose Monte Carlo scenario.

The full Monte Carlo simulations (Figs 2 MC points, 3–11) require the prior
Fornalski 2022 Dose-Response model (the cell-status probability tree with
multiplication / death / mutation / cancer states), which is **not released as
code**. Replicating it from scratch would be a dedicated multi-day project; it
is recorded in `FIRST_PASS_REPORT.md` as the next step if a deeper replication
is later approved.

## Data & code availability (per paper)

> *Data Availability Statement:* No new data creation.

No code repository, no supplementary spreadsheets, no Zenodo deposit are
linked from the paper or the journal page. All numerical comparison targets
must be read off the paper's published figures.
