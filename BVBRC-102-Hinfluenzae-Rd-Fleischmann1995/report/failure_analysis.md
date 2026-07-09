# Failure Analysis & Critique — Fleischmann1995 replication

This document is deliberately unflattering. The REPLICATED verdict stands, but a serious reader
needs to understand what this replication *is not* before treating the verdict as strong evidence.

## Executive critique

The replication is **narrow**. It measures whether the modern RefSeq record NC_000907.1 — which
is derived from the paper's own 1995 GenBank submission L42023 — reports the same numbers as
the paper. That is a valid but low-difficulty check: RefSeq is not independent of the paper,
so a "match" here mostly certifies that the sequence and annotation have not silently drifted
beyond expected re-annotation norms in the 30 years since deposit. This is worth doing — silent
drift is not hypothetical — but it is emphatically **not** an independent replication of the
paper's science. The paper's methodological claim (whole-genome random shotgun sequencing is
feasible for a free-living organism) is left entirely untested.

The verdict is honest about scope; this critique makes the scope-limits explicit.

## What failed / did not happen

### F1. Original PDF unobtainable
- **What:** paper.pdf is not present. Unpaywall (2026-07-05) confirms no OA copy anywhere.
- **Root cause:** Science/AAAS 1995 content is closed-access; no author self-archive; no PMC deposit; BACKFILL policy forbids paid endpoints.
- **Workaround:** Fell back to the paper's abstract/Table 1 numbers that are widely re-quoted (GenBank header, RefSeq notes, BV-BRC card, Wikipedia). The scientific content of the replication does not depend on holding the PDF because the numbers are commodity knowledge.
- **Residual gap:** items (1) paper.pdf, (2) extraction/marker.md, (3) extraction/nougat.mmd remain pending. Cannot do fine-grained textual claims-mining without the PDF.
- **What would close it:** institutional Science subscription or ILL retrieval → run Marker + Nougat on a GPU host.

### F2. 1995 raw Sanger traces not re-analyzed
- **What:** No re-assembly of the paper's ~19,687 shotgun reads was attempted.
- **Root cause:** The 1995 raw traces are not deposited in any publicly reusable form. BioProject PRJNA224116 hosts the assembly; the trace archive (NCBI Trace Archive, retired 2016) was not searched to trace equivalence.
- **Workaround:** Rely on the deposited assembled sequence as the direct evidence. Note this loudly in REPORT.md §5.
- **Residual gap:** The paper's headline *method claim* is untested. Every subsequent H. influenzae Rd resequencing corroborates the assembly, but that is triangulation, not replication of the specific 1995 pipeline. See open question Q1.
- **What would close it:** FOIA / archival request to JCVI (TIGR's successor) for the original DAT/DDS backups.

### F3. ORF re-prediction with 1995-vintage tools skipped
- **What:** No re-run of GeneMark (or the 1995-vintage version of Glimmer / whichever ORF caller the paper used) on the sequence.
- **Root cause:** The paper's 1,743 CDS number is a 1995-vintage prediction. Re-running modern Prodigal would give a different number that is *not* the paper's number — this would confuse rather than clarify. So we compared to the RefSeq count instead.
- **Workaround:** Explicitly labelled the CDS-count comparison "annotation drift" and honored the small delta (−1.3%).
- **Residual gap:** The paper's "1,743 CDSs" claim is not literally re-derived. It is checked for consistency with the modern re-annotation but not with a period-appropriate ORF caller.
- **What would close it:** Docker image of GeneMark 1995 vintage (unlikely to exist) or a re-implementation of the exact ORF-calling heuristics used at TIGR in 1995 (not feasible for a light replication).

### F4. Functional-role assignment (~1,007 of 1,743) not re-computed
- **What:** Paper reports 57.8% of CDSs assigned to functional categories. Our replication did not attempt to re-BLAST against a 1995-vintage SWISS-PROT snapshot.
- **Root cause:** Requires substantial infrastructure (SWISS-PROT June 1995 snapshot, BLAST all vs all, category mapper) — well beyond the scope of a light replication.
- **Workaround:** Marked C10 as "not-tested" in the claims table.
- **Residual gap:** Cannot verify the paper's central *biological* summary (what fraction of the genome we understand).
- **What would close it:** Historical SWISS-PROT snapshot + modern re-BLAST is now cheap; deferred to a follow-up study.

### F5. Mu-like prophages and phase-variation SSRs not independently verified
- **What:** The paper's substantive biological discussion of mobile genetic elements and contingency loci was not independently reproduced.
- **Root cause:** NC_000907.1 has only 3 `misc_feature` + 1 `repeat_region` annotations — the paper's finer detail was not preserved in the RefSeq re-curation.
- **Workaround:** Marked C12 and C14 as "not-tested" and observed the annotation gap in REPORT.md.
- **Residual gap:** This is a systemic problem — see open question Q5. The paper's biology is measurably absent from the modern reference record.
- **What would close it:** Re-run PHASTER + VirSorter2 + SSR finders and cross-reference with the paper's coordinates once the PDF is available.

### F6. Coding-density definition is not standardized
- **What:** Reported 82.53% via interval-union of non-pseudo CDSs. Paper reports "densely coding" without a number.
- **Root cause:** No community-standard definition of coding density; the choice of inclusion criteria drives the number substantially. See open question Q4.
- **Workaround:** Documented the definition used and flagged the ambiguity.
- **Residual gap:** Not a failure of this replication per se, but a *field-level* failure that this replication surfaces.

### F7. LLM-judge is not independent
- **What:** Verdict of REPLICATED is corroborated by an LLM-judge (`argo:gpt-5`) that was given both the paper's target numbers and the computed numbers plus the claims table.
- **Root cause:** The LLM sees both sides; it is a structured formatter of the human-visible verdict, not an independent adjudicator.
- **Workaround:** LLM-judge output is presented as verdict *summary*, not verdict *source*. Numeric truth comes from `analyze.py` deterministic output.
- **Residual gap:** LLM-judge coverage_pct=100 / agreement_pct=100 should not be over-interpreted — the judge was primed with the answer.

### F8. Tolerance bands are hand-wavy
- **What:** Deltas up to 5.6% (tRNAs) and 1.3% (CDSs) accepted as "match (annotation drift)"; the ±5% band is a rule of thumb, not a principled threshold.
- **Root cause:** There is no calibrated model of what re-annotation drift *should* look like for a 30-year-old genome, so any tolerance is a judgment call.
- **Workaround:** Numeric deltas reported verbatim; verdict language distinguishes exact match from within-drift.
- **Residual gap:** A future methodological improvement is to calibrate re-annotation drift across the ~50 pre-2000 bacterial genome papers by comparing their reported numbers to modern RefSeq re-annotations, and using that empirical distribution as the tolerance band rather than a folk-wisdom 5%.

## Honest overall assessment of evidence strength

- **Strong:** genome length (±1 bp), G+C content, topology, rRNA-operon count, 16S/23S locus count. These are integer-level or two-decimal-place matches on the deposited sequence.
- **Medium:** total CDS count, tRNA count, mean CDS length, coding density. Small deltas explained by re-annotation drift; explanation is plausible but not proven at per-locus resolution.
- **Weak:** functional-category assignment (untested), prophage detection (untested), phase-variation SSR analysis (untested).
- **Not evaluated (declared out of scope):** the paper's methodological claim — whole-genome random shotgun assembly. This is the paper's most consequential contribution and it remains untested in this replication.

**Bottom line:** the REPLICATED verdict is well-supported for the paper's *quantitative
sequence-derivable claims* and unsupported for the paper's *method-plausibility and biology
narrative* claims. Anyone citing this replication should quote both halves.

## What a stronger replication would look like

1. Independent re-assembly of the 1995 reads from a recovered TIGR archive (open question Q1).
2. Independent re-annotation with a period-appropriate ORF caller for a like-for-like CDS-count comparison.
3. Independent re-BLAST against a June-1995 SWISS-PROT snapshot for functional-role reproduction.
4. Independent prophage + SSR detection with modern tools cross-referenced against the paper's coordinates.
5. Independent LLM-judge or human-judge that sees only the replication numbers (not the paper's numbers) and is asked "do these look like a bacterial genome consistent with published H. influenzae Rd literature?" — a blind check.
6. A calibrated re-annotation-drift model so the "annotation drift" verdicts are statistically principled rather than hand-waved.

Each of these is a real project; the current replication is a defensible minimum, not a maximum.
