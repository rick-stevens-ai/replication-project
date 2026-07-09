# Failure Analysis — BVBRC-51 Minicystis rosea DSM 24000T

**Verdict:** PARTIAL (strong).
**Scope of this document:** enumerate what did *not* cleanly replicate, classify each shortfall, attribute a most-likely root cause, and record what would be required to close each gap.

The paper's core empirical claims (genome size, strand-resolved CDS count, *pfa* operon presence + synteny, dominant BGC categories) reproduced cleanly. The failure surface below is the honest residual — the reasons this replication is called PARTIAL and not fully REPLICATED.

---

## F1 — antiSMASH BGC total: 53 (replication) vs 47 (paper)

- **Symptom:** Δ+6 total BGC regions relative to the paper's headline count.
- **Category-level:** all dominant categories reproduce in rank order; increments concentrated in terpene (9→12), RiPP-like (7→9), NRPS (7→8), PKS (4→5), RRE-containing (4→5), thioamitide (2→3). Singletons (phosphonate, phenazine, siderophore, arylpolyene, lanthipeptide, indole) match exactly.
- **Root cause (most likely):** antiSMASH major-version jump v5.0 → v8.0.4 between the paper (2021) and this replication (2026). v8 ships additional detection rule sets, new RiPP subclass rules, expanded thioamitide handling, and more permissive region-boundary merging. This is a documented characteristic of the tool line, not a scientific disagreement.
- **What this replication did NOT do:** rerun antiSMASH v5.0 side-by-side to *directly demonstrate* byte-for-byte parity with the paper's 47.
- **Severity:** low. The category-level agreement, singleton reproduction, and version-shift attribution are all consistent, but the "version-shift" story is inferential rather than directly benchmarked.
- **Closure path:** build a second conda env with antiSMASH 5.0 exactly (matching the paper's version pin), rerun on the same GCA_001931535.1 assembly, and confirm the count lands at 47 with identical category shape.

## F2 — tRNA count: 89 (replication) vs 88 (paper)

- **Symptom:** Δ+1 tRNA.
- **Root cause (most likely):** tRNA-annotation method drift. PGAP (which produced the GFF3 used here) uses tRNAscan-SE 2.x with contemporary parameter sets and covariance-model updates; the paper's number came from whatever pipeline BV-BRC / RASTtk was running in 2021 (possibly older tRNAscan-SE + Aragorn cross-check).
- **Severity:** trivial. A one-tRNA difference on an 88-tRNA genome is well within annotator noise.
- **Closure path:** rerun Aragorn + tRNAscan-SE 2.x independently and confirm which single tRNA is the discrepant call.

## F3 — GC% and coding density minor drifts

- **Symptom:** GC% 69.07 → 69.10 (Δ0.03); coding density 87.31% → 87.59% (Δ0.28).
- **Root cause (most likely):** methodological rounding + differing CDS-length conventions (whether stop codons are included in CDS-length totals; whether overlapping CDS regions are double-counted or reduced).
- **Severity:** trivial. Both deltas are within normal reannotation noise.
- **Closure path:** publish the exact per-feature CDS-length aggregation formula used and re-derive; would resolve to sub-0.05% agreement.

## F4 — "Largest bacterial genome (2021)" claim: not independently benchmarked

- **Symptom:** replication confirms the 16.04 Mbp size but does *not* verify the comparative claim that this was the largest bacterial genome as of 2021.
- **Root cause:** verifying this claim requires querying the 2021 snapshot of RefSeq / GenBank complete-bacterial-genome records and computing the size distribution — a scope that was not undertaken in this pass.
- **Severity:** low-to-moderate. This is one of the paper's headline framings; leaving it unverified is a genuine gap.
- **Closure path:** pull the assembly_summary.txt from the RefSeq 2021 snapshot (available via NCBI's release archive), filter to `assembly_level == "Complete Genome"` and `group == "bacteria"`, rank by `total_length`, confirm CP016211.1 sits at the top of the 2021 distribution.

## F5 — HGT-from-Actinobacteria inference (C5): reproduced at the ortholog/synteny level, not at the phylogenetic-signal level

- **Symptom:** the paper's HGT argument rests on both synteny *and* phylogeny; this replication reproduces the ortholog identification and operon synteny but does not independently rebuild the *pfa* phylogenetic tree that grounds the HGT conclusion.
- **Root cause:** phylogenetic reconstruction was out of scope for this pass; the BLAST+synteny evidence is already sufficient to confirm the presence of the operon, which was the higher-priority testable claim.
- **Severity:** moderate. The HGT inference is consistent with the evidence collected here but not independently corroborated — a reader could still doubt the Actinobacterial origin.
- **Closure path:** pull PfaA/B/C homologs across a broad Actinobacteria / Myxobacteria / Firmicutes taxonomic sweep, align with MAFFT-LINSI, build a maximum-likelihood tree with IQ-TREE + ultrafast bootstrap, check whether the M. rosea Pfa proteins branch inside an Actinobacterial clade (paper's claim) or with the myxobacterial reference set (which would weaken the HGT story).

## F6 — ~44% paralogous coding potential: not independently recomputed

- **Symptom:** paper reports ~44% paralogous CDS; replication does not verify this.
- **Root cause:** all-vs-all self-alignment + MCL clustering was out of scope for this pass.
- **Severity:** low. Not a claim contested here; simply not independently checked.
- **Closure path:** DIAMOND self-align the proteome + MCL cluster at inflation 1.5–2.0; report the fraction of CDS in multi-member clusters.

## F7 — Single-tool BGC calling (antiSMASH only)

- **Symptom:** BGC count and category assignments rely solely on antiSMASH; no triangulation with PRISM, DeepBGC, or GECCO.
- **Root cause:** scope + compute discipline — a single tool run on the deposited genome was sufficient to reproduce the paper's own methodology (which likewise used only antiSMASH).
- **Severity:** low for reproducing the paper (which uses only antiSMASH); moderate as an *evaluation* of the paper's BGC catalog, since single-tool BGC calling is known to have false positives / false negatives.
- **Closure path:** rerun DeepBGC + GECCO on the same FASTA, tabulate agreement per region, publish a consensus BGC table.

## F8 — pfa BLAST coverage not decomposed per PKS domain

- **Symptom:** PfaA and PfaC show summed-HSP coverage of 49–79% and 79–91% respectively — strong signal but not saturating.
- **Root cause:** the tabulation aggregates HSPs into a summed-coverage number without decomposing per functional PKS domain (KS, AT, KR, DH, ACP…). Large multi-domain PKS proteins routinely hit as multiple HSPs, and a summed-coverage number can mask which specific domain is or is not present.
- **Severity:** low. The convergent antiSMASH T1PKS/hglE-KS call + PGAP's independent "PfaA subunit" annotation both make it very likely the full PKS module suite is present. But the BLAST tabulation as published here does not itself demonstrate that.
- **Closure path:** re-tabulate BLAST HSPs against a PKS-domain scan (Pfam PKS_KS, PKS_AT, PKS_KR, PKS_DH, PP-binding) so each domain is confirmed independently.

## F9 — No wet-lab confirmation of *pfa* cluster function

- **Symptom:** the *pfa* operon is inferred entirely from sequence + annotation + BGC prediction; no metabolite (EPA / DHA / arachidonic acid) detection is performed.
- **Root cause:** replication is computational-only, matching the paper's own scope. Neither the paper nor this replication does a metabolomics readout.
- **Severity:** low relative to the paper's own scope (both are inference from sequence); moderate as a general critique of the field.
- **Closure path:** LC-MS/MS of M. rosea DSM 24000T lipid extract under standard growth conditions, quantifying PUFA output vs a non-pfa-bearing myxobacterial control.

## F10 — LLM-judge divergence

- **Symptom:** `gpt-5.2` returned PARTIAL, `claude-opus-4.8` returned REPLICATED.
- **Root cause:** genuine judgment call on how much weight to place on the 53-vs-47 BGC delta. `gpt-5.2` treated it as a scoreable numeric miss; `claude-opus-4.8` treated it as a tool-version artifact and disregarded it.
- **Severity:** none for the underlying evidence; procedural only. The verdict-reconciliation rule ("follow the more conservative judge; do not inflate") lands on PARTIAL.
- **Closure path:** none needed — the divergence is honest and documented.

---

## Summary attribution table

| Failure | Class | Severity | Attributable to |
|---|---|---|---|
| F1 (BGC 53 vs 47) | Tool-version | Low | antiSMASH v8 vs v5 |
| F2 (tRNA 89 vs 88) | Annotator drift | Trivial | tRNAscan-SE version + parameters |
| F3 (GC% / coding-density micro-drifts) | Methodological rounding | Trivial | CDS-length convention |
| F4 ("largest bacterial genome") | Not benchmarked | Low-Mod | Out of scope this pass |
| F5 (HGT phylogeny) | Not benchmarked | Moderate | Phylogeny out of scope |
| F6 (44% paralog) | Not benchmarked | Low | All-vs-all out of scope |
| F7 (single-tool BGC) | Method-diversity | Low-Mod | Matched paper's own scope |
| F8 (BLAST coverage not per-domain) | Reporting granularity | Low | Tabulation format choice |
| F9 (no wet-lab) | Scope | Low (matches paper) | Computational-only replication |
| F10 (LLM-judge split) | Procedural | None | Genuine judgment divergence |

**Net honest read:** the failures collected here are dominated by *scope-limited non-benchmarks* (F4, F5, F6, F7, F9) and *tool-version drift* (F1, F2, F3). None of them contradict the paper's substantive scientific claims. That is the reason for PARTIAL rather than a hard-negative verdict, and equally the reason for PARTIAL rather than a fully REPLICATED verdict.
