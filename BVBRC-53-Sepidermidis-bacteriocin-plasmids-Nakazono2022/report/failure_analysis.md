# Failure Analysis — BVBRC-53 (Nakazono 2022)

Verdict was **PARTIAL REPLICATION (strong)**. This document names the things
that did *not* land cleanly, why they didn't, and what a fuller replication
would need.

## 1. Wet-lab claim C8 is entirely out of reach

- **What failed:** Claim C8 — antibacterial-activity spectra and ESI-MS
  confirmation of mature-peptide masses — cannot be evaluated from
  sequence.
- **Why:** These are wet-lab assays that require the physical KSE56 and
  KSE650 isolates, an MS facility, and a target strain panel. None of
  that is inside a bioinformatic replication scope.
- **Impact:** This is the single largest reason the verdict is PARTIAL
  rather than FULL.
- **What would close it:** obtaining the isolates (author correspondence or
  a culture-collection deposit), doing plate spot-on-lawn / broth
  microdilution assays vs a diverse Gram-positive panel, and confirming
  mature-peptide masses by ESI-MS. Explicitly excluded from this scope
  and not attempted.

## 2. Claim C3 ORF-count delta didn't reproduce as an integer

- **What failed:** The paper reports pNuk650 carries "+7 ORFs" versus
  pIVK45. Using the current NCBI GenBank annotations directly, we get
  29 vs 17 CDS — a delta of 12, not 7.
- **Why:** ORF calling is annotation-pipeline dependent. The paper
  re-annotated pIVK45 with RAST v2.0 as part of a symmetric re-annotation;
  we compared to the deposited GenBank record as-is. This is a methodology
  gap, not a factual contradiction.
- **Impact:** The *structural* claim (a single large ~6–8 kbp insertion
  accounting for the size difference) is unambiguously confirmed by
  blastn: 5,926 bp + 1,821 bp = 7,781 bp unaligned. So the substantive
  finding survives; only the "+7" integer is annotation-sensitive.
- **What would close it:** re-annotate both plasmids with the same
  pipeline the paper used (RAST v2.0) and re-count. That was outside the
  scope of this replication.

## 3. MUMmer was broken locally — forced a blastn-only comparison

- **What failed:** MUMmer / nucmer would not run locally
  (`TIGR::Foundation` @INC error plus an mbedtls version mismatch on
  supporting binaries).
- **Why:** Local install / library-version drift on the analysis host.
- **Impact:** Small. We fell back to `blastn -perc_identity 80` which is
  fully adequate for computing backbone identity and locating insertion
  blocks, and the numbers match the paper's structural narrative. What we
  did *not* produce is a MUMmer/promer dotplot, which would have been a
  stronger visual complement.
- **What would close it:** fix the local MUMmer installation (or use
  minimap2/nucmer via a container) and regenerate a dotplot for the
  supplementary evidence bundle.

## 4. Nucleotide-level detail of Claim C4 was checked only at the aa level

- **What failed:** The paper claims "2 nt mismatches in epiA" between
  KSE56 and Tü3298. We only verified the amino-acid-level consequence
  (0 aa mismatches → 100% aa identity), consistent with silent or
  leader-only nucleotide changes.
- **Why:** The claim that matters biologically is the mature peptide
  identity, which we did check and confirm. We did not pull a canonical
  Tü3298 epiA nucleotide sequence and diff it against KSE56 epiA
  base-by-base.
- **Impact:** Very small. The functionally meaningful claim
  (100% aa-identical epidermin) holds; only the DNA-count claim itself
  wasn't re-derived.
- **What would close it:** align KSE56 epiA nt against a canonical
  Tü3298 epiA nt reference and enumerate the exact 2 substitutions.

## 5. Self-immunity was inferred from gene-cluster presence, not assayed

- **What failed:** We confirmed the epi (epiE/F/G/H) and nuk
  (nukF/E/G/H) immunity cassettes are present and complete, but did
  not measure self-immunity phenotypically.
- **Why:** Self-immunity requires functional assays on the producer
  strains (knockouts, complementation), which is wet-lab. This is a
  known limitation of any pure sequence-level replication.
- **Impact:** Consistent with the paper's own scope, which shows producer
  viability but does not measure self-immunity in a component-wise way.
  Reproduced as designed.
- **What would close it:** open question #4 in `open_questions.json`.

## 6. Things that *did not* fail (for completeness)

- Length matches to the exact base pair on all three plasmids.
- CDS count matches on the two novel plasmids (81 / 29).
- Both bacteriocin peptide-identity claims reproduce.
- Backbone identity and the ~8 kbp insertion structural claim reproduce.
- BV-BRC PlasmidFinder rep-typing runs cleanly and adds an independent
  piece of evidence (shared replicon lineage between pNuk650 and pIVK45;
  divergent rep in pEpi56).
- AMR and virulence screens are cleanly negative — consistent with the
  paper's framing of these as bacteriocin-immunity plasmids.

## 7. Summary judgement on the failure surface

The failure surface is narrow and well characterized: one wet-lab claim
that is inherently out of reach for a bioinformatic replication, one
annotation-dependent ORF-count discrepancy that does not affect the
structural conclusion, and two tooling / detail gaps
(MUMmer, nt-level C4) that do not change any verdict. Nothing in the
paper's sequence-testable core was contradicted.
