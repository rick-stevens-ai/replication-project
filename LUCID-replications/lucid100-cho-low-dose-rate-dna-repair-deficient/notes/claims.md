# Extracted claims — Buglewicz et al. 2024 BBRC 149539

Abstract-derived (cannot inspect figures/tables; paywalled).

| # | Claim (paraphrased from abstract) | Type | Reproducible from public artifacts? | Status |
|---|-----------------------------------|------|--------------------------------------|--------|
| C1 | NHEJ-deficient and HR-deficient CHO mutants show greater radiosensitivity than WT under acute γ irradiation. | qualitative ordering | YES, via OA companion D10/SER + LQ smoke | **SMOKE PASS** |
| C2 | WT and HR-deficient cells show classical dose-rate sparing (LDR less lethal than acute at matched total dose). | qualitative trend | YES, via Lea-Catcheside G(λ) smoke | **SMOKE PASS** |
| C3 | NHEJ-deficient mutants exhibit an **inverse dose-rate effect** (IDRE) — LDR more lethal than acute at some Ḋ/D combinations. | qualitative trend | YES, via NHEJ-specific alpha-boost smoke term | **SMOKE PASS (mechanism)** — actual Ḋ window, magnitude, and which lines display IDRE require the BBRC PDF |
| C4 | LDR exposure induces cell-cycle alterations and giant-cell formation in repair-deficient lines. | wet-lab assay | NO — flow / microscopy data not deposited | **BLOCKED** |
| C5 | γ-H2AX foci accumulate during LDR exposure (DSB induction outpaces repair at steady state). | wet-lab assay | NO — foci-count tables / images not deposited | **BLOCKED** |
| C6 | Growth-inhibition / population-doubling assay shows pathway-specific LDR sensitivity. | wet-lab assay | NO — growth-curve tables not deposited | **BLOCKED** |
| C7 | HR mutants align with responses to "major DNA damaging agents" (cross-sensitivity). | qualitative meta-claim | NO — cross-agent comparison data not provided in abstract | **BLOCKED** |
| C8 | Specific dose-rate values + cell-line panel composition (which Fanconi / PARP lines used; what Ḋ range). | factual detail | NO — paper text needed | **BLOCKED** |

## What we'd need to lift claims to quantitative reproduction

1. **The BBRC PDF** (paywalled) — gives the exact cell-line panel, dose-rate values (Gy/h or cGy/min), total doses, and LQ-fit α/β per line.
2. **Author-supplied source data** (Excel-style) for clonogenic counts, foci counts, growth curves — paper says nothing about a deposit. Would require author contact (explicitly out of scope per task).
3. **Raw γ-H2AX image stacks** for foci counting reproducibility — almost never deposited.

## Suggested no-author-contact follow-ups

- If Buglewicz/Kato release a follow-up methods paper or thesis (Buglewicz CSU dissertation is plausible — checked Mountain Scholar, not found as of 2026-06-09), revisit.
- Cross-check the IDRE-in-NHEJ-mutants claim against the older literature already in the reference list (bib6 Jones 1986, bib7 Joshi/Ngo "irs-20" LDR paper, bib12 Mateos 1989) — those classic CHO LDR papers may have already established whether NHEJ mutants generically show IDRE or whether the 2024 finding is novel.
- Keep this slot in the corpus as a "wet-lab-only, paywalled, scoping-only" reference for the LUCID corpus QA pass.
