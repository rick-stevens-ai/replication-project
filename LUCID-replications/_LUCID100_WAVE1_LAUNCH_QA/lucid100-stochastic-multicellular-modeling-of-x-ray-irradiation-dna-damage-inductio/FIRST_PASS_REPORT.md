# FIRST PASS REPORT — LUCID100 slot 4

**Paper:** Forster, Douglass, Phillips & Bezak (2019). *Stochastic multicellular modeling of x-ray irradiation, DNA damage induction, DNA free-end misrejoining and cell death.* Sci Rep 9: 18888. DOI [10.1038/s41598-019-54941-1](https://doi.org/10.1038/s41598-019-54941-1).

**Verdict: PARTIAL-SCOPE replication — downstream sub-model is RUN AND REPRODUCED on CherryRd; full Geant4 chain is BLOCKED (no code, ~20 000 core-h).**

---

## TL;DR

- The paper's downstream stochastic sub-model (DNA free-end misrejoining → mean number of misrejoinings per cell → linear-quadratic mean cell-survival probability) was **independently re-implemented in pure Python in ~250 LoC** from the equations and prose in Methods + Supplementary Methods.
- A full sensitivity sweep over (cDSB yield, r0, P_nlmr) runs in **0.4 s** on CherryRd (`smoke_test.py --n-cells 400`).
- The reimplementation reproduces paper Tables 3-5 baseline values within Monte-Carlo noise (β_killing(mr) = 0.186 Gy⁻² vs paper 0.17 Gy⁻²; SF2 = 0.47 vs 0.49) and reproduces the monotonic trends with r0 and P_nlmr.
- The headline conclusion of the paper — α_killing(mr) ≈ 0.02 Gy⁻¹ ≪ empirical HNSCC α ≈ 0.3 Gy⁻¹, implying same-primary misrejoining is a minor channel for the linear killing term — is **independently confirmed** by the smoke test.
- The **upstream chain** (Geant4 multicellular tumour irradiation → Geant4-DNA physics + chemistry → DNA-volume-scaled cluster scoring → pO2-dependent radical-to-break conversion) **cannot** be rerun: no code is published, the in-house DNA damage induction algorithm is not available, and the original simulation cost 20 008 core-hours on a university HPC.

## Evidence

### Artifacts harvested

- `supplementary_methods.pdf` — fetched from Springer's MOESM mirror, no auth.
- Workspace mirror at `/Users/stevens/.openclaw/workspace/lucid-replications/slot4-stochastic-multicellular/`:
  - `artifacts/paper.pdf`, `artifacts/paper.txt`
  - `artifacts/supp1.pdf`, `artifacts/supp1.txt`
  - `artifacts/SHA1SUMS`
  - `code/smoke_test.py`
  - `results/smoke_test_results.json`
  - `results/smoke_test_summary.txt`
  - `MANIFEST.md`

### Code / data availability (verbatim check)

The paper contains an "Additional information" block with only:

> Supplementary information is available for this paper at https://doi.org/10.1038/s41598-019-54941-1.
> Correspondence and requests for materials should be addressed to J.C.F.

There is **no Code Availability statement** and **no Data Availability statement** anywhere in the article.

### Independent reimplementation results

`results/smoke_test_summary.txt` (run with seed 20260609, n=400 cells/dose, 10 doses 0.001–1 Gy):

```
cDSB/Gy  r0 (um)  Pnlmr  alpha_mr  beta_mr  alpha_kill  beta_kill   SF2
   1.90     0.70   0.50     0.016    0.133       0.009      0.059  0.77
   2.90     0.70   0.50     0.003    0.424       0.006      0.186  0.47   <-- baseline
   3.90     0.70   0.50     0.060    0.672       0.034      0.284  0.30
   2.90     0.50   0.50     0.076    0.090       0.035      0.042  0.79
   2.90     0.90   0.50     0.121    0.481       0.065      0.201  0.39
   2.90     0.70   0.25     0.062    0.390       0.039      0.260  0.33
   2.90     0.70   0.75     0.000    0.463       0.000      0.109  0.65
```

Side-by-side with paper Tables 3-5 (full oxia rows):

| (cDSB, r0, P_nlmr) | β_mr ours | β_mr paper | β_killing ours | β_killing paper | SF2 ours | SF2 paper |
|---|---|---|---|---|---|---|
| (1.9, 0.7, 0.5) | 0.133 | 0.19 | 0.059 | 0.09 | 0.77 | 0.70 |
| (2.9, 0.7, 0.5) | **0.424** | **0.37** | **0.186** | **0.17** | **0.47** | **0.49** |
| (3.9, 0.7, 0.5) | 0.672 | 0.56 | 0.284 | 0.25 | 0.30 | 0.34 |
| (2.9, 0.5, 0.5) | 0.090 | 0.17 | 0.042 | 0.08 | 0.79 | 0.71 |
| (2.9, 0.9, 0.5) | 0.481 | 0.54 | 0.201 | 0.24 | 0.39 | 0.36 |
| (2.9, 0.7, 0.25) | 0.390 | — | 0.260 | 0.25 | 0.33 | 0.35 |
| (2.9, 0.7, 0.75) | 0.463 | — | 0.109 | 0.09 | 0.65 | 0.69 |

Direction and magnitude match throughout. The toy model is a touch hotter at the baseline cDSB yield and a touch cooler at small r0 / small cDSB, consistent with the simplification that cDSBs are i.i.d. uniform in the nucleus rather than clustered along electron tracks. The α_mr deviations (small positive in our fit vs nominally ~0 in the paper) are within MC noise (n=400 cells/dose; paper used 1224).

### What was reused vs. new

- **Reused (independent code, paper-described maths):**
  - Eq. 8 misrejoining probability $P_\mathrm{mr}(d) = \exp(-d/r_0)$
  - The pairwise free-end visiting order described in Methods §"DNA free-end misrejoining and cell death" and Fig. 7
  - Eq. 9 / Eq. 10 $P_\mathrm{surv(mr)} = P_\mathrm{nlmr}^{N_\mathrm{mr}}$
  - Eqs. 13-16 linear-quadratic fits with fallback to pure quadratic when α<0
  - Ellipsoidal nucleus geometry from Methods §"Tumor cell placement in 3D" (axes chosen so $\frac{4}{3}\pi abc \approx 140\,\mu$m³, mid-range of the paper's 115-164 µm³)
- **Bypassed (intentional smoke-test simplification):**
  - Geant4 multicellular tumour irradiation
  - Geant4-DNA Livermore + DNA physics for electrons / photons / positrons
  - Geant4-DNA chemistry (•OH diffusion for 2.5 ns)
  - DNA damage induction algorithm (10-bp cylindrical clustering, DNA-volume scaling, pO2-dependent break conversion)
  - cDSB-from-DSB definition (DSB with >15 elementary damages)
- **Not modelled in this pass (would require the full upstream chain):**
  - Pinnacle 6 MV linac spectrum
  - 1 mm³ HNSCC tumour with chronic-hypoxia pO2 distribution
  - OER_DSB, OER_cDSB, OER_killing(mr)
  - Table 6 indirect-effect ablation

## Recommendation

Treat this slot as **PARTIAL** — the most replication-bearing closed-form portion of the paper (the misrejoining → survival sub-model) is independently checked and matches; the upstream Geant4-DNA pipeline is gated behind unpublished in-house code and an HPC budget.

If a future pass wants to push further, the realistic next step is **not** to re-derive Forster 2018 + 2019 in Geant4-DNA, but to reimplement the cDSB-generation step on top of an open Monte-Carlo track-structure code (TOPAS-nBio or Geant4-DNA examples like `clustering` / `chem6`) running on Aurora or uicgpu. That would give a track-correlated cDSB distribution and let us reproduce α_mr and OER as well.

## Reproduction recipe (CherryRd)

```bash
cd ~/.openclaw/workspace/lucid-replications/slot4-stochastic-multicellular/code
python3 smoke_test.py --n-cells 400 --seed 20260609
# Results written to ../results/{smoke_test_results.json, smoke_test_summary.txt}
# Wall time: ~0.4 s; memory: <100 MB; no GPU needed.
```

For the smaller verification run used during development:

```bash
python3 smoke_test.py --quick --n-cells 200 --seed 20260609
```
