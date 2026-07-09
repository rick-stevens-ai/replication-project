# BVBRC-113 — Failure Analysis

**Paper:** Nakazono et al. 2022 (PLoS ONE, doi:10.1371/journal.pone.0258283)
**Verdict:** PARTIAL, 74/100
**Purpose of this document:** identify what did *not* replicate cleanly, why, and what would fix each gap.

---

## 1. Failures / partial replications

### 1.1 "pNuk650 has an additional seven ORFs" (Claim C5) — PARTIAL

**What the paper says.** The abstract and Table 2 state pNuk650 has *"an additional seven ORFs"* compared to pIVK45.

**What we measured.** Under every straightforward counting method against the deposited pIVK45 (KP702950):
- Raw CDS count delta: **29 − 17 = +12** additional CDS on pNuk650.
- No-ortholog delta by BLASTP (pident ≥ 30%, qcov ≥ 50%): **+13** pNuk650 CDS with no reciprocal hit in pIVK45.

Neither number is 7.

**Likely root causes.**
1. **Annotation-depth asymmetry.** KP702950 (pIVK45, deposited 2020) is annotated more sparsely than OK031035 (pNuk650, deposited 2021). Small hypothetical proteins, transposase fragments, and one-exon micro-CDS that KP702950 collapses or omits are enumerated separately on pNuk650.
2. **Scope of "additional".** Fig 3A of the paper is a synteny plot; the "+7 ORFs" number likely refers only to CDS inside the ~8 kbp inserted region flanking the shared nukacin cluster — not to every pNuk650 CDS missing from pIVK45.
3. **Custom re-annotation.** The paper may have re-annotated both plasmids with a uniform pipeline (RAST) before counting, in which case the reference for pIVK45 is not the deposited KP702950 annotation but a redone one that is not itself deposited.

**Impact.** Cosmetic/numerical, not structural. The qualitative claim (pNuk650 is larger and carries extra content) is fully supported (+4,320 bp, +12 CDS, +13 no-ortholog CDS).

**Fix.** Re-annotate both KP702950 and OK031035 with Prokka or Bakta under identical parameters and recount. If "+7" then holds up under a restricted "inserted-region-only" definition, document that explicitly.

### 1.2 Epidermin cluster naming — PARTIAL

**What the paper says.** The pEpi56 epi cluster is described as *epiABCDEFGHPQTY*, i.e., 12 letters including epiY.

**What we measured.** The deposited GenBank record OK031036 carries 11 named epi loci: `epiP epiQ epiD epiC epiB epiA epiT' epiH epiF epiE epiG`. There is no CDS explicitly named `epiY` on the deposited record.

**Likely root cause.** epiY on Tü3298 (X62386) exists as a distinct short ORF only because Tü3298 has a truncated `epiT` (`epiT″/Y′` cassette). On pEpi56, which the paper reports carries an intact `epiT`, the "epiY equivalent" would be absent by definition — so the paper's *epiABCDEFGHPQTY* naming is comparative shorthand about the reference cluster, not a factual claim that pEpi56 carries a CDS annotated epiY.

**Impact.** Notational ambiguity, not a structural discrepancy. A pure in-silico verifier that reads only OK031036 cannot enumerate epiY, and there is no gene to enumerate — this is arguably correct behavior, but it renders C8 "full clusters present" only partially auditable from the deposit alone.

**Fix.** Split C8 into two sub-claims: (a) pEpi56 carries a functional epi cluster equivalent to Tü3298's (auditable by orthology, not by gene-name matching), and (b) pEpi56 carries an intact epiT (auditable by CDS length vs Tü3298's truncated epiT).

---

## 2. Not-tested claims (out of scope, not failures per se)

The following claims from the paper are wet-lab and were categorically not testable from public data:

| Claim | Why not testable in-silico |
|---|---|
| Bacteriocin purification via cation-exchange + HPLC | Requires live culture and lab equipment |
| ESI-MS mass verification of mature epidermin / nukacin | Requires purified peptide |
| Plasmid curing with acriflavine, loss-of-activity | Requires strains KSE56 / KSE650 |
| MW2 braRS mutant susceptibility assay | Requires indicator strain + producer strains |
| M. luteus co-culture qPCR | Requires all three organisms + qPCR reagents |
| Antibacterial spectra against 15+ oral/skin commensals | Requires panel of indicator strains |

These are **NOT TESTED** in this replication and are explicitly excluded from the 74/100 score.

---

## 3. Replication-side (methodological) failures / gaps

### 3.1 LLM judge — opus models failed on payload size

- `argo:claude-opus-4.7` returned HTTP 502 on the ~30 kB combined prompt.
- `argo:claude-opus-4.8` returned HTTP 502 on the same payload.
- `argo:claude-sonnet-4.6` completed cleanly and delivered the structured verdict.

**Impact.** The 74/100 score reflects a single model's structured aggregation, not a multi-model consensus. Given that the score is a deterministic rollup of per-claim MATCH/PARTIAL/MISMATCH counts (5 MATCH + 2 PARTIAL out of 8, weighted), a different judge would very likely land in the same PARTIAL band, but this is not independently confirmed.

**Fix.** Retry opus with the payload split into two chunks (evidence bundle, then claims table + verdict request); or run a second judge (e.g., argo:gpt-5.4) and compare.

### 3.2 Marker OCR extraction absent

- The extraction pipeline typically produces `extraction/marker.md` alongside the raw PDF/XML. This file was not present at report-write time.
- All quantitative claims in this replication were anchored on the deposited sequences and the PMC XML text — not on any Marker-parsed table extraction.

**Impact.** None on the sequence-level verdicts (they don't depend on Marker output). Some risk on any Table 2/3 numeric transcription, but those numbers were also cross-checked against the paper text.

**Fix.** Run Marker on the PDF (paper is CC-BY and freely downloadable from PMC) and add `extraction/marker.md` to the artifact set on next pass.

### 3.3 Ortholog thresholds not swept

- Only one BLASTP threshold pair (pident ≥ 30%, qcov ≥ 50%) was tested.
- The +13 no-ortholog count could easily shift by ±2 under different thresholds, but was not swept.

**Impact.** Does not change the qualitative conclusion (delta is much larger than 7), but does not let us claim +12/+13 is a robust point estimate.

**Fix.** Sweep pident ∈ {25, 30, 40, 50} and qcov ∈ {40, 50, 70}; report the resulting range.

### 3.4 No normalized re-annotation of pIVK45

- We accepted KP702950's deposited RAST/GenBank annotation as-is.
- The paper's "+7" figure most likely comes from a re-annotation of pIVK45 with the same pipeline used for pNuk650, which we did not perform.

**Impact.** This is the single largest reason we could not adjudicate the "+7 ORFs" claim more precisely.

**Fix.** Re-annotate both plasmids with Prokka or Bakta at identical settings, then recount.

---

## 4. What would push this replication from PARTIAL (74) toward FULL

1. Resolve the "+7 ORFs" claim by normalized re-annotation of both plasmids (Section 3.4).
2. Refactor C8 into orthology-based sub-claims that don't depend on gene-name gymnastics (Section 1.2 fix).
3. Multi-judge consensus on the verdict (Section 3.1 fix).
4. Marker OCR added for full extraction provenance (Section 3.2 fix).

The wet-lab claims (Section 2) are unreachable by any purely in-silico replication and are not counted against the score.
