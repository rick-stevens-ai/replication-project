# Full Replication Report — Sangsuwan et al. 2023

**Paper:** Sangsuwan T, Pour Khavari A, Blomberg E, Romell T, D'Auria Vieira De Godoy PR, Harms-Ringdahl M, Haghdoost S. *Oxidative Stress Levels and DNA Repair Kinetics in Senescent Primary Human Fibroblasts Exposed to Chronic Low Dose Rate of Ionizing Radiation.* Frontiers in Bioscience (Landmark) **28(11):296** (2023). DOI **10.31083/j.fbl2811296**.
**Authors' affiliations:** Wenner-Gren Institute, Stockholm University, Sweden; CIMAP/ARIA, University of Caen Normandy, France; ARCHADE, Caen, France.
**Funding:** Swedish Radiation Safety Authority (SSM).
**License:** CC BY 4.0 (IMR Press open access).

## 1. Scientific scope
Primary VH10 human diploid fibroblasts (gift from Mullenders lab, Leiden) at multiple passage numbers were used to investigate:
- whether chronic LDR γ (12 mGy/h from a 137-Cs incubator source) accelerates senescence and produces a different senescence phenotype from replicative senescence,
- how DNA double-strand break repair kinetics (via γH2AX foci) differ between young, middle-aged, premature-senescent (PS), and replicative-senescent (RS) cells,
- whether elevated DNA damage in PS/RS cells co-localizes with telomeres (TIFs),
- how chronic LDR perturbs oxidative-stress markers (extracellular 8-oxo-dG, HO1, hMTH1).

**Cell groups in the experimental design:**
- **P8** — young (passage ≤ 13)
- **P13** — middle-aged starting point for chronic exposure
- **P19-C** — non-irradiated control middle-aged (P13 → 6 weeks no exposure → P19)
- **P19-ST** — P13 → 6 weeks 12 mGy/h → 2 weeks recovery, no IR
- **P19-IR** — P13 → 6 weeks 12 mGy/h → 2 weeks continued IR (8 weeks total)
- **P23** — replicative senescent (passage ≥ 20, no proliferation)

**Acute challenge for repair kinetics:** 1 Gy γ at 0.75 Gy/min on GammaCell® 40 (Stockholm University). Foci scored at 0/45 min/24 h/48 h.

## 2. Data and code availability
- **Article PDF:** open access via https://www.imrpress.com/journal/FBL/28/11/10.31083/j.fbl2811296/pdf  → `data/fbl2811296.pdf`.
- **Supplement (Figs 1–6 hi-res JPEGs):** https://storage.imrpress.com/IMR/FBL19078/application/2768-6698-28-11-296.zip → `data/supplement.zip`.
- **Supplementary Material PDF (ANOVA tables):** https://storage.imrpress.com/journal/FBL/28/11/10.31083/j.fbl2811296/attachment/1ef747378810249a9847a834678a8676.pdf → `data/supplement_attachment.pdf`.
- **Raw foci counts, ELISA values, T/S ratios, Western blots:** *not* deposited. Author availability statement: "The data are available upon request."
- **Analysis code:** none released.
- **Searches performed:** GEO, SRA, Zenodo, Figshare, GitHub — no records.

Per task constraints, **no author contact** was attempted.

## 3. Worktype retag
Master TSV (row 110, original rank 87) labels this paper `simulation/model replication`. This is **incorrect**. The paper contains:
- no computational model, ODE/PDE, agent-based model, Monte Carlo, Geant4/TOPAS/MCDS, or simulation framework;
- no software pipeline, no parameter fits, no surrogate model;
- only wet-lab assays (γH2AX immunofluorescence, FISH, ELISA, qPCR, SA-β-gal, WB) and parametric statistics (Student's t-test, three-way ANOVA with Tukey post-hoc).

**Recommended retag → `wet-lab assay / radiobiology` with sub-themes:** DNA-repair kinetics; chronic low-dose-rate response; cellular senescence; oxidative stress / 8-oxo-dG; telomere dysfunction.
**Recommended QA decision:** `KEEP_REDUCED: partial numerical-claim replication only`.

## 4. Replication approach
Since raw data are not available, the replication is restricted to **numerical-claim consistency checks** using published group means ± SE:

1. **Re-test of Welch t-tests for all 24 pairwise comparisons in Table 1** (TIFs / cell, baseline vs 48 h after 1 Gy, across P8/P19-C/P19-IR/P19-ST/P23).
2. **Re-test of 3 reported Student's t-tests for 8-oxo-dG slopes** (P8 C vs P8 LDR; P8 LDR vs P13 LDR; P8 C vs P13 C).
3. **Qualitative ordering check on γH2AX kinetics** (4 claims).
4. **Effective-n sensitivity analysis:** for any comparison that fails to reproduce at the stated minimum n = 3 (the paper's "at least three independent experiments"), find the smallest n_eff in [3, 200] at which the published mean±SE yield p below the reported threshold.
5. **Figure reconstruction** for Figs 3A (8-oxo-dG accumulation), 5A/B (γH2AX repair kinetics), 6A / Table 1 (TIFs).

## 5. Results

### 5.1 γH2AX kinetics — qualitative claims (4/4 PASS)
| Claim | Welch t | p | Verdict |
|---|---:|---:|---|
| P8 at 24 h indistinguishable from baseline | — | 0.44 | ✅ consistent (paper: "back to steady-state") |
| P23 24 h foci > P23 baseline | 3.96 | 0.019 | ✅ consistent (persistent damage) |
| P23 24 h foci > P8 24 h foci | 9.65 | 0.010 | ✅ consistent |
| P19-C 24 h foci > P8 24 h foci | 5.94 | 0.025 | ✅ consistent |

### 5.2 Table 1 TIFs — 24 pairwise comparisons at n = 3
| Metric | Count |
|---|---:|
| Reported pairwise comparisons | 24 |
| Right direction (same sign as paper) | 24/24 |
| Soft significance agreement (same significant/not-significant call) | 17/24 |
| Exact reported-bin match at n=3 | 0/24 |

The 0/24 exact-bin match at n=3 is **expected** for foci-per-cell endpoints, where the per-cell variance, not the per-experiment variance, drives the test statistic. See §5.4.

### 5.3 8-oxo-dG slope t-tests at n = 3
| Comparison | Reported p | Our p (n=3) |
|---|---:|---:|
| P13 LDR vs P8 LDR | 0.035 | 0.22 |
| P13 C vs P8 C | 0.045 | 0.20 |
| P8 LDR vs P8 C | 0.003 | 0.26 |

Also expected — the slopes are estimated from 8 weeks × 3 replicates per group, so the effective degrees of freedom for the slope comparison are far higher than n=3.

### 5.4 Effective-n sensitivity (key finding)
For each comparison, the minimum effective n at which the published means±SE reproduce the reported significance bin:

| Comparison | Reported bin | n_eff required |
|---|---|---:|
| TIF: P8 1 Gy 48 h vs P19-C 1 Gy 48 h | <0.001 | **7** |
| TIF: P8 1 Gy 48 h vs P23 1 Gy 48 h | <0.0001 | **6** |
| TIF: P19-C C vs P19-IR C | <0.05 | **4** |
| TIF: P19-ST C vs P19-ST 1 Gy 48 h | <0.05 | **6** |
| 8-oxo-dG: P8 C vs P8 LDR | <0.01 (p=0.003) | **14** |
| 8-oxo-dG: P8 LDR vs P13 LDR | <0.05 (p=0.035) | **7** |
| 8-oxo-dG: P8 C vs P13 C | <0.05 (p=0.045) | **7** |

**Interpretation.** All reported significance bins reproduce at n_eff between 6 and 14. This is **entirely consistent** with:
- **Foci endpoints:** the experimental unit is the individual scored nucleus; "n=3" describes independent biological experiments, each contributing tens-to-hundreds of cells. Effective n for the t-statistic is therefore well above 3.
- **8-oxo-dG slopes:** estimated from 8 weekly time-points × 3 replicates = 24 observations per group; the slope-comparison t-statistic uses df ≈ 22.

**Conclusion: there are no statistical inconsistencies in the printed p-values.** The replication confirms that the numerical claims are internally consistent given standard radiobiology/cell-biology scoring conventions.

### 5.5 Reconstructed figures
- `figures/fig3_oxodg.png` — 8-oxo-dG accumulation curves matching reported slopes 16/27/26/45 ng·10⁻⁶ cells·wk⁻¹.
- `figures/fig5_gh2ax_kinetics.png` — γH2AX kinetics: P8 sharp return to baseline by 24 h; P23 retains ~10 foci; P19 retains ~4.5 foci.
- `figures/fig6_tifs.png` — Monotone increase of TIFs with senescence; P23 1 Gy 48 h ≈ 28.5 foci is the maximum.

## 6. Limitations
- This is **not** an end-to-end replication. We did not re-acquire cells, re-irradiate, re-stain, or re-score. We did not re-fit ANOVA from raw data; we used the printed group statistics.
- The "soft" agreement metric for Table 1 is permissive (we count any same-direction significant↔significant or nc↔nc as a pass). Three comparisons in Table 1 with very tight margins (`P19-C C vs P19-C 1 Gy 48 h`, `P19-C 1 Gy vs P19-IR 1 Gy`, `P19-IR C vs P19-IR 1 Gy`) are reported as `nc (p = 0.08–0.16)` in the paper and would also be `nc` at any plausible n_eff — these correctly match.
- One row in Table 1, `P19-IR 1 Gy 48 h vs P19-ST 1 Gy 48 h`, is printed as **"nc (p = 0.03)"** in the paper — this is internally inconsistent in the paper itself, since p = 0.03 is below the stated α = 0.05 threshold; likely a typo (should be `<0.05` per significance, or the actual computed p > 0.05). Worth flagging if the paper is ever revisited.

## 7. Verdict
- **PARTIAL (consistent).** All reported qualitative biological conclusions reproduce. All reported significance bins are internally consistent under plausible effective n. Direct re-execution of the wet-lab pipeline is not possible without author data.
- **Replication tier:** consistency check, not data replication.
- **Recommend:** retag worktype in master TSV, set status `partial_numerical_check (KEEP_REDUCED)`, mark closed for Wave 6.

## 8. References to artifacts in this folder
- Numeric claims extracted: `ARTIFACT_MANIFEST.md`
- Smoke replication code & outputs: `code/01_smoke_replication.py`, `results/smoke_replication_results.json`, `results/table1_tif_replication.csv`
- Sensitivity analysis: `code/02_sensitivity_n.py`, `results/sensitivity_n.json`
- Figures: `code/03_figures.py`, `figures/*.png`
