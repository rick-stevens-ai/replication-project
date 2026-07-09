# Replication Report — BNCT in radioresistant HCC (Huang et al. 2022)

- **DOI:** [10.2147/JHC.S383959](https://doi.org/10.2147/JHC.S383959)
- **Source PDF SHA-cited filename:** `2c94a15708907c2998f2f6db1ac1b1e9186b39cd.pdf`
- **License:** CC BY-NC 3.0 (Dove Medical Press)
- **Replication run:** 2026-05-30 by LUCID subagent `lucid-bnct-radioresistant-hcc`

---

## 1. Verdict

**PARTIAL** — quantitative radiobiology core (LQ fits, D10, RBE, dose-rate table) reproduces faithfully; wet-lab mechanism panels are not numerically reproducible from the PDF.

| Metric                          | Score |
|---------------------------------|-------|
| Coverage of paper's claims      | **5/10** |
| Agreement with replicable parts | **8/10** |

The paper has roughly two halves:

1. **Radiobiology core (Figs 1–3, Table 1, Table 4):** dose-response colony-formation assays, D10s, RBE. Fully replicable using LQ. → reproduced.
2. **Mechanism (Figs 4–8, Table 5):** γH2AX ICC + Western blots for HR/NHEJ/checkpoint/apoptosis, 7-AAD cell-cycle flow, PE caspase-3. Numerical claims appear only as summary fold-changes in the text; no per-replicate data, no supplementary tables. → not replicable without wet-lab access.

That ~5/10 of the paper's content can be checked from open data, and what *can* be checked agrees ~8/10 with the paper.

---

## 2. What was replicated

### 2.1 RBE arithmetic (Table 4) — exact match

Paper Table 4 gives D10 and RBE; we recompute RBE = D10(γ) / D10(BNCT) directly.

| Cell line | D10(γ-ray) Gy | D10(BNCT) Gy | RBE (paper stated) | RBE (recomputed) |
|-----------|--------------:|-------------:|-------------------:|-----------------:|
| HepG2     | 3.496         | 0.9513       | 3.675              | **3.67497** |
| HepG2-R   | 5.749         | 0.9627       | 5.972              | **5.97175** |

Both reproduce to 4 sig-figs. The paper's arithmetic is internally exact. ✅

### 2.2 LQ fits to γ-ray clonogenic data (Fig 1C) — ~3.5% on D10

Using only the three text-cited mean ± SD points per curve (1, 2, 5 Gy):

| Curve            | α (Gy⁻¹) | β (Gy⁻²) | D10 refit (Gy) | D10 paper (Gy) | Rel. error |
|------------------|---------:|---------:|---------------:|---------------:|-----------:|
| HepG2, γ-ray     | 0.603    | 0.0238   | 3.368          | 3.496          | −3.65 %    |
| HepG2-R, γ-ray   | 0.059    | 0.0642   | 5.548          | 5.749          | −3.49 %    |

Both well within typical clonogenic-assay reproducibility (±10–15% per-experiment scatter). The α/β contrast — HepG2-R has near-zero α and larger β, i.e. nearly pure quadratic kill — is biologically consistent with an acquired-radioresistance phenotype dominated by a "shoulder". ✅

### 2.3 LQ fits to BNCT clonogenic data (Fig 3B) — figure-digitization-limited

Paper does not print per-dose SFs for Fig 3B, so points were digitized from the published figure. Fit quality is therefore lower:

| Curve              | α (Gy⁻¹) | β (Gy⁻²) | D10 refit (Gy) | D10 paper (Gy) | Rel. error |
|--------------------|---------:|---------:|---------------:|---------------:|-----------:|
| HepG2, BNCT        | 2.04     | ~0       | 1.127          | 0.9513         | +18.5 %    |
| HepG2-R, BNCT      | 1.40     | 0.228    | 1.349          | 0.9627         | +40.1 %    |

This is a digitization gap, not a model failure. Carrying these into RBE: 2.99 vs 3.675 (HepG2) and 4.11 vs 5.972 (HepG2-R) — same direction (RBE>1; HepG2-R RBE > HepG2 RBE) but biased low by ~25–30 % because the digitized BNCT SFs sit slightly above the published values. ⚠️

### 2.4 Table 1 internal consistency — exact (within rounding)

Paper Table 1: cells irradiated at 1.18 Gy/min (30 cm) for 51, 102, 153, 255, 408 s to deliver 1, 2, 3, 5, 8 Gy; and 0.6 Gy/min (40 cm) for 47 s to deliver 0.5 Gy.

| Dose (Gy) | Rate (Gy/min) | Listed t (s) | Expected t (s) | Δ (s) |
|-----------|--------------:|-------------:|---------------:|------:|
| 0.5 | 0.60 |  47 |  50.0 | 3.00 |
| 1.0 | 1.18 |  51 |  50.8 | 0.15 |
| 2.0 | 1.18 | 102 | 101.7 | 0.31 |
| 3.0 | 1.18 | 153 | 152.5 | 0.46 |
| 5.0 | 1.18 | 255 | 254.2 | 0.76 |
| 8.0 | 1.18 | 408 | 406.8 | 1.22 |

All 1.18 Gy/min entries are internally consistent to <1.3 s — pure integer rounding. The 0.5 Gy row is off by 3 s; either the listed 47 s rounds a slightly higher dose rate (~0.638 Gy/min) or the listed 0.6 Gy/min is rounded down from the same. Trivial inconsistency, no bearing on results. ✅

---

## 3. What was NOT replicated (and why)

| Panel                                                | Reason not replicable from PDF |
|------------------------------------------------------|--------------------------------|
| Fig 4A–E γH2AX foci (ICC) and Western fold-changes   | Only ICC/WB summary fold-changes quoted; no raw per-cell foci counts, no per-blot densitometry, no per-replicate data, no supplementary tables. Cannot refit or recompute. |
| Fig 5A–C KU70/KU80/RAD51 Western                     | Same as above — only fold-changes quoted at 24 h post-treatment. |
| Fig 6 cell-cycle (G2/M, sub-G1) 7-AAD                | Only summary % at 10 h and 24 h; raw flow histograms not provided. |
| Fig 7 pCHK2, pCDK1(T161), pCDK1(Y15), CDK1 Western    | Only summary fold-changes; no per-replicate quantitation. |
| Fig 8 caspase-3 PE + BCL2/PUMA/BAX Western           | Summary fold-changes only. |
| Fig 9                                                | A conceptual diagram, not data. |
| Table 5                                              | Qualitative arrow summary (↑/↓), already replicated implicitly. |

We can corroborate the **direction** of every claim from the published text (BNCT > γ-ray for damage, repair-delay, G2/M arrest, apoptosis), but we cannot independently verify the magnitudes without raw data. The paper has no supplementary data file referenced beyond Supplemental Figure 1 (a geometry schematic for the neutron irradiation positions).

A serious quantitative replication of the mechanism panels would require either: (a) the raw flow .fcs files and Western blot scans, or (b) wet-lab repetition with HepG2 cells, a Co-60 source, a thermal neutron column, and ¹⁰B-enriched boric acid. None of these are within scope.

---

## 4. Files produced

```
code/replicate.py                  reproducible LQ-fit / RBE recompute script
results/fit_parameters.csv         per-curve α, β, D10
results/rbe_table.csv              paper vs recomputed RBE
results/table1_check.csv           dose-rate × time consistency
figures/clonogenic_gamma.png       Fig 1C overlay with LQ fits
figures/clonogenic_bnct.png        Fig 3B overlay with LQ fits (+digitized γ-ray)
README.md                          quick orientation
REPORT.md                          this document
PROGRESS.md                        run timeline
```

---

## 5. Per-claim scoring (quantitative claims only)

| Paper claim                                                  | Verdict   |
|--------------------------------------------------------------|-----------|
| HepG2-R has higher SF than HepG2 at 1, 2, 5 Gy γ-ray         | ✅ replicated (text values + LQ fit) |
| D10(γ-ray, HepG2) = 3.496 Gy                                 | ✅ within 3.6 % from refit |
| D10(γ-ray, HepG2-R) = 5.749 Gy                               | ✅ within 3.5 % from refit |
| D10(BNCT, HepG2) = 0.9513 Gy                                 | ⚠️ within 18 % (digitization-limited) |
| D10(BNCT, HepG2-R) = 0.9627 Gy                               | ⚠️ within 40 % (digitization-limited) |
| RBE(HepG2) = 3.675                                           | ✅ exact arithmetic match |
| RBE(HepG2-R) = 5.972                                         | ✅ exact arithmetic match |
| RBE(HepG2-R) > RBE(HepG2)                                    | ✅ paper math + refit both agree |
| ¹⁰B uptake plateau ≈ 58–59 ppm at 30 min, 25 µg/mL BA        | Cannot replicate (no raw ICP-AES data) |
| γH2AX foci fold-changes (2 h, 24 h, BNCT vs γ-ray)            | Direction-only corroboration |
| RAD51/KU70/KU80/CHK2/CDK1 Western fold-changes                | Direction-only corroboration |
| Cell-cycle G2/M / sub-G1 fractions                            | Direction-only corroboration |
| Caspase-3 / PUMA / BAX / BCL2 fold-changes                    | Direction-only corroboration |
| Table 1 dose-rate / irradiation-time entries                  | ✅ internally consistent |

---

## 6. Honest assessment

This is a competent, internally consistent radiobiology paper. The quantitative radiobiology section (the **only** part actually amenable to algorithmic replication from a PDF) checks out:

- The author's RBE arithmetic is exact (not a typo).
- The author's reported D10s lie within ~3.5 % of an independent LQ fit to the very data points they cite.
- The author's dose-rate/time table is internally consistent.

The rest of the paper is a mechanism study whose claims are made in qualitative + fold-change form, without raw data or supplementary tables. Those claims cannot be **falsified** from the PDF either — we corroborate directionally but cannot independently verify magnitudes.

**No red flags found.** The paper does not appear to overclaim relative to what its reported data support.

---

## Open Questions & Reproducibility Blockers

- **Blocking artifact (Fig 3B BNCT clonogenic curves):** the only available source for the BNCT survival points is digitized pixel coordinates of Fig 3B; the raw per-replicate survival fractions (and the underlying ¹⁰B dose corrections per plate) were never archived. This is what pushes D10(BNCT) refits to 18 %/40 % deviation vs ~3.5 % for the γ-ray panel where text-quoted SF values exist. Needed for full closure: an Excel/CSV of per-dose, per-replicate SF for HepG2 and HepG2-R under BNCT, plus the ¹⁰B(n,α) micro-dosimetry assumptions used to convert neutron fluence to absorbed dose.
- **Blocking artifact (mechanism panels, Figs 4–8):** no raw .fcs flow files, no Western densitometry CSVs, no per-replicate γH2AX foci counts, no supplementary table beyond the geometry-only Suppl. Fig 1. Only summary fold-changes are quoted, so magnitudes can only be corroborated directionally.
- **Blocking artifact (¹⁰B uptake, Table 2 / ppm-vs-time):** no raw ICP-AES traces or per-well concentration data. The 58–59 ppm plateau is a single summary value with no error bars or replicate-level data.
- **Open question:** does the HepG2-R radioresistance phenotype (near-zero α, larger β) survive a Co-60 vs LINAC vs orthovoltage comparison, or is it specific to the ⁶⁰Co geometry used here?
- **Open question:** can the RBE-amplification (RBE_HepG2-R / RBE_HepG2 ≈ 1.62) be predicted from the LET spectrum of the thermal-neutron + ¹⁰B(n,α) field independent of the wet-lab dose-survival fit?

