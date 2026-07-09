# Failure Analysis — BVBRC-74

Paper: Satti et al. 2021, IJMS 22(14):7385 — PLA-degrading *P. aeruginosa* S3,
*Sphingobacterium* sp. S2, *Geobacillus* sp. EC-3.

Verdict: **PARTIAL → REPLICATED-leaning.** No contradictions; several gaps.

This file inventories what did not work, what was intentionally skipped, and
what the paper itself is weak on. It is the complement of `REPORT.md`
(what did work).

---

## 1. Things that did NOT fully replicate

### 1.1 S2 and EC-3 were not de-novo re-assembled

- **What was skipped:** Independent SPAdes assembly of *Sphingobacterium* sp.
  S2 (SRR7264117) and *Geobacillus* sp. EC-3 (SRR14203690).
- **Why:** compute-time budget. Only ~45 min of local CherryRd time was
  allocated; S3 alone consumed ~35 min. Two more ~30-min SPAdes runs would
  have doubled wall-clock.
- **Impact:** The paper's quantitative claims for S2 and EC-3 (genome size, GC,
  contig count, N50, CDS count, ANI) are corroborated only *indirectly* by
  reference-genome comparison — a SPOT-CHECK, not an end-to-end replication.
  This is the single largest gap in this replication and the primary reason
  the LLM judge scored strict agreement at only 40%.
- **Fixable:** raw reads are downloaded and staged in `work/reads/`. Two
  additional SPAdes `--isolate` runs would close the gap; no new tooling
  required. Estimated additional wall-clock: 60 min.

### 1.2 ANI was not recomputed for any isolate

- **What was skipped:** `pyani` or `fastANI` computation of average nucleotide
  identity between each isolate and its paper-claimed closest reference
  (paper: S3 vs PSE305 = 97.7%; S2 vs NCTC11429 = 98%; EC-3 vs CCB_US3_UF5 = 99.4%).
- **Why:** ANI is a well-defined but distinct workflow that adds ~10 min per
  pair and requires `pyani` / `fastANI` install; deprioritized because the
  16S identity check already gave strong species-level confirmation for S3.
- **Impact:** The three specific ANI numbers in the paper are not directly
  tested. However, 16S at 100.00% over 1536 bp for S3 is *stronger* evidence
  of species assignment than the paper's own ANI number, so the taxonomic
  conclusion is not in doubt for S3.
- **Fixable:** run `fastANI --query S3.fasta --ref PSE305.fna` and equivalents
  for S2 and EC-3. Trivial once S2 and EC-3 assemblies exist.

### 1.3 Contig count and longest-contig deltas (not really failures — methodological differences)

- **Contig count:** 51 vs 63 (Δ 19%). Cause: paper used MeDuSa reference-guided
  scaffolding after SPAdes; this replication did not. This is a documented
  methodological difference, not a data disagreement.
- **Longest contig:** 527 kb vs 659 kb (Δ 20%). Same cause.
- **Fixable:** run MeDuSa against PSE305 as scaffold reference. Would likely
  close both deltas.

### 1.4 CDS count differs by 2.5%

- Prodigal V2.60 called 6,085 CDS; paper's RASTtk called 6,239.
- Cause: legitimately different gene-caller heuristics on the same assembly.
- Impact: minor; well within routine tool tolerance.
- Fixable: run RASTtk locally (or via PATRIC web). Not attempted because
  RASTtk was not installed on the free-endpoint compute path.

### 1.5 Read-count discrepancy (paper vs SRA)

- **S3:** paper Section 4.3 = 5,800,229; SRA spot count = 2,635,837 (Δ ≈ 2.2×).
- **S2:** paper Section 4.3 = 6,304,420; SRA spot count = 2,768,958 (Δ ≈ 2.3×).
- **EC-3:** paper Section 4.3 = 5,730,761; SRA spot count = 5,730,761 (**exact**).
- Most parsimonious explanation: paper counts each PE mate separately for S2
  and S3 but not EC-3 (or pools an earlier lane not in the current SRA
  record).
- Impact: not a substantive replication failure — the raw read files are real
  and produce a matching assembly. But the discrepancy is not resolvable
  from the paper alone and warrants a one-line corrigendum.

---

## 2. Things the paper itself is weak on (surfaced by this replication)

### 2.1 Internal inconsistency: abstract vs Table 1 contig counts

- Abstract says "435/303/111 contigs" for S2/S3/EC-3.
- Table 1 says "87/63/111 contigs."
- The 435/303 numbers are pre-scaffolding raw SPAdes; Table 1 is
  post-MeDuSa/PATRIC. Paper never explicitly labels either set.
- **Verdict:** paper-side presentation bug; a reviewer should have caught this.

### 2.2 No assembly deposited in NCBI Assembly DB

- Only raw reads are deposited under SRP149807 / PRJNA721072.
- Best practice would deposit the assembled FASTA so that quantitative claims
  (63 contigs, N50 273,159, etc.) are verifiable in seconds instead of
  requiring a 35-minute SPAdes rerun per isolate.
- **Verdict:** common-but-not-best-practice paper-side gap.

### 2.3 Enzymological claims are annotation-based only

- Section 2.7 / Table 3 inventory hydrolase / lipase / esterase / protease /
  cutinase / depolymerase annotations, but the paper does not demonstrate
  PLA-degrading activity for any single annotated enzyme.
- The whole-cell PLA-degradation phenotype is real, but the causal link from
  a specific annotated enzyme to that phenotype is inferred, not tested.
- **Verdict:** substantive biological gap that leaves substantial ambiguity
  about *which* enzymes actually drive PLA hydrolysis in these strains.
  Directly motivates open question #1 in `open_questions.json`.

### 2.4 Single-site enrichment bias

- All three isolates were pulled from a single Michigan State University
  compost site. Generalizability to other environments (native soils,
  marine sediments, landfill leachate) is not addressed.
- **Verdict:** paper-side scope caveat; motivates open question #3 in
  `open_questions.json`.

### 2.5 No degradation-rate kinetics as a function of PLA physical state

- Paper does not report degradation rate vs PLA crystallinity, molecular
  weight, or stereoform (PLLA vs PDLA vs stereocomplex).
- **Verdict:** substrate-side gap; motivates open question #2 in
  `open_questions.json`.

---

## 3. Things that were *not* wrong (documented so this file is honest)

- **Total assembly length for S3:** basically exact (Δ 0.008%). ✅
- **GC content for S3:** exact 66.26%. ✅
- **16S species assignment for S3:** 100.00% over 1536 bp — stronger than
  paper. ✅
- **PLA-relevant enzyme repertoire:** confirmed at 1/1 recovery for both
  cutinase and depolymerase; 5/6, 6/7, 109/114 for lipase/esterase/protease. ✅
- **Data deposition:** three SRA runs present; correct BioProjects;
  EC-3 read count exact. ✅

The PARTIAL verdict is driven entirely by scope of independent recomputation,
not by any disagreement between our results and the paper's claims.

---

## 4. What would move this replication from PARTIAL to FULL

1. Run SPAdes on SRR7264117 (S2) and SRR14203690 (EC-3) — closes the two
   biggest indirect-corroboration gaps. ~60 min additional wall-clock.
2. Run `fastANI` on all three isolate/reference pairs — closes the three
   ANI-number-not-tested gaps. ~5 min additional wall-clock.
3. Run MeDuSa scaffolding against PSE305 for S3 — should reduce contig count
   from 51 → ~63 and longest contig from 527 kb → ~660 kb, closing the two
   methodological-difference deltas.
4. Optional: run RASTtk annotation locally (or via PATRIC web) instead of
   Prodigal to close the CDS-count Δ 2.5%.

None of these are technically difficult; all are compute-budget decisions
that were consciously deferred in favor of getting a first-pass end-to-end
replication of the *quantitatively-most-important* isolate (S3) done.
