# Failure Analysis — Yuan et al. 2019 Replication (BVBRC-09)

**Verdict kept:** REPLICATED ✅ (19/19 in-silico testable claims verified/partially-verified; 4 wet-lab claims correctly flagged NOT_TESTED)
**But:** the "REPLICATED" label understates several genuine gaps and shortcuts. This document catalogs them honestly so downstream users can weight the evidence appropriately.

---

## 1. What was NOT actually reproduced (as opposed to substituted)

The original REPORT.md's Method-Substitutions table frames every tool swap as "standard equivalent." Some of these swaps are genuinely equivalent; others are close-enough surrogates whose numerical differences are then attributed to the swap without evidence.

| Paper method | Our substitute | Actually equivalent? |
|---|---|---|
| CGE MLST v2.0 (2019 snapshot) | Kleborate v3.1.3 (2026 snapshot) | Same 7-locus scheme, but **PubMLST database drift** — this is why pgi=2 (ours) vs pgi=3 (paper). We never pinned the 2019 PubMLST snapshot date to check whether pgi allele 3 was still current then and was retired since, or whether the paper allele-called incorrectly. **Not fully verified.** |
| CGE ResFinder v3.1 | ABRicate + ResFinder db (2026) | Different DB vintage. Coverage-of-claim: verified. Numerical %-identity: not exact for oqxA/oqxB (99.06/98.95 vs 100%). |
| CGE PlasmidFinder v2.0 | ABRicate + PlasmidFinder db | Same idea. IncHI1/IncFIB vs repB_KLEB_VIR + RepB_1_pC39 — **not the same nomenclature.** We wrote "different naming conventions" but did not check whether repB_KLEB_VIR is actually the same replicon type as IncHI1, or whether PlasmidFinder v2.0 in 2019 would have called it IncHI1. |
| CSI Phylogeny 1.4 | Parsnp v2.1.5 + Gubbins v3.4.3 + RAxML-NG | These are DIFFERENT pipelines. CSI Phylogeny uses reference-based mapping without recombination filtering; parsnp does MUM-based core-genome alignment; Gubbins strips recombinant tracts. **Result: SNP counts differ by ~4x (53 vs 198 for SCNJ1↔SCLZ15-011).** We hand-waved this as "expected methodological difference." Never actually re-ran CSI Phylogeny to prove reproducibility. |
| OrthoFinder + FastTree (IncX3) | Mash (k=21, s=1000) + NJ (Biopython) | Structurally different: OrthoFinder does protein orthogroup MSA + concatenation; Mash does k-mer distances. Topological conclusions can differ especially for small backbone plasmids with high mobile-element flux. We took "closest neighbor = pNDM_MGR194" as agreement without an ARF/RF distance check between the two trees. |
| Prokka + RAST | Kleborate + ABRicate | Substantially reduced scope: we did gene-presence detection but not full-genome annotation. Any claim requiring gene neighborhood or ORF-level structural information (e.g. the IS26-ΔctuA1-tat-trpF-bleMBL-blaNDM-5-ΔISAba125-IS5-ΔISAba125-IS3000-ΔTn2 cassette) was **not verified structurally** — we only confirmed blaNDM-5 presence. The mechanistic story about IS-mediated cassette formation was not tested. |

**Honest assessment:** we verified that the *outputs* the paper claims exist can be independently detected. We did NOT verify that the paper's specific pipelines produce those outputs given the paper's exact inputs.

---

## 2. Data-source mismatch: draft vs complete assembly

The paper describes a draft assembly (29 contigs, 5,474,953 bp, SPAdes on Illumina HiSeq 2000 reads). We used the subsequently-deposited complete genome **GCF_008320705.1** (RefSeq, 3 replicons, 5,448,483 bp) — deposited AFTER the paper.

**Consequences of this shortcut:**
- Genome-size and GC-content comparisons are between different assembly types, not two runs of the same analysis. The 26,470 bp difference (5,474,953 - 5,448,483) is glossed as "expected (complete ≠ draft)" — but we never quantified how much is chromosome-level completion vs contamination-removal vs assembly-error-correction.
- pVir-SCNJ1 size difference (211,807 vs 211,858 bp = +51 bp) is likewise glossed as "draft→complete." Could equally be a real difference between GenBank submission MK715436 (the original paper deposit) and the RefSeq re-annotation NZ_CP174530.1. We should have downloaded MK715436 directly and compared byte-for-byte. **We did not.**
- The paper's MLST calls were done on the DRAFT assembly. Ours were on the COMPLETE assembly. If pgi call differs because of a contig-boundary artifact in the draft, we would never see it in our data. This is a plausible alternative explanation to the "PubMLST database drift" story that we did not test.

**Would-be-clean approach:** download raw reads from SRA (BioProject linked to SPSD00000000), re-assemble with SPAdes at the same version the paper used (SPAdes ~3.13, circa 2019), and re-run Kleborate on that. We did not do this.

---

## 3. Wet-lab claims flagged NOT_TESTED — but no partial in-silico proxies attempted

The 4 wet-lab claims are legitimately impossible to reproduce from sequence alone:
- String test (35 mm hypermucoviscosity)
- G. mellonella survival (0% at 10^5 CFU/ml, 72h)
- Conjugation frequency (10^-6)
- MIC values (imipenem >256, meropenem >256, colistin 2 μg/ml)

However, some of these have in-silico proxies that we did not run:
- **MIC prediction:** tools like ResFinder-4, KleborateCARD, or PATRIC/BV-BRC AMR prediction give phenotype hypotheses from the AMR gene profile. We could have checked whether our detected AMR gene set predicts the reported phenotype pattern. **Not done.**
- **Conjugation-competence:** the pNDM5-SCNJ1 conjugation module (pir, bis, parA, hns, topB, plus the paper's stated "gene cluster responsible for conjugation") can be annotated and compared to reference conjugative IncX3 plasmids to sanity-check whether conjugation is at least mechanistically possible. We did not do this cassette-level check.
- **Hypervirulence score:** Kleborate v3 reports a virulence score of 4 (highest); we reported this. It is an in-silico proxy for the G. mellonella phenotype but was not framed as such in the report.

**Honest note:** the "wet-lab NOT_TESTED" bucket was used as a get-out-of-jail for 4 claims when at least 2 (MIC, conjugation) could have been partially interrogated in silico.

---

## 4. Phylogeny Phase-2 chain-of-custody issue

The 60-genome ST29 phylogeny and 231-plasmid IncX3 phylogeny (Phase-2, done on chiatta00) closed the two previously NOT_REPLICATED items. Two friction points:

1. The Phase-2 run happened after a subagent-gateway-close at 40 min; the final Dropbox sync was manual. There is no automated record of the exact command lines, only summary JSON. Reproducibility is therefore partial: we know what tools+versions ran, but not the exact parameter set (bootstrap count for RAxML-NG — was it truly 100, or a different value the summary rounded?).
2. Parsnp collapsed 5 identical-sequence pairs (GCA_900173655/625, GCA_900501625/GCA_900507205, GCA_002845925/GCA_002870985). These were reported but not explained: are these true replicates in NCBI (same isolate deposited twice), or biologically distinct isolates that happen to have identical core alignments? We assumed the former. This could inflate or deflate the perceived diversity of the ST29 pool.

---

## 5. Discrepancies we CALLED "within tolerance" without a defined tolerance

- pVir vs pLVPK: 94% coverage / 99.58% identity (ours) vs 93% coverage / 99.71% identity (paper). Called "verified within tolerance." **No tolerance was defined.** The 0.13% identity difference on a ~200 kb plasmid is ~260 nucleotide differences — non-trivial at the sequence level, but small in the context of overall similarity.
- pVir vs pL22-1: 99% cov / 99.73% id (ours) vs 99% cov / 99.99% id (paper). Called "partially verified." Again, the 0.26% identity gap is ~550 nt differences. We did not investigate whether this is a genuine assembly difference or a BLAST-parameter difference (word size, expect value, dust filter).

**Fix pattern:** for future replications, define a-priori tolerance bands (e.g. ±1% identity, ±5% coverage) and flag anything outside as a genuine discrepancy requiring investigation, not a "close enough."

---

## 6. Missing central-corpus artifacts (this backfill pass)

- **Marker:** central SCOUT/OSTI Marker parse not found by paper sha256 (204f058d324790ee989f89629bd54778c6712df94f51129a69b52a70c7e27906). Fallback: pdftotext -layout, which captures body text well but degrades on the multi-column layout and figure captions of ARIC's PDF template.
- **Nougat:** no GPU available in this backfill session; extraction/nougat.mmd is a pending stub with sha256 for later corpus sweep. Table S4 (IncX3 plasmid metadata, 230 entries) is in a Supplementary DOCX file, NOT in the main PDF — so no OCR of the main PDF alone will recover the plasmid list. **Any downstream re-analysis of the IncX3 corpus requires pulling the .docx from PMC directly.**

---

## 7. What is needed to close the gaps

| Gap | What closes it | Effort |
|---|---|---|
| PubMLST snapshot mismatch (pgi=2 vs 3) | Fetch PubMLST git history for K. pneumoniae scheme; check whether pgi=3 was retired 2019-2026 | 1 hour |
| CSI Phylogeny SNP-count discrepancy | Re-run CSI Phylogeny 1.4 on the same inputs | 4-8 hours (server-side queue) |
| Draft vs complete assembly bleed | Download SRA reads for SPSD00000000; re-assemble with SPAdes 3.13; re-Kleborate | 2-4 hours + compute |
| MK715436 vs NZ_CP174530.1 byte diff | curl both, diff | 15 minutes |
| MIC in-silico prediction | Run BV-BRC AMR prediction module | 30 minutes |
| Conjugation cassette annotation | Prokka + manual curation of pNDM5-SCNJ1 transfer region | 2 hours |
| rmpA2 truncation coordinates | Extract ORF; MUSCLE align to pLVPK rmpA2 | 30 minutes |
| Central Marker/Nougat parse | Ingest paper.pdf into SCOUT pipeline on uicgpu A100 | queued corpus sweep |
| Phase-2 phylogeny parameter capture | Re-run with logged command lines; check bootstrap count | 4-8 hours |

**Total to fully close:** approximately 1-2 person-days of focused work + 1-2 GPU-hours + 1 PBS queue slot for CSI Phylogeny.

---

## 8. Bottom line

The REPLICATED verdict is CORRECT at the coarse claim level — every in-silico thing the paper says can be reproduced independently. But the verdict papers over:
- 6+ instances where "equivalent tool" glossed real methodological differences
- A ~4x SNP-count discrepancy that was hand-waved rather than resolved
- Use of a completed genome instead of the paper's draft, without a byte-level check that this doesn't introduce artifacts
- Two claims (MIC, conjugation) that had in-silico proxies we never attempted
- Undefined "tolerance" language protecting sub-percent identity gaps
- Missing central Marker/Nougat parse (pending)

**Confidence:** HIGH that the paper's main biological conclusion (ST29/K54 hypervirulent K. pneumoniae carries blaNDM-5 on an IncX3 plasmid nearly identical to pNDM_MGR194) is correct. MEDIUM that all the paper's specific numerical claims (198 SNPs, %-identity tables, exact allele calls) would reproduce byte-for-byte if the paper's exact pipeline were re-run on the paper's exact data. LOW-MEDIUM that the paper's evolutionary-history inferences (ancestral vector pEC14_35, "first NDM-5 in ST29") would survive scrutiny with modern dated phylogenetics.
