# Replication Brief — Alter et al. 2026 (multitensor GSVD / neuroblastoma)

- **Title:** Quantum mechanics-based multitensor AI/ML uniquely able to discover, validate, and interpret predictors from small-cohort noisy high-dimensional multiomic data
- **Authors:** Orly Alter (Univ. Utah SCI / Bioeng / Human Genetics / Huntsman; Prism AI Therapeutics), Elizabeth Newman (Tufts Math), Sri Priya Ponnapalli (Scale AI), Jessica W. Tsai (CHLA / Keck USC)
- **Venue:** APL Quantum 3(2), 026116 (2026). DOI 10.1063/5.0305656. Submitted 7 Oct 2025, accepted 11 May 2026, published 22 Jun 2026. CC-BY.
- **PDF:** source/alter-multitensor-2026.pdf (15.5 MB, 22 pp). Provided directly by Rick (Cloudflare blocked the AIP scrape).

## What the paper is
A **mathematical methods paper**: it unifies the authors' prior "comparative spectral decompositions" — the **GSVD** (two matrices), **HO-GSVD** (higher-order, multiple matrices), and **tensor GSVD** — into a single multitensor framework for any number of tensors of any order. It proves existence/uniqueness, defines new metrics ("multitensor joint Shannon entropy", "multitensor comparative angular distance"), and frames the structure via quantum-mechanical **superposition + entanglement** analogies. It is NOT a deep-learning paper; the "AI/ML" is exact, structure-preserving linear-algebra (SVD-family) decompositions.

## Demonstration / application (neuroblastoma, NBL)
- Discovery cohort: **X = 101 NBL patients** from TARGET, patient-matched **tumor + blood WGS** + **tumor transcriptome (TCS)**.
- Two novel predictors discovered, each with **three "entangled" representations** (tumor genome, blood genome, tumor transcriptome).
- Tumor-DNA feature space: **2,831,960** features; shared TCS/WGS genomic features Z1=10,354 / Z2=10,475; tumor RNA 15,393 features; HO-GSVD multimatrix limit X=71.
- Validation: 398 validation patients via pseudoinverse projection; 62-patient HO-GSVD RNA classification.

## Headline quantitative claims (Table I, n=90 with full labels)
The combined GSVD predictors (u1,1 + u1,101 across 2,831,960 tumor-DNA features) beat every standard-of-care indicator:
- **Combined predictor (Tumor DNA 1+101), univariate:** log-rank **P = 2.3×10⁻⁵**, HR **4.0** (95% CI 2.0–8.1), Wald P=8.6×10⁻⁵, **concordance 0.80**, AIC 326.
- vs **MYCN amplification** (the one-gene standard of care): log-rank P=5.7×10⁻³, HR 2.4 (1.3–4.5), concordance 0.73.
- vs INSS stage (P=2.1×10⁻³, C=0.83), age (P=2.2×10⁻³, C=0.76), COG risk, MKI, ploidy, histopathology — all weaker log-rank P than the combined predictor.
- Core claim: **the two predictors combined are consistently more accurate than MYCN in every representation**, and are independent of standard indicators (Cox multivariate).

## Data availability (verbatim, full)
> Datasets 1–3 are available **upon request** in TXT format.
> **Dataset 1:** Clinical, sample, and profile labels of the discovery set of X = 101 NBL patients, reproduced from the TARGET project. Also available: corresponding tumor and blood DNA profiles — log2 of Complete Genomics DNA read counts in Z1 = 2,831,960 (tumor) and Z2 = 2,831,959 (blood) nonoverlapping 1K-nucleotide bins across the autosome + X chromosome of hg19, each profile centered at its autosomal median — and tumor RNA profiles of 71 of the patients (log2 of Illumina HiSeq 2000 RNA read counts, Z3 = 15,393 transcripts).
> **Dataset 2:** Clinical, sample, profile labels of the validation set of Y = 419 NBL patients. Also: tumor and blood DNA profiles (Illumina HiSeq 2500 DNA read counts) in the Z1 = 10,354 / Z2 = 10,475 bins shared with the discovery WGS tumor/blood bins.
> **Dataset 3:** Genomic, segmentation, and CNA labels of the CBS segments in the GSVD tumor DNA-specific patterns u1,k, k = 1, 100, 101.
> **Mathematica Notebook 1** is available upon request in PDF format.

## Code availability
- No public GitHub/Zenodo link, BUT the implementation is **Mathematica Notebook 1** (PDF, upon request) — the group works in Mathematica, not MATLAB. Requesting it gives us the authors' actual algorithm steps.
- Method also fully specified mathematically (Eqs. 1, 3, 5–8, 13) and rests on GSVD/HO-GSVD/tensor-GSVD literature (Alter-Brown-Botstein PNAS 2000; Ponnapalli HO-GSVD; Khamidullina ML-GSVD IEEE TSP 2022).

## Upgraded replicability read (after full Data-Availability statement, 2026-06-23)
The data is FAR more concretely described than "upon request" implied — exact bin counts, platforms, transforms (log2, autosomal-median-centering), and feature dimensions are all specified, and the validation cohort (Y=419) is named. Combined with Mathematica Notebook 1 (the implementation), a **numeric replication is realistically achievable** if Orly sends Datasets 1–3 + the notebook. Path likely upgrades from SPOT-CHECK toward PARTIAL→REPLICATED depending on how complete the TXT exports are. The exact pre-processed profiles (CG 1kb-bin read counts, median-centered) are the single hardest thing to reconstruct independently from raw TARGET, so her TXT datasets are the high-value ask.

## Replicability assessment (pre-work)
- **Underlying data:** TARGET NBL is public (TARGET-NBL, dbGaP/GDC) — the discovery cohort is reconstructable, though the paper's exact curated Datasets 1–3 are "upon request" only.
- **Method:** fully reproducible from equations + the public GSVD/HO-GSVD math; this is the strongest part. The GSVD of two matrices and HO-GSVD of multiple matrices are deterministic linear algebra.
- **Bottleneck:** exact feature curation (2.83M tumor-DNA features, the specific shared-feature sets, the u1,1/u1,101 antisymmetric-pattern selection) is intricate; numeric reproduction of the exact HR/P-values needs the authors' curated profiles.
- **Likely verdict path:** SPOT-CHECK → PARTIAL. We can (a) reproduce the GSVD/HO-GSVD math on TARGET-NBL WGS/RNA to confirm the antisymmetric-pattern predictor structure exists, and (b) audit the survival statistics qualitatively (KM/Cox on recovered classifications), but exact numeric match (P=2.3×10⁻⁵, HR=4.0, C=0.80) requires Datasets 1–3. Email Orly (orly@sci.utah.edu) to request Datasets 1–3 — she explicitly offers them on request and clearly wants this reproduced (she thanked Rick in the paper).

## Recommended next steps
1. **Email Orly to request Datasets 1–3** (TXT) — the clean path to a numeric replication; she invited it.
2. In parallel, **pull TARGET-NBL** WGS + RNA from GDC and stand up a GSVD/HO-GSVD reference implementation (Python: scipy.linalg has GSVD via `scipy.linalg.svd` on the quotient; or port the group's MATLAB HO-GSVD).
3. Reproduce Fig 5 (two-matrix GSVD of 101 tumor+blood WGS) and Table I survival stats; report Coverage/Agreement.
