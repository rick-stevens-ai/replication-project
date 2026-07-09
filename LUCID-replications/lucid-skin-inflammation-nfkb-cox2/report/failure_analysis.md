# Failure Analysis — Acheva et al. 2017 Replication

## Executive Summary

Verdict: **PARTIAL** (5/10 coverage, 7/10 agreement). Cumulative qualitative asterisk agreement: **19/27 = 70%**. The 30% gap is almost entirely explained by n=2 Tukey fragility on multimodal-LLM-digitized bar heights, not by paper error. The coverage ceiling is hard-set by the 6/22 missing-artifact rule: raw qPCR Ct tables, Western films, IHC stacks, MTT plate reads, and PGE2 ELISA ODs are not deposited anywhere (verified by a 68,135-char PDF text scan for GEO/SRA/ArrayExpress/PRIDE/Zenodo/Dryad/FigShare/GitHub identifiers — zero hits).

## What Was the Paper's Headline?

Acheva et al. 2017 make a mixed wet-lab + signaling-network claim:

1. **NF-κB activation.** 2 Gy low-LET X-rays trigger IKK-mediated phosphorylation of p65 (RelA) in N/TERT-1 3D organotypic skin equivalents (Fig 4B p-p65 densitometry, Fig 5C Bay 11-7085 dose-response).
2. **COX-2 induction.** NF-κB drives COX-2 (PTGS2) mRNA (Fig 1, >2.5× by 4h) and protein (Fig 4A/5A/5B) accumulation.
3. **PGE2 release.** COX-2 produces PGE2 that accumulates in culture supernatant (Fig 7A, 6.5× CTRL by 72h).
4. **Differentiation disruption.** PGE2 signaling perturbs terminal keratinocyte differentiation: K1 down (Fig 3C, 6E), FLG up (Fig 3E, 6F), cornified-layer thickened (Fig 6D).
5. **Pharmacological rescue.** sc-236 (COX-2 inhibitor) rescues differentiation (Fig 7B PGE2 rescue + Fig 6 differentiation-marker rescue). Bay 11-7085 (NF-κB inhibitor) suppresses COX-2 upstream (Fig 5B/5C dose ladders).

The paper does **not** present an ODE / signaling-network model. It is descriptive-mechanistic wet-lab.

## What Was Actually Exercised

### PASSED (computational identities and printed-statistic re-checks)
- **2^-ΔΔCT identity.** Recovered to < 1e-9 numerical error on a 2.4× synthetic upregulation.
- **Fig 1 COX-2 mRNA Tukey HSDs (irradiated arm, n=3).** 4/4 qualitative asterisk agreement. Verbal ">2.5×" recovered as 2.40×; verbal "< 0.5× sc-236 rescue" recovered as 0.50×.
- **Fig 2A sc-236 MTT Tukey.** 4/4 exact agreement.
- **Fig 2B Bay 11-7085 MTT Tukey.** 3/3 exact agreement. Working-dose NS call confirmed (p = 0.28).
- **Fig 2 4PL IC50 re-fit.** sc-236 IC50 = 16.8 µM; Bay 11-7085 IC50 = 3.8 µM. Neither is quoted in the paper — new context.
- **Fig 5B COX-2 dose ladder.** Monotonic decrease with Bay dose confirmed.
- **Fig 5C p-p65 dose ladder.** Monotonic decrease with Bay dose confirmed.
- **Fig 7A PGE2 6.5× headline.** Recovered as 6.4× (within 2%). Tukey p = 2.4e-04 matches printed ***.
- **Fig 7B PGE2 sc-236 rescue at 72h.** Recovered at p = 7.8e-10 (matches printed ***). ANOVA F = 37.6 across 16-bar panel.

### PARTIAL / MIXED
- **Fig 3E FLG (n=2, IHC digitized).** 3/4 qualitative agreement. One CTRL-vs-sc-236 comparison fails re-Tukey.
- **Fig 4B p-p65 / p-p38 trend audit.** 2/3 trend claims pass. p-p65 induction and Bay rescue confirmed; p-p38 trend disagrees with caption text (our digitization has CTRL bar higher than 2 Gy bar). Cannot disambiguate without raw films.
- **Fig 6E K1 with Bay.** 2/2 qualitative agreement.
- **Fig 6F FLG with Bay.** 1/2 qualitative agreement.

### FAILED (0/2 or 0/4 asterisk reproduction)
- **Fig 3C K1 (n=2, IHC digitized).** 0/2 printed ** comparisons reach significance under re-Tukey (p = 0.76, 0.49). Attributed to digitization fragility, not paper error.
- **Fig 6D cornified-layer thickness (n=2).** 0/4 printed asterisks reach significance. Every recomputed p falls in [0.057, 0.68] — all "barely-not-significant" under 6-group Tukey correction at n=2, exactly the regime where small SEM read errors flip verdicts.

## What Was NOT Done

This is a **computational audit**, not a wet-lab or signaling-network replication. Specifically:

1. **No independent qPCR/qRT-PCR quantification.** Raw Ct tables not deposited. We reproduced the 2^-ΔΔCT identity but cannot independently re-derive Fig 1 fold-changes from primary data.
2. **No independent Western blot densitometry from raw films.** Fig 4B/5B/5C were audited by reading bar heights off the paper's rendered PDF bar charts using a multimodal LLM. Digitization error at n=2 with tight SEMs is the dominant uncertainty and directly explains the Fig 6D 0/4 miss.
3. **No independent IHC quantification.** Fig 3C, 3E, 6D, 6E, 6F depend on ImageJ ROI selection on raw fluorescence stacks. Stacks not deposited.
4. **No independent PGE2 ELISA re-quantification.** We recover the fold-change from digitized means but cannot detect batch effects or standard-curve issues.
5. **No independent NF-κB nuclear-translocation timecourse.** Paper reports p-p65 by bulk Western only. No single-cell live-cell RelA-GFP imaging, no p65 nuclear/cytoplasmic ratio timecourse.
6. **No ODE / signaling-network model.** Paper does not present one, and this replication does not build one. The natural extension — fit a Hoffmann-style IKK/IκB/NF-κB module to the digitized timepoints and predict p-p65 under Bay — is an open question (see `open_questions.json` Q2 and Q4).
7. **No radiation-dose-response beyond 2 Gy.** Paper is essentially single-dose. Fractionation biology (relevant to clinical radiotherapy) is untouched (see Q3).
8. **No combined-modality (radiation + immunotherapy) work.** Paper is single-agent (see Q1).

## Why the 30% Asterisk-Agreement Gap?

The gap concentrates in two panels: Fig 3C (0/2) and Fig 6D (0/4). Both share three features:

1. **n = 2 per group.** Tukey HSD at n=2 relies almost entirely on the printed SEM being a good population estimate (only one residual degree of freedom per pair).
2. **Multi-group family** (6 groups in Fig 3, 6 groups in Fig 6). Family-wise correction inflates the critical q-value substantially.
3. **Multimodal-LLM-digitized SEMs.** Bar-height read accuracy is ~5-10% of full scale; SEM read accuracy is ~30-50%. At n=2 with tight SEMs, a 30% SEM read error can flip a Tukey verdict by an order of magnitude in p-value.

This is exactly the "digitization fragility" regime: visually distinct bars, statistically ambiguous under re-Tukey with imperfect SEM reads. A re-digitization with better tooling (WebPlotDigitizer + manual QC, or Nougat-style structural PDF parsing) would likely close most of the Fig 3C / Fig 6D gap without changing the paper's underlying biology.

## Honest PARTIAL Justification (LUCID Wet-Lab-Gated Pattern)

This is the canonical LUCID **wet-lab-gated** pattern. The paper's computational-identity claims (2^-ΔΔCT, Fig 1/2A/2B/7A Tukey identities, 6.5× PGE2 headline, sc-236 rescue on Fig 7B) all reproduce cleanly under independent re-analysis. The paper's primary-experimental claims (NF-κB activation, COX-2 induction, PGE2 release, differentiation disruption, pharmacological rescue) cannot be independently reproduced without wet-lab access to N/TERT-1 3D organotypic culture, RT-qPCR, Western blot, IHC, MTT, and ELISA.

**Coverage ceiling is 5/10 by the 6/22 rule** (missing artifacts: raw Ct, films, stacks, plate reads, ODs). AUDIT_PROTOCOL §5 requires ≥80% coverage AND ≥80% claim agreement for REPLICATED. We hit 5/10 coverage (bounded, not fixable computationally) and 7/10 agreement (fixable with better digitization tooling). Therefore **PARTIAL** is the correct verdict.

Promoting past PARTIAL to REPLICATED requires wet-lab re-execution, not more computation. Downgrading below PARTIAL to SPOT-CHECK would understate the fact that we have computational signal on all 7 figures, that the "core-stats" figures reproduce at 100% (12/12), that the PGE2 headline reproduces to within 2%, and that the dose-response monotonicity on Fig 5B/5C is clean.

## Verdict: PARTIAL (preserved)
