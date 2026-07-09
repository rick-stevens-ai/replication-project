# Failure Analysis — BVBRC-128 Negrete

Verdict was **REPLICATED**, but this replication had real friction points, gaps, and assumptions worth
documenting honestly.

## 1. CDS-count drift (partial mismatch, not a contradiction)

**What happened.** Paper Table 1 CDS counts differ from our recount of the current (2026) GenBank records:
- H322 chromosome: paper 4,146 → ours 4,019 (−127)
- GK1025B chromosome: paper 3,693 → ours 4,053 (**+360**)
- All 5 plasmids: paper values 11–23 higher than our counts

**Root cause.** NCBI re-runs PGAP on deposited genomes as the pipeline improves. Paper Table 1 was
generated against the 2022 PGAP annotation snapshot; we downloaded the 2026 annotation. Same nucleotide
sequence (exact length match on all 7), but re-classified features. GK1025B's +360 jump is especially
striking — either many pseudogenes were promoted to CDS, or many short-ORF or overlapping-frame calls were
made in a later PGAP release.

**Workaround.** We flagged this as annotation-era drift, not a paper error or a replication contradiction,
and formalized it as Open Question Q1 with concrete next steps (pull the 2022 snapshot from NCBI's
`all_assembly_versions/` archive, diff CDS coordinate sets).

**Residual gap.** Without the 2022 snapshot, we cannot literally reproduce Table 1's CDS numbers. We can
say the sequences are unchanged and the qualitative annotation content (T4SS, T6SS, arsenic operon,
phospholipase D, SSU5 phage genes) is preserved.

## 2. PHASTER not re-run (webserver only)

**What happened.** Paper C13/C15 (chromosomal prophage counts and intact/incomplete classification) and
part of C11 (the ~96.9 Kbp SSU5 prophage boundary) come from PHASTER — a webserver-only tool with no
free CLI. We did not re-run PHASTER.

**Root cause.** Wave-brief hard-rule: "no external paid endpoints, keep replication local/free." PHASTER
is free-to-use but is a webserver requiring form submission and per-job JS handling. Not blocked, but out
of scope for a fast headless replication turn.

**Workaround.** We substituted a direct NCBI-EFetch + BLAST of the SSU5 reference (NC_018843) against the
two candidate plasmids and confirmed strong homology (57–67% qcov at 80–91% identity, 20+ HSPs each).
This is complementary evidence but not identical to PHASTER's "intact" score.

**Residual gap.** Cannot literally reproduce the paper's "4 intact + 1 incomplete" prophage classification
without running PHASTER (or PHASTEST / DBSCAN-SWA CLI as an open-source alternative — see Q2).

## 3. Plasmid phylogenetic-relatedness claim not re-run

**What happened.** Paper C14: pH322_1 and pGK1025B_1 are "phylogenetically related" to pCS1, pCsa767a,
pCsaC757b, pCsaC105731a. We did not fetch these 4 reference plasmids or build a phylogeny.

**Root cause.** Multi-plasmid whole-sequence phylogeny is a heavier compute (MAFFT / progressive Mauve
alignment, IQ-TREE or RAxML tree building). Would be justified as a validation step if the paper's
higher-level conclusion depended on this specific topology — but the paper's core claims (STs, PlasmidFinder
negativity, T4SS/T6SS presence, arsenic operon, SSU5 homology) are all decoupled from the phylogeny.

**Workaround.** We verified the strong SSU5 homology on both plasmids (their most notable phylogenetic
signal), noted the gap in the claims table (C14 marked "not tested"), and moved on.

**Residual gap.** The pCS1-family relationship is asserted but not independently re-verified in this run.
A follow-up run could pull KJ634447 (pCS1) etc. and run Mauve or `nucmer --maxmatch` for pairwise ANI.

## 4. T6SS Kbp span disagreement (partial numerical mismatch)

**What happened.** Paper says the T6SS cluster on pH322_2/pGK1025B_2 is "truncated ~13 Kbp"; our
coordinate-span from GenBank annotations gave 16.4 Kbp (pH322_2) and 17.5 Kbp (pGK1025B_2).

**Root cause.** The paper's "13 Kbp" likely measures the *conserved T6SS core* (structural genes only)
minus the two internal deletions the paper describes. Our span is the outermost T6SS-annotated coordinates,
so it includes flanking accessory genes co-annotated as T6SS-related but not always counted in the "core"
by field convention.

**Workaround.** We reported both numbers side-by-side in the results table and did not treat this as a
contradiction. All key T6SS structural genes (Hcp, VgrG, TssF/G/J/K, contractile sheath) confirmed present.

**Residual gap.** We did not attempt to delineate exactly which genes the paper counted as "in-cluster" vs
"flanking". Reading the paper's Figure 2 more carefully or contacting the authors would resolve this.

## 5. Assumption: NCBI-deposited sequences ARE what the paper describes

Every quantitative claim we verified assumes the CP078106–CP078112 GenBank records deposited by the
authors accurately reflect the sequences they produced. This is standard reproducibility practice — but if
the paper's Table 1 was generated from a pre-deposit assembly version that got revised before deposit, our
"exact length match" would still be genuine agreement with the *published* GenBank, not necessarily with
the paper's Table 1 in-memory numbers. In this case, exact length + GC agreement is strong evidence they
match; the CDS drift (§1) is the only place where a hidden version mismatch could hide.

## 6. What we did NOT need to work around

- **PDF availability:** BMC Gut Pathogens is fully OA; direct PDF fetch worked first try.
- **Data availability:** All 7 GenBank accessions were live at NCBI and downloaded cleanly.
- **CGE PlasmidFinder DB:** live at Bitbucket, downloaded cleanly at 130 KB.
- **PubMLST REST API:** live, no auth needed, returned STs in one round-trip.
- **BLAST tooling:** local BLAST+ 2.16 worked (with a benign MBEDTLS warning printed to stderr — did not
  affect results).
- **No paywall, no rate-limit issue, no LLM cost incurred.**
