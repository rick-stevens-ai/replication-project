# Failure Analysis — BVBRC-23 Parageobacillus H2 (Mohr et al. 2018)

## Verdict recap
**PARTIAL.** Genome properties and the CODH-NiFe-hydrogenase locus pattern
reproduce; the pan-genome **core-family count does not** reproduce
numerically.

## What did NOT replicate

### Pan-genome core-family count
- **Paper:** 3509 core families across the four strains = **69.63%** of the pan.
- **Rerun (strict id50 / qcov70):** 2237 families = **43.8%** of the pan.
- **Gap:** ~1272 families / ~26 percentage points.

## Root cause (honest)

### 1. Orthology-method substitution
- **Paper:** OrthoFinder — normalised bit-scores + MCL inflation clustering.
  MCL is designed to be inclusive of paralogs and slightly divergent
  orthologs; it collapses closely-related sequences into a single
  orthogroup even when a strict pairwise-identity filter would split them.
- **Rerun:** `diamond` all-vs-all hits, then single-linkage clustering at
  id ≥ 50%, qcov ≥ 70%. Single-linkage is the *most fragmenting* clustering
  choice: a single below-threshold pairwise edge inside what OrthoFinder
  would treat as one orthogroup breaks the group into multiple clusters
  and inflates the singleton count. In this rerun the strict pipeline
  produced ~1592 strain-unique singletons — consistent with orthogroup
  fragmentation, not with biological uniqueness at that magnitude.
- Running the same pipeline at a **looser cutoff (id ≥ 40 / aln ≥ 80)**
  moved the number materially, confirming *cutoff sensitivity* rather
  than a biological disagreement with the paper.

### 2. Missing tool on the compute host
OrthoFinder was not installed on the host used for this rerun. That is
a stated operational limitation, not a scientific finding. It is the
proximate cause of the substitution and therefore of the PARTIAL verdict.

### 3. Annotation-vocabulary drift (secondary, small effect)
`prokka` and RAST agree on the broad functional categories but differ
in product-name strings. This is minor for orthology (which operates on
protein sequence, not on product-name strings) but is a caveat for the
locus-count proxy (see below).

## What this failure does NOT imply
- It does **not** contradict the paper's mechanistic claim (that
  the CODH-hydrogenase locus explains the H2 phenotype). That claim
  reproduces cleanly (see next section).
- It does **not** indicate a wet-lab or data-integrity problem in the
  original study.
- It is **not** a case of a "core-genome estimate being wrong" — it is a
  case of two different orthology-clustering engines producing different
  core-fraction numbers on the same input.

## What DID replicate (for balance)
- Genome size range: 3.88–3.99 Mb (rerun) vs. 3.96–4.01 Mb (paper) —
  VERIFIED.
- GC content: ~43.7% (rerun) vs. 43.76% (paper) — VERIFIED.
- CODH / NiFe-hydrogenase locus pattern: DSM 2543 / 6285 / 21625 each
  encode 2 CO-DH + 10 NiFe/FHL hydrogenase hits; DSM 2542T encodes
  1 CO-DH + 0 NiFe/FHL — exactly the presence/polymorphism story the
  paper invokes to explain distinct hydrogenogenic capacities. VERIFIED.

## Caveats on the locus-count proxy
The rerun uses **prokka product-name hit counts** as a proxy for the
paper's manual/Mauve locus inspection. This is appropriate for
presence/absence at a coarse locus level, but it does **not** resolve
fine polymorphism *within* the hydrogenase operon. A locus-level match
should therefore be interpreted as strong support for the mechanism,
not as a residue-by-residue reproduction.

## Path to promote PARTIAL → REPLICATED
1. Install OrthoFinder + MCL on the compute host.
2. Re-run pan/core-genome analysis using the paper's stated MCL
   inflation parameter (or the OrthoFinder default if unspecified).
3. If the core-family count lands near 3509 (~69.63%), promote to
   REPLICATED. The rest of the paper is already carried by the current
   rerun.
4. Optional: repeat the locus inspection with a synteny-aware tool
   (clinker or Mauve) to strengthen the mechanistic result from
   presence/absence to synteny-preserved orthologous locus.

## One-line summary
The single failing element is a **quantitative pan-genome statistic
whose value is a documented function of the orthology engine used**;
the paper's biologically decisive result reproduces without ambiguity.
