# Failure Analysis — BVBRC-94 (L. lactis LL16, Milerienė et al. 2023)

**Overall verdict:** PARTIAL REPLICATION (strong) — 8/10 in-silico claims reproduced, 1 spot-checked, 1 wet-lab OoS. This document catalogues **what did not fully replicate** and **why**, with honest root-cause attribution.

---

## 1. Failure #1 — Genome length gap (−115,789 bp, −4.47%)

**Claim (C2):** Paper reports assembly length = **2,589,406 bp**.
**Observed:** Deposited `GCA_029912225.1` = **2,473,617 bp**.
**Delta:** −115,789 bp (−4.47%).

**Severity:** HIGH. This is the single most material divergence and the primary reason the verdict is PARTIAL rather than REPLICATED.

**Root-cause hypotheses (none confirmable from public artefacts alone):**
1. Paper text quotes a **pre-deposit assembly stage** (raw SPAdes / pre-scaffold / pre-contamination-filter), while the deposit is a **post-polish** version.
2. Paper text quotes the **raw SPAdes** length inclusive of low-coverage / duplicate contigs that were stripped before submission to NCBI.
3. **Editorial / typesetting error** in the paper's Results section (a digit transposition or wrong number pulled from a preliminary QUAST run).

**What would resolve it:**
- Author query (out of scope for a subagent).
- **Raw-read re-assembly** from SRA/BioProject — would clarify which assembly parameters reproduce the paper's stated length. Not attempted.

**Impact on other claims:** Does NOT invalidate downstream biological claims. All safety/functional/plasmid/GAD claims target specific loci that are present in the deposited assembly; a 4.5% length gap is unlikely to hide the *presence/absence* of the specific tested genes.

---

## 2. Failure #2 — CDS / tRNA count gap (RAST vs PGAP)

**Claim (C2):** Paper reports 2,878 CDS and 63 tRNA (RAST annotation).
**Observed:** 2,507 CDS (GFF) / 2,469 (protein.faa) and 51 tRNA (PGAP).
**Delta:** −371 CDS, −12 tRNA.

**Severity:** LOW (explained). The RAST-vs-PGAP annotation gap is a well-known systematic difference: RAST + tRNAscan-SE (aggressive) overcalls both CDS and tRNAs relative to PGAP (conservative). This is a methodology artefact, not a substantive genomic divergence.

**Root cause:** Different annotators applied to the same assembly. Paper used RAST; deposit is PGAP-annotated.

**Note:** Paper's phrasing ``CDA and RNRs were 2878 and 63'' is almost certainly an OCR/editing artefact for ``**CDSs and tRNAs** were 2878 and 63'' (63 ``ribonucleotide reductases'' would be biologically absurd).

**What would resolve it:** Re-annotate LL16 with RAST directly — would reproduce paper counts within RAST's expected variability. Not attempted (RAST DB not staged on uicgpu).

---

## 3. Failure #3 — T3PKS BGC (C7) — spot-check only, no true re-detection

**Claim (C7):** Paper reports 1 T3PKS BGC (antiSMASH 5.0).
**Observed:** antiSMASH not run; PGAP-annotation grep found 1 `polyketide synthase regulator (partial)` (MDH8063741.1) + 1 `ketoacyl-ACP synthase III` (MDH8064341.1).

**Severity:** MEDIUM. The claim is *consistent* with the observation but not *reproduced* in the strong sense. A reviewer asking ``did you re-detect the T3PKS BGC?'' must be told ``no, we grepped for two marker proteins''.

**Root cause:** antiSMASH nucleotide/HMM database (`/data/stevens/antismash_db/`) was **empty** on uicgpu; a ~20 GB DB pull would be required. antiSMASH 8.0.4 itself is available in `envs/antismash/` but fails at `check_prerequisites` without the DB. Deferred rather than blocked.

**What would resolve it:** `antismash --databases /data/stevens/antismash_db --taxon bacteria LL16.fna` after the DB pull. High-priority remediation.

---

## 4. Failure #4 — BAGEL4 bacteriocin re-run not performed

**Claim (C4):** Paper reports LcnB + EnlA bacteriocin clusters (BAGEL v4).
**Observed:** tblastn against P35518 (LcnB), P35517 (LciB immunity), Q4FD00 (EnlA-like) — all confirmed.

**Severity:** LOW. tblastn is a **strict lower bound** on what BAGEL would report: BAGEL adds HMM-based context detection, immunity/regulator co-clustering, and known-cluster-type classification that raw tblastn does not. If tblastn finds them, BAGEL almost certainly will too. But the exact BAGEL output classes/subclasses were not re-generated.

**Root cause:** BAGEL4 not installed in current uicgpu envs. tblastn against canonical UniProt references was chosen as the strongest available lower-bound.

**What would resolve it:** Install BAGEL4 (or run web-BAGEL) on LL16 assembly. Low priority — the claim is already supported.

---

## 5. Failure #5 — CRISPR spacer/DR enumeration not repeated

**Claim (C6b):** Paper reports 1 CRISPR array, **3 spacers**, DR = **23 bp**, + associated Cas gene.
**Observed:** 1 `Cas2` PGAP annotation (MDH8063313.1). Spacer count and DR length **not re-enumerated**.

**Severity:** LOW-MEDIUM. The qualitative claim (single CRISPR-Cas system present) is confirmed. The **quantitative structural claim** (3 spacers, 23-bp DR) is unverified.

**Root cause:** CRISPRFinder / CRISPRCasTyper not run. This was a scope choice — presence-only was accepted given the safety+GABA claims were higher-priority.

**What would resolve it:** Run CRISPRCasTyper or CRISPRDetect on LL16 assembly; extract spacer sequences; compare count and DR length. Low-effort remediation (~10 min).

---

## 6. Non-failure — wet-lab GABA HPLC (C9)

**Claim (C9):** GABA physically produced in fermented milk (HPLC).
**Status:** Not attempted.

**Not counted as a failure:** wet-lab claims are out of scope for an in-silico subagent replication. The genomic precondition (intact gadR-gadC-gadB operon at 95–99% id) is confirmed at the strongest level of the entire replication (C8), which is the strongest possible in-silico support for the wet-lab positive result.

---

## 7. Meta-failures / hostile-reviewer angles

### 7a. Threshold-choice bias
ABRicate cutoffs (≥90% id / ≥60% cov) are defensible clinical/EFSA-matching values but are *convenient* for reproducing a ``0 AMR hits'' claim. A threshold sweep (70/50, 80/60, 90/60) was **not** performed. If a looser cutoff surfaced an AMR hit, the C3a verdict would need qualification.

### 7b. Contig-fragmentation absorbing discrepancies
Several ``consistent'' verdicts (IS6 count 4 vs paper 3; rRNA fragmented across contigs; N50 = 10,345 bp across 372 contigs) attribute mismatches to draft-assembly fragmentation. That's a real explanation, but it also **absorbs discrepancies** in a way that is hard to falsify without a long-read re-assembly.

### 7c. Single-assembly analysis, no raw-read re-assembly
The 116-kb length gap (Failure #1) could in principle only be diagnosed by re-assembling from SRA reads. Not attempted.

### 7d. LLM-judge coverage 80%, MODERATE agreement
The LLM-judge (Argo `argo:gpt-5.2`, temp=0) explicitly reports **80% coverage** and **MODERATE** agreement — its own quantification says ~20% of claim-space is not fully covered.

---

## 8. Remediation priority (if the report were to be strengthened)

| Priority | Item | Estimated effort |
|---|---|---|
| HIGH | Pull antiSMASH DB + rerun on LL16 to close C7 | ~1 h (mostly DB download) |
| MEDIUM | Threshold sweep on ABRicate (70/50, 80/60, 90/60) | ~15 min |
| MEDIUM | CRISPRCasTyper run to enumerate spacers + DR (close C6b quantitative) | ~10 min |
| LOW | BAGEL4 install + re-run (close C4 methodology gap) | ~30 min |
| LOW | RAST re-annotation to close C2 CDS/tRNA count gap | ~1 h |
| DEFERRED | SRA raw-read re-assembly to diagnose C2 length gap | ~4-8 h + author query |
| OOS | Wet-lab HPLC GABA re-measurement | N/A (subagent) |
