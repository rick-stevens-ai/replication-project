# Failure Analysis — BVBRC-73 (Rahman 2023, MDR *A. veronii* Alim_AV_1000)

Overall verdict: **PARTIAL** (4/4 unanimous free LLM judges: gpt-5.2, claude-sonnet-4.5, gemini-2.5-pro, gpt-4.1). This document itemises the four claims that did *not* cleanly replicate and diagnoses each.

---

## F1. MLST ST 492 (C7) — **CONTRADICTED** (categorical mismatch)

**Paper claim:** Alim_AV_1000 is MLST sequence type **ST 492**.

**Observation:** PubMLST REST API scan of the deposited assembly (`GCF_026738955.1`) against scheme 1 (Aeromonas 6-locus MLST) returned:

| Locus | Match | Observed | ST 492 canonical |
|-------|-------|---------:|-----------------:|
| gyrB | exact  | 633   | 112 |
| groL | exact  | 91    | 347 |
| gltA | exact  | 340   | 44  |
| metG | exact  | 124   | 217 |
| ppsA | partial | best-match allele 627 at 99.44% id, 3 mismatches, 0 gaps — probable **new allele** | 384 |
| recA | exact  | 1460  | 381 |

None of the observed alleles is an ST 492 allele. Searching all **2,755** STs currently in the PubMLST profile table returns no match; the closest STs share only one locus of six.

**Diagnosis (3 hypotheses, none exonerates the paper's specific claim):**
1. **Reporting error by the paper.** Simple mistype / wrong output copied. Consistent with the fact that four of six loci returned entirely different allele IDs, not near-neighbours.
2. **Wrong genome typed.** The paper's typing may have been run on a different in-house assembly or unpolished read set that was never deposited under GCF_026738955.1. But the deposited assembly's size (4,494,464 bp vs. paper's 4,494,515), GC (58.87% exact), and contig count (93 exact) match essentially to the base, so the deposited genome is almost certainly the paper's genome.
3. **PubMLST renumbering.** The Aeromonas scheme has grown from ~800 STs in 2018 to 2,755 today. Renumbering can move ST IDs, but it does not cleanly reassign four exact allele IDs to entirely different numbers; it would show up as incremental drift, not categorical mismatch at every locus.

**Not a database-version artefact.** This is a real disagreement. The paper's ST 492 claim, and any epidemiological argument built on ST 492, should be treated as suspect until the authors rerun PubMLST on the deposited assembly.

---

## F2. Tetracycline resistance gene (part of C10) — **NOT REPLICATED at default thresholds**

**Paper claim:** Alim_AV_1000 carries resistance genes to β-lactams **and tetracyclines** (paper text mentions "the sequence of several antibiotic-resistant genes (ampicillin, tetracycline, [others])").

**Observation:** Our 5-way abricate sweep (CARD, NCBI-AMR, ResFinder, ARGannot, MEGARes; all DBs dated 2026-Jul-03) returned **no tet-family gene** passing default thresholds (typically 80% identity, 80% coverage). The β-lactam side replicates cleanly (OXA-12 at 97.59% id, cphA4 at 96.19% id, plus the MDR-efflux regulator rsmA at 81.06% partial-length).

**Diagnosis (3 non-mutually-exclusive causes):**
1. **Gene renaming or reclassification.** A tet-family gene that was present in CARD/ResFinder in 2023 may have been merged, deprecated, or renamed since. This is common in rapidly curated AMR databases.
2. **Sub-threshold call.** The paper's tet gene may have been detected at lower identity / coverage than current default abricate thresholds. Lowering thresholds could recover it, but at the cost of specificity.
3. **Phenotype without a canonical tet gene.** The paper's Table 3 phenotypic tet resistance could reflect efflux (e.g. the observed rsmA MDR-efflux regulator activity) or an outer-membrane permeability change rather than a specific tet-family determinant.

**Impact on the paper's overall MDR claim:** limited. The qualitative "multidrug-resistant" characterisation is still defensible from the observed OXA-12 + cphA4 + rsmA combination. Only the specific tet gene sub-claim is unsupported at current defaults.

---

## F3. CDS count (C4) and tRNA count (C5) — **PARTIAL (within expected caller drift)**

**Paper claim:** 4,229 CDS and 102 tRNA (both from RAST).

**Observation:** Prodigal V2.60 returned 4,063 CDS (closed) / 4,108 CDS (open-ended) — 2.9% to 3.9% below the paper's RAST count. Aragorn returned 96 tRNA — 5.9% below paper's 102.

**Diagnosis:** This is *inter-caller drift*, not disagreement.
- RAST uses SEED + FIGfam + tRNAscan-SE, with permissive short-ORF calling — systematically higher CDS counts than Prodigal.
- tRNAscan-SE and Aragorn use different scoring models and can differ by 5-10% on the same genome.
- Neither of these is a scientific replication failure; they are pipeline-choice differences. To score them "exactly", one would rerun the paper's original RAST + tRNAscan-SE pipeline on the deposited assembly. We did not.

**Impact:** minor. Would be resolved to REPLICATED with a matched pipeline; scored PARTIAL for methodological transparency.

---

## F4. Phage regions (C12) — **SPOT-CHECK ONLY (external service failure)**

**Paper claim:** PHASTER identified 2 intact + 1 incomplete phage region.

**Observation:** `phaster.ca` API rejected our POST with broken pipe on the 4.5 MB submission. We could not independently rerun PHASTER.

**Diagnosis:** Third-party web-service fragility. phaster.ca is an unmaintained academic service that periodically drops large uploads. This is a classic reproducibility risk: a reported analysis pipeline depended on an external service that is not guaranteed to remain available.

**Impact / mitigation:** methodology is standard. To close this claim, one would rerun with a local PHASTER-family tool (PHASTEST, PhiSpy, VirSorter2). We did not attempt this.

---

## F5. Wet-lab AST (C13) — **NOT TESTABLE from a genome rerun**

**Paper claim:** Wet-lab disc-diffusion AST phenotype (paper Table 3).

**Observation:** Requires live cultures; cannot be rerun from a public assembly.

**Diagnosis / impact:** out of scope for a genome replication. Documented, not counted against the paper.

---

## Judge-stage failures (not paper claims)

Two Argo judges (`argo:claude-opus-4.7` and `argo:claude-opus-4.8`) returned upstream 502 with a message-parse validation error — an Argo-proxy bug, unrelated to our request or the paper. We substituted three additional free judges (sonnet-4.5, gemini-2.5-pro, gpt-4.1) to preserve four independent judges. All four remaining judges returned PARTIAL.

---

## Summary of failure modes

| Class | Claims |
|-------|--------|
| **Contradicted** (definite paper disagreement) | C7 (MLST ST 492) |
| **Partial — real gap** (paper claim not supported at defaults) | C10 tetracycline sub-claim |
| **Partial — pipeline drift** (would resolve with matched tools) | C4 CDS, C5 tRNA |
| **Untestable — external service down** | C12 (PHASTER) |
| **Untestable — wet-lab** | C13 (AST) |
| **Replicated** | C1, C2, C3, C6, C8, C9, C11, plus β-lactam part of C10 |

**Bottom line:** the paper's assembly and comparative-genomics story survives replication; its specific MLST ST assignment does not; its qualitative MDR characterisation survives but the tetracycline-specific sub-claim does not at current thresholds; annotation-count numbers differ within known caller drift.
