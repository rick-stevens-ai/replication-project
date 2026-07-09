# Failure Analysis — BVBRC-67 (Fusobacterium varium Fv113-g1)

**Paper:** Sekizuka et al. 2017, PLOS ONE 12(12):e0189319
**Verdict:** REPLICATED (spot-check)
**Purpose of this file:** an honest catalog of what could have failed, what did, and what
would strengthen the conclusion if the effort were extended.

---

## 1. Actual failures / divergences observed

### 1.1 C11 — FadA paralog count (13 → 8), PARTIAL

**Symptom.** Case-insensitive product-name regex on RefSeq PGAP `protein.faa` for the
strings `FadA` / `fusobacterium adhesin` yields 8 matches. The paper reports 13.

**Root cause (best explanation).** Annotation-scheme divergence. Sekizuka et al. used
RAST 2.0 + InterPro v49.0 + BLASTp and appear to have counted the broader FadA-domain
family, likely folding in hemagglutinin-related sub-family paralogs. RefSeq PGAP is more
conservative about extending the `adhesion protein FadA` product-name label to homologs
outside a strict definition. Neither number is refuted by the other; they are answering
slightly different questions.

**Not a contradiction because.** The paper's number is derived from a legitimate
homology-based scheme, and the strict-string count is a known under-estimate. A definitive
arbitration requires a domain-model search (HMMER against Pfam PF09403) which was not run.

**Failure-mode class.** Fragile string-matching against an annotation label that shifts
with pipeline choices. Preventable by anchoring the paralog count to a Pfam / TIGRFAM
domain model rather than to product-name strings.

### 1.2 Potential confusion — abstract-only reading of the genome size

**Symptom.** If a reader compares the paper's abstract ("3.96 Mb") against the RefSeq
`assemblyStats.totalSequenceLength` (4,122,841 bp), a spurious ~4 % discrepancy appears.

**Root cause.** The abstract quotes chromosome-only length. The RefSeq total includes both
plasmids (89.6 kb + 68.1 kb). Table 1 of the paper is consistent with the whole-genome
total; only the abstract's shorthand is ambiguous.

**Not a failure of the paper.** A documentation risk for downstream readers. Called out
explicitly in REPORT.md §5 to prevent recurrence.

---

## 2. Failure modes actively considered and ruled out

| # | Candidate failure mode | Outcome | Evidence |
|---|---|---|---|
| F1 | Wrong assembly (accession-mapping error, GenBank AP017968 → RefSeq mis-linked) | Ruled out | `esummary_asm.json` confirms GCF_002356455.1 is the RefSeq of AP017968; chromosome length matches paper to +0.13 %. |
| F2 | GC-content parse error (denominator including / excluding N bases) | Ruled out | Values agree with RefSeq `assemblyStats.gcPercent` (29 %) and with each plasmid's paper-reported value to within 0.05 pp. |
| F3 | Replicon mis-count from concatenated FASTA | Ruled out | Three `>NZ_...` records enumerated; each matches a paper-declared replicon. |
| F4 | Off-by-one on GFF feature tallies (parent gene vs. child CDS/tRNA/rRNA) | Considered | tRNA count exact match (58); rRNA feature count is 22 (= 7 operons × 3 + one extra 5S, consistent with paper's "7 rRNA operons"). No off-by-one. |
| F5 | Pseudogene inclusion inflating CDS count | Considered | Distinct counts reported: 3,671 total CDS features vs. 3,586 protein-coding genes; 85 pseudogenes. Both bracket the paper's 3,552 within routine PGAP-vs-RAST drift. |
| F6 | Product-name regex over-matching (e.g., `autotransporter`-adjacent labels) | Bounded, not eliminated | +1 delta on C10 (44 → 45) is well within reasonable regex tolerance. Would tighten with a Pfam-anchored count. |
| F7 | Comparator-strain confusion (ATCC 27725 vs. ATCC 25286 typos in literature) | Ruled out | `esearch` verified GCF_003019655.1 is the correct current RefSeq for ATCC 27725. |

---

## 3. Known gaps (what this replication does *not* test)

1. **C12 — RNA-seq differential expression (D-MEM vs. BHI, DRA005507).**
   The paper's mechanism-relevant claim about condition-dependent T5SS / *fadA*
   upregulation. Not re-tested. Requires FASTQ pull, aligner (HISAT2/STAR), count model,
   DESeq2 rerun. Documented in `open_questions.json`.
2. **C13 — ISFv1 / ISFv2 enumeration (47 and 48 insertions).**
   The paper's mobile-element expansion claim. Not re-tested. Requires ISEScan or
   ISfinder rerun on the closed assembly.
3. **Assembly-pipeline verification.**
   We did not independently redo the hybrid assembly from raw Illumina + PacBio + Argus
   reads. A "REPLICATED" verdict here covers the derivative statistics on the deposited
   artefact, not the assembler pipeline that produced it.
4. **Phylogenetic and ortholog claims.**
   FastTree topology and OrthoVenn "partial ortholog sharing with *F. ulcerans*" not
   re-computed. Would need OrthoFinder + IQ-TREE + fastANI + dDDH.
5. **Plasmid content characterization.**
   pFV113-g1-1 and pFV113-g1-2 are confirmed at the replicon-shape / GC level but were
   not annotated for mobilization modules, ARGs, or virulence cargo.
6. **PGAP release pinning.**
   We report "RefSeq PGAP as most recently run by NCBI" without pinning the exact PGAP
   version. A stricter replication would freeze the release.

---

## 4. Systemic risks worth flagging for the next target

- **Product-name regex fragility.** Any paralog-count claim in a bacterial-genome paper
  should be reproduced via domain-model search (HMMER against the appropriate Pfam), not
  string matching against the annotator's product label. Add this as a default rule for
  the BVBRC replication wave.
- **Abstract-only shorthand.** Chromosome-only vs. whole-genome length is a recurring
  confusion source for bacteria with sizeable plasmid load. Default to reporting both.
- **RAST → PGAP annotation drift is real but bounded.** A ±5 % drift on gene tallies
  between the paper-time RAST and current PGAP is routine and should not be treated as a
  contradiction. Codify this as an explicit tolerance band in the verdict schema.
- **Deferred claims must be recorded, not silently skipped.** C12 and C13 are recorded
  here and in `open_questions.json` so a future extension pass has a clean starting list.

---

## 5. What a strengthened replication would add

1. HMMER PF09403 domain scan on Fv113-g1 `protein.faa` to arbitrate C11.
2. RNA-seq rerun on DRA005507 to test C12 end-to-end.
3. ISEScan / ISfinder rerun on the closed assembly to test C13.
4. fastANI + dDDH matrix across all *F. varium* and *F. ulcerans* RefSeq entries to
   quantify the sub-clade placement claim.
5. Plasmid annotation with oriTfinder / MOBscan / CONJscan + CARD/VFDB BLAST for cargo
   characterization.
6. PGAP release pinning for full byte-level reproducibility.
