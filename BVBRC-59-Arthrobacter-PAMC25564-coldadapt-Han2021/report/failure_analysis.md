# Failure Analysis — BVBRC-59 (Arthrobacter sp. PAMC25564, Han et al. 2021)

**Verdict:** REPLICATED. No hard failures. This document catalogues near-misses, forced substitutions, and known replication hazards so future reruns do not re-learn them the hard way.

---

## 1. Substitutions that were forced by external outages

### 1.1 dbCAN2 / V8 HMM DB unavailable
- **Situation:** The paper used dbCAN2 (HMMER + Hotpep + DIAMOND overview) against a V8-era HMM DB hosted at bcb.unl.edu. bcb.unl.edu is offline as a consequence of a cyberattack against the host institution.
- **Substitution:** dbCAN-HMMdb-V9 from pro.unl.edu (99 MB, HMMER3-compatible). HMMER-only leg only; Hotpep and DIAMOND legs were not re-run.
- **Impact on results:** Total CAZyme count 108 → 102 (Δ6); GH/GT/AA/PL match within 0–2; CE 23 → 16; CBM 2 → 9. CBM/CE are the most version-sensitive dbCAN classes; the direction of drift (CBM up, CE down) is consistent with V9 HMM-set expansion for CBMs and tighter HMM-only filtering for CE.
- **Why this did not defeat replication:** All biologically-relevant signature families (GH1, GH13_11, GH13_26, GH65, GH77, CBM48) were fully recovered. The paper's core cold-adaptation claim rests on family presence, not on ±6 in the total count.

### 1.2 Cannot factorize DB-version vs pipeline-signature
- **Situation:** Because V8 is unavailable AND we ran HMMER-only, two variables changed simultaneously (DB version + pipeline shape). We cannot cleanly attribute the 108 → 102 delta to either variable alone.
- **Mitigation:** Documented as an open question (see `open_questions.json` Q3). A future 2×2 factorial (V8/V9 × HMMER-only/3-signature) will resolve it if the V8 DB is republished.

## 2. Annotation-vintage hazard (near-miss)

### 2.1 Current RefSeq re-annotation drifts materially
- **Situation:** RefSeq re-annotation RS_2024_05_22 reports 3,863 genes / 3,718 CDS / 75 pseudogenes for GCA_004798705.1 — different from the paper's 3,829 / 3,613 / 147.
- **Near-miss:** A naive rerun against "the latest RefSeq annotation" would produce three non-matching numbers and could easily be misread as the paper being wrong or the assembly having changed.
- **Fix applied:** Pinned the rerun to the paper-contemporaneous **2019-04-11 GenBank annotation** by requesting the original vintage via NCBI Datasets v2 + efetch. All six counts then reproduce exactly.
- **Lesson:** For any replication of a paper >2 years old that reports PGAP-annotation counts, explicitly pin the annotation vintage. Do not assume "latest RefSeq" is what the paper used.

## 3. Coverage gaps (documented, not fatal)

### 3.1 Comparator pan-CAZyme comparison not re-run end-to-end
- **What was done:** Verified 5 sampled comparator accessions resolve to real complete public genomes of the named strains via NCBI esummary.
- **What was NOT done:** Full re-run of dbCAN across all 16–26 comparators followed by pan-CAZyme statistical comparison (which is what the paper's comparative figure rests on).
- **Consequence:** The paper's biological conclusion — that PAMC25564's glycogen/trehalose CAZyme enrichment is distinctive within Arthrobacter — is *consistent with* but not *independently retested by* this replication.
- **Judged severity:** Low. Coverage 9/10 from the LLM judge reflects this gap explicitly.

### 3.2 No functional / phenotypic validation
- **What was done:** Recovered the CAZyme complement including cold-adaptation signature families.
- **What was NOT done:** RNA-seq at low temperature, enzyme kinetics of GH65/GH13_11, or any wet-lab phenotype tying specific CAZymes to cold growth.
- **Consequence:** Genomic-association claim ("these families are here in a cold-adapted isolate") is replicated; mechanistic claim ("these families cause cold adaptation") remains unproven in both paper and rerun.
- **Judged severity:** Inherent to the underlying study design; carries over, does not degrade replication verdict.

## 4. Successful risk mitigations (not failures — worth recording)

- **Free-endpoint discipline:** All compute stayed on uicgpu01 free A100 with NCBI free REST + Argo free localhost:44497 judge. No paid API calls; no compute rule violated.
- **Provenance clean:** Focal genome, proteome, and comparator strains all sourced from primary NCBI archives (no lab-internal mirror leaked into the rerun).
- **Determinism where possible:** HMMER 3.4 + canonical dbCAN parser filter (E<1e-15 if aln>80aa else E<1e-5; HMM cov>0.35; overlap>0.5) is deterministic given the same input FASTA and DB. Rerunning M4 will produce the same 102/34/43/16/5/9/0 result.

## 5. Known replication hazards for the next runner

1. **Do not use current RefSeq annotation** for paper-comparison; pin to 2019-04-11 GenBank vintage.
2. **Do not use dbCAN2 web server** as an ephemeral one-off; version the HMM DB explicitly and record which mirror/version was pulled.
3. **Do not expect ±0 on CAZyme totals** across dbCAN versions; expect ±5–10 and check the biology (family presence), not the arithmetic (class totals).
4. **Do not conflate "comparator dataset available" with "pan-CAZyme comparison reproduced"**; these are separate levels of evidence.
5. **Do not upgrade the verdict to VALIDATED without wet-lab work** — the mechanistic cold-adaptation claim is an inference from genomics in both the paper and the rerun.

## 6. Overall failure count
- Hard failures: **0**
- Forced substitutions: **1** (dbCAN V8 → V9, driven by external outage; documented and mitigated)
- Near-misses caught: **1** (annotation-vintage drift; pinned to 2019-04-11)
- Coverage gaps: **2** (pan-CAZyme comparator re-run; phenotypic validation) — both inherent, judged non-blocking.
