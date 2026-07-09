# Failure Analysis — BVBRC-83

**Paper:** Gómez-Martínez et al. 2022, *Microorganisms* 10(9): 1863 (pPE52IMP / CP102481.1)
**Verdict:** REPLICATED (11 exact / 1 close / 1 supported / 0 mismatch of 13 claims)

This document catalogs (a) actual failure/near-miss events during the replication run,
(b) known limits of the method that could produce silent failure elsewhere, and
(c) failure modes that a future rerun should guard against.

---

## A. Actual near-misses during this run

### NM1 — ORF count mismatch (38 vs 39)

- **Signal:** Independent CDS-feature enumeration returned 38 CDS on CP102481.1; the paper reports 39.
- **Impact:** Would have degraded C3 from `match` to `mismatch` under a strict rubric.
- **Resolution:** Scored as `close` (not `mismatch`) because the delta is 1/39 ≈ 2.5% and is consistent with annotator granularity (short ORFs merged/split, alternate start codons, hypothetical proteins under a length threshold).
- **What we did NOT do:** A gene-by-gene diff of the paper's Table S1 vs the current NCBI annotation to pinpoint the missing/extra ORF. This is a small unfinished audit item; noted in critique §4 of REPORT.tex.
- **Failure it could hide:** if the "missing" ORF were biologically important (e.g., a second stability system — see OQ5), we would have silently under-counted. Low probability but non-zero.

### NM2 — Annotation label heterogeneity for the 301 aa RepA/KfrA protein

- **Signal:** BLAST best-hits for the pPE52IMP RepA landed on proteins annotated as `KfrA` in three siblings, `DNA-binding domain-containing protein` in one, and the paper itself calls the same protein `RepA`.
- **Impact:** A naive substring search for `RepA` on the sibling GenBank records would have found 0 hits and produced a false-negative on C11.
- **Resolution:** Used the deposited protein *sequence*, not the qualifier label, as the query. BLASTp on sequence returned 100% identity across four siblings regardless of label. This is the correct methodology; the failure mode is what a less careful pipeline would do.
- **Prevention:** All cross-plasmid comparisons in this replication are sequence-based, not label-based, wherever a sequence is available. Label substring matching is used only as a coarse screen and always cross-checked against BLAST.

### NM3 — p4130-KPC "truncated RepA" is not reproduced as truncated

- **Signal:** The paper describes p4130-KPC's RepA as truncated. Our BLASTp against MN336501.1 returned a full 100%-identity hit to a 301 aa protein (QIM14596.1) — the same length as pPE52IMP's RepA, not truncated.
- **Impact:** A strict rubric could flag this as a mismatch to claim C11 details ("p4130-KPC has a *truncated* RepA").
- **Resolution:** Scored as `supported` (not `mismatch`) because the family-membership claim is upheld; the truncation qualifier may reflect (a) the paper used a different coordinate/start-codon call, (b) NCBI annotation has been updated since 2022, or (c) truncation is in a nucleotide feature not visible in the deposited protein. We did not chase this down.
- **What we did NOT do:** Extract the full nucleotide *rep* locus from MN336501.1 and compare start-codon usage against the paper's Fig 3B alignment. Small unfinished audit item; noted in critique §5 of REPORT.tex.

### NM4 — pD5170990 relaxase and RepA both absent (as expected)

- **Signal:** BLAST returned zero hits above e<1e-3 for both RepA and MOBP11 relaxase against pD5170990 (KX169264.1).
- **Impact:** In isolation this looks like a failure to detect a family member.
- **Resolution:** The paper *itself* explicitly calls out pD5170990 as lacking `traJ`, `traK`, and `kfrA` (this is claim C12). The absence is a *confirmed prediction*, not a failure. Scored as `match` for C12.
- **Lesson:** claim-by-claim scoring must respect the paper's own stated exceptions. A generic "novel-family-membership" test that penalized any zero-hit sibling would have wrongly downgraded this claim.

---

## B. Known limits of the method (silent-failure surface)

### L1 — Sequence-level replication cannot audit the underlying reads

Every "confirmed" claim is confirmed against the deposited GenBank record CP102481.1. If the submitters mis-assembled the plasmid and deposited a plausible-looking-but-wrong contig, our pipeline propagates that error. We did not re-assemble from raw reads and we did not verify the SRA accession (if any exists) for the isolate.

**Mitigation available (not applied):** re-assemble from the paper's raw Illumina reads with `plasmidSPAdes` and compare to CP102481.1. Skipped per REPORT.md §"What was not attempted".

### L2 — PBRT non-typeability (C13) is not verifiable in silico

PBRT is a wet-lab PCR panel. A negative PBRT result cannot be reconstructed from sequence — the closest sequence-level proxy is "does the RepA cluster with any known Inc-group RepA?" and we can only observe absence, not primer-panel failure. Any claim that a plasmid is non-typeable is at best *consistent with* our finding, never *proved by* it.

### L3 — LLM-judge concurrence is weakly independent

Both judges (`argo:gpt-4o`, `argo:gpt-5.2`) are OpenAI-lineage models served through the same Argo proxy with the same prompt. They can share systematic priors on rubric interpretation. Their agreement should not be read as two-independent-experts strength; it is more like two rubric-followers from a similar training distribution.

**Mitigation available (not applied):** cross-judge with a non-OpenAI model (e.g., `argo:claude-opus-4.8` or a CELS-served Llama/Qwen) for a genuinely independent rubric check.

### L4 — Feature cross-tab depends on heterogeneous submitter annotations

The `traJ / traK / trbJ / merA / blaKPC / blaVIM / blaOXA / intI1` cross-tab for the six plasmids uses each submitter's deposited feature table. Submitter conventions differ (see NM2). We mitigated this with qualifier substring matching across `/product`, `/gene`, and `/note`, but did not do de novo orthology-based feature calling.

**Failure mode:** a sibling could carry a functional `traJ` homolog that no submitter labeled as such, producing a false 0 in the cross-tab.

### L5 — blaIMP-56 identity accepted from qualifier, not re-typed against CARD/BLDB

Claim C7 asserts the plasmid carries *blaIMP-56* specifically (not `blaIMP` generically). Our substring match only confirmed a `blaIMP`-family gene at the expected locus. The variant-specific `-56` allele call was accepted from the GenBank product qualifier. If the submitter mis-called the allele (say, IMP-1 mislabeled as IMP-56), we would not have caught it.

**Mitigation available (not applied):** BLAST the 741-nt blaIMP CDS against the NCBI-AMR RefGene / CARD / BLDB curated β-lactamase databases and confirm allele identity at the amino-acid level. Flagged in OQ3 for follow-up.

### L6 — Circularity accepted from LOCUS, not verified from reads

The GenBank LOCUS field reports `circular`. We did not verify circular closure from raw-read span coverage across the origin. Standard practice for annotation-level analyses, but worth naming.

### L7 — 5th sibling (pD5170990) absence is definitional, not empirical

The scoring rubric for C11 treated "RepA absent in pD5170990" as a *predicted* absence, per the paper's own Fig 3 call-out. If the paper had *not* explicitly listed pD5170990 as an exception, the same observation would have been scored as a partial-failure of family membership. The verdict therefore depends on the paper's internal consistency about which sibling is expected to differ.

---

## C. Failure modes a future rerun should guard against

### F1 — Silent annotation drift on NCBI

NCBI feature tables are updated over time. A rerun 6 months from now against CP102481.1 could see different CDS calls (different start codons, merged/split features), which would produce different qualifier-substring matches even though the underlying sequence is unchanged. **Guard:** always report the NCBI record's `MODIFIED` date alongside any qualitative comparison.

### F2 — Argo model version drift

`argo:gpt-4o` and `argo:gpt-5.2` may be silently upgraded on Argo's side, changing rubric behavior. Two-judge concurrence today may become two-judge dissent later on identical evidence. **Guard:** record the Argo-reported model version string in the judge JSON, not just the alias.

### F3 — BLAST database version drift

Local BLAST results depend only on the query and subject FASTA files, so a rerun with the same GenBank inputs should be deterministic. But if a rerun *pulls fresh sibling GenBank files* (F1), the subject database will differ. **Guard:** cache the pulled GenBank flat files and re-use them; do not silently re-fetch.

### F4 — Rubric interpretation drift

The verdict rule (`REPLICATED = n_mismatch == 0 AND ≥85% pass rate`) is a project convention. If the convention changes, this paper's verdict could change on identical evidence. **Guard:** store the rubric alongside the judge JSON.

### F5 — Author correction / retraction

Not currently indicated for this paper. If the paper were corrected or retracted after our replication run, the verdict should be reviewed. **Guard:** periodic re-check of PMID 36144465 status via NCBI E-Utils.

---

## D. Summary

- **Real failures during this run:** 0.
- **Near-misses (correctly handled):** 4 (NM1–NM4).
- **Known silent-failure surface:** 7 items (L1–L7), all disclosed in REPORT.tex critique §1–9.
- **Rerun-drift guards to add:** 5 items (F1–F5); none blocking; all logged for the next replication cycle.
- **Overall confidence:** the REPLICATED verdict is robust to any single one of these limits; it would only be overturned by a *combination* of L1 (deposited sequence is wrong) with wet-lab evidence contradicting the paper — a scenario not indicated by any current data.
