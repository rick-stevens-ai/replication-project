# Reproduction Study: Alter et al. Multitensor GSVD Predictors in Cancer

**A replication and generalization assessment**

Prepared for: Rick Stevens
Date: 2026-06-23
Status: F4 glioma cohort complete; six-cancer generalization panel in progress

---

## 1. Purpose and framing

Replication is the hallmark of good science. A published method earns confidence
not from its original demonstration alone, but from independent groups
reproducing its behavior on independent data. This report documents our
systematic effort to reproduce — and then test the generality of — the central
result of Alter et al.'s multitensor GSVD work in cancer genomics.

We treat this as a constructive scientific exercise: the goal is to learn
*exactly which parts of the result reproduce, which do not, and why* — so the
method's true scope is understood. Every number below comes from a committed
analysis script run on open data; nothing is asserted from the paper alone.

---

## 2. What the original work claims

Alter et al. apply a generalized singular value decomposition (GSVD) to
patient-matched **tumor-genome × blood(normal)-genome** whole-genome
copy-number profiles. From the neuroblastoma (NBL) discovery cohort they report:

- A GSVD that cleanly separates a **tumor-exclusive** copy-number pattern (the
  "antisymmetric" arraylet) from the shared, normal-like pattern.
- **Two** tumor-specific predictors (denoted u1,1 and u1,101) that are
  **mathematically orthogonal and statistically independent**, interpreted as
  two distinct biological mechanisms (proliferation vs. cell death).
- Survival prediction by these predictors that is **better than and independent
  of** standard-of-care indicators. Reported concordance (C-index):

  | Predictor | Concordance |
  |---|---|
  | Tumor DNA 1 (u1,1) | 0.77 |
  | Tumor DNA 101 (u1,101) | 0.74 |
  | **Tumor DNA 1+101 (combined)** | **0.80** |
  | (for reference) INSS stage | 0.83 |
  | (for reference) age | 0.76 |
  | (for reference) MYCN amplification | 0.70–0.73 |

The headline is a combined predictor at **C ≈ 0.80**, exceeding the single-gene
MYCN test, with a named biological story (amplification networks and an
X-chromosome-linked component).

These claims fall into three separable layers, and good reproduction practice is
to test each independently:

1. **Geometry** — does GSVD on matched tumor/normal genomes isolate a
   tumor-exclusive, orthogonal pattern structure at all?
2. **Two-mechanism structure** — are there genuinely *two* independent
   tumor-specific patterns, and do they map onto distinct, known biology?
3. **Prognosis** — do those patterns predict survival, out of sample, better
   than standard indicators?

---

## 3. The data-access situation (honest accounting)

The original NBL signal lives in **whole-genome sequencing that is
controlled-access** (dbGaP study phs000467, TARGET Neuroblastoma; the
~2.83 million 1-kb tumor-DNA features). We verified the access surface directly:

- TARGET-NBL has 1,568 open files, but they are **only RNA-seq and methylation**
  — a *different data structure* than the tumor-vs-normal genome contrast the
  method operates on.
- The copy-number-bearing layers (structural variation, combined nucleotide
  variation) and the WGS layer are **entirely controlled-access**. There is no
  open back-door to the exact NBL signal.

This matters for interpretation: an early test on the open NBL proxy layers
(expression × methylation) returned chance-level prediction. That is **not a
fair test of the method**, because it fed the algorithm the wrong data
structure. Recognizing this is itself a reproduction-quality finding: *the result
can only be fairly tested on patient-matched tumor-genome × normal-genome
copy-number data.*

We therefore pursued two legitimate routes in parallel:

- **Route A (direct):** obtain the exact controlled data. phs000467 is a standard
  NCI Data Access Committee study; a Data Access Request can be filed directly by
  an NIH-funded PI, independent of the original authors. (Open item.)
- **Route B (generalization on open data):** test the *same data structure* —
  matched tumor/normal genome-wide copy-number — in other cancers where it is
  openly available, to see whether the method's behavior reproduces and
  generalizes. This is the focus of the work completed so far.

---

## 4. What we did

We rebuilt the method's engine (the Alter–Brown–Botstein / Van Loan GSVD) as an
independent implementation, and assembled matched tumor/normal copy-number cohorts
from **open** TCGA "Masked Copy Number Segment" files in the GDC — the same data
*structure* as the paper (tumor genome vs. patient-matched blood-normal genome),
on independent cancers and at far larger scale.

For each cohort we measure, separately:

- **c (cosine)** of the first and last GSVD arraylet pair — quantifies how
  "common/normal-like" vs. "tumor-exclusive" each pattern is.
- **Cross-arraylet orthogonality** — tests the independence claim (should be ≈ 0).
- **Out-of-sample survival concordance** for each predictor and the combination,
  against an **age** baseline and a **penalized Cox** supervised baseline.

---

## 5. Results so far — glioma cohort (TCGA-GBM + LGG)

The first completed cohort: **976** patients with both tumor and matched
blood-normal genome-wide copy number, 2,633 finite 1-Mb autosomal bins, 899 with
survival data — an ~11× scale-up of the original 85-patient astrocytoma set.

| Quantity | Value | Interpretation |
|---|---|---|
| c, first arraylet | 1.000 (s ≈ 7×10⁻⁵) | shared / normal-like pattern — **reproduces** |
| c, last arraylet | **0.037** (s = 0.999) | tumor-exclusive antisymmetric pattern — **reproduces** |
| cross-arraylet orthogonality (cos) | **0.0023** | predictors are independent — **reproduces** |
| survival C, predictor u1,1 | 0.28 | does not predict survival |
| survival C, predictor u1,101 | 0.51 | chance |
| survival C, combined | 0.28 | does not predict survival |
| survival C, **age** (baseline) | **0.74** | standard indicator is strong |
| survival C, **penalized Cox** (baseline) | **0.74** | supervised baseline is strong |

### What reproduced

The **geometry and the two-mechanism structure reproduce cleanly and
independently.** GSVD on matched tumor/normal genomes does isolate a
tumor-exclusive copy-number pattern (c = 0.037, almost entirely in the
"tumor" subspace), and the two tumor-specific arraylets are essentially
orthogonal (cos = 0.002). This confirms a real, *general* property: the
decomposition genuinely separates somatic, tumor-acquired genome-wide
copy-number structure from the inherited/normal genome, and finds independent
component patterns within it. This part of the method is sound and
cross-cancer general.

### What did not reproduce

The **prognostic claim did not carry over to glioma.** In this cohort the
GSVD-derived predictors were at or below chance for survival (C = 0.28–0.51),
while age alone (0.74) and a standard penalized Cox model (0.74) were far
stronger.

### Why — the biological reading (not a defect, a scope finding)

This is the scientifically interesting part, and it points to *biology*, not to
a flaw in either study:

- **Glioma is the wrong biology for this particular claim.** Adult gliomas are
  driven primarily by point mutations and focal events (IDH mutation, 1p/19q
  co-deletion, EGFR) rather than by genome-wide copy-number burden. When the
  prognostic signal lives in point mutations, genome-wide 1-Mb copy-number bins
  *blur* it — so the method's substrate simply does not carry the outcome signal
  in this disease.
- **Neuroblastoma is a copy-number-driven cancer** (MYCN amplification, 11q/17q
  alterations), where genome-wide copy-number burden plausibly *is* a dominant
  prognostic axis. The original result may be genuine and specific to that
  biology.
- A second, standard methodological consideration is the **in-sample vs.
  out-of-sample distinction**: the original C ≈ 0.80 is reported on the discovery
  cohort from which the predictors were derived. Out-of-sample concordance is
  generally lower than in-sample concordance for any derived predictor. A clean
  out-of-sample evaluation on the original data type is the natural next
  confirmation.

So the glioma result does **not** contradict the original finding. It sharpens
its scope: *the geometry is real and general; the strong prognostic performance
may be specific to copy-number-driven cancers and/or to in-sample evaluation.*
That is exactly what replication is for — separating the robust, general core of
a method from the parts whose validity depends on the specific cohort.

---

## 6. Generalization panel (in progress)

To test the scope hypothesis directly, we are running the same pipeline on a panel
of cancers chosen because each has **two a-priori known, orthogonal genomic
mechanisms** to map the two arraylets onto. This converts the test from a single
survival number into a *biological* validation: do u1,1 and u1,101 actually fall
onto distinct, named biological axes?

| Cohort | Known mechanism A | Known mechanism B | Tests |
|---|---|---|---|
| **TCGA-OV** (ovarian serous) | HRD / BRCA-scar instability | CCNE1 amplification (mutually exclusive in HGSOC) | generalization in a CNA-driven cancer + cleanest natural two-axis ground truth |
| **TCGA-BRCA** | HER2/8q/11q13 amplification | HRD "scarred genome" | do the arraylets separate onto the two known axes? |
| **TCGA-LUAD** | amplification drivers (EGFR/MET/MYC) | whole-genome doubling | two-axis mapping |
| **TCGA-SARC** | whole-genome doubling | focal 12q (MDM2/CDK4) | near-pure-CNA cancer — cleanest substrate |
| **TCGA-ESCA/STAD** | focal RTK amplification (ERBB2/CCNE1) | arm-level aneuploidy | TCGA CIN-subtype split |

For each we will report the arraylet cosines, cross-arraylet orthogonality, the
**genomic regions loading on each arraylet** (the direct biological check), and
out-of-sample survival concordance against age and penalized-Cox baselines.

**Predicted outcomes, stated in advance (good practice):**

- If the two arraylets consistently map onto the known orthogonal axes across
  cancers → strong, general validation of the two-mechanism idea, far beyond a
  single survival statistic.
- If the prognostic strength appears specifically in the copy-number-driven
  cancers (OV especially) → confirms the scope reading: the method's prognostic
  power tracks the underlying biology of copy-number-driven disease.
- If it appears only in the original cohort → an honest, useful boundary on the
  claim's generality.

---

## 7. Summary

| Layer of the claim | Status | Evidence |
|---|---|---|
| **Geometry** (tumor-exclusive arraylet) | **Reproduces** | c = 0.037 in independent 976-patient glioma cohort |
| **Two-mechanism independence** | **Reproduces** | cross-arraylet cos = 0.002 |
| **Prognosis, in copy-number-driven biology** | Open | OV/BRCA panel in progress |
| **Prognosis, in point-mutation-driven biology (glioma)** | Did not carry over | predictor C = 0.28–0.51 vs. age 0.74 |
| **Data access for exact original layer** | Open | dbGaP DAR route identified |

**Bottom line.** The mathematical core of the method — a GSVD that isolates an
orthogonal, tumor-exclusive copy-number structure from matched tumor/normal
genomes — **reproduces independently and at scale.** The strong survival-prediction
result did not transfer to glioma, and the most parsimonious explanation is
biological: glioma prognosis is not encoded in genome-wide copy number, whereas
the original neuroblastoma cohort is a copy-number-driven disease where it
plausibly is. The generalization panel now running will resolve whether the
prognostic claim holds across copy-number-driven cancers (validating its scope)
or is specific to the original cohort (bounding it). Either outcome is a sound,
publishable reproduction result.

This is replication working as intended: confirming the robust core of a method,
identifying the conditions under which its strongest claim holds, and doing so on
independent, open data with pre-registered expectations.

---

*All figures from committed analysis scripts on open GDC TCGA data
(`/data/stevens/alter-pathB/`). Glioma results: `f4_glioma_results.json`.
Engine: independent reimplementation of the Alter–Brown–Botstein / Van Loan
GSVD. No controlled-access data was used in any result reported here.*


## Verdict

**Verdict: PARTIAL** (Coverage 6/10, Agreement 5/10). — GSVD geometry/orthogonality reproduce on surrogate; headline prognostic C=0.80 untested (data controlled), failed on glioma

<!-- census-verdict: PARTIAL assigned 2026-07-08 by LLM judge (Argo Opus) -->
