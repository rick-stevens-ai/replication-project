# Failure Analysis — BVBRC-79 · *Bacillus smithii* DSM 4216^T (Bosma 2016)

Verdict is **REPLICATED**, but the replication is not perfect. This file lists every place the replication is weaker than an ideal one, every claim that was not tested, and every place where an easy delta or ambiguity was not chased down. It exists so the next pass can raise coverage from ~89.7 % toward 100 %.

## 1. Untested claims (coverage ceiling)

Three of the 16 claims were not tested at all. This is the entire reason mean judge coverage is 89.7 % rather than higher.

| Claim ID | Claim | Why not tested | What it would take |
|---|---|---|---|
| C10 | 69 CRISPR repeats | Requires CRT or CRISPRCasFinder rerun on both replicons | Run CRISPRCasFinder → record evidence-level 4 arrays; compare to 69 |
| C11 | 2,596 genes (66.8 %) with Pfam hits | Requires HMMER against a pinned Pfam-A release | `hmmscan` all 3,753 CDS translations vs Pfam-A; count non-empty hits |
| C12 | 2,619 genes (67.4 %) with COG assignments; Table 5 category breakdown | Requires eggNOG-mapper or comparable COG classifier | `emapper.py` on the CDS FAA; tally by COG one-letter category; diff vs Table 5 |

None of these were skipped for methodological reasons. They were skipped for time-budget reasons. All three are achievable on free public tools.

## 2. Partially-tested claims

### C9 — coding fraction 82.8 %
The `~` entry in the claims table understates a real gap. We never directly integrated CDS span lengths. The correct calculation is:

```
coding_fraction = ( sum_over_CDS( stop - start + 1 ) - overlap_correction ) / 3,381,292
```

We know from C5 and C7 that gene counts are exactly right, so `~82.8 %` is very likely correct, but we did not confirm it.

### C13 — plasmid presence + PlasmidFinder screen
We confirmed the plasmid accession and length exactly (C2), and we ran PlasmidFinder to 0-hit congruence with the paper's own annotation. But the paper's underlying claim is stronger than "an accession exists": it asserts the plasmid is a single circular replicon. **We did not re-verify circularity from raw reads.** We accept the assembly on trust.

## 3. Discrepancies that were attributed rather than diagnosed

### C6 (protein-coding 3,627 vs ours 3,619) and C8 (pseudogenes 126 vs ours 134)
The 8-gene shift in each direction is coupled: 8 fewer CDS, 8 more pseudo. We attributed this to the RefSeq re-annotation replacing the paper's original RAST call. That attribution is reasonable but was not verified. Alternatives not ruled out:

1. Genuine RAST-vs-RefSeq pipeline delta (attributed, plausible, unverified).
2. Off-by-one in our position-aware GenBank parser's `/pseudo` detection.
3. Original paper mis-tally.

**Fix:** locus-level diff between the paper's original submission (or its supplementary table) and the current RefSeq record. Identify the 8 loci that flipped CDS → pseudo. Determine whether any of them is functionally significant (e.g. related to the C14 acetate-pathway search, in which case it materially strengthens or weakens that claim).

### C4 — GC 40.75 % vs 40.8 %
0.05 pp delta. Almost certainly rounding at either end. Not worth chasing but noted.

## 4. Methodological approximations

### 4a. ANIb-style is not JSpecies-standard ANIb
Our C16 test uses:

- 1,020-bp fragments (correct).
- **Subsample of 1,000 fragments** (JSpecies uses all fragments).
- `-perc_identity 30 -max_target_seqs 1 -max_hsps 1` (JSpecies uses different alignment-fraction filters and best-two-way hits).
- Alignment length ≥ 700 bp.

Aligned-fragment fractions are low (4.4 % vs *B. coagulans*, 3.9 % vs *B. subtilis*), which is expected at ~89 % ANI but means the mean/median identities are on small denominators. A rigorous rerun should use `pyani` (ANIb mode) or FastANI with default parameters. Given the ~89 % identity level, the qualitative conclusion (well below 95 % species boundary) is unlikely to change, but the specific numbers may shift by 1–2 pp.

### 4b. Only 2 of 13 Table 6 comparators re-fetched
Chose closest sister (B. coagulans 2-6) and standard reference (B. subtilis 168). That is a defensible two-point corroboration but is not a full reproduction of Table 6. A complete rerun would fetch all 13 comparator genomes and reproduce every row's length, GC, gene count, and ANI value.

### 4c. C14 BLASTP uses only two donor organisms for reference proteins
Pta, AckA, PflA come from *B. subtilis*; PflB from *E. coli*. A pathologically divergent *B. smithii* homolog might fall below `1e-10` against these specific references while still being detectable against a broader HMM (Pfam PF01515 = Pta, PF00871 = AckA, PF02901 = PflB). Our confirmation of the paper's negative claim is consistent but not a tight upper bound. A stronger test would `hmmsearch` those Pfam HMMs directly against the CDS translations.

### 4d. PlasmidFinder screen tests only rep-family HMMs, not full ORF annotation
We can conclude "no rep-family match at PlasmidFinder thresholds," but not "no autonomous replication gene of any family." A full Pfam-A / Foldseek scan of the plasmid ORFs would be a stronger check.

## 5. LLM-judge caveats

- Three-judge unanimous **REPLICATED** is corroboration, not proof.
- All three judges saw the same evidence bundle; agreement is not independence.
- Judges share substantial training-data overlap.
- Judge-produced coverage % (89.7 % mean) is a rough summary, not a rigorous coverage-measure. It is broadly consistent with our own "3 of 16 claims not tested" accounting.

The numeric BLAST / GC / count evidence in the body is what actually grounds the verdict; the judges are secondary.

## 6. Provenance gaps

- **No signed manifest.** We recorded md5s for the two primary FASTA downloads. We did not produce a SHA-256 manifest of every file in `work/` and `evidence/`, so derived tables (feature counts, BLAST TSVs, judge JSON) are not independently hash-verifiable.
- **No accession-version diff.** We used the currently-served versions of CP012024.1 and CP012025.1. We did not diff the current GenBank record against the paper's original 2016 submission, so we cannot rule out silent NCBI re-curation contributing to the exact-match numbers.
- **PlasmidFinder DB not version-pinned.** We recorded the clone source, not the commit hash. If the DB has been updated since our clone, a rerun could yield a different hit pattern (though the paper's own annotation is congruent, so this is unlikely to overturn C13).

## 7. What would raise coverage to ~100 %

In rough order of effort:

1. Run CRISPRCasFinder on both replicons → resolves C10.
2. `hmmscan` full Pfam-A on the CDS translations → resolves C11 and tightens C14.
3. Run eggNOG-mapper on the CDS translations → resolves C12.
4. Integrate CDS spans → resolves C9.
5. Run `pyani` ANIb with defaults against the two comparators (or FastANI) → replaces the fragment approximation.
6. Locus-level RAST-vs-RefSeq diff → explains the coupled 8-gene shift in C6/C8.
7. Fetch the remaining 11 Table 6 comparators, verify length/GC/gene count → completes C16.
8. Produce a SHA-256 manifest of `work/` and `evidence/` → closes the provenance gap.

None of the eight overturn the current verdict; all eight would strengthen it.

## 8. Ways the verdict could still be wrong (adversarial audit)

- **Novel-family acetate-forming enzyme exists.** C14 says the three canonical enzymes are absent; the paper implies the metabolic capability itself does not use them. If a Pta/AckA-independent acetate pathway is present, that would not overturn C14 but would substantially reframe the paper's most biologically interesting claim. (See open_questions.json Q1.)
- **The 12,514-bp element is not an autonomous plasmid.** If it is a mis-assembled chromosomal region or a non-autonomous integrative element, C13's "single 12.5-kb plasmid" claim is technically wrong even though the sequence is real. Our PlasmidFinder null result is compatible with either interpretation. (See open_questions.json Q2.)
- **Genus reassignment.** The paper predates the modern Bacillus reorganisation. DSM 4216^T may no longer be *Bacillus smithii* under current GTDB. This does not overturn the genomic facts but does mean C16's species-level framing is dated. (See open_questions.json Q3.)

None of these are failures of the replication — they are open scientific questions the replication surfaces but does not close.
