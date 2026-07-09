# Failure analysis --- honest critique

**Slot:** `lucid100-cho-low-dose-rate-dna-repair-deficient`
**Paper:** Buglewicz et al., *BBRC* 698: 149539 (2024), DOI 10.1016/j.bbrc.2024.149539.

This file exists to be blunt about what did NOT work in this replication attempt. It is a
critique of our own work, not a defense of it.

## Verdict cross-check finding (per Rick's 2026-07-06 rule)

**The queue label ``REPLICATED'' is INCORRECT for this slot.** On-disk REPORT.md verdict is
**NO-GO** (re-tiered 2026-06-25 from an initial SPOT-CHECK). Under Rick's ``real verdict
wins'' rule I preserved the on-disk NO-GO and did not upgrade any part of this backfill's
narrative to match the queue label.

Root cause of the mismatch is most likely stale-queue: the queue was populated before the
2026-06-25 SPOT-CHECK $\to$ NO-GO re-tier and never refreshed. Recommend an upstream sweep to
re-import verdicts from on-disk REPORT.md headers.

This slot has NEVER met a REPLICATED bar. Any downstream table, aggregation, or metric that
counts this slot as REPLICATED is wrong.

## What actually did not work

### 1. Primary paper acquisition failed

- Elsevier BBRC paper is closed-access. Zero OA locations in Unpaywall, Semantic Scholar,
  EuropePMC, OpenAccessButton, PMC, arXiv, bioRxiv, medRxiv, or CSU's Mountain Scholar
  (Buglewicz dissertation). Re-verified 2026-06-22 and 2026-07-06.
- No sci-hub, no author preprint on lab website, no ResearchGate deposit.
- Consequence: every quantitative claim from the paper is unverifiable. We do not know the
  actual dose rates, the actual clonogenic SF values, the actual $\gamma$-H2AX foci counts,
  the actual cell-cycle gate fractions, or which specific CHO mutants were in the panel
  beyond the ones implied by the companion papers.

### 2. Author data deposit does not exist

- Checked GEO, SRA, ArrayExpress, Zenodo, Figshare, OSF, Dryad, Mendeley Data.
- No matching accession. This is common for wet-lab clonogenic + microscopy studies in BBRC
  (short-format journal, no data-sharing mandate before 2024) but it means there is no
  fallback path around the paywall.

### 3. Orchestrator staging silently no-oped

- The LUCID-100 pipeline was supposed to stage each paper as `.pdf` + `.md` (Marker parse) +
  `.txt` for all slots. For this slot, no such files were produced --- presumably because the
  publisher fetch failed and the pipeline did not emit a diagnostic. This is a pipeline
  reliability gap that should be flagged in the LUCID-100 post-mortem.

### 4. Smoke model is a plausibility exercise, not a reproduction

- The LQ + Lea--Catcheside + phenomenological NHEJ IDRE model **can reproduce the qualitative
  ordering and the direction of every attempted claim**, but that is not the same as
  reproducing the paper. We chose the model parameters $(\alpha, \beta, \tau, \phi, \dot D_0)$
  to make the ordering match the OA companion paper's SER table; we did NOT calibrate to the
  target paper's reported values (because they are paywalled). The smoke model would give the
  same PASS if the paper had reported half the effect size, or twice, or a different
  dose-rate location for the IDRE inflection point.
- The IDRE term $\alpha_{\rm eff}(\dot D) = \alpha(1 + \phi e^{-\dot D/\dot D_0})$ is a
  behavior-fitting choice. Multiple distinct mechanisms (cell-cycle redistribution,
  mitotic-catastrophe accumulation, alt-EJ mis-processing of complex DSBs, replication-fork
  collision with unrepaired DSBs at LDR) can all generate IDRE. The smoke does not
  discriminate among them.

## Specific gaps flagged by hard-requirement checklist

Rick's 2026-07-05 hard requirements flagged the following specific critique points; addressing
each honestly:

### (a) Were ALL mutant lines tested, or only a subset?

**Only a subset --- 3 of a likely 8--12.** The smoke covers WT + one HR-deficient + one
NHEJ-deficient representative. It does not model:

- Additional NHEJ-deficient lines: xrs-5 (Ku80$^-$), xrs-6 (Ku80$^-$), XR-1 (XRCC4$^-$).
- Additional HR-deficient lines: irs1SF (XRCC3$^-$), irs-2, irs-3 (XRCC2$^-$).
- NER-deficient lines: UV5 (XPD$^-$), UV41 (ERCC4/XPF$^-$), UV61 (ERCC6/CSB$^-$).
- Base-excision / SSB / PARP-axis: EM9 (XRCC1$^-$), EM-C11 (XRCC1$^-$).
- Fanconi anaemia lines that Kato lab occasionally includes.

Whether the paper actually included all of these or a smaller focused panel is unknown ---
BBRC-length papers typically limit to 3--6 lines, so the smoke's 3-line scope may be closer to
the paper's actual scope than the ``$\leq30\%$'' figure in REPORT.md suggests. But without the
Methods section we cannot know.

### (b) Was the dose-rate range covered both the instantaneous limit and truly protracted (>24 h)?

**Neither can be verified from public data.** The smoke sweeps $\dot D$ continuously from
$\approx0.01$ to $\approx10$\,Gy/h --- a 3-decade window --- but this window is arbitrary and
not anchored to the paper. In particular:

- The **instantaneous / acute limit** (single-fraction $\dot D \gtrsim 1$\,Gy/s) is where the
  paper's ``acute'' arm sits, but the actual $\dot D$ value is paywalled.
- The **truly protracted regime** (say $\dot D < 0.05$\,Gy/h with exposure duration $>24$\,h,
  i.e. multiple cell-cycle lengths) is where cell-cycle redistribution during exposure
  dominates the biology and where the LQ + Lea--Catcheside formalism is known to
  under-represent survival. Whether the paper covers this regime is **unknown from the
  abstract**; BBRC-scale experiments typically span 1--2 orders of magnitude of $\dot D$, so
  the truly-protracted end is likely NOT covered by the paper. This is Open Question \#1.

### (c) Was the reduced dose-rate effect in repair-deficient cells quantitatively fit or just qualitatively noted?

**In this replication: only qualitatively noted.** The smoke reports the direction (LDR/acute
SF ratio $\ll 1$ for NHEJ$^-$, $>1.2$ for WT and HR$^-$) but does not fit a curve to any
target data. There is no residual, no confidence interval, no comparison to a specific
reported ratio in the paper.

Whether the paper itself fit a quantitative model is unknown from the abstract. BBRC-length
papers usually report LQ $\alpha/\beta$ tables and possibly a Lea--Catcheside G-value plot,
but a mechanistic fit of IDRE (e.g. a two-compartment model with fast + slow repair, or an
explicit cell-cycle redistribution model) is beyond typical BBRC scope. This is Open Question
\#1 as well.

## Residual uncertainty

Even if the paper became OA tomorrow, several residual uncertainties would remain:

- Absolute clonogenic SF values in these old CHO lines drift over cell-line passages and
  between labs by up to a factor of $\approx2$; anchoring to the paper's own numbers is a
  weak absolute standard.
- The IDRE finding in NHEJ$^-$ CHO has been reported by other groups (Nagasawa, Mitchell,
  Bedford, Marples/Joiner) at various dose-rate windows; the Buglewicz claim's novelty
  relative to that prior literature is not assessable from the abstract alone.
- $\gamma$-H2AX foci-per-cell counts depend heavily on microscope + segmentation pipeline;
  even source-data spreadsheets would not eliminate a $\pm20$--$50\%$ inter-lab spread.

## What would move this slot up a tier

Concrete evidence-quality thresholds:

- **NO-GO $\to$ SPOT-CHECK$^*$** (partial re-instatement without hard-ceiling rule): obtain
  the BBRC PDF. Even without source data, the actual $\dot D$ grid + reported ordering would
  let us re-anchor the smoke model to real numbers.
- **SPOT-CHECK $\to$ PARTIAL:** BBRC PDF + at least one figure's source data (e.g. the
  headline clonogenic SF-vs-$\dot D$ curves) allowing numerical tolerance checks.
- **PARTIAL $\to$ REPLICATED:** full source data for $\geq2$ endpoints + $\geq$3 cell lines +
  independent recomputation of the LQ fits with residuals matching the paper's within
  $\pm10\%$.

None of these are achievable from public artifacts as of 2026-07-06.

## What would NOT move this slot up

Adding more analytical smoke models, ensemble-averaging different IDRE parameterizations,
running the existing smoke at higher grid resolution, or generating more figures: none of
these produce new evidence about the paper. They would only inflate the artifact count without
changing the verdict. This backfill deliberately does not do any of them.
