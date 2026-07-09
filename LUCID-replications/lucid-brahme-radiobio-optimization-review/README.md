# lucid-brahme-radiobio-optimization-review

LUCID100 max-rate backfill — Wave 6, slot 60 (paper rank 91 in `LUCID100_SOLID_MASTER_QA.tsv`).

## Paper
- **Title:** New Radiation Oncology Optimization Principles Based On In-Vivo Predictive Assay and Recent Developments in Molecular Radiation Biology
- **Author:** Anders Brahme (Karolinska Institutet)
- **Venue:** Annals of Case Reports, 9:1625, 2024 (Gavin Publishers)
- **DOI:** [10.29011/2574-7754.101625](https://doi.org/10.29011/2574-7754.101625)
- **PDF (OA):** [Gavin Publishers PDF](https://www.gavinpublishers.com/assets/articles_pdf/New-Radiation-Oncology-Optimization-Principles--Based-On-In-Vivo-Predictive-Assay-and-Recent-Developments-in-Molecular-Radiation-Biology.pdf)
- **Local copy:** `paper.pdf` (4.5 MB, PDF 1.7), text extract `paper.txt` (2,159 lines)

## Paper type
- **Format:** Single-author "Research Article", but in substance a **broad review / opinion / synthesis**.
- **Content:** 38 figures, no Methods section in the experimental sense, no new wet-lab/clinical dataset. References are dominated by the author's own earlier work (Brahme refs [1-3, 5-6, 19-21, 23, 34, 45, 51-55]).
- **Venue caveat:** Gavin Publishers' *Annals of Case Reports* is widely flagged in predatory-publisher lists. There is no evident peer-review trail.

## Central scientific claims
1. **LDHS / LDA / HDA framework.** Most TP53-intact normal tissues are Low-Dose Hypersensitive and Low-Dose Apoptotic; the fractionation window at ≈ 2 Gy/Fr defines the *normal-tissue* tolerance (not the tumor dose).
2. **Optimal fraction size ≤ 2.3 Gy/Fr** with low ionization density / low LET to organs at risk, exploiting the ½ Gy threshold for full DNA repair onset.
3. **Light-ion advantage (He–B).** Lightest ions retain the fractionation window in plateau (low LET in normal tissues) while delivering high LET only in the Bragg peak, maximizing apoptosis/senescence in the tumor. Carbon and heavier ions lose this window.
4. **RHR (Repairable-Homologous-Repairable) cell-survival model** is preferred over LQ; explicitly separates NHEJ vs HR repair and apoptosis, and describes LDHS where LQ fails.
5. **Biological optimization via P+ (complication-free cure).** Eq (1): `P+ = PB − PI + δ(1−PB)PI`, δ ≈ 0.2.
6. **Microdosimetric heterogeneity caps γC.** Increasing LET widens microscopic relative variance, capping the dose-response steepness γC at ≈ 4 for neutrons/carbon, vs ≈ 5–6 for photons/lithium.
7. **BIOART / IVPA workflow.** PET-CT before vs after 1 week of ≈18 Gy gives D0,eff per voxel, enabling individualized biologically optimized dose redistribution.

## Equations of interest (explicitly stated)
- **Eq (1)** complication-free cure: `P+ = PB − PI + δ(1 − PB) PI`, δ ≈ 0.2.
- Tumor cure ∝ `e^(−N)` with `N` = mean surviving clonogens (Poisson eradication).
- `γC ≈ ln(N)/e` low-LET asymptotic slope.
- LQ / RCR / RHR survival forms compared in Figure 7.

## Data, code, supplementary
- **Data:** None new. All quantitative content is replotted from Brahme's prior papers (refs 1–3, 23, 34, 45, 53, 55).
- **Code:** None.
- **Supplementary:** None.
- **In Vivo Predictive Assay data:** Conceptual; the single illustrative case (Figure 11, large lung cancer, FDG-PET pre / post 18 Gy) has no patient-level data deposited.

## Verdict
- **NO-GO for true replication** of any new finding — there is no new finding. All figures are conceptual or replots from earlier Brahme publications already in the literature.
- **GO for a small didactic smoke** that reimplements the *named* equation (Eq 1, P+) on toy sigmoid PB / PI dose-response curves, qualitatively recovering the published claim that δ ≈ 0.2 yields a higher P+ at the optimum than the independence assumption (δ = 1), and that high-LET (low γC) shrinks the therapeutic window.
- Recommend a **QA retag** from `candidate_curated` to `NO_GO_REVIEW_ONLY` (review/perspective in predatory venue; figures non-original; no new data or code), with a note that the smoke artifact below provides a defensible "demonstrated-the-formalism" output.

## Layout
- `paper.pdf` / `paper.txt` — source.
- `artifacts/MANIFEST.md` — artifact harvest table.
- `smoke/p_plus_smoke.py` — minimal Python reproduction of Eq (1) on toy sigmoid PB / PI.
- `figs/` — generated plots.
- `PROGRESS.md` — chronological log.
- `FIRST_PASS_REPORT.md` — final verdict and recommendation.

## How to run the smoke
```bash
cd smoke
python3 p_plus_smoke.py
```
Outputs `../figs/p_plus_smoke.png` and `../figs/p_plus_smoke.csv`. Numpy + matplotlib only.
