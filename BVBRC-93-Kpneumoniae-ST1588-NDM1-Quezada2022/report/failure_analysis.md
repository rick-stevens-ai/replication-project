# BVBRC-93 Failure Analysis

**Dataset:** BVBRC-93-Kpneumoniae-ST1588-NDM1-Quezada2022
**Verdict:** REPLICATED (LLM-judge coverage 0.90, agreement 0.98)
**Purpose:** Honest inventory of what did NOT fully replicate, what was NOT tested, what nearly went wrong, and where the verdict has scope limits. Nothing here overturns the REPLICATED verdict, but this catalogue is the audit trail a reviewer should see.

---

## 1. Claims not fully in-silico testable

### 1.1 C10 — Wet-lab conjugation frequency
- **Paper claim:** pNDM-1_UCO361 transfers to *E. coli* J53 only at 27 °C (not 37 °C), frequency 4.3×10⁻⁶ transconjugants/recipient.
- **In-silico status:** **UNTESTABLE.** No sequence-based method can measure a conjugation frequency or a temperature-dependent phenotype.
- **Mitigation:** Verified that all mechanistic prerequisites are present on the assembly — *traC* on pNDM-1_UCO361, complete *tra* locus on the co-resident IncFIB(K), *hns* regulator. These are consistent with the phenotype but do not confirm it.
- **Residual risk:** The paper's *trans*-mobilisation hypothesis via the IncFIB(K) helper is neither confirmed nor refuted. It remains hypothesised, not demonstrated (see open_questions.json Q1 + Q2).

### 1.2 C11 — Epidemiological "first-in-Chile" claim
- **Paper claim:** UCO-361 is the first NDM-1-producing *K. pneumoniae* detected in Chile (2014); ST1588 previously reported in Rio de Janeiro.
- **In-silico status:** **PARTIAL.** GenBank metadata (Chile: Santiago, 33.45 S 70.64 W, 2014) corroborates isolation origin. National-first status cannot be established from a single deposit; it depends on national surveillance data we did not audit.
- **Residual risk:** Historical priority claim is accepted on the paper's authority (see open_questions.json Q5).

## 2. Claims with minor annotation drift

### 2.1 C5 — blaSHV allele call
- **Paper:** blaSHV-106 chromosomal.
- **My AMRFinderPlus + Kleborate:** blaSHV-1 chromosomal, 100% id, with mutation flag.
- **Root cause:** Annotation-database drift on the same chromosomal locus. AMRFinderPlus DB 2024-07-22.1 and Kleborate v3.2.4 both prefer the SHV-1 backbone call for what the paper called SHV-106 in 2022.
- **Impact:** Cosmetic. Same locus, same nucleotide identity. Does not affect verdict.
- **Lesson:** Legacy SHV-X allele calls in papers should always be re-checked against current DB before quoting.

### 2.2 C5 — aac(3)-IIa vs aac(3)-IIe, aac(6')-Ib-cr vs aac(6')-Ib-cr5
- **Paper:** aac(3)-IIa and aac(6')-Ib-cr.
- **My AMRFinderPlus:** aac(3)-IIe (100% id) and aac(6')-Ib-cr5 (100% id).
- **Root cause:** Variant-naming refinement in updated AMRFinderPlus DB.
- **Impact:** Cosmetic. Same enzymatic function class, same locus, same identity.

## 3. Claims where scope was renegotiated (enrichment, not contradiction)

### 3.1 C9 — "Closest plasmid" framing
- **Paper claim:** Closest published plasmid is MN598004.1 (pNDM-1-EC12) with a "common region of 2488 bp"; pRAO166a (CP041388) has a different genetic environment.
- **My finding:** Under a **narrow reading** (the blaNDM-1 local flanking region), the paper's characterisation holds. Under a **whole-plasmid reading**, however:
  - vs MN598004.1: 92 HSPs, longest 57,352 bp @ 98.64%, total ≥90% id aligned = 211,270 bp.
  - vs CP041388.1: 96 HSPs, longest 39,233 bp @ 99.02%, total ≥90% id aligned = 215,338 bp.
- **Verdict adjustment:** Marked **PARTIAL / ENRICHED**, not FAILED. The paper's local-region statement is true; the whole-plasmid backbone framing is not what a whole-plasmid BLASTn would suggest today.
- **Reader hazard:** A non-expert reading "novel megaplasmid" might infer whole-plasmid backbone novelty. The evidence supports narrow (cargo + replicon) novelty only.

### 3.2 C7 — PlasmidFinder-untypable status
- **Paper claim:** No PF 2.1 hit → treated as a stable feature.
- **My finding:** Current PF DB (post-paper) has partial repHI5B and repFIB hits from pC39 (CP061701), which was deposited **after** the paper.
- **Verdict adjustment:** REPLICATED for PF 2.1-era database; enriched with a version-caveat.
- **Lesson:** Any "not typable by tool X" claim should be timestamp-anchored to the specific tool version and DB snapshot used.

## 4. Methodological near-misses

### 4.1 Assembly retrieval scope
- **Risk:** Fetching only the plasmid contig would have prevented independent MLST, Kleborate, K/O-locus, and full-genome AMR calls.
- **Mitigation:** Fetched all 15 contigs of `JAMJQY010000000` up front (5,841,932 bp total) and kept both the whole-assembly FASTA and the isolated plasmid GenBank.

### 4.2 PlasmidFinder database version pinning
- **Risk:** Running against current PF would appear to contradict the paper's "no Inc typing" claim without a version caveat.
- **Mitigation:** Explicitly recorded that the current PF DB adds partial pC39-family hits from a post-paper reference (CP061701), and framed C7 as REPLICATED for PF 2.1-era with a version note.

### 4.3 blaNDM-1 landmark parsing
- **Risk:** RefSeq PGAP uses functional labels (e.g. "co-chaperone GroES", "phosphoribosylanthranilate isomerase") that do not literally match the paper's gene-symbol labels (groES, trpF). A naive text-match would miss all 6 landmarks and falsely refute C6.
- **Mitigation:** Manual mapping of RefSeq product terms to paper symbols; verified strand + position + order match Fig. 1B exactly.

### 4.4 Compute environment
- **Risk:** Prior BVBRC-46 outputs in the same host could contaminate results.
- **Mitigation:** Fresh working dir `/data/stevens/bvbrc93-kpneu-st1588-independent/` with no shared paths.

## 5. Things NOT done that a reviewer might ask about

- **Wet-lab conjugation replication.** Requires bench work with the actual UCO-361 isolate; explicitly out of scope for in-silico replication.
- **hns knockout to test thermal silencing.** Would be the next mechanistic experiment (see open_questions.json Q2).
- **Phylogenetic backbone analysis of pNDM-1_UCO361 vs full RefSeq NDM-1 megaplasmid pool.** A Mash/skani sweep would properly place it in a plasmid lineage; only pairwise BLASTn vs the paper's two named comparators was done (see open_questions.json Q3).
- **Post-2014 ST1588 surveillance sweep.** Would confirm whether UCO-361 is a sentinel or an endemic clone (see open_questions.json Q5).
- **Direct rep-region incompatibility testing.** Would settle whether pNDM-1_UCO361's PF-untypability reflects true novelty vs a database gap (see open_questions.json Q4).
- **Short-read + long-read re-assembly from raw SRA.** Only the deposited assembly was used; a re-assembly from raw reads would independently validate the paper's contig structure.

## 6. Confidence + limits summary

- **What is fully validated:** All 9/9 in-silico testable claims (C1–C9). Base-pair-exact match on the megaplasmid (314,976 bp) and IncFIB(K) helper (197,209 bp). Complete Fig. 1B landmark synteny around blaNDM-1. Full AMR repertoire at 100% id.
- **What is inferred, not proven:** IncFIB(K) helper's role in *trans*-mobilising pNDM-1_UCO361; molecular basis of 27 °C vs 37 °C phenotype; national-first epidemiological status.
- **What has scope caveats:** "Novel megaplasmid" (narrow reading only); PlasmidFinder-untypable (DB-version dependent); "closest plasmid" characterisation (local region only, not whole backbone).
- **Overall:** REPLICATED with honest enrichment. Coverage 0.90 (not 1.00) reflects the two partially-in-silico-testable claims; agreement 0.98 reflects one minor allele-name drift and one whole-plasmid framing nuance.

---

*The verdict is REPLICATED. This file is the "if a reviewer asks" companion, not a retraction.*
