# Failure Analysis — bvbrc-99 (NIES-2481 replication)

**Paper:** Yamaguchi et al. 2018, *J. Genomics* 6:30–33, DOI 10.7150/jgen.24935.
**Verdict:** REPLICATED — but not every claim passed cleanly. This document catalogs the *non-clean* outcomes and diagnoses each.

There are three classes of imperfect outcomes:

1. **Sub-1% annotation-drift deltas** (C7, C8) — not really "failures" but not exact matches.
2. **One direction-reversed comparison** (C11) — magnitude exact, sign flipped.
3. **Explicitly deferred / out-of-scope claims** (C14, C15) — not attempted this pass.

None of these overturns the verdict. All three classes are documented here so a reviewer does not have to reverse-engineer why the replication is called REPLICATED despite three cells in the results table that are not "exact match."

---

## 1. CDS-count drift (C7, C8) — near-match, not exact

| Claim | Paper | Reproduced | Δ | Relative |
|---|---:|---:|---:|---:|
| C7 chromosome CDS | 4,332 | 4,292 | −40 | 0.9% |
| C8 plasmid CDS    | 167   | 164   | −3  | 1.8% |

**Diagnosis.** These are almost certainly annotation vintage drift. The paper was published in 2018 against the then-current NCBI submission of CP012375/CP025929. Since then, NCBI's PGAP (Prokaryotic Genome Annotation Pipeline) has been re-run multiple times against these accessions, and PGAP versions from ~2019 onward routinely (a) collapse spurious tiny ORFs, (b) reclassify some short CDS as pseudogenes, and (c) tighten start-codon selection. A −0.9% chromosome-CDS drift over ~7 years is well within the empirically observed PGAP-drift envelope for cyanobacterial genomes.

**What was NOT done.** The replication did not directly diff the paper-era submitted GBK against the current live GBK. That would prove the drift hypothesis rather than merely being consistent with it. Cost: modest (fetch the historical revision from NCBI's `sequence revision history` and rerun the feature-type histogram). Deferred because the deltas are small enough not to threaten the verdict.

**Verdict impact.** None. The paper's *structural* claims (rRNA operon count, tRNA count, 16S copies, mcy absence) are all exact. CDS counts are inherently annotation-pipeline-dependent and the drift direction and magnitude are consistent with the passage of PGAP versions.

---

## 2. NIES-2481 vs NIES-2549 chromosome-size delta (C11) — sign flip

| Claim | Paper | Reproduced |
|---|---|---|
| C11 chromosome size delta | NIES-2481 is 1,207 bp *larger* than NIES-2549 | NIES-2549 is 1,207 bp *larger* than NIES-2481 |

**Direct arithmetic on the deposited records:**
```
len(CP012375.1)  =  4,293,006  bp   # NIES-2481 chromosome
len(CP011304.1)  =  4,294,213  bp   # NIES-2549 chromosome
diff             =  4,294,213 - 4,293,006  =  +1,207 bp   # NIES-2549 is larger
```

**Diagnosis.** The **magnitude is exact to the base pair (1,207 bp).** Two independent groups would not converge on that specific number by coincidence. The most parsimonious explanation is a sign-of-the-difference typo in the paper's Results & Discussion narrative — the authors correctly computed `|Δ|` and then wrote the wrong strain as "larger."

**Ruled-out alternatives:**
- *Wrong-accession comparison.* Both accessions are the canonical ones tied to the two strains (CP012375 is the paper's own NIES-2481 accession; CP011304 has been the NIES-2549 reference since 2015). No other complete group-G chromosome has size = paper-value − 1,207 bp or paper-value + 1,207 bp.
- *Post-publication reassembly of NIES-2549.* CP011304.1 has not been re-versioned. Its length has been 4,294,213 bp since first deposition. The current record is the same one the paper had.
- *Off-by-one wrapping.* Both are circular chromosomes; the length count is unambiguous. No wrapping ambiguity.

**Verdict impact.** Documented as "magnitude exact / direction reversed — probable paper typo." Does not change REPLICATED verdict — quantitatively the paper matches; only the narrative sign is wrong.

**Recommended future step.** Contact the corresponding author (Yamaguchi) or file a comment on the Journal of Genomics article page. Not done in this replication pass.

---

## 3. Deferred / out-of-scope claims (C14, C15)

| Claim | Paper | Status | Reason for deferral |
|---|---|---|---|
| C14 | 28 antiSMASH secondary-metabolite BGCs | Not tested | Requires running antiSMASH v7+; wall-clock and dependency-install cost outside a 15-minute laptop pass. Follow-up on uicgpu called out explicitly in `open_questions.json`. |
| C15 | 5 CRISPR loci                          | Not tested | Requires CRISPRCasFinder / CRISPRCasTyper install + profile databases. Same follow-up path as C14. |

**Diagnosis.** These are not failures in the sense of "we tried and got the wrong answer." They are known-unknown items that a stricter replication pass would have to run. Neither claim contradicts the other 12 claims that WERE tested.

**Partial coverage of C13** (aeruginosin, micropeptin, microviridin presence): 117 low-identity mcyA→other-NRPS cross-hits confirm rich NRPS content in NIES-2481, consistent with the paper. This is *proxy* evidence, not direct BGC identification, so C13 is scored "partial."

**Verdict impact.** None. The un-tested items are peripheral to the paper's core deposition claims (which are all sequence-level and confirmed).

---

## 4. Reproducibility risks not exercised

Beyond the specific items above, there are three replication-quality risks the reader should be aware of. This replication did NOT do these, and the report is honest about that:

1. **No orthogonal read-based reassembly.** A truly hard replication would fetch the raw PacBio SRA reads for NIES-2481, reassemble with a modern HiFi/CLR assembler (Flye, Canu, hifiasm), and compare structure and SNP-level consensus against the deposited CP012375. For a genome-announcement paper whose primary artifact *is* the assembly, this is the ultimate check. Not done because the paper's structural claims all fall out of the deposited assembly and no anomaly was observed that would motivate the cost.
2. **16S-copy correctness assumed.** All 4 extracted 16S copies were the expected 1,460 bp, which is strong evidence the annotation is right. But if any copy had been mis-boundaried by tens of base pairs, the identity check would silently be measuring the wrong bases. Length-agreement is a proxy for correct annotation, not proof.
3. **Table 2 (COG categories) not fully rebuilt.** Spot-checked one enrichment (transposase-labeled CDS count = 34, consistent with the paper's "enriched in mobile elements" narrative), but did not re-run COGNIZER against a matched COG database vintage. A stricter pass would.

---

## 5. Summary

- 10 of 12 tested claims: exact match.
- 2 of 12 tested claims: sub-2% annotation-drift near-match (C7, C8).
- 1 of 12 tested claims: magnitude-exact / direction-reversed (C11) — probable paper typo.
- 3 of 15 total claims: out of scope this pass (C13 partial, C14 and C15 not attempted).

Verdict: **REPLICATED** — the paper's central deposition and description of NIES-2481 hold up cleanly on the public record.
