# PEDIATRIC ANALOG — Alter et al. 2026 multitensor GSVD on medulloblastoma

**Goal (Rick):** does the prognostic/method claim of Alter et al. 2026 transfer
to a pediatric copy-number-driven cohort — specifically the canonical CN-driven
medulloblastoma pair Group3 (MYC-amplified) vs Group4 (isodicentric-17q) — or
was the result NBL-specific?

**Compute:** uicgpu (CPU; linear-algebra workload). Engine = the same tested
`gsvd_reference.py` (10/10 unit tests, reconstruction <1e-8) + `survival_stats.py`
(scipy KM/log-rank/Cox/concordance fallback — `lifelines` not installed; engine
flagged in JSON output).

**Bottom line up-front:** the prognostic claim **does NOT transfer** to pediatric
medulloblastoma any better than it did to neuroblastoma. The unsupervised GSVD
"most-exclusive" arraylets pick up a weak subgroup signal (Pearson r ≈ 0.19),
while ordinary PCA on a single layer recovers the same subgroup axis at r ≈ 0.70
on expression and r ≈ 0.68 on methylation — a 3-4× advantage for the simpler
method, on the same matched patients. On the sharpest Group3-vs-Group4 test,
the GSVD-based 2D centroid classifier hits 63.2 % accuracy (vs a 69 % majority-G4
prior); PCA on either single layer hits 95-96 %. The "tumor-exclusive" pattern
selection rule — central to the paper — is identifying the *least* informative
arraylets in this cohort.

---

## What we could and could not get from open data

**Got (free, no dbGaP):**
- Cavalli/Northcott/Taylor lab MB resource via GEO:
  - **GSE85217**: Affymetrix HuGene 1.1 ST expression, 21 642 probes × **763 primary MB samples**, with per-sample subgroup labels (WNT/SHH/Group3/Group4) and second-level subtype labels (alpha/beta/gamma/delta).
  - **GSE85212**: Illumina 450K methylation, 321 175 CpGs × **763 primary MB samples**, patient-matched to GSE85217 on the `MB_SubtypeStudy_55XXX` IDs.
  - SubSeries of GSE85218 (SuperSeries, Cavalli et al. 2017 Cancer Cell).
  - Subgroup labels present in series-matrix sample characteristics.
- cBioPortal **mbl_icgc** study (Northcott 2017 ICGC, **n=125** patients) with
  per-patient OS_MONTHS, OS_STATUS, PFS, SUBGROUP, M_STAGE, AGE, SEX, mutation
  count from WGS. Used for FRONT 1 (standard-of-care survival baseline).
- cBioPortal **mbl_sickkids_2016** study (n=46, only 28 with OS) — used as
  secondary baseline, sample too small for strong conclusions.

**Could not get (open-data gap, intrinsic):**
- **Per-sample overall-survival data from the Cavalli n=763 cohort.** OS appears
  only in the paper's paywalled supplementary tables; the GEO release contains
  no `!Sample_characteristics_ch1` survival field. Confirmed by inspecting
  `gse85217_meta.txt` (only `tissue:`, `subgroup:`, `subtype:` are exposed).
  This is the equivalent of the NBL Path-B "WGS is dbGaP" gap.
- **Genome-wide copy-number matrix per patient.** The cBioPortal MB studies
  expose only `MUTATION_EXTENDED/MAF` and a handful expose `STRUCTURAL_VARIANT`
  — none expose `COPY_NUMBER_ALTERATION` profiles. The CPTAC pediatric brain
  study (`brain_cptac_2020`) has discrete + log2 CNA + RNA-seq + survival but
  contains only **22 MB samples** out of 218 total — too small for cohort-scale
  GSVD survival work.
- **WGS-resolution (1-kb-bin) CN profiles like the paper's.** Open MB resources
  use either Affymetrix expression or Illumina 450K methylation — both
  feature-rich but not 1-kb CN bins. As with NBL Path-B, this is a genuine
  resolution-gap limitation intrinsic to the open data, not a tuning failure.

**Substitute strategy (mirrors NBL Path-B):** run the GSVD on two genuine
patient-matched omic layers (expression × methylation, exactly as NBL Path-B
did), evaluate the unsupervised arraylets against the established prognostic
axis (SUBGROUP), and compare against PCA on each single layer. For real per-
patient OS use the independent mbl_icgc cohort with the established subgroup
axis.

---

## FRONT 1 — Standard-of-care survival baselines (the bar the method must beat)

Computed on cBioPortal **mbl_icgc** (n=103 with valid OS) and **mbl_sickkids_2016**
(n=28 with OS). All numbers from the project's KM/log-rank/Cox/concordance code,
real OS_MONTHS / OS_STATUS data, no synthetic outcomes.

**mbl_icgc (Northcott 2017, n=103 with OS):**

| Indicator | n | C-index | HR | log-rank P |
|---|---|---|---|---|
| Subgroup ordered (Grp3>Grp4>SHH>WNT) | 94 | **0.610** | 1.49 | Cox P=0.108 |
| **Group3 vs rest (binary)** | 103 | **0.598** | **2.54** | **0.027** |
| **Group3 vs Group4 only** | **56** | **0.662** | **4.05** | **0.014** |
| M+ vs M0 | 102 | **0.621** | **2.78** | **0.009** |
| Age (continuous) | 103 | 0.503 | 1.00 / yr | 0.987 |
| Age ≥10 yr | 103 | 0.516 | 1.18 | 0.683 |
| Female vs male | 103 | 0.520 | 1.16 | 0.71 |

**Finding 1:** In this open cohort, the **Group3-vs-Group4 contrast hits
C=0.662, HR=4.05, log-rank P=0.014** — this is the sharpest, most CN-mechanism-
specific pediatric prognostic signal available open. **This is the bar the
GSVD predictor must beat** in an unsupervised, label-free way, to support the
paper's central claim that the method finds a tumor-exclusive prognostic axis
that beats clinical standard of care.

**mbl_sickkids_2016 (n=28 with OS):** sample is too small for any indicator to
reach significance (best concordance 0.572, all P > 0.05). Reported for
completeness in `results/f1_baseline.json` but not used for conclusions.

---

## FRONT 2 — The method (GSVD) on matched open MB multiomic layers

**Cohort:** Cavalli matched expression × methylation, **n=762 patient-matched**
on `MB_SubtypeStudy_XXXXX` IDs (1 of 763 dropped — one patient missing from
the methylation matrix). Subgroup distribution after matching:
SHH=222, Group4=326, Group3=144, WNT=70.

D1 = expression (top 5 000 high-variance probes, median-centered)
D2 = methylation (top 10 000 high-variance CpGs, median-centered)
GSVD (`gsvd_reference.py`) → c/s ratios span [0.285, 22.12]; k_first=761
(RNA-exclusive, c/s ≈ 22.12), k_last=0 (Meth-exclusive, c/s ≈ 0.285),
k_shared=36 (c≈s).

**Unsupervised arraylet recovery of MB subgroup (Pearson r vs the prognostic
ordering WNT(0)<SHH(1)<Group4(2)<Group3(3)):**

| Predictor | n | Pearson r vs subgroup | P |
|---|---|---|---|
| GSVD u_first (RNA-exclusive) | 762 | +0.193 | 7.5e-8 |
| GSVD u_last (Meth-exclusive) | 762 | −0.187 | 1.9e-7 |
| GSVD u_shared (c≈s) | 762 | −0.367 | 9.7e-26 |
| **Expression PC1 (PCA on D1)** | 762 | **+0.702** | **3.8e-114** |
| **Methylation PC1 (PCA on D2)** | 762 | **+0.680** | **1.2e-104** |

**Unsupervised subgroup CLASSIFICATION (4-class nearest-centroid in 2D, where
chance ≈ 33-43 % depending on prior; majority-class Group4 prior = 42.8 %):**

| Method | 2D-centroid accuracy | KMeans (k=4) ARI |
|---|---|---|
| GSVD (u_first × u_last) | **0.416** | **0.093** |
| **Expression PCA (PC1×PC2)** | **0.963** | **0.891** |
| **Methylation PCA (PC1×PC2)** | **0.944** | **0.617** |

**C2 orthogonality:** cos(u_first, u_last) in the patient mode = **−0.218**
(paper claims ~0). Closer to zero than the NBL Path-B result (0.33) but still
not strictly orthogonal.

**Robustness:** GSVD numbers reproduce across feature-count choices
(top_rna=2 000, top_meth=5 000 gave acc=0.445 / ARI=0.141 — qualitatively the
same; PCA accuracies stayed at ≈ 0.96 / 0.94). The method is numerically stable
across configurations, but the predictive signal is weak across all of them.

### What the paper's pattern-selection rule actually picks

I scanned all 762 GSVD arraylets and ranked them by |Pearson r| against the
prognostic ordering. The **top single-arraylet** is pattern **k=19** with
**r = +0.732, P = 5.8e-129** — i.e. there *is* a GSVD pattern that approximately
matches expression PC1 (r = 0.702) at subgroup recovery, but it is **NOT**
the one the paper's "most-exclusive" rule selects (which picks k=761 / k=0).
The paper's selection criterion (extreme c/s ratio = "exclusive to one layer")
recovers patterns with r ≈ 0.19 — well below an interior pattern that picks
out subgroup just as well as PCA does. **The paper's central pattern-selection
rule, applied to pediatric MB data, picks bad arraylets.**

(Full top-10 in `results/f2_pattern_scan.json`.)

---

## Subgroup-restricted test (Group3 + Group4 only — the CN-driven pair)

Rick's "sharpest pediatric-CN-specific test." Re-running the GSVD on patients
restricted to Group3 + Group4, n=470 (G3=144, G4=326), evaluating against
the binary Group3-vs-Group4 label.

| Predictor | Pearson r vs Group3 | 1D-threshold acc | 2D centroid acc |
|---|---|---|---|
| GSVD u_first (RNA-exclusive) | −0.190 | 0.581 | — |
| GSVD u_last (Meth-exclusive) | −0.168 | 0.581 | — |
| GSVD u_shared | +0.083 (NS) | 0.526 | — |
| GSVD (u_first × u_last) 2D | — | — | **0.632** |
| **Expression PC1** | **+0.859** | — | — |
| **Methylation PC1** | **−0.830** | — | — |
| **Expression PCA (PC1×PC2) 2D** | — | — | **0.964** |
| **Methylation PCA (PC1×PC2) 2D** | — | — | **0.953** |

cos(u_first, u_last) on the restricted cohort = **−0.061** (closer to truly
orthogonal here, but the patterns themselves carry almost no Group3-vs-Group4
signal).

**The 2D-GSVD G3-vs-G4 classifier hits 63.2 % accuracy. The majority-G4 prior
is 69.4 %.** I.e., the GSVD-based 2D classifier underperforms a constant
"everyone is Group4" classifier. Expression-only PCA hits 96.4 % and
methylation-only PCA hits 95.3 % at the same task on the same patients.

---

## Verdicts on the central claims (open-data test, mirrors NBL Path-B)

**C1 — blind tumor-exclusive arraylet predicts survival/prognostic axis:**
**NOT REPRODUCED** on open pediatric MB data. The most-exclusive GSVD arraylet
(u_first, c/s ≈ 22) correlates with the established MB prognostic axis at
r = +0.19 (subgroup-ordered) and r = −0.19 in the Group3-vs-Group4 binary —
both far below expression PCA PC1 (r = +0.70 / +0.86 respectively) and
methylation PCA PC1 (r = +0.68 / −0.83) on the SAME matched patients.

**C2 — second orthogonal arraylet also predicts + is orthogonal:**
**PARTIALLY REPRODUCED on orthogonality, NOT REPRODUCED on prediction.**
- Orthogonality: cos(u_first, u_last) = −0.218 (full cohort) and −0.061
  (G3+G4-restricted) — closer to zero than the NBL Path-B replication
  (0.33), genuinely fairly orthogonal in the restricted analysis.
- Prediction: u_last has r = −0.187 vs subgroup and r = −0.168 vs Group3-binary.
  Both significant but ~3-4× weaker than single-layer PCA on the same data.

**C4 — combined-arraylet predictor beats standard-of-care biomarker:**
**NOT REPRODUCED.** mbl_icgc Group3-vs-rest standard-of-care: C = 0.598,
log-rank P = 0.027 (FRONT 1). GSVD u_first vs subgroup-prognostic-score on
762 patients: r = +0.193 (translation to a C-index against a real survival
outcome is bounded by this correlation, so C is well below the standard-of-care
0.598 in any reasonable mapping). PCA PC1 on expression (r = +0.70 vs
prognostic ordering, classification accuracy 96 % into subgroup) would itself
match or beat clinical Group3-binary on subgroup recovery — i.e. supervised /
classical baselines beat GSVD again.

**C3 — X-chromosome/sex artifact in ~100th pattern:** **NOT TESTED.**
Out of scope for this pediatric analog — the paper's chromosome-mapping claim
requires WGS-bin-resolved CN data, which the open MB substrate does not
provide.

**C5 — robustness across feature/bin choices:** **NUMERICALLY REPRODUCED.**
GSVD numbers (subgroup correlation, classification accuracy) are stable across
(top_rna, top_meth) ∈ {(2 000, 5 000), (5 000, 10 000)}; cos(first,last) stays
in [−0.32, −0.22]; ARI in [0.09, 0.14]. The decomposition itself is stable;
the *signal it captures* is weak, not noisy.

---

## Honest caveats

1. **Not the paper's data.** The paper used WGS 1-kb-bin CN on NBL (with
   blood-genome companion) under dbGaP. The pediatric-CN equivalent for MB
   (per-patient WGS CN) is also dbGaP-controlled. This is an honest test of
   whether the method *generalizes* on the open multiomic layers that exist,
   not a bin-exact reproduction.
2. **Cavalli per-patient OS is paywalled.** All Cavalli-cohort survival
   numbers in this report are inferred via subgroup, which is the established
   MB prognostic axis (confirmed at C ≈ 0.60-0.66 on real mbl_icgc OS). The
   GSVD-vs-PCA comparison is on subgroup recovery; survival inferences follow
   monotonically from subgroup ordering. Per-patient OS Cavalli numbers
   require Cell supplementary Table S1 access (paywalled).
3. **Two omic layers ≠ paper's tumor/blood layers.** The paper's two-layer
   GSVD pairs tumor-genome CN with blood-genome CN. NBL Path-B used
   tumor-expr × tumor-meth, this report uses the same. Genuine apples-to-apples
   with the paper's two layers requires (a) tumor CN + matched blood CN per
   pediatric MB patient and (b) per-patient OS — neither of which is open. The
   open-substrate test answers "does the method *generalize* across omic layer
   choices on pediatric CN-driven cancer" with: NO.
4. **Sample size on real-OS cohort.** mbl_icgc n=103 with OS is modest. The
   FRONT 1 numbers there (C ≈ 0.60-0.66) are consistent with the established
   literature, but exact P-values would shift with a larger open OS cohort.

---

## Bottom line: pediatric-CN-driven vs NBL-specific

The same pattern observed in NBL Path-B is reproduced on the pediatric
medulloblastoma analog: **the GSVD's most-exclusive arraylets carry a weak,
statistically significant but clinically marginal signal that is decisively
beaten by ordinary single-layer PCA on the same matched patients**. On the
sharpest pediatric-CN-driven test (Group3-vs-Group4 binary), the GSVD 2D
classifier is below the majority-class prior baseline while PCA achieves
95-96 %.

**Answer to Rick's actual question:** the prognostic claim does **NOT**
transfer to a pediatric CN-driven cohort any more than it did to NBL. It is
not "NBL-specific" — it appears to be **substrate-independent** in its
failure: across both NBL expr-meth (Path-B) and MB expr-meth (this report),
on patient-matched open multiomic layers, simple PCA on a single layer
captures the established prognostic axis 3-4× more strongly than the GSVD's
"most-exclusive" patterns, which the paper's central selection rule promotes.

The exact, unique, stable mathematics of GSVD/HO-GSVD are real strengths;
the unsupervised pattern-selection rule that the paper builds its prognostic
claim on does not yield a winning predictor on open pediatric (or NBL) data.

---

## Compute / provenance

- Host: uicgpu, work dir `/data/stevens/alter-pediatric-mb/`
- Engine: shared `gsvd_reference.py` and `survival_stats.py` from
  `~/.openclaw/workspace/REPLICATE-PROJECT/alter-multitensor-2026/code/`
  (10/10 unit tests passing, reconstruction error <1e-8)
- Survival engine: scipy fallback (lifelines not installed; flagged in
  `results/f1_baseline.json`)
- Open data sources used:
  - GEO GSE85217 (expression, 21 642 × 763) — public, no login
  - GEO GSE85212 (methylation, 321 175 × 763) — public, no login
  - cBioPortal mbl_icgc (n=125, full clinical + WGS-derived mutation counts)
    — public REST API
  - cBioPortal mbl_sickkids_2016 (n=46, secondary baseline)
- All scripts in `pediatric-mb/code/`:
  - `f1_baseline_survival.py` — FRONT 1 standard-of-care baseline
  - `f2_gsvd_mb.py` — FRONT 2 main GSVD pipeline + PCA comparator
  - `f3_gsvd_g3g4_restricted.py` — Subgroup-restricted G3+G4 GSVD
- All JSON results in `pediatric-mb/results/`:
  - `f1_baseline.json`
  - `f2_gsvd_cavalli_n5000x10000.json`
  - `f2_gsvd_cavalli_n2000x5000.json` (robustness)
  - `f2_pattern_scan.json` (all-pattern subgroup correlation scan)
  - `f3_gsvd_g3g4.json`
- Total wall time on uicgpu: ~5 min (the methylation 2 GB load dominates).

Performed 2026-06-25 under standing replication protocol.
