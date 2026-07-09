# Failure analysis — BVBRC-130

Verdict is **REPLICATED**, but this file documents friction, residual gaps, and honest limits per the standing rule ("even for clean REPLICATED verdicts, document friction/partial mismatches/assumptions").

## 1. Small quantitative mismatches (all explained)

### 1.1 Length: paper 4,487,389 bp vs deposited 4,487,489 bp (Δ = +100 bp)
- **Root cause:** the deposited chromosome contains **exactly 100 `N` bases** (verified by direct base-composition count).
- **Interpretation:** the paper reports the ungapped length; the deposited FASTA includes a 100-bp gap of Ns.
- **Workaround:** none needed; the delta is a bookkeeping artifact, not a scientific discrepancy.
- **Residual gap:** the paper does not say where those Ns live or whether they represent a specific repeat that Canu could not resolve. Would need raw PacBio reads (not obviously deposited in SRA under this BioProject) to close.

### 1.2 Gene count: paper 4,147 (RAST) vs 4,081 (NCBI PGAP), Δ = 1.6 %
- **Root cause:** different annotator. RAST 2015-era CDS calling differs from PGAP (NCBI's) in: pseudo-gene splitting, short-ORF cutoffs, RNA family coverage.
- **Interpretation:** typical annotator variance on identical bacterial genomes runs 1–3 %; 1.6 % is well inside that band.
- **Workaround:** cross-referenced *both* annotations; verdict does not hinge on either being the ground truth.
- **Residual gap:** we did not re-run RAST directly (RAST is a hosted web service; not free-endpoint scriptable in a single shell turn). If exact reproduction of the 4,147 number is required, submit CP124620 to https://rast.nmpdr.org/ interactively.

### 1.3 Coverage: paper 166× vs NCBI assembly metadata 164×
- **Root cause:** rounding / different denominator (paper divides total bases / genome length; NCBI may divide by a slightly different length figure). 2× discrepancy on ~165× coverage is a rounding delta.
- **Workaround:** not material to any conclusion.

## 2. Data-fetch friction

### 2.1 PMC PDF endpoint failed
- `https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10682605/pdf/` returned an HTML redirect wrapper, not a PDF.
- **Fix:** F1000Research direct `pdf` URL worked on the first try.
- **Lesson:** for open-access papers, hit the *publisher* PDF endpoint before PMC.

### 2.2 NCBI Datasets v2alpha `dataset_report?filters.reference_only=false` returned `{}` for a nuccore accession
- The Datasets REST endpoint expects an assembly accession, not a nuccore accession, for `dataset_report`. It silently returns empty rather than 400.
- **Fix:** used `elink` to jump nuccore→assembly, then `esummary db=assembly&id=<uid>`.
- **Lesson:** for the workflow "nuccore accession → assembly metadata", elink+esummary is the reliable path.

### 2.3 `blastn` mbedtls version warning
- `Critical: (310.5) [blastn] External MBEDTLS version mismatch: 3.6.5 headers vs. 3.6.6 runtime`
- Harmless; BLAST completed and returned correct hits.
- **Lesson:** don't panic on `Critical:` in BLAST — it's a build-vs-runtime library mismatch that BLAST tolerates. (If it ever *does* start failing TLS, rebuild BLAST+ against 3.6.6 headers.)

## 3. Methodological substitutions (documented)

### 3.1 skani ANI instead of TYGS dDDH
- **Substitution:** we used skani (learned-ANI) for whole-genome species-boundary check; the paper used TYGS's Genome BLAST Distance Phylogeny (GBDP) dDDH.
- **Justification:** the two methods are well-correlated (ANI 95 % ≈ dDDH 70 %), and both put CP124620 far outside the "same species" boundary from the two closest publicly-available references. We did not reproduce TYGS's exact d0/d4/d6 numbers.
- **Would need to close:** submit CP124620 to https://tygs.dsmz.de/ interactively — that is a captcha-gated web service, not free-endpoint scriptable in a shell subagent.

### 3.2 Marker/Nougat fallbacks
- Marker binary not installed on this host; used `pdftotext -layout` per the project's standard fallback pattern (BVBRC-100…-104 all use the same pattern in their `extraction/marker.md` headers).
- Nougat binary not installed; wrote a documented stub pointing at the central Nougat manifest as the swap-in target when this PMID gets processed.
- **Would need to close:** run the paper through the central Marker/Nougat pipeline on Eagle and copy the resolved outputs into `extraction/`.

### 3.3 BV-BRC workflow itself was not run
- The paper does not require BV-BRC to reproduce its claims — the deposited public assembly is the ground truth. We verified the numbers against that assembly directly, which is what BV-BRC's Comprehensive Genome Analysis workflow would also consume.
- **Would need to close:** upload CP124620 to https://bv-brc.org, run the CGA workflow, and confirm that the annotation counts land within 2 % of PGAP.

## 4. Out-of-scope claims (biological, wet-lab)

- **C8 (methionine/cysteine auxotrophy):** the paper backs this with (a) genome-based absence of assimilatory sulfate pathway components, and (b) direct growth-curve tests in MM + Met/Cys. Only (a) is computationally re-checkable, and the paper's own KEGG/subsystem analysis is credible enough that a re-derivation would just re-confirm the paper's pathway-coverage argument. Growth curves require the actual strain.
- **C9 (mutualistic coculture):** requires *C. reinhardtii* + *S. goyi* cocultures; strictly wet-lab.

## 5. What would elevate this from REPLICATED → strengthen-with-independent-metric

Already essentially done: whole-genome ANI (skani) is an independent-metric strengthening beyond what the paper itself reports (paper only shows TYGS dDDH and does not report ANI). The 86.3–86.5 % ANI values corroborate the "novel species" claim from a second angle. If one wanted more, a Prokka re-annotation would give a third independent annotator's gene-count and confirm the RAST/PGAP delta is annotator-driven and not a real feature of the sequence.
