# Failure Analysis — BVBRC-64 Lactobacillus reuteri PNW1

**Verdict:** REPLICATED (strong). This file catalogues what was **NOT** replicated, what was only **PARTIALLY** replicated, and what was **NOT REACHABLE** in silico, plus the root cause of each gap. None of the items below invalidate the overall verdict; they qualify it.

## Category A: Hard failures (a paper claim was directly contradicted)

**None.** No test performed here contradicts any claim in Alayande et al. 2020.

## Category B: Partial confirmations (claim not exactly reproduced, but consistent)

### B1. D-lactate dehydrogenase named CDS
- **Paper claim (C3):** D-lactate dehydrogenase (EC 1.1.1.28) is present.
- **This replication:** PGAP annotation of the deposit contains NO CDS with the literal name "D-lactate dehydrogenase". It contains **4 CDSs** annotated `D-2-hydroxyacid dehydrogenase` (ROV59554.1, ROV60471.1, ROV62790.1, ROV63523.1).
- **Root cause:** Annotator conservatism. `D-2-hydroxyacid dehydrogenase` is the Pfam / enzyme-family name that includes D-LDH; PGAP does not commit to substrate specificity without experimental evidence. The paper used RAST, which is more willing to assign a specific EC number based on best-hit homology.
- **Fair verdict:** ✅ consistent, name-only mismatch attributable to annotator naming policy. Underlying biology is present.
- **How to fully close:** run RAST (or Bakta with the same reference set the paper used), or perform a substrate-specificity assay on the recombinant enzyme.

### B2. Helveticin J named CDS
- **Paper claim (C3):** Bacteriocin **helveticin J** is present.
- **This replication:** PGAP annotation contains 1 CDS annotated `>ROV54067.1 bacteriocin, partial` and does NOT commit to any bacteriocin subfamily. Literal "helveticin" appears 0 times in `protein.faa`.
- **Root cause:** Same as B1 — RAST commits to the class-III subfamily label; PGAP does not. Additionally, the CDS is flagged as `partial`, so PGAP may be unable to identify subfamily-defining residues.
- **Fair verdict:** ✅ consistent, bacteriocin CDS is present, subfamily assignment differs by annotator.
- **How to fully close:** BLAST ROV54067.1 against BAGEL4 / BACTIBASE curated bacteriocin databases; if the top hit is a helveticin-family class-III bacteriocin at reasonable e-value and identity, the paper's specific label is confirmed.

### B3. CRISPR arrays with associated Cas
- **Paper claim (C6):** 5 CRISPR CDSs, each associated with Cas genes (CRISPRFinder).
- **This replication:** MinCED v0.4 finds **0 CRISPR arrays** on the deposited FASTA. Output GFF is empty.
- **Root cause:** Assembly fragmentation. The deposited assembly has 420 contigs and N50 ≈ 28 kb. CRISPR arrays are internally repetitive and are frequently broken across contig boundaries in short-read SPAdes assemblies. MinCED cannot resolve an array that spans a contig break.
- **Fair verdict:** ⚠️ **partial (null-result-under-tool-choice, not contradiction).** The paper's claim is not confirmed by my independent tool, and is not contradicted either.
- **How to fully close:** Nanopore-sequence PNW1 to ≥100× coverage, hybrid-assemble, then rerun MinCED / CRISPRCasFinder.

### B4. Prophage count (2 intact regions)
- **Paper claim (C6):** 2 intact prophage regions (PHASTER).
- **This replication:** PGAP annotation contains 31 phage- or integrase-related CDSs, including one clean structural module (phage terminase small subunit + portal + major capsid + tail tape measure + multiple tail proteins + 14 integrases). Consistent with ≥1 and plausibly ≥2 prophage regions.
- **Root cause:** PHASTER is a paywalled hosted service and was not rerun (standing "free-endpoints-only" policy for this project). Also, PHASTER's specific `intact / incomplete / questionable` classification is not directly recoverable from raw PGAP CDS names.
- **Fair verdict:** ✅ consistent; exact count not re-verified.
- **How to fully close:** run VirSorter2 or Phigaro (both FOSS) on the FASTA, or submit to PHASTER manually.

## Category C: Not reproducible in silico (constitutively out of scope)

### C1. Bacteriocin agar-well-diffusion assay vs STEC O177 (paper claim C7)
- **Paper measured:** crude supernatant zone = 20.0 ± 1.00 mm; partially purified (0.25 mg/ml) = 23.3 ± 1.15 mm against Shiga-toxigenic *E. coli* O177.
- **Why unreachable:** Requires the live *L. reuteri* PNW1 isolate and a STEC O177 tester strain. Not an in silico operation.
- **Fair verdict:** ❌ **not testable in silico by construction.** Not counted against the paper.

### C2. PathogenFinder human-pathogen probability
- **Paper claim (C5):** PathogenFinder reports probability = 0 that PNW1 is a human pathogen.
- **Why not rerun:** PathogenFinder is a hosted CGE service that requires web submission with rate limiting; not a self-hostable FOSS CLI at the time of this replication under the free-endpoint policy.
- **Compensating evidence:** Zero VF hits across 3 independent databases (VFDB, VICTORS, ecoli_vf) plus only 2 narrow-spectrum LAB-typical AMR genes — the paper's "zero pathogen probability" is **entirely consistent** with the independent VF screen, but not **independently reproduced by the same tool**.
- **Fair verdict:** ✅ consistent (via proxy).

## Category D: Paper-level concerns the paper does not discuss

These are not replication failures per se, but issues surfaced by the replication that the paper does not mention. They belong in the peer-review layer.

### D1. RefSeq mirror is suppressed as "contaminated"
- **Observation:** NCBI's assembly warnings field: `warnings: ["contaminated"]`. RefSeq mirror GCF_003790365.1 was removed by RefSeq staff: *"This record was removed by RefSeq staff. Reason: contaminated."* The GenBank record GCA_003790365.1 remains live and is what the paper analyses.
- **Impact:** The paper does not mention this. Fine-grained gene inventory (especially *absence* claims) should be treated with more caution than the paper implies. Contamination inflates apparent gene content, weakening absence claims.
- **Impact on this replication:** AMR/VF calls (C4, C5) target well-characterised loci with high sequence identity and are unlikely to be affected. But the "only lnu(C) and tet(W)" absence claim IS in principle weakened.

### D2. Assembly is fragmented
- **Observation:** N50 = 28,048 bp, L50 = 24, 420 contigs.
- **Impact:** This is the mechanistic reason B3 (CRISPR) failed. Also limits confidence in prophage count and in any mobilome-vs-chromosome location assignment.

### D3. tet(W) is a PGAP-annotated pseudogene (`frameshifted`)
- **Observation:** The same tet(W) locus that all four AMR databases call at 100% coverage is flagged by PGAP as `pseudo=true, Note=frameshifted, product=tetracycline resistance ribosomal protection protein Tet(W)`.
- **Impact:** The paper's homology-based *presence* screen is correct. Whether the strain is phenotypically tetracycline-resistant is a separate question the paper did not test with a MIC. For EFSA QPS purposes (feed-additive safety), presence-based screening is the required screen — but the qualification (functional or not?) matters for the paper's implicit safety framing.

## Root-cause summary

| Category | Item | Root cause |
|---|---|---|
| B1 | D-LDH named CDS missing | RAST vs PGAP naming policy |
| B2 | Helveticin J subfamily missing | RAST vs PGAP naming policy; CDS also `partial` |
| B3 | CRISPR arrays absent | Assembly fragmentation (N50 ≈ 28 kb) |
| B4 | Prophage count not re-verified | Paywalled tool (PHASTER); free-endpoints-only policy |
| C1 | Bacteriocin assay | Constitutively in vitro |
| C2 | PathogenFinder | Paywalled hosted service |
| D1 | RefSeq suppression | Paper omission; NCBI contamination flag |
| D2 | Fragmentation | Short-read SPAdes on a MiSeq run in 2018; is what it is |
| D3 | tet(W) pseudogene | PGAP flags it; homology screens miss the frameshift |

## Net take

**No failures that undermine the REPLICATED verdict.** The two annotator-attributable gaps (B1, B2) are consistent-with-paper. The one truly partial result (B3, CRISPR) is a null-under-tool artifact, not a contradiction. The remaining items (C1, C2) are constitutively out of scope for in silico replication. The Category-D observations are peer-review-layer concerns about the paper's framing, not replication failures.
