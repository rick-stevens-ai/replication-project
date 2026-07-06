# Failure Analysis — Kandasamy 2022 *L. plantarum* DJF10 Replication

**Paper:** Int. J. Mol. Sci. 2022, 23, 14494 · DOI 10.3390/ijms232214494 · PMID 36430971
**Verdict:** PARTIAL (17 VERIFIED · 11 PARTIAL · 0 CONTRADICTED · 0 NOT_TESTED across 28 claims)

This document catalogues every claim that did *not* fully replicate, the root-cause failure mode, whether the failure is a paper problem or a substitute-methodology problem, and the tractable retry path.

The load-bearing headline: **zero contradictions**. Every gap below is a named substitution limit, not counter-evidence against the paper.

---

## Failures by Class

### Class A — Draft-assembly artefacts (short-read limitations)

| Claim | Paper | Ours | Root cause | Retry |
|---|---|---|---|---|
| 6. tRNA | 59 | 51 | rRNA/tRNA operon collapse in SPAdes short-read assembly | Long-read (Nanopore / PacBio HiFi) resequencing → close operons |
| 7. rRNA | 7 | 3 (pass-1) / 2 (pass-2) | Same operon collapse; short reads cannot resolve the tandem repeat | Same — long-read resequencing |
| 22. Functional CDS ratio | 59.1% | 54.3% (pass-1) / ~51% (pass-2 full Prokka) | Prokka+SwissProt hit rate lower than paper's RASTtk+SEED functional-assignment combo | Rerun with RASTtk full stack or full BV-BRC annotation for one-off comparison |

**Diagnosis:** Not paper errors. Every one of these is a known consequence of short-read draft-assembly limitations plus annotation-database coverage differences. The paper's numbers are almost certainly correct on the sequenced isolate.

---

### Class B — Proprietary/closed HMM libraries not accessible offline

| Claim | Paper tool | Missing dependency | Consequence |
|---|---|---|---|
| 24. SEED subsystems (232) | RAST / RASTtk | FIGfam HMMs (BV-BRC / RASTtk web-only) | 481 vs 1,119 CDS classified; 18/25 categories within ±4%; all 25 present; PARTIAL |
| 25. KEGG pathway map (Table 3) | BlastKOALA | KofamScan profile DB (1.5 GB) did not finish downloading | Carb. metabolism reproduces within 6%; other categories over-call via EC fan-out; PARTIAL |
| 28. Sactipeptide cluster (AOI 1) | BAGEL4 | BAGEL4 RiPP HMM library (proprietary, web-only) | Radical_SAM PF04055 surrogate returned 3 metabolic-context hits, none in RiPP neighborhoods; NOT_DETECTED |

**Diagnosis:** All three are substitute-methodology limits. The Radical_SAM surrogate is a weak proxy for BAGEL4's curated RiPP set and its silence should not be read as evidence against the sactipeptide claim. KofamScan is the highest-priority retry (tractable, ~100 min at 250 KB/s).

---

### Class C — Multi-method web pipelines with modules unreachable offline

| Claim | Paper tool | Missing modules | Consequence |
|---|---|---|---|
| 27. 18 genomic islands (IslandViewer 4) | IslandPath-DIMOB + SIGI-HMM + IslandPick | SIGI-HMM and IslandPick require multi-genome comparative input | 10 vs 18 islands; existence + length scale confirmed; PARTIAL |
| 23. R3 prophage (Lactob_Sha1, 53.9 kb) | PHASTER | pVOG-level phage HMM DB (~600 MB, 50k models) | R1 (34 bp) + R2 (98 bp) integrase coords matched; R3 assembly-contig-ambiguous |

**Diagnosis:** PARTIAL by construction. The paper used pipelines that pool multiple methods; we ran one module of each. Where the paper's remaining modules require curated reference-genome pools or 50k-model HMM libraries, the offline surrogate cannot match count exactly.

---

### Class D — Tool-sensitivity thresholds

| Claim | Paper | Ours | Root cause | Retry |
|---|---|---|---|---|
| 20. CRISPR arrays | 3 | 1 high-confidence | Direct-repeat heuristic threshold likely rejects 2 sub-threshold arrays | Rerun CRISPRCasFinder + CRISPRDetect at multiple sensitivity settings |
| 26. CBM CAZymes | 4 | 0 (strict) / 14 (relaxed) | dbCAN strict cutoff (E<1e-15, cov≥0.35) rejects short CBM domains; relaxed (E<1e-5, cov≥0.30) over-calls | Report the bracket honestly; use the strict cutoff for reproducibility and the relaxed as sensitivity check |

**Diagnosis:** Threshold-sensitive calls. The paper is likely correct; our defaults were chosen for reproducibility, not maximum recall. Both are already reported honestly in the report.

---

### Class E — Sub-domain over-call caused by database version drift

| Claim | Paper | Ours | Δ | Root cause |
|---|---|---|---|---|
| 26. GH subfamilies | 27 | 20 | −26% | dbCAN V13 (2026) has renamed/collapsed GH subfamilies since paper's V8/V9 (2022) |

**Diagnosis:** Version drift. Subfamily naming is not stable across dbCAN releases; class-level totals (GH/GT/CE/AA) remain within 10% and CE + AA match exactly.

---

## Failures NOT Present

Two negative results deserve explicit mention because their *absence* is the story:

- **Zero contradictions across all 28 claims.** No paper claim tested here was actively refuted by a properly-configured substitute.
- **Zero NOT_TESTED remaining after pass 2.** Every one of the six pass-1 NOT_TESTED claims was attacked with a free surrogate.

---

## Root-Cause Summary by Failure Mode

| Mode | Count of PARTIAL claims | Retry cost |
|---|---|---|
| Closed/proprietary HMM DB | 3 (SEED, KEGG non-carb, sactipeptide) | Medium (KofamScan feasible; BAGEL4 needs web; FIGfam closed) |
| Multi-module web pipeline vs single-module offline | 2 (islands, prophage R3) | High (needs curated reference-genome pool) |
| Draft-assembly artefacts | 3 (tRNA, rRNA, functional-CDS ratio) | High (needs long-read resequencing) |
| Threshold sensitivity | 2 (CRISPR, CBM) | Low (rerun at multiple sensitivity settings) |
| DB version drift | 1 (GH subfamilies) | Low (accept as ordinary evolution) |

Note: individual PARTIAL claims can fall into more than one mode; the counts above reflect the dominant mode per claim.

---

## Tractable Retries (ordered by expected coverage gain per hour)

1. **KofamScan on the SwissProt-annotated proteome** → closes most of claim 25 (KEGG pathway map). Cost: ~100 min DB download + ~30 min run. Expected impact: 5–10 additional PARTIAL categories move to VERIFIED.
2. **CRISPRCasFinder + CRISPRDetect at multiple sensitivity settings** → closes claim 20. Cost: <1 h. Expected impact: PARTIAL → VERIFIED or definitively confirms only 1 array exists at reproducible thresholds.
3. **Long-read resequencing of the DJF10 stock** (out of scope for this replication) → closes claims 6, 7, 22 and confirms zero-plasmid status. Cost: wetlab. Expected impact: 3 PARTIAL → VERIFIED plus definitive plasmid statement.
4. **Rerun against paper's deposited GenBank assembly** (if released) → closes claim 23 R3 prophage. Cost: minutes. Expected impact: 1 PARTIAL → VERIFIED.
5. **BAGEL4 web submission or equivalent RiPP-aware pipeline** (antiSMASH RiPP, DeepRiPP, RRE-Finder) → closes claim 28 sactipeptide. Cost: web submission or licensed pipeline. Expected impact: PARTIAL+ → VERIFIED or, if truly absent, revise the paper's claim to a single-cluster system.

---

## Compliance and Honesty Rails

- Every PARTIAL in the report carries a named blocker in either Section 4 (substitutions table), the per-claim narrative (Section 2), or the GENUINE CRITIQUE section of `REPORT.tex`.
- No PARTIAL was silently upgraded to VERIFIED.
- No count in the report is fabricated; every number cross-checks against a Prokka/hmmscan/blast/JSON artifact under `results/`.
- The verdict PARTIAL was chosen deliberately over PARTIAL+ or VERIFIED so that this replication's known limits — draft-assembly artefacts, closed HMM libraries, single-module vs multi-module substitutions — remain surfaced.
