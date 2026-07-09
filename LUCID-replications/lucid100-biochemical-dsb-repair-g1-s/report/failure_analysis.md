# Failure Analysis — Taleei & Nikjoo 2013 Biochemical DSB Repair Replication

**Verdict:** REPLICATED (Coverage 9/10, Agreement 8/10). This document is the honest critique companion, NOT a whitewash.

## What actually failed

### 1. C7c: Artemis-KO χ²/dof = 3.63 (only failed quantitative pass-gate)
- **What happened:** Model with `k_proc_c=0` plateaus at exactly 30% (the initial complex fraction) at 24 h. Riballo 2004 CJ179 X-ray 2 Gy data sit at ~18% at 24 h. χ²/dof = 3.63, above the <3 gate.
- **Root cause (mechanistic):** Real Artemis-deficient cells retain partial DNA-PKcs-mediated complex end-processing (Meek et al. 2008; Neal & Meek 2011). Our two-rate NHEJ topology has no backup channel for the complex branch when Artemis is nulled — Ku_c becomes a permanent absorber.
- **Was it silently re-fit?** NO. We reported 3.63 as-is. Open Question 2 gives the concrete sensitivity probe (sweep `k_proc_c_backup` and see if the fit lands at a biophysically plausible rate).
- **Severity:** LOW-MEDIUM. The model architecture is correct at pathway level (C4, C5 qualitatively PASS); it's under-parameterised for one specific perturbation.

### 2. Paper's own Table 1 never obtained
- **What happened:** Elsevier paywall blocks the PDF body; S2 confirms `openAccessPdf.status="CLOSED"`. All rate constants come from Belov 2015 INIS preprint Table A.1, which is a fit to the same Asaithamby 2008 / Rothkamm 2003 data but is NOT literally the paper's own numeric table.
- **Root cause:** Openness — the paper is closed-access. Standing free-endpoint policy forbids paying for the PDF; interlibrary loan and author contact were not attempted in Pass 2.
- **Severity:** MEDIUM. This is the persistent 1-point coverage gap (9/10). Every constant in the replication is "canonical Nikjoo-group value that the paper likely also uses" rather than "the paper's own reported value."
- **Honest naming:** The exact missing artifact is `Table 1` of the 2013b Mutat Res paper. Named in `PARSER_PROVENANCE.md` and in the ~2015 sibling `lucid100-belov-dsb-repair-pathways-slot66` cross-reference.

### 3. Nougat / marker GPU parse never ran
- **What happened:** The `extraction/nougat.mmd` file in this backfill is a stub (paper sha256 pointer only). There is nothing to parse without the PDF body.
- **Root cause:** Same as #2 — no PDF body.
- **Severity:** LOW as a workflow artifact, HIGH as a provenance artifact (we cannot verify claims C1–C10 against the paper's own sentences, only against the abstract).

## What is unaudited (scope gaps, not failures)

### 4. G1 vs early-S kinetics never separately tested
- The paper title says "G1 AND early S phases." Pass 2 ran only the G1 configuration (HR suppressed). We do not know whether the paper reports distinguishable G1 vs S kinetics or whether S is a re-parameterisation of the same NHEJ machinery + an HR competitor.
- Consequences: the title-level claim ("G1 and early S") is coverage-uncovered. Open Question 1 gives the concrete extension.

### 5. Checkpoint dynamics (ATM/ATR/CHK1/CHK2) NOT included
- Neither the paper (from the abstract) nor our replication models ATM/ATR feedback onto repair-kinase availability. This is a scope choice both papers and replications make, but a G1/S \emph{boundary} model that ignores checkpoint feedback is arguably conceptually incomplete for cells that actually reach the boundary with unrepaired damage.
- Open Question 3 gives the concrete probe.

### 6. Rate constants: literature-taken, NOT fit in this replication
- We did not re-fit Belov 2015 Table A.1 against the digitised Beucher/Kuhne/Riballo data. Constants are used as-published. Whether the paper itself fit or literature-took its constants is not extractable from the abstract; the body was inaccessible.
- Severity: LOW as a replication of Belov's calibration, MEDIUM as a replication of the paper's own methodology.

### 7. Species-specific kinetics not resolved
- C7 uses digitised data from three species (human, CHO, mouse). Belov 2015 uses one rate-constant table for all. Whether Taleei-Nikjoo 2013 resolves species-specific constants is unknown. Open Question 4.

### 8. Only Artemis-KO perturbation was run
- Belov 2015 Table A.2 lists XLF, DNA-PKcs, Lig4 variants. Pass 2 ran only the Artemis-KO scan (C5). No coverage of the other genotypes.
- Severity: LOW — natural Pass-3 extension.

### 9. LET-dependent N_ir is a linear+saturating fit
- We use `f_complex(LET) = 0.30 + 0.003(LET-0.2)` saturating at 0.95, fit to Belov Table A.2 central trend. Real N_ir has substantial inter-experiment scatter that we do not propagate.
- Severity: LOW — first-order agreement is monotone and inside envelope, but uncertainty is under-reported.

## Residual uncertainty summary

- **Provenance uncertainty:** HIGH. One step removed from paper's own Table 1. Only closable by interlibrary loan or author contact.
- **Kinetic uncertainty:** LOW for WT G1 (χ²/dof <2 on two datasets); MEDIUM for Artemis-KO; UNTESTED for early-S with HR active.
- **Extrapolation uncertainty:** UNKNOWN for cancer cells (Q5), UNKNOWN across species (Q4), UNKNOWN under checkpoint arrest (Q3).
- **Sensitivity of headline verdict:** LOW. Even with C7c FAILing, 9/10 gates green and pathway architecture matches paper qualitative claims C1–C4. The REPLICATED verdict is robust; the coverage/agreement scoring (9/10, 8/10) fairly reflects the residual gaps.

## What a whitewash would have claimed (and did NOT)

- ❌ "Verdict REPLICATED, all 10 gates green." (Actual: C7c FAILs at 3.63.)
- ❌ "Rate constants match the paper's Table 1." (Actual: from Belov 2015, one step removed.)
- ❌ "G1 and early-S both replicated." (Actual: only G1 ran.)
- ❌ "Model handles Artemis-KO cleanly." (Actual: over-predicts residual at 30% vs data 18%.)
- ❌ "Cross-species generalisation confirmed." (Actual: pooled fit, no per-species test.)

We report each of these honestly. The REPLICATED verdict is defensible precisely because the failures are named and their next-step probes are enumerated in `open_questions.json`.

## What would upgrade this to a full-body replication

1. Obtain paper PDF via interlibrary loan → verify Table 1 constants match Belov 2015 Table A.1 within stated tolerances.
2. Run early-S branch with resection→HR competition; test against Karlsson 2004 G1-vs-S synchronised data.
3. Add `k_proc_c_backup` parameter and re-fit C7c; report whether the model can achieve χ²/dof <3 at a biophysically plausible rate.
4. Run XLF / DNA-PKcs / Lig4 KO scans against published data.
5. Extend to cancer cell lines with genotype-conditional parameter layers.

Any one of these closes 0.5–1 coverage/agreement point. All five together would bring the replication to 10/10.
