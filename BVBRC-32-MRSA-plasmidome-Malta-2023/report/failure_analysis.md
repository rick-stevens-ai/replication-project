# Failure Analysis — BVBRC-32

Honest accounting of what did **not** reproduce in the independent
re-analysis of Al-Trad et al. 2023 (MRSA plasmidome, HSNZ Kuala
Terengganu, Malaysia; DOI 10.3390/antibiotics12040733).

Overall verdict: **PARTIAL replication** (LLM-judge `argo:gpt-5.2`).
This file catalogues the failures behind that "PARTIAL" and their
root causes.

---

## Failure 1 — Naming mismatch (task ledger vs paper)

**Symptom.** Task brief tagged this replication `-Malta-2023`; the paper
is Malaysia (HSNZ Kuala Terengganu), not Malta.

**Root cause.** Ledger-side mislabel. CrossRef DOI 10.3390/antibiotics12040733
and PMID 37107095 both confirm Malaysia. Not a replication failure; a
naming failure upstream.

**Impact.** None on the replication itself — all analysis is on the
correct paper. Directory name retained for ledger continuity per REPORT.md.

**Prevention.** Ledger entries should include the CrossRef-confirmed title
and BioProject as fields, not just a location keyword.

---

## Failure 2 — Sample delta: 88 recovered vs 94 cited (C1 denominator)

**Symptom.** Paper cites 94 total MRSA (79 sequenced + 15 previously
published); the replication recovered 88 GCA assemblies from PRJNA722830.

**Root cause.** The 15 previously published Malaysian MRSA genomes
(AOCQ/ANPO/AMRB/AMRC/AMRD/AMRE00000000 + PRJNA503680) were not pulled;
only the study's own submissions under PRJNA722830 were retrieved.

**Impact.** All replication percentages are relative to 88. C1
(plasmid-carriage) is reported as 85/88 vs paper's 85/94 — the plasmid-free
absolute count (3) matches exactly, but the base rate is slightly
inflated.

**Prevention.** Future retrievals should explicitly enumerate the paper's
external-genome accession list at Stage 2 and pull those alongside the
BioProject.

---

## Failure 3 — 74% plasmid-resistance headline did not reproduce as an equal number (C7)

**Symptom.** Paper: **74% (140/189)** of plasmids carry resistance.
Replication: **~47%** of replicon contigs carry AMR or biocide genes.

**Root cause (compound, not decomposable without more work).**
1. **Unit mismatch.** "Plasmid" in the paper is a curated, PCR-gap-closed
   molecule (n=189). "Replicon locus" in the replication is a rep hit on a
   draft contig (n=279). Multi-replicon plasmids inflate the locus count.
2. **DB coverage.** The paper's numerator includes **heavy-metal operon**
   hits (cadAC/cadDX/czcD/mer). Neither ResFinder nor DisinFinder carries
   these; the replication's numerator is AMR + qac only.

**Impact.** Verdict for C7 is PARTIAL / NOT-TESTED, not VERIFIED. This is
a real gap. Cannot be closed without (a) plasmid gap-closure and (b) a
curated heavy-metal operon DB.

**Prevention.** Report proportions in explicit units (per curated
molecule vs per replicon locus vs per genome). Never compare a
per-molecule proportion to a per-contig proportion without flagging it.
Add BacMet or a project-curated HM operon DB to the replication stack.

---

## Failure 4 — Heavy-metal operon sub-counts entirely untested (C11)

**Symptom.** Paper reports cadAC 46, cadDX 26, czcD 2, mer 6. Replication
reports **NOT TESTED** for all of these.

**Root cause.** ResFinder and DisinFinder do not carry cadAC/cadDX/czcD/mer.
No dedicated heavy-metal operon reference DB was assembled for this
replication.

**Impact.** One entire claim row unverified. Verdict is honestly recorded
as NOT TESTED rather than fabricated as VERIFIED.

**Prevention.** Integrate a heavy-metal operon DB (BacMet, MetalRes, or a
project-specific curated set) into the CGE BLASTn pipeline as a
standard fourth screen alongside PlasmidFinder / ResFinder / DisinFinder.

---

## Failure 5 — 2nd/3rd tier replicase rank does not match exactly (C4)

**Symptom.** Paper: RepA_N=57, Rep_1=54 (as the 2nd/3rd tier). Replication:
RepA_N=60 loci, Rep_1=57, Rep_3=58 — same top tier but the exact rank of
Rep_1 vs Rep_3 flips when counted as loci vs curated plasmids.

**Root cause.** Same unit-mismatch as Failure 3: locus count vs curated
plasmid count. Additionally, the paper treats some RepA_N + Rep_3
co-occurrences as multireplicon plasmids (contributing 39 combined to
Rep_3's tally), which the replication cannot resolve without gap closure.

**Impact.** C4 verdict is PARTIAL. Top-tier membership is confirmed;
exact order is not.

**Prevention.** Report per-superfamily counts in both units (loci and
genomes) and treat "which is second" as a resolution-dependent question,
not a fixed rank.

---

## Failure 6 — Extra Inc18 signal not in the paper's 7 superfamilies

**Symptom.** Replication detects Inc18 (rep16) in 20 genomes; the paper
does not report Inc18 as one of its 7 superfamilies.

**Root cause.** DB-version / threshold-sensitivity difference, most
plausibly. Either the paper's PlasmidFinder run predated the Inc18
additions in the Gram-positive DB, or the paper applied a stricter
filter that suppressed borderline Inc18 hits.

**Impact.** Not treated as a contradiction. Documented as an "extra" in
REPORT.md and this failure log. No claim of novel discovery.

**Prevention.** Pin the CGE PlasmidFinder DB commit hash used in each
replication; compare to the paper's stated retrieval date. If the paper
does not state a date, note the DB version as a replication caveat.

---

## Failure 7 — LLM judge downgrade (opus-4.8 → gpt-5.2)

**Symptom.** Intended judge `argo:claude-opus-4.8` returned HTTP 502;
final verdict rendered by `argo:gpt-5.2`.

**Root cause.** Argo endpoint transient failure on the opus-4.8 proxy at
run time.

**Impact.** Per-claim judgments should be treated as ordinal, not
calibrated. Overall verdict "PARTIAL REPLICATION" is consistent with the
per-claim table (8 verified / 2 partial / 1 not tested) and does not
appear to be a judge-model artifact, but this cannot be proved without a
re-run.

**Prevention.** Retry the judge with `opus-4.8` (or better) once the
proxy is healthy; record both verdicts if they disagree.

---

## Failure 8 — blaTEM allele-family cross-hit (manual exclusion)

**Symptom.** A single genome produced weak `blastn` hits to the entire
Enterobacterales `blaTEM` allele family in the ResFinder DB (n=1 each).

**Root cause.** ResFinder ships all alleles including Enterobacterales
β-lactamases. Raw allele-level counting will collect cross-family weak
hits.

**Impact.** Excluded manually from the plasmid-AMR tally.
Non-principled exclusion: reproducible only because it is documented.

**Prevention.** Filter ResFinder DB by expected organism family before
BLASTn, or apply a stricter identity threshold (≥95%) for β-lactamase
allele calls. Add an automated post-BLAST filter that flags multi-allele
hits within a single family as suspicious.

---

## Failure 9 — Scope exclusions (SNP phylogeny, spa/ST typing, virulence)

**Symptom.** REPORT.md does not verify any of: SNP-based epidemiology,
spa/ST typing, PVL/tst/enterotoxin virulence-gene detection.

**Root cause.** Deliberate scope decision — replication targets the
plasmidome and AMR-gene layers only.

**Impact.** Real, and acknowledged in REPORT.md §Genuine Critique. Any
downstream claim about clonal lineage, outbreak epidemiology, or
virulence-plasmid carriage is out of scope for this replication.

**Prevention.** These belong in a follow-up (see `open_questions.json`
Q4 and Q5 for concrete next steps).

---

## Aggregate lesson

The "PARTIAL" verdict is driven overwhelmingly by two categories of
failure:

1. **Unit-mismatch failures** (Failures 3 and 5) — comparing per-molecule
   curated counts to per-contig locus counts. Fixable only by long-read
   plasmid gap-closure.
2. **DB-coverage failures** (Failures 3 and 4) — heavy-metal operons not
   in ResFinder/DisinFinder. Fixable by integrating a dedicated HM DB.

Neither is a substantive disagreement with the paper. The paper's
qualitative plasmidomic story reproduces robustly on an independent
pipeline.
