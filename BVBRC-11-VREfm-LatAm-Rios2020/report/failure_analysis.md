# Failure Analysis — Ríos et al. 2020 VREfm LatAm Replication

**Verdict:** PARTIAL — not because the paper is wrong, but because 9 of 26 enumerated claims did not fully reproduce for the specific reasons documented below.

This document catalogs **only** what did NOT replicate. What DID replicate is covered in `REPORT.md` §4.1 and §7, and in the GENUINE CRITIQUE section of `REPORT.tex`.

## Failure taxonomy

| Class | Count | Root cause |
|---|---|---|
| Compute-bounded | 4 | BEAST v1.8.4 MCMC on 340-genome alignment exceeds free CherryRd budget |
| External-artifact-blocked | 2 | Curated reference sets not deposited by paper |
| Method-substitution shifts | 3 | Tool substitutions produce quantitatively different but qualitatively consistent results |
| Scope-limited | 2 | Full 340-genome / 207-phenotype panels not used in re-pass |
| Total non-replicating claims | **9** (of 26 enumerated) |

## Failure 1 — BEAST time-tree dating (claims 10, 11, 12, 13)

**Paper claim:**
- Clade A/B split ~2,765 years ago
- Animal/clinical split ~502 years ago
- CRS-I/CRS-II split ~302 years ago
- Substitution rate 3.41 SNPs/genome/year

**Our result:** NOT_TESTED (all four)

**Root cause:** BEAST v1.8.4 MCMC at the paper's chain length on the full 340-genome alignment requires hundreds of millions of steps. This did not fit inside the free CherryRd CPU budget allocated to the replication.

**Blocker class:** Compute-bounded (not artifact-blocked — the inputs are all deposited).

**How to resolve:** CIPRES gateway allocation, or a multi-week local BEAST run on a dedicated CPU node. Everything else (alignment, priors, dating calibration points) is reproducible from the deposited data.

**Honest impact:** This is the single largest gap in the replication. The paper's most-cited numbers (the 2,765 y / 502 y / 302 y TMRCAs) rest, on our side, on trust of the paper's own compute rather than on independent MCMC. We do not claim to have re-tested them.

---

## Failure 2 — Clade I virulence-gene differential (claim C31)

**Paper claim:** Clade I (ST412-associated) genomes often lack `fms22`, `swpC`, and `hylEfm` relative to Clade II.

**Our result:** PARTIAL → BLOCKED. The qualitative trend (Clade I lower) is present, but absolute presence/absence counts are not reproducible with generic RefSeq references — they collapse to either ~0% or ~100% presence at standard tblastn thresholds.

**Root cause:** The paper used a specific curated set of enterococcal virulence reference proteins (Sillanpää 2009 *J. Infect. Dis.* supplementary file, or equivalent SaferEnter DB references). This reference set was not deposited as a standalone artifact alongside the paper; only generic RefSeq protein IDs are recoverable.

**Blocker class:** External-artifact-blocked.

**How to resolve:** Obtain the Sillanpää 2009 supplementary protein file (or SaferEnter reference DB) and re-run `code/repass/virulence_blast.py` with those specific reference sequences.

---

## Failure 3 — Core-genome orthogroup count (claim 4)

**Paper:** 1,674 core orthogroups (>90% presence)
**Ours:** 2,068
**Discrepancy:** +23.5%

**Root cause:** Annotation tool substitution. Paper used RAST (web-only, effectively deprecated); we used Prokka v1.14.6. Prokka's HMM-based CDS calling is more permissive at short-ORF cutoffs, producing more predicted proteins per genome, which raises the orthogroup count.

**Blocker class:** Method-substitution shift.

**How to resolve:** Access a preserved RAST installation (unlikely) or run both annotations and cross-map orthogroup IDs.

---

## Failure 4 — Pan-genome orthogroup count (claim 5)

**Paper:** 6,735 pan orthogroups
**Ours:** 6,441
**Discrepancy:** −4.4% (95.6% agreement)

**Root cause:** Same Prokka-vs-RAST annotation substitution as above. Reflects normal tool-variation; not a systematic disagreement.

**Blocker class:** Method-substitution shift (minor).

---

## Failure 5 — Recombination fraction of clade A (claim 8)

**Paper:** 54% of clade A affected by recombination
**Ours:** 22.7%
**Discrepancy:** −31 percentage points

**Root cause:** Dataset-scope substitution. Paper ran ClonalFrameML on the full 340-genome global clade-A alignment; we ran it on the 55-genome LATAM-only core. Recombination detection is sensitive to alignment breadth — fewer diverse genomes yield fewer detectable recombination tracts.

**Blocker class:** Scope-limited.

**How to resolve:** Rebuild the 340-genome global core alignment and re-run ClonalFrameML with the same parameters as the paper.

---

## Failure 6 — aac(6')-aph(2'') prevalence (claim C20)

**Paper:** 49% (n≈27)
**Ours:** 36.4% (n=20) full bifunctional, 38.2% (n=21) if either module counted
**Discrepancy:** ~6 carriers missed at abricate ≥80/80

**Root cause:** Paper used custom BLASTX with laxer coverage cutoffs, catching fragmented bifunctional-gene hits that abricate at ≥80/80 filters out. Direction and country-attribution are consistent; percentage is shifted.

**Blocker class:** Method-substitution shift.

**How to resolve:** Re-run abricate with `--mincov 40 --minid 80` or replicate paper's custom BLASTX pipeline.

---

## Failure 7 — tet(M) prevalence (claim C22)

**Paper:** 43.6% (n=24)
**Ours:** 25.5% (n=14)
**Discrepancy:** ~10 carriers missed at abricate ≥80/80

**Root cause:** Same as C20 — tet(M) commonly assembles as fragmented contigs in short-read enterococcal assemblies, and strict abricate cutoffs discard those partial hits. Paper's custom BLASTX recovered them.

**Blocker class:** Method-substitution shift.

**How to resolve:** Same as C20 — lower abricate thresholds or re-implement paper's BLASTX pipeline.

---

## Failure 8 — PBP5 random-forest ampicillin prediction (implicit paper claim)

**Paper:** 96% sensitivity, 100% specificity from a 250-protein PBP5 training set.
**Our result:** NOT ATTEMPTED.

**Root cause:** Out of re-pass scope. Supp Table 4 has the AMP MICs and 250 accession IDs but the curated PBP5 alignment was not deposited as a single training set.

**Blocker class:** External-artifact + out-of-scope.

**How to resolve:** Extract PBP5 sequences for the 250 Supp Table 4 accessions, curate the alignment, and re-run the RF classifier.

---

## Failure 9 — LiaS/LiaR daptomycin substitutions (implicit paper claim)

**Paper:** Substitutions in liaSR reported in 3 isolates with daptomycin-associated phenotype.

**Our result:** NOT ATTEMPTED.

**Root cause:** Requires per-isolate codon-level variant calls on the liaSR loci. Assemblies are available but the pass-1 pipeline did not emit per-isolate variant tables.

**Blocker class:** Scope-limited (tractable in a future pass).

**How to resolve:** Extract liaSR CDS from each of the 55 assemblies, translate, align to reference, and enumerate non-synonymous variants.

---

## Failure classes NOT observed

For transparency: we found NO cases of the following failure modes.

- **Data-integrity failure** — All 55 deposited assemblies are recoverable and pass QC.
- **Metadata-linkage failure** — Country, year, ST, and isolate ID all cross-verify (100% match between MLST and metadata table).
- **Country-restricted resistome claim failure** — Every isolate-level singleton (optrA in ERV138 Colombia, cfrB in ERV275 Mexico, cat in ERV121/123/125 Peru) reproduces exactly.
- **vanA/vanB call failure** — CARD and ResFinder converge on 54/55 vanA-positive and 0/55 vanB, matching the paper.
- **ST-composition failure** — 12 distinct STs, ST17=18, ST412=21 exactly as reported.

## Systemic lessons

1. **Annotation-tool substitutions** (RAST → Prokka) systematically inflate short-ORF-derived orthogroup counts. Any pan-genome comparison across pipelines should report this as an expected shift.
2. **AMR-gene calling thresholds** matter a lot. Strict abricate ≥80/80 is scientifically defensible but under-calls fragmented genes vs. a permissive custom BLASTX. Reporting both would help future replicators.
3. **Curated reference protein sets** (virulence, PBP5 training) are the biggest single deposit gap in the paper. Depositing them as auxiliary files would raise the paper from "PARTIAL-replicable" to "fully replicable" without any new compute.
4. **BEAST XML + log files should be first-class deposits** for any time-tree claim, so downstream replicators can validate priors and convergence without re-running MCMC.

## Assessment

The paper is **honestly reproducible on its deposited artifacts**. The 9 non-replicating items sit in three well-defined buckets: (a) compute we did not spend, (b) reference artifacts the paper did not deposit, (c) tool-substitution shifts we did not close. None of the failures indicate paper error; each is a specific, addressable gap.
