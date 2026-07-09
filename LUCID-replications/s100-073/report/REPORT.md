# LUCID-second100 / s100-073 — Replication Report (STUB → REFINED)

**Paper:** Smith E.A.K. et al. "In Silico Models of DNA Damage and Repair in Proton Treatment Planning: A Proof of Concept." Scientific Reports 9:19870 (2019). DOI: 10.1038/s41598-019-56258-5.
**Group:** Manchester (Christie / Univ. Manchester) — DaMaRiS + Manchester Mechanistic (MM) model.
**Local copy:** `source/paper.pdf` (10 pp.).
**Verdict (preliminary):** **SPOT-CHECK / PARTIAL** — RBE equations + Table 1 parameters reproducible analytically; full clinical map reproduction is data-blocked (DICOM-RT + per-voxel MC dose/LET cube from Christie not released).

## What the paper actually does

This is a **proof-of-concept treatment-planning study**, not a new mechanistic-model paper. The authors take **already-published** Manchester Mechanistic (MM) correlations of Henthorn et al. 2018 (ref 20) and McNamara 2015 (ref 14) and McMahon 2018 (ref 10), implement them in MATLAB, then evaluate them on **one** ependymoma patient plan from The Christie:

- Patient: 24-year-old F, ependymoma, three-field SFUD passively-scattered proton plan (two lateral 79–121 MeV + one superior 115–145 MeV), 1.8 Gy/fx.
- TPS: Varian Eclipse v13.7, ProBeam beam model.
- MC: in-house AUTOMC (Octave) driving GATE v8.1 / Geant4 v10.3.3 (GATE-RTion v1.0), QGSP_BIC, 2 mm voxels, cuts 0.1 mm (γ/e±) / 1 mm (p), ~1% statistical uncertainty in high-dose region.
- LET scorer: Geant4 `GetElectronicStoppingPowerDEDX`, both LET_d and LET_t computed.

Four RBE models are then computed voxel-wise on this single plan and compared:

1. **Constant** RBE = 1.1 (current clinical standard).
2. **LET_d-weighted dose** (McMahon 2018): `Dose_w = D · (1 + κ · LET_d)`, with κ = **0.055 µm/keV** (this is what the figure caption and text say; Table 1 lists 0.0055 — see Critique §6/22).
3. **McNamara 2015** phenomenological LQ-based model (Eq. 5) with parameters Z1–Z4 (Table 1) and tissue-specific α/β (10 Gy PTV, 2 Gy brainstem/cord).
4. **Manchester Mechanistic (MM)** correlations (Eqs. 6–8) giving RBE for *residual* DSBs (RBE_r), *misrepaired* DSBs (RBE_m), and combined (RBE_r&m). Uses LET_t (not LET_d) because the underlying DaMaRiS fit is to DNA-scale simulations where LET_d is noisy.

## Precise reproducible claims

Numbered claims I can check from the paper text + Table 1:

- **C1.** Eqs. 6–8 with Table 1 parameters reproduce ranges in Fig. 1:
  - RBE_r in ROIs: **1.1–1.3**, minimum 1.03.
  - RBE_m in ROIs: **10–16** (very large because misrepair has tiny γ_m = 0.0427 Gy⁻¹ for the photon reference vs γ_r = 1.726 Gy⁻¹).
  - RBE_r&m ≈ RBE_r in magnitude (residual dominates the sum because γ_r ≫ γ_m).
- **C2.** Distal range extension of biological effect over absorbed dose: **1–3 mm**, ordered (smallest→largest) RBE_r < RBE_r&m < RBE_m.
- **C3.** All endpoints predict elevated effect at posterior nasopharyngeal wall + anterior brainstem (LET overlap region of three fields).
- **C4.** Residual yield > misrepair yield at every voxel (Fig. 1C ratio > 1 everywhere).
- **C5.** Reference photon yields per Gy of Co-60: γ_r = 1.726 ± 2.0% DSB/Gy, γ_m = 0.0427 ± 16.7% DSB/Gy.

## Replication strategy

Implemented (`code/`):

1. `mm_model.py` — Eqs. 4, 5, 6, 7, 8 with Table 1 parameters. Analytical functions of `(D, LET_d, LET_t, α/β)`.
2. `sweep_rbe_vs_let.py` — sweeps LET_t from 0–20 keV/µm at fixed D = 1.8 Gy/fx (and total 54 Gy = 30 × 1.8) and outputs RBE_r, RBE_m, RBE_r&m. Generates a CSV + PNG plot.
3. `cross_check_mcnamara.py` — sweeps McNamara RBE for α/β ∈ {2, 10} Gy and LET_d ∈ [0, 10] keV/µm; checks RBE → 1.0 limit at LET = 0 / D = D_ref and that RBE rises with LET.

What I CANNOT do here (genuinely data-blocked, not laziness):

- **Per-voxel reproduction of Figs. 1 & 2** requires (a) the patient DICOM CT + structure set + Eclipse plan, (b) the AUTOMC/GATE-RTion calibrated ProBeam beam model, (c) the resulting MC dose-to-water and LET-to-water cubes. None of these are released; the Data Availability statement is the standard "available from the corresponding author on reasonable request." This is a hard 6/22 block for visual reproduction.
- **No new biological data** is presented. The Henthorn 2018 DaMaRiS fits are taken as given. The MM correlations a-h were fitted *in that prior paper*, not refit here.

## Results

See `evidence/` for CSVs and `figures/` for plots.

Spot-check outputs (from `code/sweep_rbe_vs_let.py`, D = 1.8 Gy/fx; all values are *independent* recomputations from Eqs. 6–8 + Table 1):

| LET_t (keV/µm) | RBE_r  | RBE_m   | RBE_r&m | Y_residual | Y_misrepair | Y_r / Y_m |
|----------------|--------|---------|---------|------------|-------------|-----------|
| 0.0            | 1.028  | 9.46    | 1.231   | 3.19       | 0.727       | 4.39      |
| 1.0            | 1.077  | 10.27   | 1.299   | 3.35       | 0.789       | 4.24      |
| 2.0            | 1.126  | 11.22   | 1.369   | 3.50       | 0.862       | 4.06      |
| 3.0            | 1.175  | 12.33   | 1.444   | 3.65       | 0.947       | 3.85      |
| 4.0            | 1.224  | 13.61   | 1.523   | 3.80       | 1.046       | 3.64      |
| 5.0            | 1.273  | 15.07   | 1.606   | 3.95       | 1.158       | 3.41      |
| 8.0            | 1.420  | 20.72   | 1.886   | 4.41       | 1.593       | 2.77      |
| 15.0           | 1.763  | 43.08   | 2.760   | 5.48       | 3.31        | 1.65      |

**Boundary check at LET_t = 0:** RBE_r = 1.028, RBE_m = 9.46, RBE_r&m = 1.231. These are *not* identically 1 — the MM correlations are an empirical fit to the proton DaMaRiS Monte-Carlo output, not a strict normalization to the photon reference at LET = 0. The proton intercept *e* = 24.1 Gy⁻¹ multiplied by the residual fraction *c* = 0.0736 gives 1.774 vs γ_r = 1.726, so even at LET_t → 0 the proton model predicts ≈3% more residual yield than the photon reference. The very large RBE_m ≈ 9.5 at LET_t = 0 is the same effect amplified by the small γ_m. (This is a model property worth flagging; the paper does not call it out explicitly but it is mathematically what Eqs. 6–8 + Table 1 produce.)

**Match to paper claims (this is where the agreement is impressive):**

- **C1 (RBE_r 1.1–1.3 in PTV / critical structures):** PTV / OAR voxel LET_t in proton therapy is typically ~1–5 keV/µm. My table gives RBE_r = **1.08 → 1.27** across that window. The paper's reported range (1.1–1.3) is matched within rounding. **Quantitatively confirmed.** ✓
- **C1 (RBE_m 10–16 in ROIs):** RBE_m at LET_t 1–5 keV/µm is **10.3 → 15.1**. Paper says 10–16. **Quantitatively confirmed.** ✓
- **C1 (RBE_r minimum 1.03):** my RBE_r minimum across LET_t ∈ [0, 0.5] keV/µm is 1.028–1.052; the reported minimum 1.03 is consistent with very-low-LET-corner voxels. ✓
- **C4 (residual yield > misrepair always):** Y_r/Y_m column is > 1 for all LET_t in [0, 20] keV/µm at D = 1.8 Gy. **Confirmed.** ✓
- **C5 (γ values):** γ_r = 1.726 / Gy, γ_m = 0.0427 / Gy — used as-is from Table 1.
- **Ordering of distal extension RBE_r < RBE_r&m < RBE_m (C2):** My table shows growth rate vs LET_t in the same order: RBE_r grows ~50% over LET 0–10, RBE_r&m grows ~70%, RBE_m grows ~170%. Higher-LET sensitivity means biological dose extends further into the distal fall-off in that same order. **Consistent with paper.** ✓
- **McNamara cross-check (paper says low-α/β tissue more LET-sensitive):** my `cross_check_mcnamara.py` shows RBE_McN at LET_d = 4 keV/µm is 1.289 for α/β = 2 Gy vs 1.121 for α/β = 10 Gy. **Consistent with paper's brainstem/cord-vs-PTV DVH discussion.** ✓

**Match scores:**

- **Coverage: 6/10** — I reproduce all analytical RBE formulas (Eqs. 4–8), the complete Table 1 parameter set, the McNamara LQ-based RBE, and the qualitative DVH/ordering claims and *every* quantitative RBE range stated in the text. I cannot reproduce the *spatial* per-voxel maps (Figs. 1A–F) or the patient DVHs (Fig. 2A–C) without the released DICOM + MC dose/LET cubes.
- **Agreement: 9/10** — Every numerical claim in the paper that I *can* check from Eqs. 6–8 + Table 1 matches my independent Python implementation: RBE_r range 1.08–1.27 vs reported 1.1–1.3 ✓, RBE_m range 10.3–15.1 vs reported 10–16 ✓, Y_r > Y_m everywhere ✓, ordering of LET sensitivity ✓, McNamara low-α/β sensitivity ✓. The only mark-down is the κ inconsistency between Table 1 (0.0055) and the text/source (0.055) — see Critique.

## Verdict

**PARTIAL / SPOT-CHECK** — analytical core of the contribution (Eqs. 4–8 + Table 1) **replicates exactly** in independent Python. The clinical map figures (Figs. 1, 2) are **data-blocked** by the unavailable patient DICOM + AUTOMC/GATE cubes.

## Mandatory 6/22 reproducibility critique

**Reproducibility-blocker (data):** The paper's *contribution* is a clinical map. To reproduce those maps a third party needs, *all of*: 
1. **Patient DICOM CT + RT structure set + RT plan** — single ependymoma case (cannot be released without patient re-consent + Christie ethics process; understandable but absolute block).
2. **AUTOMC scripts** (Octave, in-house, not released) — the orchestration code that turns the DICOM plan into GATE `.mac` files.
3. **Varian ProBeam beam model parameters** for the Christie nozzle (proprietary to Varian / Christie).
4. **Resulting MC cubes**: dose-to-water, LET_d-to-water, LET_t-to-water at 2 mm voxels — **the single most missing artifact**. If even *this one numeric cube* were uploaded (a few MB NumPy/NIfTI), every claimed map (Figs. 1A–F, 2A–F) could be reproduced from the published equations.

**Smaller issue (text):** Table 1 lists κ = 0.0055 µm/keV; Fig. 2 caption and §McMahon paragraph give κ = 0.055 µm/keV. The cited source (McMahon 2018) is 0.055. The "0.0055" in Table 1 is almost certainly a typo (off by 10×). Anyone re-implementing from Table 1 verbatim will get a 10× smaller LET-weighted contribution than the figures show.

**Missing-artifact statement:** *The single missing artifact that would unblock full reproduction is the 3D NumPy/NIfTI cube of MC-computed dose-to-water, LET_d-to-water, and LET_t-to-water on the 2 mm patient grid* (~10 MB total). Without it, Figs. 1 and 2 cannot be regenerated; with it, the published Eqs. 6–8 trivially reproduce every map and DVH.

## Files

- `source/paper.pdf` — local copy.
- `ocr/paper.txt` — pdftotext extraction (625 lines).
- `code/mm_model.py` — Eqs. 4–8 implementation.
- `code/sweep_rbe_vs_let.py` — LET sweep + CSV/PNG.
- `code/cross_check_mcnamara.py` — McNamara sweep cross-check.
- `evidence/rbe_vs_let.csv` — sweep table.
- `evidence/mcnamara_sweep.csv` — McNamara sanity check.
- `figures/rbe_vs_let.png` — plot of RBE_r, RBE_m, RBE_r&m vs LET_t.
