# LUCID100 Slot 36 — Deactivation Theory for Proton Therapy

**DOI:** [10.1140/epjd/e2019-90263-5](https://doi.org/10.1140/epjd/e2019-90263-5)
**arXiv:** [1901.08194](https://arxiv.org/abs/1901.08194)
**Title:** Renormalization of radiobiological response functions by energy loss fluctuations and complexities in chromosome aberration induction: deactivation theory for proton therapy from cells to tumor control
**Authors:** R. Abolfath, Y. Helo, L. Bronk, A. Carabe, D. Grosshans, R. Mohan (MD Anderson / Penn / Yale / Invicro)
**Journal / Year:** Eur. Phys. J. D 73:64 (2019)
**LUCID100 wave / slot:** Wave 4 / Slot 36 / Rank 67
**Worktype:** simulation/model replication

## What the paper claims

A multi-scale, analytical mechanistic model that:

1. Renormalizes the linear–quadratic (LQ) α(LET), β(LET) coefficients by perturbative expansion of a **DSB master equation** (Eq. 1) in lineal/specific energy moments — i.e. **energy-loss fluctuations** (Landau/Vavilov / Neyman distributions of z) dress the bare chromosome repair (γ₁) and misrepair (γ₂, γ₃, …) rates, giving λ_eff = γ₁ Λ(Δ), γ_eff = γ₂/2! Γ(Δ) (Eqs. 6–8).
2. Attributes high-LET non-linearity in RBE to **continuous transitions** in chromosome-aberration complexity (binary → ternary → quaternary → higher-order recombinations) as LET grows from Bragg-plateau to distal-edge.
3. Couples the microscopic DSB master equation to a macroscopic **birth-death Markov chain** (Eq. 40) for cell colony dynamics, giving an effective SFeff and Tumor Control Probability TCP (Eqs. 46–53).
4. Global-fits H460 and H1437 NSCLC clonogenic survival data of Guan et al. (Sci. Rep. 5:9850, 2015 — ref [13]) acquired on the MD Anderson mono-energetic scanned proton beam set-up.

Key practical predictions:
- α = α₀ + α₁·LET_d, β ≈ β_x (linear) for LET_d ≤ 5 keV/µm and LET_d ≥ 15 keV/µm with different slope coefficients in each regime; an intermediate 5–15 keV/µm gap where data are missing is interpolated via a 3D global-fit surface (Eq. 32).
- L = αD + βD² lethal-lesion form retained, with α,β power series in LET_d (Eqs. 21–22).
- TCP = exp(−Σ_k N_k · SF_k), CDP for in-vitro 100-cell-per-well assays.

## Repository layout

```
lucid100-deactivation-theory-proton-rbe/
├── README.md                 (this file)
├── PROGRESS.md               (chronological log)
├── ARTIFACT_MANIFEST.md      (file inventory + checksums)
├── FIRST_PASS_REPORT.md      (verdict + replication path)
├── artifacts/
│   ├── paper.pdf             (arXiv 1901.08194v1, 9.7 MB)
│   ├── paper.txt             (pdftotext extraction)
│   └── springer_landing.html (Springer paywall stub; HTML not PDF)
├── code/
│   └── smoke_deactivation.py (minimal SF(D,LET) reproduction)
├── figures/
│   ├── alpha_beta_vs_LET.png
│   ├── sf_vs_dose_H460.png
│   └── rbe_vs_LET.png
└── reports/                  (reserved for downstream artifacts)
```

## Replication status (first pass)

- ✅ Paper PDF harvested from arXiv (Springer paywalled, returned HTML)
- ✅ Equations + parameters mapped (Eqs. 15, 21–22, 32, 40, 46–53)
- ✅ Minimal smoke script reproduces Eq. 32 LQ form and Eq. 15 power-series α(LET), β(LET), generates SF(D) for H460 across LET_d = 0.9 – 19 keV/µm
- ✅ Smoke verifies expected qualitative behavior: α and β both monotonic ↑ with LET_d; SF at fixed D decreases with LET; RBE_10% ≈ 1.0–1.4 in plateau, ≈ 1.5–1.7 near Bragg peak (consistent with Guan et al. and Fig. 6 of the paper)
- ❌ **No GitHub / code / supplementary data / deposited dataset** referenced in the manuscript
- ❌ Full quantitative reproduction of Fig. 6/7/8 requires the underlying Guan et al. SF(D, LET) measurements and the authors' 3D global-fit coefficients (a_i, b_i, b_ij). Neither is published in tabular form.

**Verdict:** AMBER — replicable in form, partial in numerical values. See `FIRST_PASS_REPORT.md`.

## Heavy compute

None required. The model is fully analytical (≤ 6th-order polynomial in z_D, closed-form LQ). Birth–death master eq. could be Monte-Carlo simulated for TCP but is not needed for the smoke test — Eq. 51/53 is closed-form once α(LET),β(LET) are known. **Runs on CherryRd CPU in < 1 s.** No HPC scheduling.

## External dependencies for strict replication

- **Guan et al. 2015 (Sci. Rep. 5:9850)** — primary experimental SF(D, LET) for H460/H1437 NSCLC + LET spectrum at each depth. Open access.
- **Abolfath et al. 2017 (Sci. Rep. 7:8340)** — companion paper, also OA — provides the 3D global-fit numerical procedure but again does NOT release coefficient tables.
- Neyman / Landau / Vavilov distribution PDFs — standard, derivable.
- MC track-structure ν, z, y distributions: TOPAS / Geant4-DNA referenced as Nikjoo, Friedland — already cached in sibling LUCID replications (slot 47 TOPAS-nBio, slot 56 SPT-SDD/MEDRAS).

## Author contact / paid endpoints

None used. No author contact attempted (per task brief).
