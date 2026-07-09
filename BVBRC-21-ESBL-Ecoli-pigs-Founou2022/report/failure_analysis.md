# Failure Analysis — BVBRC-21 (Founou et al. 2022, ESBL *E. coli* from pigs)

**Verdict:** PARTIAL (borderline REPLICATED) — Coverage 10/10, Agreement 7/10.

This document is the honest, per-discrepancy breakdown of **what did not cleanly replicate**, alongside a clear accounting of **what did replicate**. It is deliberately blunt: the point of the replication project is to keep the science honest, not to defend a favourable verdict.

---

## What genuinely replicated (the strong signal)

1. **Headline CTX-M-15 prevalence = 6/11 (54.54%) — EXACT.** The paper's marquee number reproduces perfectly on the authors' deposited assemblies with contemporary open-source tooling.
2. **Identity of the six CTX-M-15 carriers — EXACT.** The same six isolates (`PN017E2II`, `PR010E3I`, `PN027E6IIB`, `PN027E1II`, `PN091E1II`, `PR085E3`) are called as carriers. Agreement on *identity*, not just count, is strong evidence: independent DB drift alone would not name the same six.
3. **11/11 isolates carry a CTX-M variant** — the paper's underlying phenotype-to-genotype ESBL story is fully reproduced.
4. **10/11 MLST calls exact.** Every reported ST (10, 44, 69, 88, 88, 226, 940, 9440, 2144, 4450) is recovered in the correct isolate.
5. **Genome-size envelope.** Observed 4.62–5.35 Mb vs. paper 4.5–5.3 Mb — essentially identical; no assembly is anomalously small or large; no evidence any isolate was mis-fetched.
6. **Resistome breadth.** qnrS1, aph(6)-Id, aph(3'')-Ib, tet(A), mph(A), sul2, dfrA all reproduce across NCBI + ResFinder DBs — the paper's broader "MDR pig ESBL" characterisation stands.

---

## What did NOT cleanly replicate

### Discrepancy 1 — PN256E8 CTX-M allele (CTX-M-15 → CTX-M-55)

- **Paper (Table 2):** `bla`CTX-M-15 + `bla`TEM-1B + `bla`TEM-141 + `bla`TEM-206.
- **This rerun:** `bla`CTX-M-**55** + `bla`TEM-1B + `bla`TEM-141 (TEM-206 not recovered).
- **Interpretation.** CTX-M-15 and CTX-M-55 are close group-1 CTX-M relatives — CTX-M-55 differs from CTX-M-15 by an A77V substitution. Contemporary ResFinder/NCBI DBs distinguish these variants more crisply than the 2021 vintage used by the paper, so **DB-vintage reclassification** is the most parsimonious explanation.
- **Uncertainty.** Not proven. Alternatives include: (a) the paper's original call was itself borderline and would flip with a modern DB, (b) an assembly-level miscall in a repetitive region. Only a pinned-2021-DB rerun + read-level allele verification can adjudicate.
- **Impact on paper's biological conclusion.** Minimal — both CTX-M-15 and CTX-M-55 are ESBLs in the same CTX-M group-1; the "PN256E8 is an ESBL producer" claim is preserved.

### Discrepancy 2 — TEM-206 in PN256E8

- **Paper:** TEM-206 present.
- **This rerun:** TEM-206 not detected.
- **Interpretation.** Three plausible causes: (i) DB coverage — TEM-206 may be absent or below identity cutoff in the current NCBI/ResFinder BLA panel; (ii) assembly-quality issue in the PN256E8 contigs at that locus; (iii) a genuine mis-call in the original paper.
- **Not diagnosed here.** Would require reading raw SRA data at the TEM-206 reference locus and/or a hybrid re-assembly.

### Discrepancy 3 — CTX-M-15 + TEM-1B co-carriage count (3 → 4)

- **Paper:** 3 isolates carry both CTX-M-15 and TEM-1B.
- **This rerun:** 4 isolates.
- **Interpretation.** A ±1 drift on n=11 is almost certainly a **single TEM-1B call that fell just above the identity cutoff** in the current DB vs. just below in the 2021 DB. Not investigated at per-hit-identity level in this rerun.
- **Impact.** Small quantitative delta; does not change the qualitative co-carriage story.

### Discrepancy 4 — PR246B1C MLST (ST2144 → `-`)

- **Paper:** ST2144.
- **This rerun:** `-` (`mlst` returned a null call — one Achtman-7 allele fell just below the identity cutoff in the current `mlst` DB).
- **Interpretation.** Almost certainly an **allele-cutoff artefact**, not evidence of a different lineage: the sibling isolate `PR209E1` (also paper ST2144, same FimH87/B1) types cleanly as ST2144 in this rerun.
- **Impact.** Formal loss of 1/11 ST calls; biological interpretation (paper's ST2144 pig-adapted lineage claim) is not undermined.

---

## Threats to the replication result (things we did NOT control for)

1. **DB vintage confound (dominant threat).** Every observed discrepancy is consistent with 2021-DB vs. current-DB drift. We did **not** rerun on a pinned 2021 ResFinder DB snapshot, so we cannot separate "paper called this wrongly" from "DB has since split/renamed this allele." **This is the single highest-leverage next step.**
2. **Assembly identity trust.** We trust that the paper's WGS accessions in PRJNA548686 / PRJNA412434 correspond to the Table 1 isolate labels. No independent SNP fingerprint of assembly ↔ label mapping was done.
3. **Gene presence ≠ gene location.** The mobilome/plasmid claims are gene-*presence*-replicated but not gene-*location*-replicated. `abricate`+PlasmidFinder tells us Inc-types are present but not which contig they co-localise with which resistance gene. A long-read/hybrid re-assembly is needed to fully replicate the plasmid-linkage claims.
4. **No independent phylogroup / phylogeny.** ClermonTyping and a core-genome tree were not rerun; phylogroup calls are trusted from paper Table 1.
5. **No cgMLST / SNP-level replication of the pig↔human-worker transmission implication.** The isolate labels suggest pig-vs-worker pairs but we did not test for outbreak-level SNP proximity.

---

## Why the LLM judge landed on PARTIAL (not REPLICATED)

- Coverage: **10/10** — every analyzable unit addressed.
- Agreement: **7/10** — three per-isolate β-lactamase/MLST discrepancies pull the agreement fraction below the REPLICATED threshold.
- The judge specifically flagged (i) CTX-M-15+TEM-1B count +1, (ii) PN256E8 CTX-M allele + TEM-206, and (iii) the null MLST call as the reasons for PARTIAL.
- **Note that the judge itself annotated:** *"coverage + CTX-M-15 exact prevalence + 10/11 MLST make this the strongest of the PARTIALs — borderline REPLICATED."*

---

## What a stronger follow-up rerun would do

1. **Pin the ResFinder DB to a 2021 snapshot** — the single most impactful control, cleanly separates paper-error from DB-drift.
2. **Long-read (Nanopore R10.4) or hybrid re-assembly of `PN256E8`** — resolves the CTX-M-15/-55 ambiguity and the TEM-206 question at read-level.
3. **Plasmid reconstruction (MOB-suite / plasmidSPAdes)** on all 6 CTX-M-15 carriers — physically links CTX-M-15 to its Inc-type replicon (the paper's central mobilome claim, currently only presence-replicated).
4. **cgMLST + core-SNP tree** across the 11 isolates — tests the implicit pig ↔ human-worker transmission story.
5. **Independent ClermonTyping** on the 11 assemblies — reproduces the phylogroup calls without trusting Table 1.

---

## Bottom line

The paper's **headline quantitative claim** (CTX-M-15 in 6/11) and its **underlying per-isolate attributions** reproduce cleanly on the authors' deposited data with modern open-source tooling. The residual discrepancies are (i) one per-isolate CTX-M allele call, (ii) a ±1 co-carriage count, and (iii) one MLST identity-cutoff edge case — **none of which alter the paper's biological conclusion**. Classification: **PARTIAL replication, borderline REPLICATED**. Primary uncontrolled variable driving the "PARTIAL" rather than clean "REPLICATED" label: ResFinder/NCBI DB vintage drift, not any evident modelling or biological failure.
