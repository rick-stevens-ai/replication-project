# Failure Analysis — BVBRC-66 (Sadek 2020, *E. hormaechei* blaVIM-1 + mcr-9)

**Verdict:** REPLICATED. This file documents where the replication was nonetheless \*imperfect\*, what \*failed\* in the pipeline, and what would strengthen the result. The point is honesty, not blame.

---

## 1. Hard failures (things that did not work as expected)

### 1.1 LLM-judge — Claude Opus 4.8 and 4.7 both returned 3× 502 errors

- **Symptom:** Argo proxy at `127.0.0.1:44497` returned HTTP 502 Bad Gateway for the identical judge prompt against Claude Opus 4.8 (3 attempts) and Claude Opus 4.7 (3 attempts).
- **Root cause:** Argo upstream availability, not this pipeline.
- **Recovery:** Fell back to Claude Sonnet 4.6, which succeeded on first attempt with the same prompt.
- **Impact:** None on the underlying evidence (which is deterministic BLAST output); the LLM was only used to score / summarise. The judge output is stored as an ancillary artifact, not as an arbiter.
- **Prevention:** Standing model-cascade rule (Opus → Sonnet → Haiku) already in place; this is expected behaviour of a free-tier Argo path.

### 1.2 SRA record SRR11478637 is a placeholder — raw reads unavailable

- **Symptom:** `sra-tools` prefetch returned an object with only 5 spots / 5.2 Mb total — nowhere near a real Illumina + Nanopore submission (should be tens of GB).
- **Root cause:** Depositor submission-form artifact. The assembled genome length (~5.2 Mb) was entered where per-read counts should have been. Nanopore fast5 was never deposited at all.
- **Recovery:** No recovery possible. Verified the deposited \*assembled\* molecules (CP053190–CP053194.1) directly instead of re-running assembly from reads.
- **Impact (large):** Full \*de novo\* re-assembly is impossible. Any assembly artifact silently propagates into our checks (see §2.1).
- **Prevention:** Not within scope; this is a NCBI data-deposition gap that would require contacting the depositor.

### 1.3 IS903 canonical query hit at 87.6% id, not 100%

- **Symptom:** MK479294.1 (canonical IS903 tnpA + mgrB, 1,209 bp) matched pMS-37a at 87.6% identity across 1,062 bp — well below the 99–100% we saw for every other query.
- **Root cause:** IS903 is a variant \*family\* (IS903B, C, D sub-lineages from different Enterobacteriaceae). The ISfinder canonical allele is not necessarily the exact allele that colonised pMS-37a.
- **Recovery:** Accepted the hit on the basis of (a) length ≈ full IS903, (b) position 133 bp 5' of *mcr-9* (matches paper), (c) high specificity within the plasmid.
- **Impact (moderate):** The claim survives at 2/3 rather than 3/3 by the LLM-judge scoring. A strict "100% id or nothing" reviewer could challenge it as a family-level rather than element-level confirmation.
- **Prevention:** Would need ISfinder curator sub-family assignment (open question OQ2 in `open_questions.json`).

## 2. Soft failures / known limitations

### 2.1 Cannot validate assembly correctness from reads

Every replicon we tested was the deposited assembled molecule; the underlying Unicycler assembly step cannot be re-derived. Specific risks:

- **Mis-joins across repetitive IS elements.** IncHI2 backbones are laced with IS elements; Nanopore + Illumina hybrid usually resolves these correctly, but a mis-oriented segment or missed junction would be invisible to us.
- **Dropped small plasmids.** If a 5th small plasmid existed and was filtered out at the Unicycler graph-simplification step, we would never see it.
- **Copy number.** Coverage-based confirmation of *mcr-9* / *bla*<sub>VIM-1</sub> copy number is impossible without reads.

**Mitigation:** none available with public data as of 2026-07-02.

### 2.2 Phenotype (colistin MIC 0.5) is not reproducible from sequence

The paper's ``silent *mcr-9*'' framing depends on the colistin-susceptible MIC of 0.5 µg/mL, which cannot be verified from sequence. We have \*genetic\* support for the mechanism (mcr-9 present, downstream qseB/qseC absent from the plasmid), but the causal link between "no qseC/qseB" and "colistin-S" is a paper \*hypothesis\* that we can neither confirm nor falsify from public data alone.

**Mitigation:** would require recovering the strain from a culture collection and re-doing broth microdilution.

### 2.3 Chromosomal qseBC copies raise a trans-regulation question

Our tblastn found bona-fide *qseB* (80.7% aa id, 218 aa) and *qseC* (69.5% aa id, 449 aa) copies on the chromosome (CP053190.1 near position 3.93 Mb). The paper's model requires the plasmid *mcr-9* to be regulated \*in cis\*; whether the chromosomal QseBC can trans-activate *mcr-9* is unaddressed by the paper. This is not a bug in the replication — it is a scientific gap that our replication newly \*surfaces\* (open question OQ1).

### 2.4 tetA at 95%: variant, not perfect match

`tet(A)_6_AF534183` scored 95% id / 94% qcov on pMS-37a — above ResFinder's 80/60 threshold but not perfect. The paper does not specify which *tetA* allele it detected, so this is a soft mismatch rather than a discrepancy. Multiple *tet(A)* sub-alleles exist; the pMS-37a copy is likely a divergent variant.

### 2.5 ΔaadA22 identified as truncated aadA1

The paper reports ΔaadA22 (a truncated variant of *aadA22*). Our best hit was `aadA1_5_JX185132` at 100% id / **90% qcov** — the truncation is consistent with a Δ-form, but the specific allele call (`aadA22` vs. `aadA1`) is not resolvable at the BLAST level without a strain-specific reference. Called it a match on the basis of the truncation matching the paper's Δ note.

### 2.6 Dependency on live upstream databases

- PubMLST scheme allele set and ST profile table are pulled live at run time. If PubMLST is unreachable, MLST fails. If PubMLST curators renumber an allele (rare but possible), a rerun could produce a different call.
- ResFinder and PlasmidFinder are pulled from Bitbucket HEAD; both are actively curated and gene names/allele numbers evolve.
- **Mitigation:** snapshot each database with a git commit hash at run time so a rerun is deterministic.

## 3. What would definitively strengthen the replication

Ranked by cost-effectiveness:

1. **(Cheap, ~1 hour)** Snapshot PubMLST / ResFinder / PlasmidFinder DB state at run time (git commit + tarball) to lock reproducibility across future reruns.
2. **(Cheap, ~1 day)** Submit the pMS-37a IS903 region (positions 136,074–137,131) to the ISfinder curator for formal sub-family classification (IS903B/C/D vs. novel).
3. **(Medium, ~1 week)** Contact the depositor / NCBI to have the raw Illumina fastq + Nanopore fast5 deposited so a full \*de novo\* re-assembly becomes possible.
4. **(Medium, ~2 weeks + wet lab)** Recover the strain from culture collection; re-do broth-microdilution colistin MIC + qPCR of *mcr-9* expression to verify the silent-*mcr-9* phenotype.
5. **(Expensive, ~1 month + wet lab)** Chromosomal *qseBC* knockout + plasmid-borne *qseBC* complementation experiment to test whether trans-activation by chromosomal QseBC contributes to *mcr-9* silencing (or lack thereof).
6. **(Expensive, ~1 quarter of desk work)** Pan-plasmid analysis of all NCBI IncHI2/mcr-9 plasmids to see whether the specific IS903-mcr-9-IS1 + no-qseBC architecture is a recurrent motif or a one-off (open question OQ3).

## 4. What did NOT fail

For balance:

- **Isolate resolution:** clean single-hit BioSample from a minimal `esearch` query. No ambiguity.
- **MLST:** 7/7 loci at 100%/100% → ST279 exactly. No tie-breaking, no partial calls.
- **AMR gene calling:** 6 of 8 pMS-37a genes at 100%/100%; the two others (tetA 95%, dfrA1 99.79%) are still comfortably above thresholds.
- **Plasmid Inc typing:** IncHI2 + IncHI2A at 100%/100% on the correct plasmid.
- **IS1 downstream:** 99.87% id, 4 bp 3' of *mcr-9*. Textbook.
- **qseB/qseC absence on plasmid:** conclusively demonstrated (only a 27%-id paralog on pMS-37a; real copies on chromosome as expected).
- **Complete assembly:** 5 circular replicons, sizes match paper.
- **Pipeline runtime:** minutes on a laptop. No cluster needed. No paid API calls. Zero cost.

## 5. Summary

The replication itself is strong. The failure modes are (a) an LLM upstream 502 handled by cascade, (b) an SRA data-deposition gap that blocks reassembly, (c) an IS903 sub-family ambiguity that is a real biological open question rather than a pipeline bug, and (d) a phenotype-vs-sequence gap that no amount of desk work can close.

None of these overturn the REPLICATED verdict on the genomic claims. They correctly mark the boundary between what \*was\* replicated (all deposited-sequence-derived claims) and what \*could not be\* (raw-read reassembly and wet-lab MIC).
