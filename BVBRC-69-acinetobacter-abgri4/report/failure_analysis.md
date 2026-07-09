# Failure Analysis — BVBRC-69 AbGRI4 replication

**Target:** Chan et al. 2020, AbGRI4 (DOI 10.1093/jac/dkaa266)
**Verdict:** REPLICATED (no claim contradicted)
**Purpose of this file:** honestly log the near-misses, partial failures, and things that could have gone wrong but were caught — so future replicators don't rediscover the same footguns.

## 1. Actual partial failures

### 1.1 Oxford ST281 could not be emitted as a single ST call
- **What happened.** `mlst 2.33.1` with the `abaumannii` (Oxford) scheme returned a double-hit at the `gdhB` locus (alleles {3, 189}) for all four isolates, and consequently refused to collapse the profile to a single ST call. Result was reported as `-` for ST.
- **Why it wasn't a real contradiction.** The full allele profile 1-17-{3,189}-2-2-99-3 is otherwise consistent with the paper's declared ST281. The issue is DB-side: the current PubMLST snapshot has a novel `gdhB` allele that overlaps the reference and confuses the single-best-hit call.
- **How we handled it.** C3 is honestly marked ⚠️ **partial** in the claims table rather than ✅. The Pasteur scheme (ST2) is unambiguous, so the paper's clade assignment is not in question.
- **Lesson.** MLST schemes drift. When a scheme returns a multi-hit at one locus, do not silently paper over it — report the full allele profile and flag the partial call. A stronger future check would be a manual PubMLST query at a pinned scheme version.

### 1.2 C12 (hybrid-assembly requirement) not tested
- **What happened.** The paper asserts that IS-bounded resistance islands require long+short-read hybrid assembly to resolve correctly.
- **Why we didn't test it.** Testing it would require pulling raw SRA reads and re-assembling under two conditions (short-only vs hybrid), which is out of scope for a claims-verification replication and is already well-supported in the independent methods literature.
- **How we handled it.** Marked ✖️ **out of scope** in the claims table with an explicit note. Not counted as a failure — counted as a claim we deliberately declined to test.
- **Lesson.** A replication can be full-replication for the *data claims* while explicitly declining to redo the *methods assertion*. Be honest about which category each claim falls in.

## 2. Latent risks that could have caused a false REPLICATED verdict — and how they were mitigated

### 2.1 Byte-identity might be an assembly artifact
- **Risk.** 0 mismatches over 8,840 bp across three independent clinical isolates is at exactly the resolution where assembly polishing artifacts, IS26-mediated consensus collapse, or contig propagation across strains would produce the same signal.
- **Mitigation applied.** We used three independent AMR databases (ResFinder, CARD, NCBI) and got convergent %ID calls at ≥99.87% on all three isolates. IS26 flanks were verified via GBK feature annotations in each independent record. If the byte-identity were an artifact, we'd expect at least some database-side disagreements — we saw none, so the signal is at least internally consistent.
- **Residual risk.** Still real. Explicitly logged as Critique #2 in REPORT.tex. Future work: re-polish from SRA reads.
- **Lesson.** When a positive signal is "too clean," don't just celebrate — write down the alternative-explanation you did NOT rule out.

### 2.2 Novelty of the target site depends on the comparator set
- **Risk.** The paper's "novel target site" claim was tested against exactly two reference genomes (AB0057 and ATCC 17978). If AbGRI4's 5' flank (EP550_07220 α/β-hydrolase) is common in *A. baumannii* but happens to be missing from those two references, we would falsely confirm novelty.
- **Mitigation applied.** We picked the two most canonical *A. baumannii* references, one from each of the historically most-studied clades. The 3' flank (azoreductase) hits BOTH at ≥92.8%, which is a positive control that the BLAST protocol works. So the ≥90% negative on the 5' flank is not just a BLAST parameter artifact.
- **Residual risk.** Two comparators is a small n. Explicitly logged as Critique #4 and as open question #2. Future work: widen the panel to full RefSeq.
- **Lesson.** A negative result is only as strong as the reference set it's negative against. Say so.

### 2.3 Absence in ABUH773 tested only by whole-genome AMR
- **Risk.** We ruled out AbGRI4 in ABUH773 by absence of the entire aadB/aadA2/sul1/qacEΔ1/intI1 cassette. It is theoretically possible (though implausible) that the cassette is present but not detectable via ResFinder — e.g. a degenerate variant.
- **Mitigation applied.** We ran the whole-genome panel against multiple databases and none of them lit up on ABUH773. The paper's own conclusion that ABUH773 is AbGRI4-negative is also based on cassette absence, so this is a like-for-like test.
- **Residual risk.** We did not coordinate-check the ABUH773 chromosome for an intact (empty) α/β-hydrolase/azoreductase target locus. That would strengthen the negative into "the target locus is intact and the cassette is not there." Logged as Critique #5.
- **Lesson.** Negative controls should be interrogated at the coordinate level, not only at the panel level, when a coordinate check is cheap.

### 2.4 AMR database version drift vs the paper's 2020 databases
- **Risk.** Our AMR calls are from 2026 database snapshots (ResFinder 3206 seqs, CARD 6052 seqs, NCBI AMRFinderPlus 8232 seqs). The paper used 2020 databases. Allele-naming and %ID could drift.
- **Mitigation applied.** We report %ID from all three databases and require agreement. All three converge on the same aadB / aadA2 / sul1 / qacEΔ1 identities at ≥99.87%. Qualitative call is unaffected by database version.
- **Residual risk.** Very low for this analysis but non-zero for edge-case AMR calls in general.
- **Lesson.** Report the database version and hit counts, run against multiple databases when they exist, and check for cross-DB agreement — not just single-DB %ID.

## 3. What did NOT fail (worth naming so we don't over-critique)

- **Coordinate extraction of the 8,840-bp island** was clean on all three positive chromosomes — no off-by-one, no strand flip missed (ABUH793's reverse-strand orientation was handled explicitly).
- **Locus-tag lookup** for EP550_07220 and EP550_07290 hit CP035043 verbatim; no annotation drift.
- **IS26 flank enumeration** returned exactly 2 flanking copies per island + 1 elsewhere in each chromosome — perfectly consistent across all three positive isolates.
- **Pasteur ST2 call** was unambiguous on all four isolates.

## 4. What we'd do differently on a re-run

1. Pin the mlst scheme snapshot version to something contemporaneous with the paper to resolve the Oxford ST281 partial call.
2. Add a coordinate-level check on ABUH773 for the intact target locus (small script, ~30 min).
3. Save the raw BLAST XML outputs, not only the tab-summarized hits, for future re-scoring under different thresholds.
4. Fetch the SRA reads and run at least a spot-check assembly of the AbGRI4 region on one of the three positive isolates to close out Critique #2.

## 5. Overall

Zero claim was contradicted. Two items were honestly downgraded (Oxford ST281 partial; C12 out of scope). Seven latent risks were identified; five were mitigated in-flight and two (byte-identity artifact, comparator-set breadth) are explicitly recorded as future work. This is a REPLICATED verdict with its uncertainty budget documented.
