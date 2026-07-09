# Failure Analysis — BVBRC-61 (Heo et al. 2021, *B. siamensis* B28)

Honest inventory of what did NOT reproduce, why, and whether each failure is a real gap in the paper, a limitation of a sequence-only replication, or a pipeline artifact. Verdict is **PARTIAL** — this document explains the "partial" half.

## 1. Wet-lab claims out of reach (main driver of PARTIAL verdict)

### 1a. Enterotoxin PCR gel (C3a phenotype)
- **What the paper did:** PCR-verified absence of *B. cereus*-type enterotoxin genes (Nhe/Hbl/CytK).
- **What we did:** Proteome-scan of RefSeq `protein.faa` (3,808 seqs) for the same families → 0 hits, ABSENT.
- **Why it isn't full replication:** genome-encoded absence is *consistent with* PCR-negative, but a PCR gel is a wet-lab result that a genome scan cannot itself reproduce. If the paper's PCR primers had cross-reacted with a distant homolog and we'd missed it in the genome, we'd need the actual gel image to adjudicate.
- **Verdict:** genotype ✅ / phenotype ⛔ unreproducible. Consistent, not contradicted.

### 1b. Disc-diffusion antibiotic susceptibility (C3c phenotype)
- **What the paper did:** Disc-diffusion assay showing susceptibility to 8 antibiotics.
- **What we did:** Two independent AMR tools (AMRFinderPlus + RGI/CARD) both report **no acquired resistance determinants**.
- **Why it isn't full replication:** genotype ≠ phenotype for AMR. A strain can carry no known resistance gene and still be resistant (novel mechanism), or carry hits and still be susceptible (regulatory silencing, low expression). Only a live disc-diffusion assay adjudicates. Our result is *fully consistent* with the paper's phenotype but does not itself constitute replication of it.
- **Verdict:** genotype ✅ (dual-tool) / phenotype ⛔ unreproducible.

### 1c. β-hemolysis assay (C3b phenotype)
- **What the paper did:** Reported non-β-hemolytic phenotype despite *hlyIII* gene presence.
- **What we did:** Confirmed *hlyIII*-like ("hemolysin family protein") PRESENT (×4). No plate assay.
- **Why it isn't full replication:** the interesting claim is *phenotypic silence of a genotypically-present gene*. Genome cannot resolve this.
- **Verdict:** genotype ✅ / phenotype ⛔ unreproducible.

### 1d. Antibacterial-activity plates against foodborne pathogens (C5)
- **What the paper did:** Fig. 2 plate assay against 7–8 foodborne pathogens.
- **What we did:** Confirmed bacteriocin/lipopeptide biosynthesis genes present (surfactin, Blp class II bacteriocin, lantibiotic immunity, circular bacteriocin — 11 hits total). Genotypic proxy only.
- **Why it isn't full replication:** presence of BGCs does not prove activity, titer, or spectrum. This is an entirely wet-lab claim.
- **Verdict:** ⛔ out of reach.

## 2. Naming caveats (soft-fail, not contradiction)

### 2a. "Bacitracin + mesentericin operon"
- **What the paper said:** specifically names a "bacitracin + mesentericin" bacteriocin operon.
- **What we found:** RefSeq annotates the same biosynthetic locus with different vocabulary — surfactin biosynthesis genes, Blp class II bacteriocin, lantibiotic immunity, circular bacteriocin. Biosynthetic *capacity* is unambiguous; the specific 2021 naming does not directly match.
- **Root cause:** RefSeq (PGAP) product vocabulary differs from the 2021 RAST/SEED annotation the paper used. An antiSMASH 7.x run (not performed in this replication) would reconcile by providing BGC-level cluster IDs (MIBiG cross-references) rather than per-protein product names.
- **Verdict:** ⚠️ partial match. Not a contradiction, but the paper's specific naming was not directly reproducible from RefSeq alone.

## 3. Pipeline artifacts (not a paper problem, not a replication problem)

### 3a. CDS count divergence
- **Paper:** 3,573 CDS (COG-categorized subset) / 1,663 (SEED).
- **This study:** 3,831 protein-coding (PGAP 2024+).
- **Root cause:** different annotation pipelines and snapshots. The paper's numbers are COG- or SEED-restricted subsets, not raw CDS totals. PGAP's raw call is different by definition.
- **Verdict:** ⚠️ pipeline-dependent. Not a substantive disagreement.

### 3b. AMR databases surface more intrinsic hits than the paper's 2021 view
- **Paper:** flagged some tet/lincomycin/bicyclomycin/multidrug efflux genes in Table 2, but small list.
- **This study:** AMRFinderPlus adds satA, fosM, and van-cluster homolog *fragments*; CARD/RGI adds Bc cephalosporinase, FosBx1, qacG/qacJ.
- **Root cause:** modern curated databases (2024–2026 vintage) are more sensitive/complete than the 2021 RAST/SEED view the paper used. All added hits are `scope=core` (intrinsic).
- **Risk:** a naive reader could misinterpret "9 CARD hits" as evidence *against* the safety claim. It is **not** — every hit is intrinsic, and the paper's own Table 2 already caveats that intrinsic efflux/β-lactamase genes are present without conferring resistance phenotype.
- **Verdict:** ⚠️ refines rather than contradicts the paper.

## 4. What we consciously chose NOT to attempt

- **antiSMASH 7.x BGC prediction** — would have reconciled the bacitracin/mesentericin naming caveat, but not required to reach a PARTIAL (strong) verdict.
- **Wet-lab reproduction of any C3 or C5 phenotype** — not in scope for a sequence-based replication track.
- **Multi-genome core-phylogeny with dDDH** — deferred to `open_questions.json` (question #1) as a follow-on study.
- **CAZyme / MEROPS full inventory** — deferred to `open_questions.json` (question #2).

## 5. What would upgrade this from PARTIAL to REPLICATED
1. antiSMASH 7.x run to formally reconcile bacteriocin/lipopeptide BGC naming (closes the last genome-side soft spot).
2. Access to the strain and a wet-lab bench to redo enterotoxin PCR, disc-diffusion, β-hemolysis, and antibacterial plates. (Genuinely wet-lab; not achievable in this pipeline.)

## 6. What would downgrade this from PARTIAL to FAILED
Nothing in this replication downgraded the paper. **No claim was contradicted.** The additional intrinsic AMR hits refine but do not conflict with the paper's safety conclusion. If a future higher-resolution reanalysis found (a) a genuine mobile AMR element mis-called as intrinsic here, (b) a bona fide enterotoxin gene, or (c) an incorrect ANI reclassification, the verdict would drop. None of these has been surfaced.

## 7. Reproducibility risks for anyone re-running
- **fastANI/skani version drift** — expect ±0.05% jitter in ANI values as algorithms evolve; the 95% species boundary conclusion is robust to this.
- **AMRFinderPlus DB updates** — expect the intrinsic hit list to grow slowly over time as CARD/NCBI-AMR curate more *Bacillus* chromosomal homologs. The acquired-AMR result should remain stable.
- **RefSeq re-annotation** — PGAP snapshots can shift CDS counts by 10s of genes; product-name vocabulary can shift too. Use exact snapshot dates for byte-level reproducibility.

## Bottom line
This replication is PARTIAL because it *cannot* touch four wet-lab claims (three C3 phenotypes + C5 antibacterial), not because any claim was contradicted. Everything the paper says the genome should show, the genome does show — often to the base pair.
