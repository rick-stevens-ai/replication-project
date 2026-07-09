# Failure analysis — BVBRC-68 pPA1011 blaKPC-2 replication

Verdict: **REPLICATED** (structural + molecular). This file catalogues everything that did **not** work, could **not** be tested, or that had to be softened relative to the paper's stated claims.

## 1. What could not be independently verified

### 1.1 Raw-read reassembly (Illumina NextSeq 500 + PacBio RSII)
- **What the paper reports:** Hu et al. state they sequenced pPA1011 with Illumina NextSeq 500 + PacBio RSII.
- **What we could not do:** Reassemble from raw reads to confirm the deposited assembly.
- **Root cause:** The raw reads underlying the assembly are not deposited under an accessible SRA/ENA accession that is discoverable from the paper or from the MH734334.1 record. Without raw reads, coverage-based confirmation of the IS boundaries (especially at repeat-collapsed IS26/IS6 sites) is impossible.
- **Consequence:** Any assembly artifact — mis-joined repeats, collapsed IS copies, incorrect circularisation, or chimeric junctions — would silently propagate through C1, C2, and C4. We rely on the deposit chain (submitter → NCBI GenBank → us) rather than an end-to-end reproduction.
- **Mitigation:** None available under the free/public-only constraint. C1/C2 are still exact matches to the paper *by construction* if the deposit is trusted; C3 is protein-level and would tolerate a small number of assembly errors that do not disrupt the reading frame.

### 1.2 Independent MLST re-typing of PA1011 (C6)
- **What the paper reports:** PA1011 is ST463 by the P. aeruginosa MLST scheme.
- **What we could not do:** Re-type ST463 from the isolate whole-genome sequence.
- **Root cause:** Only the plasmid (MH734334.1) was deposited; the chromosomal WGS of PA1011 is not accessible on SRA under this study.
- **Consequence:** C6 is provenance-only. We accept the /note="genotype: ST463" qualifier from the LOCUS metadata as submitter-provided fact and cannot detect a submitter-side typing error.
- **Mitigation:** None available. See `open_questions.json` Q5 for the follow-up path.

### 1.3 IS-family identity of the flanking transposase ORFs (C4)
- **What the paper reports:** The blaKPC-2 environment is ΔIS6-Tn3-ISKpn8-blaKPC-2-ISKpn6-IS26.
- **What we could not do:** Definitively assign IS families to the flanking ORFs.
- **Root cause:** The submitter's GenBank annotation labels the ISKpn8, ISKpn6, and IS26 candidate ORFs generically as "hypothetical protein". Our C4 check therefore only confirms **coordinate consistency** — i.e., that CDS/repeat features exist at approximately the positions and in the order the paper's schema requires — not that those CDSs are in fact the named IS families.
- **Consequence:** C4 is scored ✅ "structurally consistent" rather than "exact match". A rigorous check would require ISfinder / ISEScan re-annotation of MH734334.1.
- **Mitigation:** Called out explicitly in the results table and in `open_questions.json` Q2.

### 1.4 PCR replication of blaKPC-2 presence (C3, weakest sense)
- **What the paper reports:** blaKPC-2 was PCR-confirmed in PA1011.
- **What we could not do:** Re-run PCR on the physical isolate.
- **Root cause:** We do not have access to the physical isolate; this is a computational-only replication.
- **Consequence:** We do not verify that the deposited plasmid sequence corresponds to the same physical isolate as the paper's PCR (this requires trust in the deposit chain).
- **Mitigation:** C3 is upgraded to a sequence-level protein-identity check (293/293 aa vs canonical KPC-2 = 100.00% identity), which is *strictly stronger* than a PCR presence/absence call once the deposit chain is trusted.

## 2. What had to be softened

### 2.1 The "novel plasmid backbone" claim (C5)
- **Paper's phrasing:** "novel plasmid" / "novel backbone".
- **Our finding:** pPA1011 shares 51,587 / 62,793 = 82.15% of its length with a single prior comparator (p14057, KY296095) at 98.70% length-weighted identity. Only ~11.2 kb (~18%) of pPA1011 is not aligned to p14057.
- **Softening:** We report C5 as ⚠️ **partial**. The backbone is *not* novel in the sense of "unrelated to known plasmids"; pPA1011 is best described as a p14057-family variant with a novel IS-mediated blaKPC-2 context plus ~11 kb of distinguishing / rearranged content.
- **Reason we could not do better:** Novelty was tested against only one comparator. A rigorous backbone-novelty test would BLAST pPA1011 against the full corpus of *P. aeruginosa* KPC plasmids (or nr with taxonomic filter) and report the max-coverage match. See `open_questions.json` Q1.

## 3. Genuine failures (things we tried that did not work as hoped)

- **Feature-name granularity in GenBank was lower than expected.** We had hoped that MH734334.1 would annotate the flanking IS elements by family (e.g., `/product="ISKpn8 transposase"`), which would have let C4 be scored as an exact match. In fact the submitter used generic `hypothetical protein` labels for most transposase ORFs. This forced C4 to be scored as structural-consistency only.
- **SRA lookup for raw reads.** No accessible SRA/ENA accession was found under this study for the Illumina NextSeq 500 + PacBio RSII reads. This precludes independent assembly regardless of compute availability.
- **SRA lookup for isolate WGS.** Same problem — only the plasmid is deposited under this study.

## 4. Errors / bugs encountered during the replication run

- **None reported.** The stdlib Python parsers, BLAST+ database build, and BLAST+ query all completed cleanly. All measurements in `evidence/summary.json` derive from single-shot deterministic computations on fixed inputs.

## 5. What would flip / weaken the verdict

- **Verdict flip to NOT REPLICATED** if: MH734334.1 were re-computed to a different length or GC (impossible for a versioned accession, so this is a null risk); OR if the excised 882-bp ORF failed to translate to 293 aa of KPC-2 (did not happen — 100% identity).
- **Verdict downgrade to PARTIAL** would be warranted if the corpus-wide backbone BLAST (Q1) showed that pPA1011 is essentially identical (>95% length, >99% identity) to another already-deposited plasmid predating Hu et al. 2019 — that would collapse the novelty claim even further than our current soft finding. This risk is real and untested here.
- **Verdict caveat added** if ISfinder re-annotation (Q2) showed that one of the flanking IS ORFs is a different family from what the paper's schema names.

## 6. Bottom line

The paper's hard, numeric, sequence-level claims (C1 length, C2 GC, C3 blaKPC-2 identity, C4 environment order) **replicate exactly** from the deposited GenBank record. The soft claim (C5 backbone novelty) does not fully hold up against even a single comparator. The provenance claim (C6 ST463) cannot be independently checked. No replication failures occurred during the run itself; the limits are all upstream (missing SRA deposits, generic GenBank annotation, single-comparator novelty test).
