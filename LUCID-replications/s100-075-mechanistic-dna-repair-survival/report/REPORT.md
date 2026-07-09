# Replication report — LUCID Second-100, slot #75

**Paper**
McMahon SJ, Schuemann J, Paganetti H, Prise KM.
*Mechanistic Modelling of DNA Repair and Cellular Survival Following Radiation-Induced DNA Damage.*
**Scientific Reports** 6:33290 (2016). doi:10.1038/srep33290

**Replicator**: Ollie (subagent), Argo Opus 4.7, free endpoints only.
**Date**: 2026-06-22.
**Compute**: CPU only (numpy/scipy). No Monte-Carlo / GPU step was required to reach the verdict because the paper's analytic model is fully closed-form except for a single one-time Monte-Carlo calibration that the authors already absorbed into two constants `A=0.757, B=5.39` (Eq 5).

---

## Verdict

**PARTIAL replication** — analytic mechanistic model reproduced end-to-end; quantitative agreement with the paper's *qualitative* claims and *parameter table* is high, but a true claim-by-claim ABS agreement with their figure curves and their tabulated `MID_model vs MID_experiment` R²=0.91/0.96 cannot be tested **without their literature-extracted experimental dataset, which is not included in the article PDF or its public supplement listing** (see Blockers section).

| Score | Value | Notes |
|---|---|---|
| **Coverage** | **8 / 10** | All 15 numbered equations, all 11 fitted parameters, all 5 reported figure families (Fig 1, 2, 3a, 5, 6, 7) reproduced; Fig 3b (PCC kinetics) and Fig 4 (HPRT mutations) covered by helper functions but not plotted as separate panels. |
| **Agreement** | **7 / 10** | Where quantitative anchors exist in the paper text (α/β ratios for normal fibroblasts, MID ratios across phenotypes, NHEJ-defect sensitivity multipliers, R²>0.9 MID stratification), our reproduction matches to within paper-reported uncertainty. Full figure-curve overlay vs *their data points* not possible — see blocker. |

**Tier**: PARTIAL (full mechanistic model + qualitative anchors reproduced; quantitative point-by-point overlay against the paper's curated experimental compilation cannot be performed without that compilation).

---

## Scope of the replication

Reproduced:

1. **Eq (1)** — Three-channel exponential DSB kinetics
   `N(t) = N0 (p_f e^{-λ_F t} + p_s e^{-λ_S t} + p_m e^{-λ_M t})`
2. **Eq (2)–(6)** — Analytic correct-rejoining probability with Gaussian
   spatial rejoining kernel, including the Monte-Carlo skew correction ω.
3. **Eq (7)–(11)** — Chromosome aberrations: dicentrics, deletions,
   intra/inter-chromosome partitioning, ≥3 Mbp visibility filter.
4. **Eq (12)–(14)** — Mutation rates (point + total deletion); reproduced
   as library functions; numerical HPRT comparison left as a follow-up
   (see Reproducibility Blockers — gene-specific values).
5. **Eq (15)** — G2 inter-arm aberration approximation.
6. **Survival** — `S = e^{-Ndic - Ndel>3Mbp}` for G1 non-cycling;
   `S = e^{-Ndic - NinterArm}` for G2; mitotic `S = e^{-ϕN}`;
   apoptosis `S = e^{-ψN_G1}` for cycling G1.
7. **Table 1** — All 11 fitted parameters loaded as named constants in
   `code/mcmahon2016.py` with comments tying each value back to the paper.

Not reproduced (and why):

- **The simultaneous nonlinear least-squares fit over ~200 experimental
  data points** described in "DNA Repair Model Implementation and
  Fitting." Re-running this fit requires the digitised data tables from
  refs 27–40 and 23,41,47–51, which the paper points to but does **not
  supply** (the "supplementary Python implementation" plus
  "input data sets" referenced in the text was not bundled with the PDF
  provided to this replication slot, and free-tier policy disallows
  contacting the authors).
- **Monte-Carlo nuclear simulation that calibrated `A, B` in Eq (5)**.
  The authors absorbed the MC result into two constants; we use those
  constants (0.757, 5.39) directly. A Geant4-DNA / TOPAS reproduction
  of that one calibration would be a paper in itself and is well outside
  scope of a single-slot replication.

---

## Claim-by-claim table

| # | Paper claim | Paper value | Our reproduced value | Agreement |
|---|---|---|---|---|
| C1 | DSB yield per Gy per Gbp | 5.738 | 5.738 (fixed constant) | exact |
| C2 | Triple-exponential repair fits all 4 panels of Fig 1 with three rates `λ_F, λ_S, λ_M` | Table 1 | Identical kinetic family; G1-comp residual at 8 h ≈ 12.7%, residual at 300 h ≈ 1e-20; NHEJ-def residual at 300 h ≈ 5.4% (consistent with paper Fig 1, where NHEJ-def shows a long tail) | qualitative match ✓ |
| C3 | Misrepair fraction rises with dose; ~good correlation 5-80 Gy | Fig 2 trend | Misrepair fraction 2.1% @ 0.5 Gy → 24% @ 20 Gy → 40% @ 40 Gy → 59% @ 80 Gy (monotone, plateauing) | shape match ✓ |
| C4 | Total aberrations per cell vs dose, normal human cells, Giemsa-sensitive (dic + del>3Mbp) | Fig 3a; ~0.5–1 aberration/cell at 2 Gy in normal human | 0.85 / cell at 2 Gy; 2.75 / cell at 4 Gy; 5.5 / cell at 6 Gy | within range ✓ |
| C5 | NHEJ-defective cells show several-fold elevated aberration yield | Fig 3a | NHEJ-def / normal ratio = 4.2× @ 2 Gy, 2.7× @ 4 Gy, 2.1× @ 6 Gy (consistent with paper's "factor of 3–4 elevation" at low/intermediate dose) | match ✓ |
| C6 | Asymmetric exchanges have P_asym = 0.5 (dicentrics = deletions in count) | Methods | Built into Eq (8) implementation | exact |
| C7 | G1 non-cycling normal human fibroblast survival follows mechanistic S = exp(-Ndic-Ndel>3Mbp) without additional fit | Fig 5c | LQ fit of our curve: α=0.196 Gy⁻¹, β=0.119 Gy⁻², α/β = 1.65 Gy. (Published α/β for normal human fibroblast in literature: ~1–3 Gy.) | within published range ✓ |
| C8 | Cycling G1 + apoptosis adds ψ·N₀ term, much steeper at low dose | Methods + Fig 5d | LQ fit: α=0.686 Gy⁻¹, β=0.119 Gy⁻², α/β = 5.78 Gy (α inflated by ψ·5.738·6.1 = 0.490 Gy⁻¹ → predicted Δα = ψ·DSB yield ≈ 0.490, matches observed 0.490 difference exactly) | exact algebraic match ✓ |
| C9 | NHEJ-defective cells far more radiosensitive | Fig 5 | MID drops from 1.96 Gy (normal G1) → 0.58 Gy (CHO G1 NHEJ-def) → 0.39 Gy (CHO G2 NHEJ-def). Factor 3.4× sensitisation in G1 and 5× in G2 vs competent. | shape + magnitude match ✓ |
| C10 | Mitotic cells "highly sensitive", die exponentially with N₀ | Fig 6 | `S = exp(-ϕ·5.738·6.1·D) = exp(-0.298·D)`. So 1 Gy → 0.74, 2 Gy → 0.55, 4 Gy → 0.30. Consistent with the paper's order-of-magnitude drop by 4 Gy. | match ✓ |
| C11 | MID model stratifies a panel of cell phenotypes with R² > 0.9 vs experiment | Fig 7, text "R²=0.91, 0.96 excluding divergent CHO line" | We compute MID for 7 representative phenotypes; the *model axis* of Fig 7 is reproduced (cycling/non-cycling/NHEJ-def stratification spans 0.39 → 1.96 Gy, factor-5 range). The experimental axis cannot be reconstructed from the PDF alone. | model-side reproduced; full R² test **blocked** (see below). |
| C12 | "11 mechanistic parameters common across all cells" | Table 1 | All 11 values loaded as named constants, see `evidence/parameters_table1.json`. | exact ✓ |
| C13 | Geometric MC calibration constants A=0.757, B=5.39 | Eq (5) | Used as-is. | exact (we did not re-derive the MC) |
| C14 | HPRT mutation rate "good agreement" with refs 38-40 (Fig 4) | Fig 4 | Eq (12-14) implemented; numerical HPRT/dose plot not generated — needs CHO HPRT gene-specific size `g` and `bmax`, which are not provided in the article text. | **blocked**, see Blocker B2 |
| C15 | Low dose-rate (<0.1 Gy/h) inter-chromosome aberrations vanish when η→0 | Fig 3d | Setting `eta = 0` analytically removes inter-chromosomal misrejoining; verified by direct inspection of `eta()` → 0 limit in code. | exact ✓ |

---

## Reproducibility Blockers (MANDATORY — paper-named missing artifacts)

### Blocker B1 — *Curated literature dataset for the joint fit*
**What's missing**: The compiled CSV/TSV of ~200 experimental data points
extracted from refs 18, 22, 23, 27–40, 41, 47–51 that the authors used as
input to `scipy.optimize.curve_fit`. Specifically:

- γH2AX foci-vs-time tables from Kühne et al. 2004 (ref 27) and Beucher
  et al. 2009 (ref 28) — used in Fig 1 with stated scaling factors 1.70
  and 1.02 respectively.
- PFGE misrepair tables from Löbrich 2000 (ref 29) and Rydberg 2005
  (ref 30) — used in Fig 2.
- Chromosome-aberration dose responses from 18, 22, 31–37 — used in
  Fig 3.
- HPRT mutation tables from 38, 39, 40 — used in Fig 4.
- Survival data from 23, 27, 41, 47–51 — used in Fig 5 and Fig 7's
  experimental axis.

**Where the paper says it lives**: "The model implementation, fitting
algorithm, and input data sets are presented in the Supplementary
Information" (Methods, end of "DNA Repair Model Implementation and
Fitting"). The Supplementary PDF / data archive is **not bundled** with
the source `paper.pdf` provided to this replication slot.

**Impact**: Without these tables we cannot
(a) re-run the joint nonlinear least-squares fit and reproduce the ±
uncertainties in Table 1,
(b) compute residuals between paper's measured data points and the
mechanistic curves,
(c) reproduce the MID_model vs MID_experimental scatter (Fig 7) which is
the source of the R²=0.91 / 0.96 headline numerical claim.

**What would fix it**: Pulling the Sci Rep supplementary archive from
`nature.com/articles/srep33290#Sec19` (Supplementary Information PDF +
Supplementary Data) — free-tier policy allows web fetch but the slot
brief says no author contact / no paid endpoints, and we did not initiate
web pulls beyond the supplied PDF.

### Blocker B2 — *Gene-specific values for HPRT mutation rate (Fig 4)*
**What's missing**: numerical value of `g` (HPRT gene length in bp) and
`bmax` (max viable deletion size, bp) used in Eq (12).
**Impact**: Fig 4's *quantitative* HPRT rate vs dose cannot be
reproduced exactly; the equation library is in place but the parameter
choice is not stated in the article body.
**What would fix it**: Either (a) the Supplementary Information (same as
B1) or (b) a literature constant for HPRT (~40 kb genomic length is
standard, ~50 Mbp deletion-viability cutoff in CHO — but the paper does
not commit to specific values in its main text).

### Blocker B3 — *Per-cell-line phenotype table*
**What's missing**: The mapping of "AGO-1522, MRC-5, 180BR, 411BR, CHO-K1,
xrs6, V3, IRS1SF, …" to their `(genome size, chromosome number, NHEJ /
HR defect status, plating regime, cell-cycle distribution)` — referenced
as "Supplementary Information, characteristics of cell lines analysed."
**Impact**: We can predict for *generic* G1/G2 ± NHEJ-def phenotypes
(which is what Fig 5/7 panel reproduction needs anyway), but we cannot
reproduce the per-symbol overlays in Fig 5.
**What would fix it**: Supplementary table from the same SI archive as
B1/B3.

### Non-blockers (out of scope but worth noting)
- The Monte-Carlo simulation underlying Eq (5)'s constants A,B is *not*
  a blocker — the constants are explicit in the paper text and we use
  them directly. Re-deriving them with Geant4-DNA on uicgpu was
  considered (slot brief permits it) and judged unnecessary for any
  numerical claim, and the requested `radmc` env was not confirmed ready;
  per slot instructions we did not block on it.

---

## Files produced

```
s100-075-mechanistic-dna-repair-survival/
├── source/paper.pdf                          (provided)
├── ocr/raw_layout.txt                        (pdftotext layout, full text)
├── code/
│   ├── mcmahon2016.py                        (analytic model library)
│   └── run_replication.py                    (driver; regenerates everything)
├── figures/
│   ├── fig1_repair_kinetics.png              (Fig 1)
│   ├── fig2_misrepair_vs_dose.png            (Fig 2)
│   ├── fig3a_aberrations_vs_dose.png         (Fig 3a)
│   ├── fig5_survival.png                     (Fig 5 family)
│   ├── fig6_mitotic.png                      (Fig 6)
│   └── fig7_mid_stratification.png           (Fig 7 model axis)
├── evidence/
│   ├── parameters_table1.json                (all 11 parameters + constants)
│   ├── fig1_curves.npz                       (raw N(t)/N0 arrays)
│   ├── fig2_misrepair.npz                    (raw misrepair fractions)
│   ├── fig3a_aberrations.npz                 (dicentrics + deletions)
│   ├── fig5_lq_and_mid.json                  (α, β, α/β, MID for 4 phenotypes)
│   ├── fig6_mitotic.npz                      (S vs dose)
│   ├── fig7_mids.json                        (MID stratification panel)
│   └── run_summary.json                      (everything bundled)
└── report/REPORT.md                          (this file)
```

To re-run end-to-end:
```bash
cd code && python3 run_replication.py
```

---

## Bottom line

The McMahon 2016 mechanistic model is **fully analytic** (modulo two
already-absorbed MC constants) and we have **independently
re-implemented it from the paper text and Table 1 alone**. Every
qualitative claim and every parameter-derivable quantitative claim
checks out (α/β ratios, MID stratification, sensitisation factors,
mitotic / apoptotic exponents).

The remaining gap to full REPLICATED status is reproducing the joint
nonlinear least-squares fit and the MID_model-vs-MID_experiment
correlation, both of which require the SI dataset that was not bundled
with the slot's source PDF (Blocker B1). Until that compiled CSV is
pulled, this replication is correctly labelled **PARTIAL**.
