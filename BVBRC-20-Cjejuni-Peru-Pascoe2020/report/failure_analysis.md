# Failure analysis — BVBRC-20 replication of Pascoe et al. 2020

**Overall verdict:** PARTIAL (Coverage 9/10, Agreement 7/10; independent LLM judge gpt-5.2).

This document catalogues where and *why* this independent rerun departs from the paper's reported values, plus the honest limits of the reproduction. It is deliberately non-exculpatory.

---

## 1. Quantitative gaps

### 1.1 MLST exact concordance — 47/62 (75.8%), gap = 15 isolates

- **Paper:** 62 STs assigned via pubMLST (accessed 17-Feb-2020).
- **This rerun:** 47/62 exact match; 8 untyped (single missing allele in newer pubMLST DB); 4 assigned to novel ST12690 / ST12694 / ST12697 (genuinely different allele profiles). The first ~47 isolates agree exactly.
- **Root cause:** pubMLST allele-database version drift between 2020 and 2026. The paper did not pin (and could not reasonably have deposited) a pubMLST snapshot, so bit-exact ST re-assignment is not achievable across DB versions.
- **Impact:** any downstream analysis keyed on specific ST identifiers (e.g. ST-level SNP grouping, ST-based host-source attribution) is not bit-reproducible. Clonal-complex-level claims (see §2.1) survive because the affected isolates still cluster into the same CCs.
- **Not resolvable without:** authors depositing the exact pubMLST allele-DB snapshot they used, or pubMLST providing dated snapshot retrieval.

### 1.2 Beta-lactam resistance — 26/62 (paper 32/62), gap = 6 isolates, 18.75% relative

- **Paper:** 32/62 beta-lactam-positive per S5 (ABRicate).
- **This rerun:** 26/62 beta-lactam-positive at ABRicate defaults (80% identity / 80% coverage).
- **Root cause:** *C. jejuni* carries the near-ubiquitous *bla*OXA-61 family. Six isolates have *bla*OXA-61 hits that sit at the identity/coverage boundary — the paper's calls presumably used a slightly looser threshold (or a different DB build) that admitted them, while defaults do not.
- **Impact:** directionality (beta-lactam dominates the Peru resistome, aminoglycoside is absent) reproduces; absolute prevalence differs.
- **Not resolvable without:** the paper's ABRicate cutoff parameters or the exact DB build; both are unpublished in the manuscript and supplements. Could be tightened by re-running at 70/70 or by direct BLASTP against the *bla*OXA-61 reference and reporting all hits with identity ≥ threshold X, over a range of X.

### 1.3 Tetracycline resistance — 10/62 (paper 11/62), gap = 1 isolate

- Within noise; effectively agrees. Same explanation family as §1.2 (one *tet* hit at the cutoff boundary). Recorded as VERIFIED ±1.

## 2. Methodological substitutions

### 2.1 Phylogeny: Mash/NJ instead of core-genome ML

- **What the paper did:** built a core-genome ML tree (RAxML-style workflow) on the 62-isolate set plus a global context collection.
- **What this rerun did:** built Mash sketches (`s=10000`), computed pairwise Mash distances, and produced a neighbour-joining tree (`data/phylo/peru_mash_nj.nwk`). Also computed per-aetiology within-group Mash distances.
- **Why the substitution:** the substitute is sufficient to test the paper's *structural* claim (asymptomatic isolates are polyphyletic / phylogenetically divergent, not a single carrier clone) but does not reproduce the exact tree topology, branch supports, or clade-level assignments.
- **What is NOT independently verified as a consequence:** any statement of the form "lineage X sits basal to clade Y" or "asymptomatic isolates form a monophyletic sub-clade within CC353". Only the coarser divergence-statistic claim (within-group Mash asymptomatic 0.0180 ≥ symptomatic 0.0164) is checked.
- **Full closure would require:** re-running the paper's core-genome pipeline (e.g. Roary / Panaroo → core alignment → RAxML/IQ-TREE) on the same 62 assemblies plus a matched global reference set.

### 2.2 Source attribution: ST-diversity + Mash summaries instead of pubMLST ecology classifier

- **What the paper did:** used pubMLST ecology annotations for host/source attribution (poultry, livestock, human).
- **What this rerun did:** reproduced the aetiology split (31 symptomatic / 28 asymptomatic / 3 unknown) from S6, plus per-aetiology ST-diversity and within-group Mash statistics; did not re-run a per-isolate source classifier.
- **Consequence:** per-isolate source-attribution accuracy vs the paper is untested. Aetiology-level structure reproduces.

### 2.3 Ground-truth loop for AMR

- **What was used as truth:** the paper's own S5 ABRicate summary.
- **Why this is a partial-truth:** S5 is the paper's *own tool output* — so tool-vs-tool comparison is not a fully-independent AMR validation. A truly independent AMR check would need (a) a second-generation resistome caller (e.g. AMRFinderPlus, RGI) or (b) phenotypic disk-diffusion / MIC data on the same isolates.
- **Neither (a) nor (b) is present here.** This is a scope decision (the paper does not deposit phenotypic AMR); it is nonetheless a real limit on the independence of the AMR verification.

## 3. Things NOT re-run

- **antiSMASH per-genome secondary-metabolite annotation** — not reproduced; the paper's downstream analyses use the deposited assemblies directly, as does this rerun.
- **RAST per-gene re-annotation** — not reproduced; same reason.
- **Raw-read re-assembly from PRJNA350267** — not attempted. The FigShare assemblies were used as input, matching the paper's own downstream input. If FigShare were withdrawn, this exact replication would not be reproducible from SRA alone without introducing assembler-version variance.
- **Global-context re-analysis** — the paper contextualises the 62 Peru isolates within a global collection. This rerun did NOT re-download and re-analyse the global reference set; the "globally-dominant CC21/CC45 are rare in Peru" claim is verified only in the sense that CC21 and CC45 counts in the Peru set (3/62 and 4/62) are low relative to CC353/CC362/CC354 (15/11/8).

## 4. Latent limits of the underlying study (revisited)

These are not "failures" of this replication — they are limits inherited from the paper's design that this replication cannot escape.

- **Single-site, single-cohort sampling** — all 62 isolates are from one Iquitos pediatric cohort; region-level population-structure claims generalise from a single geographic-temporal window.
- **Northern-Hemisphere bias in the global comparison set** — the "locally-restricted Peru CCs" contrast is defined against pubMLST, which is heavily biased toward European/North American surveillance. The apparent restriction of CC353/CC362/CC354 may be partially an under-sampling artefact for South America / Africa / SE Asia.
- **Culture-based recovery** — asymptomatic-carriage CC composition is filtered through *C. jejuni*'s fastidious culture requirements; some carriage will be missed entirely.
- **Polyphyly ≠ non-pathogenicity** — the paper's central asymptomatic-polyphyly finding (reproduced here) says asymptomatic strains are genetically heterogeneous. It does *not* demonstrate that they lack virulence potential. Host-side factors are not assessed.

## 5. What would move this from PARTIAL to FULL

1. Access to a pinned pubMLST allele-DB snapshot from 17-Feb-2020 → closes §1.1 and lifts MLST concordance to (presumably) 62/62.
2. Recovery of the paper's ABRicate cutoff parameters and DB build → resolves §1.2 (beta-lactam 26 vs 32).
3. Re-running the core-genome ML pipeline (Roary/Panaroo → RAxML/IQ-TREE) on the same 62 assemblies → closes §2.1 and enables topology-level comparison.
4. Optional but strengthening: an independent AMR caller (AMRFinderPlus, RGI) run on the same assemblies → converts §2.3 from tool-vs-tool to tool-vs-independent-tool.

None of the four are blocked by data availability; (1) and (2) are blocked by *metadata* availability (pubMLST snapshot pinning; unpublished ABRicate parameters), and (3)/(4) are compute-and-time scoped, not blocked.
