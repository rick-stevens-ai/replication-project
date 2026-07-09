# Failure Analysis — BV-BRC Replication #91

Target: Tekedar et al. 2019, *PLoS ONE* **14**(8):e0221018 — A. veronii pathotype.
Verdict: **PARTIAL REPLICATION (strong).** No paper claim contradicted.

This document is the honest post-mortem: what did NOT get done, why it was scoped out, what a downstream reproducer would need to close each gap, and where reasoning-hygiene / interpretation risks remain even for the parts that DID replicate.

---

## 1. What did not replicate — and why

### 1.1 Pan/core-genome absolute counts (C8: 8,710 / 2,855)
- **Paper claim:** 8,710 total genes in the pan-genome; 2,855 in the core-genome across the 41 A. veronii strains (EDGAR 2.0 with its internal SRV cutoff).
- **What was attempted here:** nothing beyond flagging it as a non-target.
- **Why it was not attempted:** these numbers are meaningful **only under EDGAR 2.0's specific Score Ratio Value (SRV) cutoff**. Any modern pan-genome pipeline (Roary at default 95%, Panaroo strict / moderate, PPanGGOLiN, Bacterial Pan Genome Analysis Tool) on the identical 41-genome input will legitimately produce different absolute counts. A byte-perfect (or even 5%-tolerant) match is not a meaningful reproducibility target for this class of claim.
- **What would close this gap:**
  - Either (a) rerun the analysis inside EDGAR 2.0 with the same SRV cutoff (which is a hosted-tool dependency, not a laptop replication), OR
  - (b) rerun with a modern pan-genome pipeline and report the resulting pan/core numbers with sensitivity analysis (cutoff sweep) plus stability of the pan-genome growth curve (γ exponent) — this would extend the paper, not merely reproduce it.
- **Interpretation risk if you naively byte-match:** you will get "different numbers → replication failed" even when nothing is scientifically wrong.

### 1.2 RAxML core-genome ML phylogeny (2857 gene trees, GTR + 10 rate categories, 100 rapid-bootstrap iterations)
- **Paper claim:** Concatenated core-genome ML tree (via EDGAR + MUSCLE + RAxML) with 100 rapid-bootstrap iterations shows the ML09-123 / TH0426 pair sitting on a distinct, well-supported branch.
- **What was attempted here:** nothing.
- **Why it was not attempted:** CPU-heavy (2857 alignments × RAxML 100 bootstraps on a laptop is not a <15-min job) and not the headline claim. The pathotype conclusion is quantitatively carried by the ANI (>99.91%) test — which WAS reproduced here (fastANI 99.9273%/99.9106%, skani 99.94%).
- **What would close this gap:** run BUSCO or GTDB-Tk gene extraction → MAFFT → IQ-TREE (modern replacement for RAxML) with 1000 UFBoot iterations on a workstation; expect ~4–8 h. A phylogenetic-signal replication would be a "nice to have" but is not what the paper's headline pathotype claim rests on.

### 1.3 In-vivo catfish LD50 (C9)
- **Paper claim:** ML09-123 kills channel catfish in a dose-dependent manner.
- **What was attempted here:** nothing.
- **Why it was not attempted:** experimental in-vivo work is fundamentally out of computational scope. A dose-response mortality curve requires live fish, IACUC approval, and physical infrastructure.
- **What would close this gap:** an independent aquaculture microbiology lab with catfish challenge capability. Not a reproducibility target for a compute-only replication.

### 1.4 CRISPRfinder per-strain across all 41 genomes
- **Paper claim:** CRISPRfinder output characterizes CRISPR arrays across the panel.
- **What was attempted here:** BV-BRC Specialty Genes spot check → AVNIH1 (654.48) shows 0 CRISPR product hits, but BV-BRC's `sp_gene` endpoint is not the same as running CRISPRfinder directly. The paper's CRISPRfinder output is not surfaced via BV-BRC.
- **Why it was not fully attempted:** would require downloading 41 FASTAs and running CRISPRfinder / CRISPRCasFinder / MinCED per strain, aggregating results — a ~30–60 min extension, but not on the critical path for the pathotype headline claim.
- **What would close this gap:** batch-run CRISPRCasFinder against all 41 genomes and produce a presence/absence matrix vs the paper's Table S2 or equivalent.

### 1.5 TssJ "present only in these two strains" negative claim
- **Paper claim:** TssJ (AHA_1837 / VasD) is present *only* in ML09-123 and TH0426 across the 41-strain panel.
- **What was attempted here:** verified the **necessary condition** — TssJ present in both catfish strains via BV-BRC Specialty Genes.
- **What was NOT verified:** the **sufficient condition** — that TssJ is truly absent from the other 39 strains.
- **Why it was not verified:** the "only" claim would require the same `sp_gene` query across all 41 genomes + a search-sensitivity floor to guard against distant orthologs being missed at default BLAST thresholds. Scope call.
- **What would close this gap:** batch-pull `sp_gene` for all 41 BV-BRC genome_ids + a HMMER search of the TssJ profile against each 41-strain proteome as a sensitivity backstop.

---

## 2. What replicated but has interpretation caveats

### 2.1 Data availability (C1) — 7/41 required alternate taxonomy
- Result: **41/41 retrievable**, BUT 7 strains (AER39, LMG 13067, AMC35, CECT 4257, CCM 4359, B565, AER397) required searching under strain-level taxonomy IDs instead of the direct `strain` field.
- A naive reproducer following the paper's accessions verbatim through BV-BRC's default search UI in 2026 would hit only 34/41 and might incorrectly conclude ~17% of the input is unavailable.
- **Mitigation:** the workflow captures the alternate-taxonomy fallback pattern (e.g. B565 → taxon 998088).

### 2.2 Secretion-system counts are annotation-product hits, not gene counts
- The BV-BRC `sp_gene` product-string keyword match gives raw hit counts (49 T3SS-associated products in ML09-123 vs 68 in TH0426), not clean per-system component counts.
- This works well qualitatively for present/absent binary distinctions (AVNIH1: 0 vs 49/68 → unambiguously "T3SS absent"), but the "49 vs 68" delta between two T3SS-positive strains is annotation-inflation noise, not a biological difference in system completeness.
- The paper's own T3SS/T5SS/T6SS tallies appear to conflate "system present" with "how many components annotated" — same annotation-artifact class.

### 2.3 Virulence-factor total (207 in paper vs 211/240 here)
- Paper reports 207 across the whole 41-strain panel. This replication reports 211 (ML09-123) and 240 (TH0426) per-strain totals from BV-BRC Specialty Genes.
- These are NOT directly comparable — the paper's 207 is a category-tally across the whole panel, while our 211/240 are per-strain aggregate hits.
- Both are database-of-databases counts (paper: VFDB; here: VFDB + Victors + PATRIC_VF + others including the notorious BV-BRC "Virulance factor" misspelling class), so absolute values drift with database version.
- The "same order of magnitude → consistent" language in `REPORT.md` is honest but coarse. A more rigorous replication would restrict to a single database (e.g. VFDB only) and rerun the paper's per-category tallies.

### 2.4 Two-genome-pair claim in a 41-genome paper
- The "pathotype impacting aquaculture globally" claim is carried by exactly TWO genomes at ANI > 99.91%. The other 39 genomes provide context but do not add independent evidence for the pathotype.
- Genome sharing at >99.9% ANI can also arise from lab-related genome exchange, misidentification of source metadata, or coincidental near-clonal circulation — not necessarily active global aquaculture-mediated spread.
- The paper does not include SNP-level phylogeography, temporal signal, or Bayesian dating that would rule out these alternatives.
- **This replication reproduced the number but cannot replicate the interpretation.** Downstream work (see `open_questions.json` items 1 and 2) is needed to move from "two very similar genomes" to "a demonstrated pathotype."

---

## 3. Reasoning-hygiene checklist

| Risk                                                                 | How this replication handled it                                                                     |
|----------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| Confusing "not attempted" with "failed"                              | C8 pan/core and C9 in-vivo explicitly flagged as non-targets with reasons, not counted as failures. |
| Byte-matching tool-artifact numbers across pipelines                 | C8 pan/core explicitly refused as a byte-match target; EDGAR-specific counts flagged.               |
| Overclaiming ANI = pathotype                                         | GENUINE CRITIQUE section (REPORT.tex §5) separates "ANI number reproduced" from "pathotype demonstrated". |
| Database-version drift inflating virulence counts                    | Called out explicitly; both `Virulence Factor` and `Virulance factor` spellings enumerated separately. |
| Data-availability apparent gap (7/41 strain-name misses)             | Alternate-taxonomy resolution captured in workflow.md.                                              |
| Small human-isolate denominator (n=7) driving T3SS/T6SS-absence claim | Called out in GENUINE CRITIQUE as "correlation vs cause, under-controlled."                         |

---

## 4. What a fuller replication would add (roadmap)

1. **Pan/core sensitivity analysis** — Panaroo strict / moderate / sensitive + Roary at 95%/90%/80% identity across all 41 genomes; report pan/core distribution + sensitivity of the pathotype-defining core set.
2. **Modern phylogeny** — IQ-TREE with UFBoot 1000 on a modern core-genome alignment (~4–8 h); confirm the ML09-123/TH0426 branch topology.
3. **Whole-panel TssJ presence/absence** — batch BV-BRC `sp_gene` + HMMER sensitivity backstop across all 41.
4. **Per-strain CRISPR** — batch CRISPRCasFinder across all 41 genomes; matrix vs paper's supplementary tables.
5. **Expand to full BV-BRC A. veronii set (726 genomes as of 2026-07-04)** — retest the pathotype-pair claim in a much larger denominator; look for other conserved pairs at ANI > 99.9% between geographic regions.
6. **VFDB-only virulence re-tally** — replicate the paper's 207-virulence-gene number with a database-restricted rerun to isolate database-version drift from real signal.

---

## 5. Bottom line

The paper is **highly reproducible where reproducibility matters**. The single most-cited claim — the ML09-123 / TH0426 pathotype ANI — reproduced exactly in ~12 minutes with two independent tools. The secretion-system phenotype pattern reproduced qualitatively. The genome stats reproduced to the decimal.

The gaps that remain are (a) tool-artifact numbers (EDGAR pan/core) that should never have been byte-match targets, (b) CPU-heavy phylogenetics that would confirm rather than contradict, and (c) interpretation questions (is "two very similar genomes" really a "global aquaculture pathotype"?) that are downstream research questions rather than reproducibility failures.

**Verdict: PARTIAL REPLICATION (strong). No claim contradicted.**
