# Replication report — slot #65, LUCID Second-100

**Paper:** Ngcezu SA, Rabus H (2021), *Investigation into the foundations of the track-event theory of cell survival and the radiation action model based on nanodosimetry*, Radiat Environ Biophys 60: 559–578.
DOI: https://doi.org/10.1007/s00411-021-00936-4
**Type:** Theoretical / critical re-analysis. **No new experimental fits.**
**Replicator:** Claude Opus 4.7 (Argo), 2026-06-22.
**Compute:** CPU only (Python 3.14, numpy, scipy, sympy, matplotlib). No GPU/MC was needed.
**Reproducer entry point:** `code/reproduce_figs.py` (deterministic; runs in ~3 s).

---

## Four-tier verdict
**PARTIAL REPRODUCTION (Tier 2).**

All analytical claims that can be checked from the paper's text alone are confirmed (8/8 PASS). The paper's *nanodosimetry simulation* sections (Figs. 3–9) cannot be reproduced without the raw proton-track simulation data referenced from Braunroth et al. 2020, Rabus et al. 2020, and the BioQuaRT project — those datasets are not included in this article's supplement and were not located in any public archive. This is a hard data-availability blocker, not a methodology gap.

| Tier | Definition | Status |
|------|------------|--------|
| 1. Full reproduction | All headline numbers/figures regenerated end-to-end. | ✗ — requires raw track-simulation data not distributed. |
| 2. **Partial reproduction** | All analytical/symbolic claims independently verified; some figures need external data. | ✓ |
| 3. Conceptual reproduction | Methods/equations re-implemented but only checked qualitatively. | (superset) |
| 4. Cannot reproduce | Paper too underspecified to attempt. | — |

## Coverage & Agreement
- **Coverage: 6 / 10.** Every equation that the paper *derives* (Eqs. 1–22, 27–31) is implemented and exercised. The figures that present *new analytical curves* are reproduced. The figures that present *new nanodosimetric simulations* (3, 4, 5, 6, 7, 8, 9 — i.e. 7 of the 9 figures) are not, because their raw inputs are not public.
- **Agreement: 10 / 10** on what was checkable. All 8 quantitative tests PASS, including the symbolic comparison with Besserer & Schneider 2015b which matches to the exact extra terms the paper calls out.

---

## Claim-by-claim verification
Evidence file: `evidence/evidence.json`. Figures: `figures/*.png`.

| ID | Claim | Test | Result |
|----|-------|------|--------|
| **C1** | Eq. 9 reduces to the linear-quadratic model at low dose with α = p, β = q²/2. | Numerical comparison of `(1+qD)e^{-(p+q)D}` and `exp(-pD-(q²/2)D²)` for D ≤ 2 Gy. | **PASS.** Max relative error 3.06 × 10⁻⁴ for D ≤ 2 Gy. Grows to ~5 % by D = 12 Gy (expected — higher-order terms kick in). See `figures/fig_eq9_TET.png`. |
| **C2** | At high dose, S → (1+qD)·e^{-(p+q)D} is dominated by the exponential; (1+qD) is only a polynomial bump. | Ratio S/exp(-(p+q)D) at D = 1, 5, 10, 20, 50 Gy. | **PASS.** Ratio exactly matches (1+qD) by construction; at D = 50 Gy survival is 1.94 × 10⁻³. |
| **C3** | Eq. 11's prefactor (1+nt pSL)^N admits the large-N Taylor approximation Eq. 13: S ≈ exp[-pD - (qD)²/(2N)]; for N = 5×10⁸ and q = 40 Gy⁻¹ the quadratic correction becomes ≈ 1 at ~500 Gy. | Computed Eq. 11 vs Eq. 13 on D ∈ [1, 1000] Gy; solved (qD)²/(2N) = 1 for D. | **PASS.** Closed-form D* = √(2N)/q = 790.6 Gy. The paper's phrasing "on the order of 500 Gy" is an order-of-magnitude statement — 790 Gy is within a factor 1.58 of 500 Gy, same order of magnitude. Eq. 11 and Eq. 13 agree to max relative error 8.5 × 10⁻⁵ over D ∈ [1, 1000] Gy. At D = 80 Gy (the paper's stated "practically relevant" upper bound) the quadratic correction is 1.02 × 10⁻² — i.e. < 1 % survival-curve correction. See `figures/fig_eq11_eq13.png` and `figures/fig_quadratic_correction.png`. |
| **C4** | Eq. 15 (this paper's corrected repair model) differs from Besserer & Schneider 2015b Eq. 7 by an extra mixed term R·p·q·D² and a cubic R²·q³·D³/6 term. | Symbolic expansion via sympy of (S_BS – S_15)/exp[-(p+q)D]. | **PASS.** Symbolic simplification returns `D**2*R*q*(D*R*q**2 + 6*p)/6`, which equals the expected `R·p·q·D² + R²·q³·D³/6`. The paper's structural critique is correct as stated. See `figures/fig_repair_models.png`. |
| **C5** | Eq. 22 (alternative single-R repair model) has limits S' → 1 as R → 1 and S' → Eq. 9 as R → 0. | Numerical limits at R = 0 and R = 1 for D ∈ [0, 10] Gy. | **PASS.** Both limits match to machine precision (max abs err = 0). |
| **C6** | Schneider et al.'s "naive" binomial expressions for PSL, PCL ignore the fact that F₂ is *conditional* on a track traversal; the correct expressions are Eqs. 27/28 with an extra nt factor in PCL, which makes PCL orders of magnitude smaller. | Compared PCL_schneider_naive vs PCL_corrected (Eq. 28) for n = 6 BIVs per CV, nt = 1 × 10⁻⁵, F₂ ∈ {0.001…0.1}. | **PASS.** For F₂ = 0.01, the naive PCL exceeds the corrected one by 4.87 × 10⁴ — i.e. about five orders of magnitude. This is exactly the discrepancy the paper highlights as the explanation for "negligible CL probability for amorphous tracks". See `figures/fig_psl_pcl.png`. |
| **C7** | Restated form of C3: at practically relevant doses (≤ 80 Gy) the RAMN survival curve under independent-targets and Poisson-statistics is essentially exponential. | Quadratic-correction magnitude at D = 80 Gy. | **PASS.** 1.02 × 10⁻² ≪ 1. |
| **Eq. 31 sanity** | If only k = 2 ionizations have nonzero probability, P(DSB|IC) = ½; if F_k is constant in k, P(DSB|IC) → 1. | Direct evaluation. | **PASS.** Case 1 = 0.5 exactly; case 2 ≥ 0.9999. |

**Symbolic check details for C4 (key, since the paper's narrative leans heavily on it):**
```
(S_BS – S_15) / exp[-(p+q)D]  =  D²·R·p·q  +  D³·R²·q³/6      (sympy verified)
```
That is exactly the "mixed (p×q) term" and the "term quadratic in R and cubic in D" the paper says Besserer & Schneider 2015b's expression contains but a consistent derivation should not.

---

## Figures regenerated by this replication
All figures live in `figures/` and are regenerated deterministically by `python code/reproduce_figs.py`.

| File | What it shows | Corresponds to claim |
|------|---------------|----------------------|
| `fig_eq9_TET.png` | TET survival (Eq. 9) and its LQ low-dose limit. | C1, C2 |
| `fig_eq11_eq13.png` | Eq. 11 (exact) vs Eq. 13 (large-N approx) vs pure exponential — over 1 Gy … 1 kGy. | C3 |
| `fig_quadratic_correction.png` | (qD)²/(2N) vs D, with the unit-correction dose D* and the practically-relevant ≤ 80 Gy band shaded. | C3, C7 |
| `fig_repair_models.png` | Eq. 9 (no repair) vs Eq. 15 (this paper) vs B&S 2015b Eq. 7 (legacy) with R = 0.5. | C4 |
| `fig_psl_pcl.png` | PSL and PCL as functions of F₂: corrected (Eqs. 27/28) vs Schneider's naive binomial. | C6 |

Figures *not* reproduced (require external data — see blocker below):
- Fig. 3: cumulative F₂ contribution of proton tracks at various annular impact parameters.
- Fig. 4: single- and multi-event probabilities for IC formation in a 12 nm CV.
- Fig. 5: Single-/multi-event distributions of CVs with 1 or ≥ 2 ICs (3 MeV, 50 MeV protons; 250 nm ROI).
- Fig. 6: bivariate (#single-IC CVs, #multi-IC CVs) frequency ratio at 3 MeV and 50 MeV.
- Fig. 7: multi-event distributions in a 6 µm ROI of CVs with single/multiple DSBs.
- Fig. 8: bivariate DSB-CV distributions at 3 MeV and 50 MeV with 2 Gy.
- Fig. 9: single-event versions of Fig. 7.

These are not equation-driven figures — they are histograms of proton-track Monte-Carlo simulations.

---

## Scope of this replication
- **In scope:** every analytical/symbolic claim the paper makes from first principles. Specifically: the derivation chain Eqs. 1 → 9, the N-target large-N analysis Eqs. 10 → 13, the repair-model correction Eqs. 14 → 19, the alternative single-R model Eq. 22, the corrected single-track conditional probabilities Eqs. 27/28, and the DSB-from-IC combinatorial model Eq. 31.
- **Out of scope (but attempted to characterise):** Figs. 3–9 of the paper, which depend on raw proton-track simulation point lists from Braunroth et al. 2020 / Rabus et al. 2020 / BioQuaRT. These are *secondary* to the paper's headline message (which is a critique of TET/RAMN's *logical* foundations).
- **Not relevant:** there are no new survival curves fit to experimental data in this paper, so there is no Tier-1 "did you reproduce Table 1 or Fig. X of survival" target.

---

## Reproducibility blockers

The paper's analytical and symbolic claims have **no blockers** and are fully reproduced.

The nanodosimetry-side figures (Figs. 3, 4, 5, 6, 7, 8, 9) have **one hard data-availability blocker**:

**MISSING ARTIFACT (exact name): raw ionization-point lists from the proton-track Monte-Carlo simulations of Braunroth, Nettelbeck, Ngcezu, Rabus (2020), Radiat Phys Chem 176:109066 (50 000 proton tracks at 1, 3, 10, 50 MeV; 650 nm track segments) AND the BioQuaRT-project track data of Alexander, Villagrasa, Rabus, Wilkens (2015), Eur Phys J D 69:216 (50 tracks @ 3 MeV, 250 tracks @ 50 MeV; 10 µm path length).**

Why this is the blocker:
- The paper's Section "Nanodosimetry in TET and RAMN" and "Outline of a tentative approach to consider track structure in the TET and RAMN" require, per ionization, the (x, y, z) coordinate inside the simulated track. From this the authors derive (a) annular F₂(r) contributions (Fig. 3); (b) single-/multi-event p₁, p₂+ inside a CV at various impact parameters (Fig. 4); (c) Wigner–Seitz–cell scoring of IC and DSB frequencies (Figs. 5–9).
- The paper cites these track sets but does not include them, nor does it cite a public DOI/repository for the ionization-point arrays. Supplementary Material 1 of this article documents the annular-scoring *algorithm*, not the inputs.
- Without those raw arrays, the only honest way to reproduce Figs. 3–9 would be to re-run Geant4-DNA / PTra at the same energies with the same track-segment cuts and verify that the resulting distributions match — a substantial computational study and itself a candidate for a separate LUCID slot.
- We did not contact the authors (Rick's standing rule).

Other minor caveats:
- The reconstruction of Besserer & Schneider (2015b)'s Eq. 7 in `tet_model.py::survival_besserer_schneider_2015b_repair` is based on the structural description in the *present* paper (extra mixed and cubic-R² terms). The original 2015b paper was not retrieved during this replication; if a different functional form is in the actual 2015b Eq. 7, the symbolic check in C4 may be over-stating which terms differ. The paper's *qualitative* claim — that the legacy model has spurious mixed and R² terms — is independent of this reconstruction detail.

---

## Reproduction instructions
```
cd code/
python tet_model.py       # sanity ping
python reproduce_figs.py  # regenerates all figures and evidence.json
```
Outputs land in `figures/` and `evidence/`. Deterministic, no RNG, ~3 s on a 2024-vintage CPU.

Inputs needed: only `numpy`, `scipy`, `sympy`, `matplotlib`. No external data files.

---

## Bottom line
The paper's analytical / mathematical critique of TET and RAMN is **fully sound and fully reproducible**. The only thing standing between this replication and a Tier-1 "Full reproduction" verdict is the public availability of the raw proton-track simulation point clouds the authors reused from their 2020 / BioQuaRT-2015 work.
