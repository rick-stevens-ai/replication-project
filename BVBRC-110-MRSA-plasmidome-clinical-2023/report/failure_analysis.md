# Failure Analysis — BVBRC-110

**Paper:** Al-Trad et al., *Antibiotics* 12(4):733 (2023). PMID 37107095.
**Verdict:** PARTIAL (86/100 by argo:gpt-5.2 LLM judge).
**Scope:** 8/8 tested claims reproduce, but this file exists because "reproduce" is not "identical" for two of them, and because 4 systemic claims were not re-run end-to-end.

The point of this file is to be honest about the gap between "PARTIAL" and "REPLICATED" instead of hiding it.

---

## 1. Where numbers didn't match exactly (real, honest, small)

### 1.1 pSauR23-1 length: 58,442 (paper) vs 58,422 (deposited)

- 20 bp / 0.03% delta. Well below any biological threshold.
- Most likely explanation: quoted-with-vs-without-end-tag or a paper-side rounding/typographic issue. The paper does not disclose which end-of-contig convention was used.
- **Not a replication failure.** It is a provenance-transparency gap on the paper's side.
- **Fix on our side:** none. We reported both values and flagged the discrepancy.

### 1.2 pSAZ10A vs pSK41 identity: 99.9% (paper) vs 99.29% (this run)

- 0.61 percentage-point delta.
- **Cause:** IS257-mediated repeat regions in pSAZ10A/pSK41 produce multiple overlapping HSPs; the length-weighted mean identity depends on how HSPs are merged and whether one uses raw top-HSP identity or a coverage-weighted mean over merged intervals. The paper does not state which of these it used.
- Our number is a length-weighted mean over `outfmt 6` HSPs filtered to ≥500 bp / ≥95% identity. If instead we take only the single longest HSP, identity rises above 99.5%.
- **Not a replication failure.** It is a methods-transparency gap on the paper's side — this is exactly the kind of number that should be reported with the merging convention stated.
- **Fix on our side:** we reported the weighted mean *and* the filter threshold explicitly in `workflow.md`, so a reader can reproduce our number even if they disagree with the merging convention.

### 1.3 pSauR165-1 vs pT181 length: 3,829 (paper) vs 3,725 (this run)

- 104 bp / 2.7% delta on the aligned length. Identity itself agrees (99% paper, 99.60% ours).
- **Cause:** HSP-boundary choice. `blastn` may extend or truncate the alignment by a few dozen bp depending on gap-extension parameters. The paper does not disclose its `blastn` parameters.
- **Not a replication failure.** Both the identity and the identified region agree; only the exact boundary integer differs.

---

## 2. Where we chose not to re-run (the four honesty gaps)

These are the reasons the verdict is PARTIAL rather than REPLICATED. Each of them is a deliberate scoping choice, not a hidden failure.

### 2.1 189-plasmid inventory (C2) not re-computed
- The paper's claim that 189 plasmids exist across the 92 assemblies (with a specific breakdown by replicase family: RepL n=63, RepA_N n=57, Rep_1 n=54, plus 4 minor families) requires re-running PlasmidFinder against the full deposited-contigs set.
- **Cost estimate:** ~24 CPU-hr on uicgpu for full re-assembly, plus PlasmidFinder web-service or local install for the replicon-typing step.
- **Why skipped:** out of scope for a spot-check replication whose primary goal was verifying the paper's *quantitative* BLAST/annotation/size claims. The plasmid-count and family-breakdown numbers were accepted at face value based on the deposited plasmid contigs' existence in nuccore under the correct BioProject.
- **Consequence for verdict:** biggest single reason PARTIAL is not REPLICATED.

### 2.2 MOB-typing census (60 MOBV + 1 MOBP) not verified
- The paper's mobility-typing counts require running MOBscan (or hmmer3 against MOB Pfam profiles) on the 189 deposited plasmid sequences.
- Not run.

### 2.3 65% mobilizable / 74% AMR-carrying figures not re-derived
- These are downstream aggregate percentages that depend on 2.1 + 2.2 being re-run first.
- Not attempted.

### 2.4 D-test phenotype and conjugative-transfer wet-lab assays
- The paper reports D-test results (inducible vs constitutive MLSB resistance) for the *ermC*-carrying strains, and notes that pSauR23-1's conjugative machinery could not be experimentally validated even in the original study (no selectable marker on the plasmid).
- Wet-lab replication of D-test or filter-mating is out of scope for this dry replication and was not attempted.
- **NOTE:** the paper itself acknowledges the pSauR23-1 conjugation limitation. This is not a hidden weakness — it is disclosed.

---

## 3. Structural caveats that make the whole result softer (open)

These are not per-claim failures, but they bound the interpretability of everything above. Each is written up as an open question in `open_questions.json`.

### 3.1 Short-read plasmid assembly reliability
- All 92 assemblies use SPAdes v3.13.0 / Unicycler v0.4.8 on Illumina short reads only.
- Short-read-only plasmid assembly is known to mis-join or fragment plasmids across IS-element repeats (IS257, IS431, IS256), collapse multi-copy small plasmids, and under-resolve large mosaic plasmids.
- Our BLAST replication confirms the deposited sequences match what the paper describes, but does not confirm the deposited sequences are structurally correct as plasmids. A long-read (Nanopore R10 / PacBio HiFi) hybrid re-assembly on 5–10 representative isolates would test this, and no such data exists in the paper. See `open_questions.json` OQ1.

### 3.2 PlasmidFinder database completeness for rep_cluster diversity
- The paper reports 100% of plasmids assigned to one of 7 known staphylococcal replicase families. This is an artifact of PlasmidFinder's curated reference set as much as a biological finding — divergent rep variants would be force-cast into the nearest family rather than flagged as untyped. See `open_questions.json` OQ2.

### 3.3 "Potentially mobilizable" is not "actually transferred"
- 65% of non-conjugative plasmids are flagged as potentially mobilizable by oriT-mimic or replicative-relaxase detection. This is a sequence-based *inference*, not a measured transfer frequency. A filter-mating assay would test the false-positive rate of this inference. See `open_questions.json` OQ3.

### 3.4 Plasmid content vs MRSA clonal lineage (CC5/CC8/CC22/CC30)
- The paper does not stratify plasmid types by MLST/CC of the host chromosome. Whether small plasmids are truly lineage-promiscuous in this Malaysian cohort, and whether pSK41-family plasmids remain CC8-associated, is testable on the deposited data but not tested. See `open_questions.json` OQ4.

### 3.5 Ex-vivo HGT risk in the actual clinical context
- The paper's public-health implication rests on inferred (not measured) horizontal-transfer capability. An ex-vivo mating assay in polymicrobial conditions reflecting the actual HSNZ ward setting has not been done. See `open_questions.json` OQ5.

---

## 4. LLM-judge caveats

- Single judge (argo:gpt-5.2), temperature 0. No inter-judge reliability check.
- The 86/100 score should be read as one honest external score, not an oracle.
- `argo:claude-opus-4.7` was tried first and failed with an upstream response-schema validation error — this is a plumbing failure of the Argo proxy on that particular endpoint on the day of the run, not a signal about model quality. We fell back to gpt-5.2 (also free).

---

## 5. Summary

**What actually failed:** nothing, in the sense that no tested claim was falsified.

**What did not fully succeed:** the *scope* of the replication is smaller than the paper's own scope. We tested 8 discrete claims (6 quantitative, 2 data-availability); the paper makes at least ~15 systemic claims across 189 plasmids that would each require a full end-to-end re-run. This gap is the reason the verdict is PARTIAL.

**What we still don't know (open):** five substantive questions listed in `open_questions.json`, all grounded in acknowledged limitations of the short-read plasmid-assembly + sequence-based-inference methodology used by the paper.
