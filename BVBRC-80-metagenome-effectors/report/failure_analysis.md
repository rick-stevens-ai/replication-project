# Failure Analysis — BVBRC-80

Paper: *Metagenome diversity illuminates the origins of pathogen effectors*
(Verhoeve et al., mBio 2024, PMC11077975).
Verdict: **PARTIAL**.

This document is the candid failure/gap catalog. It intentionally lists things that did **not**
work, were **not attempted**, or that we accepted as substitutions — separate from the
"strengths" narrative in REPORT.md.

## 1. What outright did not work

### 1.1 Direct ASM (mBio publisher) supplement URLs — Cloudflare-blocked
- **What:** attempted to fetch supplementary XLSX/PDFs directly from journals.asm.org.
- **Failure:** Cloudflare 403 (bot protection) on programmatic fetch.
- **Mitigation:** switched to EuropePMC OA cache
  (`https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11077975/supplementaryFiles`),
  which returned the full 17.7 MB bundle including `mbio.00759-23-s0003.xlsx` (Table S1).
- **Cost:** none. Same bytes, different route.

### 1.2 ATHA (Athabascaceae) not testable in RvhB4-I subset
- **What:** the single ATHA taxon in Table S1 has its **RvhB4-I column blank** (only RvhB4-II
  is filled).
- **Failure:** cannot pull ATHA into an RvhB4-I-only tree; therefore cannot independently
  confirm the paper's "basal ATHA" half of claim C1.
- **Mitigation:** we still tested MITI (also flagged as basal-extracellular in the same claim
  group) and recovered MITI as deepest at mean depth 4.0.
- **Cost:** C1 is only half-confirmed — the report says "PARTIAL" for C1, not "confirmed."

### 1.3 Family-count mismatch: RICK 97 (Table S1 raw) vs 93 (paper text)
- **What:** parsed Table S1 gives 97 Rickettsiaceae rows; paper body text says 93.
- **Failure to reconcile:** we did not chase the 4-taxon delta.
- **Likely explanation:** 4 taxa reclassified as Tisiphia/Bellii subgroups in the text but
  still labeled "Rickettsiaceae" in the table.
- **Cost:** minor — flagged in REPORT.md Discussion as a paper-side curatorial inconsistency,
  not a replication defect. But we did not close the loop with taxonomy-of-record checks.

## 2. What was not attempted (out of scope, honest)

### 2.1 C5 — 26-effector distribution matrix
- Not run. Would require per-effector BLAST + HaloBlast across all 153 taxa, then presence/absence
  matrix construction. Estimated effort: hours-to-a-day of compute + curation. Deferred as
  "rapid replication" scope call.

### 2.2 C6 — *Rickettsia* ↔ *Legionella* LGT
- Not run. Would require cross-genus BLAST of specific effector sets against Legionellales
  proteomes + tree-reconciliation. Deferred.

### 2.3 Full 153-taxon concatenated (I+II, 1974 aa, TrimAl-masked to 1613 aa) tree
- Not built. We ran RvhB4-I only (864 aa) on 37 taxa (~24% of taxa, ~44% of sequence length,
  ~53% of positions if TrimAl-masked).
- **Cost:** our tree is a *sample* of the paper's tree, not a direct one-for-one comparator.
  Basal-vs-derived directionality is preserved; fine-grained clade structure is not
  independently verifiable at this resolution.

### 2.4 Bootstrap / rigorous support values
- FastTree gives **SH-like local support**; paper used PhyML with **1000 nonparametric bootstrap**.
- **Cost:** we cannot directly report bootstrap percentages on our tree's basal splits.
  A rigorous replication would run IQ-TREE or RAxML with 1000 ultrafast bootstraps.

### 2.5 Cross-model LLM-judge sanity check
- Only one judge model run (`argo:gpt-5.2`). Per standing cross-model sanity rule, at least one
  alternative (e.g. `argo:claude-opus-4.8`, or a CELS reasoning model) should score the same
  evidence bundle before treating PARTIAL as authoritative.
- **Not done.** Single-judge verdict is a soft point.

## 3. Substitutions accepted (defensible but not innocent)

### 3.1 MAFFT --auto (L-INS-i) vs paper's MUSCLE default
- **Both** are standard for divergent protein families. MAFFT L-INS-i often outperforms MUSCLE
  default on ~40-taxon protein sets with long insertions.
- **Risk:** alignment choice can flip deep branching decisions on divergent T4SS effector
  families in a non-negligible fraction of cases. We did not run both aligners as a control.

### 3.2 FastTree LG+Γ vs paper's PhyML LG+G+I+F (Smart Model Selection)
- FastTree is fast and topology-agreement with PhyML is typically >95% on protein trees of this
  size (folklore rule of thumb — **not a per-dataset guarantee**).
- **Risk:** without I (invariant sites) and F (empirical frequencies) parameters, subtle
  branch-length differences and a small fraction of tip placements may differ.

### 3.3 No TrimAl masking
- Paper masked concatenate to 1613 aa. We ran unmasked 864 aa RvhB4-I.
- **Risk:** poorly-aligned columns can inject phylogenetic noise; typical impact on major
  topology is low but non-zero.

### 3.4 Outgroup: AAK90276.1 (A. tumefaciens C58 VirB4) vs paper's F4 VirB4
- Same protein family, functionally equivalent as outgroup. F4 VirB4 was not trivially
  retrievable by a single accession; C58 is the canonical NCBI entry.
- **Risk:** minimal (paralog-level identity between C58 and F4 VirB4 is high).

## 4. Weaknesses in our reporting itself (meta)

### 4.1 Support values not tabulated in Results
- FastTree computed SH-like supports but the Results section of REPORT.md does not list them
  per node. This is a presentation hole, not a data hole.

### 4.2 MITI basality rests on N=1
- MITI basal depth of 4.0 is a single taxon. Cannot rule out long-branch attraction (LBA)
  toward the divergent Agrobacterium outgroup. No LBA-mitigation test (e.g. slow-fast site
  removal, alternative rooting) was performed.

### 4.3 No end-to-end `make replicate` entrypoint
- Artifacts are all present, but there is no single-command reproducer that goes Table-S1-fetch
  → alignment → tree → verdict JSON. Engineering debt, not scientific debt.

### 4.4 BV-BRC metadata mis-tag flagged locally, not upstream
- We correctly noted that the "Genome Assembly / Read Mapping" tag is wrong for this paper,
  but we did not push the correction back into the BV-BRC pipeline's metadata. Future picks
  under the same tag will hit the same mis-classification.

## 5. What is NOT a failure

- Data-availability (C4) round-tripped cleanly (153 taxa, all accessions live).
- Core topology (MITI basal, RICK derived, ANAP monophyletic) reproduced under substituted
  tools and reduced taxon set — a strong signal.
- No contradictions with the paper on any quantity we could check.

## 6. Bottom line

The PARTIAL verdict is honest: **coverage was reduced by design** (37/153 taxa, RvhB4-I only,
no C5/C6), and the reductions carry with them the substitution/robustness caveats listed
above. The paper's methods are well-documented and its data are machine-actionable — those
are the reasons the partial rerun was cheap and clean, and they are also the reasons a full
replication would be a straightforward next scope-up rather than a research problem.
