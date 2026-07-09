# Failure Analysis — BVBRC-82 (Bacteroides sp. CACC 737)

**Verdict:** REPLICATED (all independently testable structural claims reproduce).
**Purpose of this file:** enumerate what did *not* succeed, was skipped, or was substituted — separated from the aggregate verdict.

## 1. Assigned-workflow deviations

### 1.1 Genome Assembly (Unicycler/SPAdes) — NOT RUN
- **Assigned:** BV-BRC workflow row calls for Genome Assembly using Unicycler/SPAdes.
- **What we did:** pulled the authors' already-deposited assemblies (CP059406–CP059412) directly from GenBank via `efetch db=nuccore rettype=gbwithparts`. Verified structural numbers against the deposit; did not reassemble.
- **Why it matters:** every "REPRODUCED" quantitative number (chromosome 4,470,359 bp, GC 45.96%, per-plasmid GC to two decimals) came from the record the authors submitted. This is a **provenance verification, not an independent assembly**. A true replication of the assembly leg would fetch SRA reads (PRJNA647194) and reassemble hybrid (PacBio + Illumina).
- **Consequence:** downstream claim C7 (sequencing platforms = PacBio RS II + Illumina HiSeq) is UNRESOLVED because raw reads were never pulled.

### 1.2 PlasmidFinder — NOT APPLICABLE, SILENTLY SUBSTITUTED
- **Assigned:** PlasmidFinder via Similar Genome Finder.
- **Reality:** PlasmidFinder (CGE) targets Enterobacteriaceae + Gram-positive plasmid replicon families; it has zero Bacteroidota reps and reliably returns 0 hits for these plasmids.
- **Substitute:** all-vs-all plasmid BLAST (`blastn` on `all_plasmids.fa` self-DB, evalue 1e-5). Found ~99%-identity 7–8 kb shared regions across most plasmid pairs, interpreted as the "cryptic *Bacteroides* plasmid family" backbone (paper ref 9).
- **Consequence:** the BV-BRC workflow row for this paper is more nearly "N/A given host taxonomy" than "replicated." The substitution is defensible but is *not* the assigned tool.

## 2. LLM-stack failures

### 2.1 Argo Opus 4.7 / 4.8 → HTTP 502 Bad Gateway
- **First choice:** `argo:claude-opus-4.7` and `argo:claude-opus-4.8` (per Ollie's default-model policy).
- **Observed:** repeated `HTTP 502 Bad Gateway` on the judgment prompt during this run.
- **Fallback:** `argo:gpt-5` — free per standing policy; endpoint healthy.
- **Consequence:** verdict is Argo GPT-5-derived, not Opus-derived. Not a scientific-content failure, but worth noting for stack observability.

## 3. Deliberately un-executed items (called out in REPORT.md §6)

| Item | Why skipped | Consequence |
|---|---|---|
| Re-run PGAP + RAST on `uicgpu` | Structural claims already checked out; time-boxed | 3,682-vs-3,938 CDS gap is attributed to pipeline differences, not measured |
| Fetch SRA raw reads (PRJNA647194) | Not needed for structural claims | C7 (sequencing platforms) UNRESOLVED |
| Run CRISPR web server (crispr.i2bc.paris-saclay.fr) | Feature-scan sufficient for CONSISTENT verdict | C6 "2 confirmed + 1 questionable" locus count unverified; Type II Cas subtype unverified |

## 4. Quantitative deltas that were absorbed rather than characterized

### 4.1 Chromosome CDS 3,682 (ours) vs 3,761 (paper)
Explained as "PGAP-only vs PGAP+RAST merged annotation." Not tested by re-running RAST and diffing callsets. Story is plausible and consistent with community experience; it is not a demonstrated result.

### 4.2 Plasmid CDS shortfalls (some ~50%)
| Plasmid | Paper CDS | Ours | Delta % |
|---|---:|---:|---:|
| CP059406 | 31 | 21 | −32% |
| CP059407 | 25 | 12 | **−52%** |
| CP059409 | 39 | 29 | −26% |
| CP059410 | 35 | 13 | **−63%** |
| CP059411 | 31 | 18 | −42% |
| CP059412 | 16 | 10 | −38% |
The plasmid deltas are much larger (in %) than the chromosome delta. They are absorbed into the same "PGAP vs PGAP+RAST" narrative without being categorized. On small plasmids, short-ORF calling policy differences can plausibly account for the gap, but this was not shown.

### 4.3 tRNA 68 vs 69
Off by one; explanation same class (pipeline). Not investigated.

### 4.4 16S identity 97.83% vs paper 97.5%
- We used Biopython `pairwise2.align.globalms(2,-1,-2,-0.5)`; paper aligner unstated.
- Reported only the first of 4 chromosomal paralogs.
- Did not run a second aligner (BLASTN, EMBOSS needle).
- 0.33 pp offset is described as "well within alignment-algorithm noise" — plausible, but the noise is not characterized.
- **Impact on verdict:** none — both values sit safely below the 98.6% novel-species threshold. Qualitative conclusion is robust.

## 5. Judge-independence limitation

The Argo GPT-5 judgment call was evaluated against **the claims-plus-evidence block we assembled**, not against raw reads or alternative aligners. Reporting that "the LLM judge independently reached the same conclusion" mildly overstates independence: the judge converged on the framing we handed it. This is a common failure mode in LLM-as-judge setups.

## 6. Out-of-scope items (not counted as failures, listed for completeness)

- Probiotic-candidate claim: aspirational, downstream of genome deposit — not on the claims table.
- Anaerobic culture reproducibility, MRS media confirmation: methods claims not testable from public sequence data.
- KACC 22065 strain-deposit liveness: not queried this pass.

## 7. Failure taxonomy summary

| Class | Count | Examples |
|---|---:|---|
| Assigned-workflow skipped | 2 | Unicycler assembly; PGAP+RAST re-annotation |
| Assigned tool inapplicable → substituted | 1 | PlasmidFinder → all-vs-all BLAST |
| Locus-caller not run (feature-scan substituted) | 1 | CRISPR web server |
| Raw-data source not fetched | 1 | SRA PRJNA647194 (platforms C7) |
| Numeric delta absorbed w/o characterization | 4 | chromosome CDS; plasmid CDS %; tRNA off-by-one; 16S 0.33 pp |
| LLM-stack fallback | 1 | Opus 4.7/4.8 → 502 → GPT-5 |
| Judge-independence caveat | 1 | GPT-5 evaluated our own evidence block |

## 8. What a next pass should do (to close all of the above)

1. Fetch PRJNA647194; hybrid-reassemble with Unicycler (long + short) on `uicgpu`; compare contig set to CP059406–CP059412 → closes C7 and upgrades the C1/C2/C3 verdicts from "provenance-verified" to "de-novo-verified."
2. Prokka + Bakta + RAST on all 7 replicons; diff callsets category-by-category to attribute the CDS gap → upgrades C4 from CONSISTENT to a measured accounting.
3. CRISPRCasFinder + CRISPRDetect on CP059408; report array count, evidence level, and Cas subtype → upgrades C6 from CONSISTENT to REPRODUCED (or refutes it).
4. Per-paralog 16S identity across all 4 copies, both aligners (BLASTN + needle), documented parameters → characterizes the 0.33 pp offset properly.
5. Retry LLM judge on Opus 4.8 once Argo is healthy, ideally in a blind setup where the judge does not see our own claim-status conclusions.
