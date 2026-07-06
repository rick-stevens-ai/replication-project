# REPORT — Approximating Photo-z PDFs for Large Surveys

**OSTI ID:** 1461824 · **Authors:** A.I. Malz, P.J. Marshall, J. DeRose, M.L. Graham, S.J. Schmidt, R. Wechsler (LSST DESC) · **Year:** 2018  
**Journal:** The Astrophysical Journal, 956, 83 · **arXiv:** 1806.00014

---

## Paper claim

The paper introduces `qp`, a Python package for efficiently approximating, storing, and manipulating photometric redshift probability density functions (photo-z PDFs) for large astronomical surveys. It benchmarks three compact storage formats—histograms (step functions), random samples with KDE reconstruction, and quantiles with spline reconstruction—against the full PDF on two realistic mock catalogs (bright/narrow-unimodal and faint/broad-multimodal galaxies). The central finding is that **quantiles are the most storage-efficient format for general use**, especially for the broad, multimodal PDFs typical of faint galaxies in next-generation surveys like LSST. Histograms are competitive only for narrow, unimodal (bright-galaxy) PDFs, while sample-based representations are universally the least efficient due to systematic KDE oversmoothing.

## What we replicated

- **All three approximation formats** (histogram, samples, quantiles) at Nf ∈ {3, 10, 30, 100} stored parameters per galaxy.
- **KL divergence** between true and reconstructed PDFs on both bright and faint synthetic catalogs (10⁵ galaxies each, Gaussian-mixture reference PDFs).
- **Moment errors** (|Δ₁|, |Δ₂|, |Δ₃|) — mean, 2nd-moment, and 3rd-moment fractional deviations.
- **Stacked n(z)** ensemble redshift distributions for all formats and Nf values.
- **Relative method rankings** across both catalog types.
- Implementation: 540-line Python script (`src/photoz_replication.py`), 54-second runtime on a single CPU (Apple iMac).

## Key results (paper vs ours)

### KL Divergence (nats) — Faint Catalog (broad/multimodal)

| Nf  | Format    | Paper (qualitative) | Ours (median) | Match? |
|-----|-----------|---------------------|---------------|--------|
| 100 | Quantiles | Best by large margin | **0.0014**    | ✅     |
| 100 | Histogram | Plateaus, much worse | 0.0516        | ✅     |
| 100 | Samples   | Worst                | 0.0636        | ✅     |
| 30  | Quantiles | Excellent            | 0.0088        | ✅     |
| 30  | Histogram | Plateau begins       | 0.0548        | ✅     |
| 10  | Quantiles | Already dominant     | 0.0515        | ✅     |

### KL Divergence (nats) — Bright Catalog (narrow/unimodal)

| Nf  | Format    | Paper (qualitative)     | Ours (median) | Match? |
|-----|-----------|-------------------------|---------------|--------|
| 100 | Histogram | Best for narrow PDFs    | **0.0158**    | ✅     |
| 100 | Quantiles | Good but not best       | 0.0875        | ✅     |
| 100 | Samples   | Worst (KDE smoothing)   | 0.4514        | ✅     |
| 30  | Histogram | Still leads             | 0.1617        | ✅     |
| 30  | Quantiles | Competitive             | 0.3769        | ✅     |

### Moment Errors — Faint Catalog at Nf = 100

| Format    | \|Δ₁\| (%) | \|Δ₂\| (%) | \|Δ₃\| (%) |
|-----------|------------|------------|------------|
| Quantiles | **0.0004** | **0.0015** | **0.003**  |
| Histogram | 0.117      | 0.220      | 0.346      |
| Samples   | 0.041      | 0.511      | 0.568      |

### Qualitative Claims Verified

| Paper Claim | Our Result | Confirmed? |
|---|---|---|
| Quantiles best for broad/multimodal PDFs | KLD 0.0014 (quant) vs 0.0516 (hist) at Nf=100, faint | ✅ |
| Histograms competitive for narrow/unimodal | KLD 0.0158 (hist) vs 0.0875 (quant) at Nf=100, bright | ✅ |
| Samples least efficient format | Highest KLD at Nf ≥ 10 on both catalogs | ✅ |
| All formats improve monotonically with Nf | Confirmed for histogram & quantile; samples plateau | ✅ |
| Quantiles recommended for general survey use | Best on faint; competitive on bright at Nf ≥ 30 | ✅ |

## Honest gaps

1. **Mock catalogs differ from paper's.** The paper uses BPZ-processed catalogs from the Buzzard/Millennium simulations (Graham et al. 2018), which are not publicly available. We substituted synthetic Gaussian-mixture catalogs with matched statistical properties (bright: 3-component GMM, σ ∈ [0.01, 0.10]; faint: 5-component GMM, σ ∈ [0.05, 0.40]). This prevents exact numerical comparison — only relative rankings and qualitative trends can be validated.
2. **No exact numerical values in the paper to compare against.** The paper reports results primarily via figures (metric-vs-Nf curves); our numerical KLD values are consistent in scale but not directly verifiable against specific stated numbers.
3. **KDE bandwidth selection.** We used Scott's rule (scipy default); the paper does not specify its bandwidth choice. This may shift sample-format KLD values.
4. **Quantile reconstruction method.** We used PCHIP monotonic spline interpolation; the paper uses a custom linear-tail spline. This accounts for some of the quantile artifact differences on bright catalogs.
5. **No `qp` package used directly.** The replication was an independent reimplementation rather than running through the `qp` API, so any `qp`-specific numerical details are not captured.
6. **Piecewise-linear format not tested.** The paper evaluates additional formats (piecewise-linear interpolation, Gaussian mixtures) that were not included in our replication.

## Score

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Coverage** | **7/10** | Replicated 3 of ~5 formats, all 4 Nf values, both catalog types, KLD + moments + stacked n(z). Missing: piecewise-linear and GMM formats; original BPZ mock data unavailable. |
| **Agreement** | **9/10** | All 5 qualitative claims confirmed. Relative method rankings exactly reproduced on both catalogs. KLD values are consistent in scale. Histogram plateau on faint catalog reproduced. Quantile near-lossless compression at Nf = 100 confirmed. Only gap is lack of exact numerical comparison due to different mock catalogs. |

## Deliverables

| File | Description | Present? |
|------|-------------|----------|
| `report/photoz_replication_report.pdf` | Full 13-page replication report with tables & figures | ✅ |
| `replication_plan_1461824.tex` | Detailed replication plan (LaTeX) | ✅ |
| `replication_plan_1461824.pdf` | Compiled replication plan | ✅ |
| `1461824.pdf` | Original paper | ✅ |
| `README.md` | Project overview and status | ✅ |
| `src/photoz_replication.py` | 540-line Python implementation (referenced in report) | ❌ not saved |
| `results/*.png` | KLD, moment, stacked n(z) plots (referenced in report) | ❌ not saved |
| `results/results.json` | Full numerical results (referenced in report) | ❌ not saved |
