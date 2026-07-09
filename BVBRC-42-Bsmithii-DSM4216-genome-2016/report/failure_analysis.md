# Failure analysis — BVBRC-42 *B. smithii* DSM 4216ᵀ (Bosma et al., 2016)

Verdict: **PARTIAL REPLICATION (strong, independently confirmed)**.

This document honestly enumerates what did NOT replicate, gaps between paper claims and this replication, and the reasons — separating (a) genuine bounds of the in-silico method, (b) annotation-era drift artifacts, and (c) explicitly out-of-scope components. It is the companion to the GENUINE CRITIQUE section of `REPORT.tex` / `REPORT.md`.

---

## 1. Fully replicated (no failures)
- **Genome size (3,381,292 bp)** — EXACT match.
- **Chromosome CP012024.1 (3,368,778 bp)** — EXACT match.
- **Plasmid CP012025.1 (12,514 bp)** — EXACT match.
- **rRNA gene count (33, from 11 operons × 3)** — EXACT match.
- **G+C content (40.75% rounds to paper's 40.8%)** — matches.
- **Headline biological claim** — absence of *pta* and *ackA* (plus PflB, Pdc, PFOR) confirmed by tblastn (well below the pident≥40 ∧ qcov≥70 ∧ e≤1e-20 presence rule) AND independently by GFF product-name scan across BOTH the 2015 GCA and 2026 GCF annotations. Zero hits either way. Decade-independent.
- **Positive controls (Ldh, PdhA)** — deep unambiguous ortholog scores (96%/100% qcov, e-values 2.8e-134 / 0), so the negative calls for the ABSENT panel are genuine losses, not failed searches.
- **Independent reproduction (2026-07-03)** — 15/15 checkable metrics MATCH, 0 MISMATCH; bit-identical tblastn (BLAST determinism).

---

## 2. Partial matches — genuine but bounded discrepancies

### 2.1 Protein-coding gene count: 3,619 vs paper 3,627 (Δ = −0.2%)
- **What differs:** we count 3,619 CDS on the GCA (2015) proteome; paper reports 3,627 (Table 4) / 3,635 ORFs (Table 6).
- **Why:** the paper's internal count uses the RAST-era submission with a slightly different pseudogene / partial-CDS handling than what is exported in the public `protein.faa`. This is not a genome-substance disagreement.
- **Verdict:** within tolerance (<0.4%); reported transparently. Cannot be closed further without the paper authors' exact per-feature call list.

### 2.2 DNA coding fraction: 81.4% vs paper 82.8% (Δ = 1.4 percentage points)
- **What differs:** our coding-bp / total-bp ratio is 81.4%; paper reports 82.8%.
- **Why:** the independent reproduction attributes it to inclusion of pseudogene CDS in the coding-bp numerator, plus small differences in the ORF-boundary definitions of the 2015 RAST vs the exported GFF.
- **Verdict:** close, explained; not a substantive disagreement.

### 2.3 GCF (2026 RefSeq PGAP) CDS count drops to 2,970 with 73 pseudogenes
- **What differs:** 2026 RefSeq re-annotation calls fewer intact CDS + 73 pseudogenes vs the 2015 RAST-era annotation the paper used.
- **Why:** classic annotation-pipeline drift over a decade. PGAP is more aggressive about pseudogene calls than 2015 RAST.
- **Verdict:** genome sequence is identical (all lengths match to the base pair, rRNA count unchanged, tblastn results unchanged). Reporting it explicitly to prevent future readers from citing the RefSeq number as a "reduction" — the underlying genome is the same.

---

## 3. Cross-DB-version compromise — COG table (Table 5)

- **What differs:** raw Pearson r on all 22 COG categories is 0.615 (not the ~0.9+ we'd want for a clean replication of Table 5).
- **Why:** the paper used 2015 IMG/RAST COG assignments. We used 2026 NCBI COG DB via COGclassifier v2. Between those two DB releases:
  - Category **R** ("general function prediction only") shrank from paper's 382 to our 133.
  - Category **S** ("function unknown") shrank from 236 to 98.
  - Category **D** shows a known COGclassifier-v2 over-assignment quirk.
- Once D, R, S are excluded, Pearson r rises to **0.912** and Spearman ρ to **0.919** on the stable specific-function categories (C/G/E/M etc.).
- **Verdict:** an **honest workaround, not a true replication of Table 5**. We report both the raw r=0.615 and the excl-D/R/S r=0.912 numbers; readers must accept the annotation-era caveat.

---

## 4. Judgement call — Pdc partial-domain hit

- **What differs:** Pdc (P06672) tblastn best hit is 40.0% pident but only 34% qcov (partial-domain).
- **Why called ABSENT:** does not clear the qcov≥70 presence rule. Paper also calls it ABSENT. A laxer coverage cutoff (say qcov≥25) could have called it PRESENT as a domain-level remnant.
- **Verdict:** we call ABSENT (paper agrees). The rule is transparent; a reader who disagrees with the qcov threshold can rescore from the raw `metabolic_tblastn.tsv`.

---

## 5. NOT reproduced — paper's own workflow layer (C11)

These are the reasons the verdict is **PARTIAL**, not REPLICATED:

### 5.1 RAST manual-curation pipeline
- **What was not done:** the paper's expert per-gene curation on top of the RAST auto-annotation (EC-number rescue, functional-role reassignment).
- **Why:** paper-specific; not scriptable without the paper's curator notes. Our tblastn + name-scan is stringent but does not replicate the paper's per-gene expert calls.

### 5.2 antiSMASH secondary-metabolite clusters
- **What was not done:** antiSMASH run + comparison of secondary-metabolite biosynthetic gene cluster catalogue.
- **Why:** out of scope. Not required to test the paper's headline central-metabolism claims.

### 5.3 CRISPR-finder inventory
- **What was not done:** CRISPR array detection + `cas` gene typing.
- **Why:** out of scope. The paper's numbers are taken at face value.

### 5.4 InterPro domainome EC-rescue
- **What was not done:** InterProScan run + rescue of borderline enzymes (e.g. the methylglyoxal→L-lactate route the paper rescues).
- **Why:** out of scope. This is a bounded gap — if a headline claim rested on a domainome rescue, we could not audit it. But the pta/ackA loss does not; it is a straightforward tblastn negative on two annotation eras.

### 5.5 Table 6 comparative genomics
- **What was not done:** re-computation of the paper's comparison to 14 other Bacillus/Geobacillus genomes.
- **Why:** out of scope. All 14 genomes are public and could be added; it just wasn't the priority for verifying the paper's own central claims.

### 5.6 Fig. 4 metabolism-map redraw
- **What was not done:** the manually drawn central-metabolism map.
- **Why:** figure-craft, not evidence. All the underlying genes are confirmed via tblastn + name-scan.

---

## 6. Structural limits (not fixable without changing method)

- **In-silico only.** No wet-lab validation of the paper's phenotype claims (55 °C growth, L-lactate as major product, spore formation).
- **Single-genome scope.** Only the type strain; strain-to-strain variation within *B. smithii* not explored.
- **Ortholog-only presence/absence.** tblastn + name-scan can miss deeply-diverged homologs or fused domains; we mitigated with two orthogonal methods and two annotation eras, but the residual risk is nonzero.

---

## 7. What would move the verdict from PARTIAL to REPLICATED
1. Reproduce Table 5 with the exact 2015 IMG/RAST COG DB (or archival snapshot) rather than the 2026 NCBI COG DB.
2. Re-run RAST on the raw reads with the 2015 pipeline version to close the CDS-count and coding-fraction gaps.
3. Re-run Table 6 comparative genomics on the 14 named genomes.
4. Re-run antiSMASH, CRISPR-finder, InterProScan on `GCA_001050115.1` and cross-check counts.
5. Redraw Fig. 4 from the reproduced presence/absence panel.

None of these are blocked by evidence; they are all scope decisions.

---

## 8. What would REFUTE the paper's headline
- A convincing tblastn hit for *pta* (P39646) at pident ≥ 40 ∧ qcov ≥ 70 ∧ e ≤ 1e-20 on the *B. smithii* genome — we find pident 26.4 / qcov 59% / e = 0.62, far below threshold. Refuted.
- A convincing tblastn hit for *ackA* (P37877) at the same rule — we find 24.4 / 55% / 2.3. Refuted.
- A GFF product-name entry containing `phosphotransacetylase`, `phosphate acetyltransferase`, or `acetate kinase` in EITHER the 2015 GCA or 2026 GCF annotation — zero hits in both. Refuted.

The headline stands under both orthology and annotation, in both 2015 and 2026, and under an independent fresh-subagent re-run. This is as strong as an in-silico confirmation gets.
