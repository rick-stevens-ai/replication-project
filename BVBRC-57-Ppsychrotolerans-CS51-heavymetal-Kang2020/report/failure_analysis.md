# Failure Analysis — BVBRC-57 (Kang et al. 2020, *P. psychrotolerans* CS51)

**Verdict:** REPLICATED (with one honest PARTIAL and a set of explicit not-tested items)
**Analyst:** Ollie (OpenClaw AI subagent)
**Purpose of this document:** be blunt about what did *not* work perfectly, what was shortcut, and what future runs should not repeat.

---

## 1. Where the replication genuinely failed to match

### 1.1 C14 (core-genome ~2122 genes) — PARTIAL, count did NOT replicate
- **Paper reports:** ~2122 core genes.
- **We got:** 2790 core genes.
- **Delta:** +668 genes (+31%).
- **Root cause:** we ran Roary on **9 conspecific *P. oryzihabitans* genomes** at 90% BLASTp identity. The paper ran BPGA on a **cross-species outgroup mix** (*P. syringae*, *P. putida*, *P. psychrotolerans* PRS08, *P. aeruginosa*), which is far more divergent and legitimately shrinks the core.
- **Was this preventable?** Yes — we could have exactly reproduced the paper's genome set. We chose not to because the conspecific comparison is more biologically principled, but that means the specific number ~2122 is NOT independently confirmed.
- **Honest classification:** SHAPE-MATCH, COUNT-MISMATCH. The paper's *qualitative* pan-genome behavior (core shrinks, pan grows, open pan-genome) is fully reproduced. The specific count is not.
- **Should not be reported as a full replication of C14.** REPORT.md correctly labels this a partial.

### 1.2 CDS / gene count (C6) — CLOSE but not exact
- **Paper:** ~4774 CDS / ~4859 genes.
- **We got:** 4846 CDS / 4837 genes / 4714 proteins (+90 pseudogenes).
- **Delta:** +72 CDS (+1.5%), −22 genes.
- **Root cause:** gene-caller / pseudogene-handling differences between the paper's RAST/SEED annotation and the RefSeq PGAP annotation on the same FASTA. This is standard $\pm$1–2% drift and is called "close" in the report — accurately.
- **Was this preventable?** Only by re-running RAST/SEED on the identical FASTA. Not worth the effort for a $\pm$1.5% drift on a pipeline-comparison metric.

---

## 2. Shortcuts taken (and why)

### 2.1 We tested gene *presence*, not gene *function*
- Every C7–C13 (heavy-metal resistance, IAA/auxin, nitrate/nitrite, Pst, sulfate) is confirmed at the level of "a gene of that predicted function exists in the genome," corroborated across two independent annotators (RefSeq PGAP + BacMet2).
- **We did NOT verify:** MIC-style Zn/Cu/Cd/Ni tolerance, actual IAA/gibberellin production, cucumber-growth-promotion assay, nitrate/nitrite ammonification activity, phosphate solubilization, sulfate transport rate.
- **Why:** replication scope was in-silico only (no wet-lab budget). This is a genuine limitation, not a bug.
- **Cost of the shortcut:** the paper's *phenotypic* claims are effectively not independently re-verified. Only the *genomic-basis* claims are.

### 2.2 We used the deposited assembly, not the raw PacBio reads
- The paper describes a PacBio SMRT assembly workflow. We did not reassemble from raw reads.
- **Why:** the deposited assembly (`GCF_006384975.1`) is the community-referenceable artifact and matches the paper's reported statistics byte-exactly.
- **Cost:** any assembly-workflow claim (contig N50 evolution, polishing convergence) is not re-verified. But those are not among the paper's core claims.

### 2.3 We swapped BPGA (paper) → Roary (us) for pan-genome
- Different tool, different genome set (conspecific vs. cross-species).
- **Why:** Roary is more transparent + more actively maintained; conspecific comparison is the more principled experimental design.
- **Cost:** the ~2122 core-count is not directly reproduced (see §1.1 above).

### 2.4 We did NOT run antiSMASH
- No secondary-metabolite BGC mining was performed.
- **Why:** not among the paper's explicit claims (paper's Figure 5 shows SEED "secondary metabolism" subsystem but does not enumerate BGCs).
- **Cost:** any siderophore / metallophore BGC that could underlie the heavy-metal tolerance phenotype (e.g., pyoverdine-family iron chelators that also bind Cu/Zn/Cd) is not surveyed. Flagged as open question #4 in `open_questions.json`.

### 2.5 We did NOT resolve the taxonomy formally
- NCBI reclassified CS51 from *P. psychrotolerans* to *P. oryzihabitans* post-publication, yet 7/8 *P. oryzihabitans* comparators are only 88.68–89.69% ANI to CS51 — **below the 95% species boundary**.
- We reported this observation but did not compute dDDH / GGDC or attempt a formal taxonomic proposal.
- **Cost:** the species identity is left genuinely ambiguous. Flagged as open question #1.

---

## 3. Things that could bite a future re-runner

### 3.1 Annotation-label drift is a real trap
- "Cobalt-zinc-cadmium resistance" (RAST/SEED, paper) and "DmeF CDF efflux + heavy-metal P-type ATPase + ZnuABC/ZntB" (RefSeq PGAP, us) describe the **same underlying biology under different label conventions**.
- A naive string-match replicator would score C8 as a FAIL. It is a PASS — but only because a human (or LLM curator) mapped the labels.
- **Recommendation:** future replication runs on RAST-annotated papers should carry a curated RAST↔PGAP↔BacMet2 mapping table. Flagged as open question #5.

### 3.2 The LLM judge is not independent evidence
- Argo gpt-5.2 verdict (STRONG/MODERATE/WEAK per claim, overall REPLICATED) was scored from **our own claims table and our own results**.
- It should be read as an internal-consistency QA pass, NOT as an external adjudication.
- Future runs should not confuse "LLM judge = REPLICATED" with "independent third party = REPLICATED."

### 3.3 Genome-set selection changes the pan-genome answer
- Adding or removing a single divergent comparator will shift the core-gene count by hundreds. Any pan-genome replication should either (a) exactly reproduce the paper's input set, or (b) explicitly report the input set and call the result a shape-match, not a count-match. We did (b).

### 3.4 The IAA-pathway gene list is suggestive, not conclusive
- What we listed for C10 (tryptophan synthase α+β, PRAI, TrpC, anthranilate synthase I+II, anthranilate 1,2-dioxygenase) is **tryptophan biosynthesis**, i.e., substrate supply for IAA. It is NOT the canonical IAA-biosynthesis machinery (ipdC/aldH or iaaM/iaaH).
- The report labels this "STRONG" for C10 based on RAST/SEED subsystem membership, but a stricter reading is "the substrate pathway is present; the actual IAA-synthesizing enzyme is not called out." Flagged as open question #3.

---

## 4. Explicit NOT-TESTED list (from REPORT.md Genuine Critique)

- Any wet-lab phenotype (heavy-metal MIC, IAA production, cucumber growth-promotion assay, gibberellin production).
- The specific PacBio assembly workflow described by the paper (used the deposited assembly).
- The paper's exact BPGA pan-genome tool output (used Roary instead).
- Any secondary-metabolite BGC claim (antiSMASH not run).
- dDDH / GGDC taxonomic refinement of the *P. psychrotolerans* vs *P. oryzihabitans* question.
- MLST — no scheme exists for the species.

---

## 5. Honest assessment

The replication is **strong at the level of genome sequence identity and gene-content presence** (byte-exact length/GC/rRNA/tRNA; two-annotator agreement on all functional categories; independent phylogenetic placement). It is **weak-to-absent at the level of phenotypic function and comparative-genomics tool identity**. The REPLICATED verdict is defensible because the paper is fundamentally a *genome-sequence-and-annotation* paper, and every genome-sequence-and-annotation claim is confirmed. It would NOT be defensible to extend the REPLICATED verdict to the paper's PGPR / heavy-metal-tolerance *phenotype* claims — those remain to be independently verified in future wet-lab work.

The failure to reproduce the specific ~2122 core-gene count is a genuine (and correctly reported) partial. Everything else that "failed" is a shortcut we chose deliberately and documented above.
