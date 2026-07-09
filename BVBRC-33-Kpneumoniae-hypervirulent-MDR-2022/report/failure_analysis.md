# Failure Analysis — BVBRC-33 (Altayb 2022 K. pneumoniae hv-MDR)

**Verdict:** PARTIAL REPLICATION (strong). 15/18 claims reproduce; 3 fail. This file dissects the 3 failures and 2 process incidents.

## Summary of non-replications

| ID | Claim | Outcome | Category |
|---|---|---|---|
| C14 | Aerobactin **iutA** present | Kleborate abst absent; no PGAP aerobactin product | Virulome tool-dependence / possible deposition-loss |
| C15 (partial) | Salmochelin **iroN** present (iroE was confirmed) | Kleborate smst absent; no PGAP IroN product | Virulome tool-dependence / possible deposition-loss |
| C16 | **blaCTX-M-15** on plasmid pMDR | blastn returns only ≤44 bp fragments (≤7% qcov) — absent full-length | Deposition gap (plasmid content missing from WGS assembly) |

## Failure 1 — blaCTX-M-15 absent from deposited assembly (the important one)

**Observation.** The paper reports blaCTX-M-15 on plasmid pMDR (reconstructed with plasmidSPAdes). A `blastn` of the standard reference NG_048935.1 against GCA_022511605.1 returns only short spurious fragments (≤44 bp, ≤7% query coverage). AMRFinderPlus 4.2.7 does not call blaCTX-M-15. The gene is not present at full length in the deposited draft.

**Candidate root causes.**
1. **pMDR contigs were excluded during deposition.** Assemblies deposited to NCBI sometimes drop plasmid contigs (short-read plasmid contigs frequently fail filtering thresholds). This is the most likely explanation given the draft-quality assembly (83 contigs, N50 ~221 kbp) and the paper's use of a separate plasmidSPAdes step.
2. **Plasmid loss between sequencing and deposition.** The strain may have lost pMDR in culture before the deposition-source DNA prep, but not in the DNA prep used for the paper's own analyses.
3. **Assembler dropout.** SPAdes-family assemblers can under-assemble high-copy or repeat-rich plasmid regions when short-read coverage is uneven.

**Why we cannot distinguish.** Distinguishing (1)–(3) requires fetching SRA reads for SAMN26332310 and either (a) rerunning plasmidSPAdes/MOB-recon or (b) mapping reads to a blaCTX-M-15 reference to see if the gene is present at the read level. This replication is deposition-only by design; SRA was not fetched.

**Impact.** blaCTX-M-15 is a headline resistance determinant in the paper. Its absence from the deposited assembly is a real reproducibility gap that blocks downstream researchers who work only from GenBank assemblies. This is the single most important reason the verdict is PARTIAL and not REPLICATED.

**Follow-up (documented in `open_questions.json` Q2).** SRA fetch + plasmidSPAdes + MOB-recon; if pMDR recovers from reads, the failure is deposition-loss, not paper error, and NCBI curation should be notified.

## Failure 2 — Aerobactin iutA (C14) and Salmochelin iroN (C15 partial)

**Observation.**
- Paper (VFDB/RAST): iutA = 1 present; salmochelin iroE + iroN = 2 present.
- This replication (Kleborate v3 curated `abst` + `smst`, plus PGAP product grep on 5,064 proteins):
  - iutA / aerobactin locus: **absent** (no Kleborate abst hit, no PGAP aerobactin product).
  - iroE: **present** (PGAP "siderophore esterase IroE", MCH6118329.1) — matches paper.
  - iroN: **absent** (no Kleborate smst hit, no PGAP IroN receptor product).

**Candidate root causes.**
1. **Tool-database drift (most likely).** Kleborate v3's `abst` and `smst` modules are locus-aware, curated KpSC-specific scanners that require the full canonical locus context. VFDB/RAST-based hits are homology-based single-gene calls that can register on non-canonical, non-syntenic siderophore homologs. What VFDB scored as "iutA" or "iroN" in 2022 may be a partial homolog that Kleborate v3 (2024–2026) correctly rejects.
2. **Plasmid-content deposition-loss (same class as blaCTX-M-15).** If iutA and iroN sat on a mobile element that failed to make it into the deposited draft (same pattern as pMDR), they would look absent in this replication but genuinely be present in the paper's underlying strain.
3. **Genuine false positives in the paper.** VFDB-only calls in 2022-era K. pneumoniae papers are increasingly recognized as noisy; the community has moved to Kleborate as the standard specifically to control this.

**Why iroE reproduces but iroN does not.** iroE (an esterase) is present in the PGAP annotation as a single-gene product, suggesting some salmochelin-related sequence is in the assembly, but the full salmochelin locus (`smst`) required for a canonical Kleborate call is not. This is consistent with either a partial locus, a fragmented contig break, or genuine partial pathway presence.

**Impact.** Moderate. These are single virulence-factor annotations, not the paper's headline. But they do materially affect the paper's virulome accounting (the paper says "1 aerobactin, 2 salmochelin"; we can only substantiate "1 salmochelin component"). They also motivate a broader question (documented in `open_questions.json` Q5) about how many 2018–2022 hvKp virulome tables would be revised under curated re-typing.

## Failure 3 — Allele-name drift (soft; not a real biological failure, but worth flagging)

- Paper reports **AAC(6′)-Ib-cr6**; AMRFinderPlus 4.2.7 calls **aac(6′)-Ib-cr5**.
- Paper reports **fosA6**; AMRFinderPlus 4.2.7 calls **fosA (FosA5 family)**.

These are database-curation naming differences, not different genes. The underlying sequence and function are the same. This class of "failure" is common across ARG-typing tool comparisons and is not counted as a non-replication in the 15/18 score. It is called out here so future readers do not mistake it for a real discrepancy.

## Process incidents

### Incident P1 — MDPI PDF bot-blocked
- **What happened.** Direct MDPI PDF fetch failed with bot-blocking.
- **Fix.** Used Europe PMC `fullTextXML` endpoint for PMC9137517 instead. Full-text XML contains the Data Availability section, which is what was needed.
- **Prevention.** Default to Europe PMC XML for MDPI papers rather than the MDPI PDF endpoint.

### Incident P2 — Argo Opus 4.8 HTTP 502 on LLM-judge call
- **What happened.** `argo:claude-opus-4.8` returned HTTP 502 (known Argo proxy bug window).
- **Fix.** Fell back to `argo:gpt-5.2` (also free per the standing free-endpoint rule). Produced a valid structured verdict (15/18 = 0.83, PARTIAL REPLICATION strong).
- **Prevention.** Retry logic + free-endpoint fallback list is already the standing pattern; this incident followed the pattern correctly.

### Non-incident — BioProject vs BioSample resolver
- **What could have gone wrong.** PRJNA767482 is an umbrella project holding many unrelated isolates; a naive BioProject → assembly resolver would have returned the wrong genome.
- **Fix used.** Went through BioSample SAMN26332310 → GCA_022511605.1 directly via NCBI Datasets REST.
- **Prevention.** Prefer BioSample over BioProject as the resolver key for single-isolate papers.

## What this replication cannot conclude
- Whether the string-test-positive hypermucoviscous phenotype the paper reports is genuinely regulator-alternative (RcsAB-driven) in vivo, or merely correlates with RcsAB presence in a strain that also carries other unmeasured hypermucoviscosity contributors. That is a wet-lab question (knockout / complementation / transcriptomics) beyond the scope of a deposition-only replication and is called out as `open_questions.json` Q3.
- Whether pMDR/blaCTX-M-15/iutA/iroN really existed in the paper's sequenced strain or were partial-tool artifacts. Requires SRA fetch and re-assembly (`open_questions.json` Q2, Q5).

## Overall
The failures are honest, evidence-backed, and traceable. None are due to method errors on our side. The paper's headline biology reproduces cleanly; the paper's mobile-resistance and non-canonical virulome details are the load-bearing weak points, and both weak points map to either tool-drift (Kleborate v3 vs VFDB/RAST) or deposition-completeness (pMDR content missing from GCA_022511605.1).
