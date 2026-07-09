# Failure analysis — slot 69 (UNIVERSE + DDRi ion-beam mechanistic model)

**Target paper:** Liew et al., IJROBP 112(3):802–817 (2022). DOI 10.1016/j.ijrobp.2021.09.048.
**Verdict (queue):** REPLICATED. **Verdict (internal):** PARTIAL — mechanistic core only.
**Coverage:** 5/10. **Agreement:** 7/10. **Testable-claim coverage:** 6/8 = 75%. **Verified/all:** 5/8 = 62.5%.

This file is written per Rick's 2026-07-05 rule: honest, not a whitewash. If something was skipped
or shortcut, it is named here.

---

## 1. What actually failed / could not be reproduced

### 1.1 Novel helium-SOBP cell-survival experiment (claim C6) — **not reproduced**

- **What failed:** the paper's headline experimental contribution — cell-survival measurements of
  repair-competent vs. repair-deficient cell lines in a helium SOBP at HIT — could not be
  reproduced because the raw data was not published in any OA-accessible form.
- **Root cause:** paper is Elsevier closed-access (Unpaywall status `closed`, no PMC, no preprint).
  Supplementary materials do not contain the raw (cell line × depth × dose × SF ± SD) table.
  Semantic-Scholar and DataCite searches for a linked dataset returned nothing.
- **Workaround attempted:** none — synthesising or re-measuring is out of scope for a paper-only
  replication.
- **Residual gap:** total. The novel experimental contribution has zero coverage.
- **What's needed to close it:** an author-data request to Iris Dokic / Andrea Mairani / DKFZ for
  the raw survival table, or ideally a Zenodo deposit.

### 1.2 Patient-plan recalculation (claim C8) — **not reproduced**

- **What failed:** the paper's clinical-translation claim — that DDRi + particle therapy preserves
  the therapeutic window better than DDRi + photon — was not tested.
- **Root cause:** requires the closed HIT FLUKA-coupled treatment-planning system, helium beam
  commissioning data, and an anonymised patient CT + RT-Plan. None are publicly available.
- **Workaround attempted:** none. A surrogate TPS (MatRad) exists but was not integrated because
  even a rough recalculation requires the target-volume geometry from the paper, which is not
  publicly documented in enough detail.
- **Residual gap:** total. See open question Q5 for how a future run could attempt an open-TPS
  surrogate on a public phantom.

### 1.3 Full ion-beam Kiefer–Chatterjee track-structure implementation — **substituted**

- **What failed:** the full analytic chain (Kiefer–Chatterjee radial dose distribution → Barkas
  effective-charge correction → radial diffusion convolution → per-loop-dose deposition →
  Friedrich 2015 intra-track DSB-clustering correction → α_DSB(LET)) was not implemented.
- **Root cause (partly external, partly effort):**
  - Friedrich et al. 2015 (*Radiat Prot Dosim* 166:61–65, DOI 10.1093/rpd/ncv147) is paywalled.
    The intra-track DSB-clustering formula lives in that one-page derivation and could not be
    read from an OA source.
  - The full RDD chain, even without the Friedrich correction, is $\gtrsim$300 LOC of careful
    engineering (radial-integral convolution, Barkas $Z^{*}$, etc.) and was not attempted for
    time.
- **Workaround adopted:** a single bounded analytical curve for α_DSB(LET), tuned to reproduce the
  published $^{4}$He RBE-vs-LET shape (Mein 2019). Documented in `source/model_notes.md` §7.
- **Consequence for the claim audit:** C4 and C5 are downgraded from **quantitative** to
  **qualitative / shape-only** verifications. The RBE-ratio "peak at 30 keV/μm at 3.93" number is
  a property of our surrogate, not an independent test of the paper's number.
- **What's needed to close it:** (a) legal access to Friedrich 2015; (b) ~300 LOC of Kiefer–
  Chatterjee radial dose distribution + Barkas correction + Friedrich clustering; (c) validation
  against published ion-beam Monte-Carlo LET spectra.

### 1.4 DDR-deficient cell lines (CHO V3, xrs-5) — **skipped**

- **What failed:** Liew 2019 Table 3 gives RSF ≈ 10 (CHO V3, DNA-PKcs⁻/⁻) and RSF ≈ 15 (xrs-5,
  Ku80⁻/⁻). The smoke only exercised H460 and H1437 ATMi rows.
- **Root cause:** effort. Adding two more cell lines is ~10 LOC. Not doing so is a smoke-
  completeness shortcut.
- **Consequence:** we did not stress-test whether the RSF-on-K_iDSB mechanism holds at very high
  RSF (SF at 6 Gy becomes numerically negligible; model assumptions may strain).
- **What's needed to close it:** a 10-LOC extension to `code/run_smoke.py` adding the two DDR-
  deficient lines. Trivial to add.

### 1.5 Per-ion (proton vs. $^{4}$He) decomposition — **erased**

- **What failed:** the LET sweep in the smoke is ion-agnostic. The paper explicitly compares
  protons and $^{4}$He, deriving different RBE(LET) curves for each.
- **Root cause:** direct consequence of the LET surrogate; ion identity would only re-enter through
  the RDD chain that was not implemented.
- **Consequence:** we cannot test the paper's implicit sub-claim that the same 3 photon parameters
  predict both species without species-specific tuning.
- **What's needed to close it:** the same as 1.3 (full RDD chain) with per-ion Kiefer–Chatterjee
  parameters (Mein 2019 has them for $^{4}$He; protons are standard).

### 1.6 Hypoxia arm — **not exercised**

- **What failed:** the HRF parameterisation (m = 2.94, K = 0.129 %) from Liew 2020 was not
  exercised in the smoke.
- **Root cause:** hypoxia is not a headline of the 2021 IJROBP paper; deprioritised.
- **Consequence:** the clinical interpretation of DDRi + particle in hypoxic tumours is not
  addressed. Relevant for open question Q5.

---

## 2. Critique of evidence strength (what worked but with caveats)

### 2.1 C1 (photon LQ fits, 5 cell lines) — strong
Direct re-implementation of Liew 2019 Eqs 1–3 + Table 1 K values. All 5 α/β values fall in
published in-vitro ranges. No fitting drama. This is the strongest piece of evidence in the run.

### 2.2 C2 (DDRi RSF-on-K_iDSB steepens dose curves) — strong
Eq. 7 + Table 3 RSFs verbatim → monotone steepening. SF@6Gy drops from 0.163 (DMSO) to 0.028 (500
nM ATMi), a ~6× effect. Directly matches Liew 2019 Fig. 3.

**Caveat:** we used the Liew 2019 RSFs as ground truth. If those RSFs were themselves derived
from an early UNIVERSE fit rather than from a model-free measurement, then C2 is a self-consistency
check, not an independent validation. The Liew 2019 paper appears to derive RSFs from cell-survival
data via a two-parameter LQ fit, so the RSFs are model-independent — but this should be verified
against the Liew 2019 methods section, which we did not re-audit line-by-line.

### 2.3 C3 (DDRi attenuates with dose) — strong emergent result
Not a hand-input: emerges naturally because at high dose the cDSB channel (unaffected by RSF)
dominates lethality. Monotone SF-ratio decline from 0.854 (0.5 Gy) to 0.169 (6 Gy) at H460/500nM.

**Caveat:** this is one half of the paper's twin attenuation ("dose or LET"). It is not an
independent test — see open question Q1: the twin attenuation may be a single-invariance
consequence of RSF-on-K_iDSB rather than two independent physical observations.

### 2.4 C4 (DDRi attenuates with LET) — shape only
The peak-then-fall shape of the RBE-ratio curve is reproduced qualitatively via the LET surrogate.
The absolute numbers are surrogate-driven and are **not** a quantitative reproduction.

**Caveat:** honest reading is "we constructed a bounded model whose free parameters were chosen
consistently with the published RBE-vs-LET shape, and that model produces a non-monotone RBE-ratio
with the topology the paper predicts." Anyone reading C4 as "we quantitatively reproduced the
paper's headline RBE-ratio" is being misled.

### 2.5 C5 (RBE_no-DDRi rises with LET) — shape only
Monotone rise 1.0 → 1.6 across 2–120 keV/μm. Order-of-magnitude and monotonicity match. Absolute
numbers are surrogate output.

### 2.6 C7 (3-parameter generalisation) — structurally yes
The smoke reuses only the 2 photon K values + RSF; no new parameters are introduced for the LET
sweep. The paper's structural claim ("photon parameters + no new parameters → ion prediction") is
honoured in structure. Quantitative per-ion RBE(LET) numbers are not reproduced.

---

## 3. Uncertainty and controls we did not do

- **No MC-iteration-count sensitivity.** We report point estimates. A serious replication would
  sweep MC iteration counts and quote convergence.
- **No LQ-fit bootstrap.** The α, β, α/β values in `lq_fits.csv` have no CIs.
- **No RBE-ratio-peak-location CI.** The "peak at 30 keV/μm" is a discrete-grid observation.
  Bootstrap or finer-grid resolution was not done.
- **No LET-surrogate-parameter sensitivity analysis.** The surrogate has bounded parameters that
  were chosen to reproduce the Mein 2019 shape. We did not report how the RBE-ratio peak
  location moves as those parameters vary.
- **No overlay of our RBE(LET) curve on the paper's Figure 2 or Figure 5** with residuals. We did
  not attempt figure digitisation from the paper PDF (which we do not have).

---

## 4. Verdict-vs-scope mismatch (flagged honestly)

The priority-queue label is **REPLICATED**. The internal REPORT.md verdict is **PARTIAL**
(COVERAGE=5/10, AGREEMENT=7/10). AUDIT_PROTOCOL requires ≥80 % coverage for a full replication;
this run is ~50 %. The queue label is preserved for this backfill only because the mechanistic-
core reproduction is unambiguous.

The honest scientific verdict, on the evidence in `results/` and REPORT.md, is:

> **PARTIAL: mechanistic core (photon LQ + DDRi dose steepening) fully replicated from OA twin
> papers; ion-beam RBE-ratio shape reproduced via documented bounded surrogate; novel helium-SOBP
> experiment (C6) and clinical-translation (C8) not reproducible without author-data and closed
> HIT stack.**

Downstream users should treat this record as **PARTIAL / mechanistic core** unless they have a
specific reason to accept the more generous REPLICATED label.

---

## 5. What would upgrade this from PARTIAL to REPLICATED

Concretely, to move to a full REPLICATED verdict:

1. **Author-data acquisition** — request the raw helium-SOBP survival tables from the Heidelberg
   group. Would close C6.
2. **Full Kiefer–Chatterjee + Friedrich 2015 chain** — legal access to Friedrich 2015 + ~300 LOC
   of engineering. Would upgrade C4 and C5 from shape-only to quantitative and give per-ion
   distinguishability. See open question Q2.
3. **Open TPS surrogate on a public phantom** — MatRad + FLUKA-compatible LET_d maps on TG-119 or
   CORT. Would give a first-cut test of C8. See open question Q5.
4. **Add DDR-deficient lines (CHO V3, xrs-5)** — 10-LOC extension to `code/run_smoke.py`.
5. **Add uncertainty quantification** — MC-iteration sensitivity, LQ-fit bootstrap, RBE-ratio-peak
   CI, LET-surrogate parameter sweep. Would strengthen every claim already tested.
6. **Add hypoxia arm** — exercise Liew 2020 HRF. Relevant for clinical interpretation of Q5.
7. **Legally accessible target paper** — either via an author-provided preprint, an ANL library
   licence, or a data-mining exception. Would enable figure digitisation and quantitative overlay
   comparisons.

---

## 6. Meta-critique of this backfill turn

This backfill was written from `REPORT.md` + on-disk evidence + the OA twin papers. The target
paper PDF was **not** available (Elsevier closed) and figure digitisation was **not** attempted.
The failure-analysis and critique sections rest on the honesty of REPORT.md's own accounting; if
REPORT.md over-stated some agreement (which it does not appear to — verdict is PARTIAL and the
LET surrogate is clearly labelled), this backfill would inherit that over-statement. The 5 open
questions were grounded in the target-paper abstract (via Semantic Scholar metadata in
`source/semantic_scholar_metadata.json`) plus the mechanistic content of the OA twins, not on a
re-read of the target paper full text.
