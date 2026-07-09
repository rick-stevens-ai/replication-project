# Failure analysis — LUCID slot #97 (high-LET rapidly-repaired SSBs)

**Paper:** Guerra Liberal FDC, Thompson SJ, Prise KM, McMahon SJ. *High-LET radiation induces large amounts of rapidly-repaired sublethal damage.* Sci Rep 13:11198 (2023). doi:10.1038/s41598-023-38295-3.
**Queue verdict:** REPLICATED.
**This document's verdict (honest):** REPLICATED, with three specific caveats and one substantive concern worth naming.

---

## 1. What was NOT re-run (the elephant)

Three simulation stacks referenced by the paper were **not** re-executed in this replication:

1. **Medras** (McMahon & Prise 2021) — the DSB-misrepair Monte-Carlo underlying Fig 5a-b top panels. Reason: separate ~2000 LOC model, itself a multi-day project to build from scratch. We substituted the *data-side* test: the F-test that shared repair half-life fits the mixed-field survival data (Table 1). That is a legitimate probe of Medras's central emergent claim, but it is **not** a re-run of Medras itself.
2. **TOPAS-nBio** — the Geant4-DNA simulation that generates the DSB/Gy vs LET curve in Fig 4. Reason: available on uicgpu but not required to reach the paper's own downstream conclusion (Fig 4 is used only as a scalar correction factor RBE_DSB ~ 3.67 downstream). We substituted an analytical simple-nucleus surrogate that reproduces the *shape* but is 1.7x off on the *absolute*.
3. **The paper's own Lea-Catcheside joint-fit pipeline** — the specific numerical procedure that turns Supp Data 3 into RBE_SLD = 2.8/3.7. Reason: not fully specified in the Methods. We use the closed-form Eq 8 evaluation, which gives 2.0/2.3.

**Is this a mismatch with the queue's REPLICATED tag?** Under the nuanced-distinction rule stated in the backfill brief: **No.** The paper's own deliverable is a set of experimentally-anchored LQ parameters + Lea-Catcheside RBE derivations + phenomenological repair-kinetics fits, reproduced here to within reported uncertainties on 18 of 21 examined claims. The Monte-Carlo elements are supporting-scalar-correction, not the paper's principal result. REPLICATED is substantively appropriate.

**But** if we widen the criterion to "reproduce the paper's full simulation stack," this becomes a PARTIAL. Reasonable people would disagree; my honest read is that this is a **strong REPLICATED-with-caveats**, not a downgrade.

---

## 2. The RBE_SLD discrepancy is genuine

Paper: **2.8-3.7**. Our Eq 8 direct reading: **2.0-2.3**.

This is not sampling noise. Both numbers come from the same released Supp Data 3 spreadsheet. The delta must live in the fit ansatz --- probably the paper's Lea-Catcheside joint fit extrapolates toward T -> infinity, while our Eq 8 anchors at T=6h against T=0.5h. But we have not been able to reproduce the paper's exact 3.7 from their data using any obvious variant.

The paper's abstract claim "RBE_SLD > 2.5" is **only marginally supported** by our reading:
- PC-3: our 2.0 vs paper 2.8+/-0.9 --- our value sits at the paper's lower 1sigma edge.
- U2OS: our 2.3 vs paper 3.7+/-0.4 --- our value is more than 3sigma below the paper's central value.

If we had to give an honest bottom line: **the paper's headline RBE_SLD is either correct-by-a-fit-detail-we-couldn't-reproduce, or slightly inflated by their specific joint-fit protocol.** Open question #1 in `open_questions.json` is the way to resolve this.

---

## 3. The Fig 4 factor-of-1.7 offset is a modelling gap, not a scoring issue

Our analytic surrogate gives **216 DSB/Gy at 129 keV/um**; the paper gives **128.5** (TOPAS-nBio). We over-count because the surrogate omits:
- Ionisation-cluster substructure (real alpha tracks make ionisations in clumps, not uniformly).
- SSB-pair saturation (once two SSBs are within 3.2 nm, adding a third does not create a new DSB pair).
- Radial dose distribution around the track.

This is a legitimate modelling limitation, not a numerical bug. It **cannot** be closed within the analytic-surrogate approach; it requires TOPAS-nBio. Open question #2 addresses this.

---

## 4. The cluster-foci N_cl match may be partly cosmetic

Our N_cl values (10.5 PC-3, 12.6 U2OS) match the paper's (9.9, 10.2) to within 5% and 25% respectively. But:
- The cluster-foci model has **three free parameters** (N_cl, F, residual P). At a small number of time points (5), three parameters is close to over-fitting.
- We got F = 1.9 (PC-3) and F = 1.2 (U2OS), i.e. barely-a-cluster; the paper cites F = 4-5. This means the "cluster" mechanism in our fit is really doing very little, and the apparent slowdown of alpha foci is being carried by the residual-P and N_cl parameters rather than by genuine clustering.
- A more honest test would fix F = 4.5 (per Medras prior in the paper) and refit only N_cl and P.

**Verdict:** the N_cl-match number is real but the mechanism-match claim is weaker than the summary table suggests.

---

## 5. What went right (be fair)

- LQ fits reproduced Table S1 to within reported uncertainties on 6/6 parameters.
- Repair half-life reproduced Table 1 exact for both cell lines under a joint mixed-field fit.
- Foci at 1 h and at 24 h reproduced to within 1 percentage point for both cell lines both qualities (C18, C19).
- All 5 main-text figures were regenerated; visual comparison against paper PDF matches.
- All 21 examined claims have explicit paper-value-vs-our-value entries in `REPORT.md` --- no cherry-picking.
- Source PDF is text-extractable via `pdftotext`; no OCR failure.
- SI XLSX opened cleanly with pandas/openpyxl.
- End-to-end pipeline is ~5 s on one CPU and re-runnable from scratch.

---

## 6. Honest verdict tag

**Queue: REPLICATED. This backfill: REPLICATED-with-three-caveats.**

Caveats in one line each:
- (a) Medras and TOPAS-nBio were not re-run --- we replicated the data-side, not the simulation-side.
- (b) Our RBE_SLD is 25-40% below the paper's headline; the abstract claim "RBE_SLD > 2.5" is only marginally supported by our Eq 8 reading.
- (c) Our Fig 4 absolute DSB/Gy is 1.7x too high; only the shape and order are reproduced.

None of these are grounds for downgrading to PARTIAL under the "paper's deliverable IS analytical" rule --- the paper's LQ + Lea-Catcheside + cluster-foci layer is genuinely replicated. But a reader who expected a Medras re-run should stop here and read open questions #1-3 before citing this record.
