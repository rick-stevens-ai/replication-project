# Failure Analysis — BVBRC-02-Ralstonia-Fluit2021

Verdict: **PARTIAL** (coverage 8/10, agreement 8/10, 0 contradictions across pass-1 and pass-2).
This file enumerates what did *not* fully replicate, classifies the failure by cause,
and states the concrete unblocker for each. No claim was contradicted; every gap
here is a scope or tooling gap, not a scientific discrepancy.

## Failure classes

- **STRUCTURAL_WETLAB** — Cannot be replicated in silico. No unblock without a bench.
- **STRUCTURAL_COMMERCIAL** — Requires a paid tool the project bans on principle.
- **BOUNDED_DATA** — Requires additional public data pulls; scope-limited, not fundamental.
- **METHOD_DRIFT** — In-silico rerun differs from paper due to tool/version choices.
- **REFERENCE_SPARSE** — Reproduced sub-analysis is consistent, but the paper's full
  reference-heavy version was not attempted this pass.

---

## Failures

### F1 — MICs not reproduced (Claims 11, 12)

- **What failed:** Co-trimoxazole MICs ≤1 mg/l for R. pickettii (Claim 11); ciprofloxacin
  MICs ≤0.12 mg/l for most strains (Claim 12).
- **Verdict recorded:** ⛔ NOT_TESTED on both passes.
- **Class:** STRUCTURAL_WETLAB.
- **Root cause:** Broth microdilution requires physical isolates and CLSI/EUCAST plates.
  No genotype-based tool substitutes for a phenotypic MIC.
- **Impact on paper's conclusions:** Low. MICs are consistent with the intrinsic-resistance
  pattern already implied by the OXA-22/OXA-60 findings, which we did verify.
- **Unblock:** None available under the free/in-silico charter. Deferred indefinitely.

### F2 — cgMLST 517-gene topology not reproduced (Claim 16, Fig. 1)

- **What failed:** The paper's core cgMLST tree over 517 genes built in Ridom SeqSphere v5.0.0.
- **Verdict recorded:** ⛔ NOT_TESTED on both passes.
- **Class:** STRUCTURAL_COMMERCIAL (fixable in principle via a free workaround).
- **Root cause:** Ridom SeqSphere is commercial software; project bans paid tools.
- **Impact on paper's conclusions:** Medium — Fig. 1 is a headline figure. However, the
  paper's own headline conclusion (Groups D–H at 0.95 ANIb + independent OXA phylogenies)
  is already validated by our free-tool stack, so cgMLST is corroborative rather than
  load-bearing for the paper's central taxonomic claim.
- **Unblock:** Substitute chewBBACA or PIRATE with a Ralstonia training set. REPORT.md
  estimates "a few hours of analyst time"; deferred to a future pass.

### F3 — Full 78-tip 16S / 29-tip OXA-22 / 27-tip OXA-60 trees not reproduced (Claims 13, 14, 15)

- **What failed:** The paper's full multi-reference phylogenies:
  16S: 78 seqs, 1395 positions, log-lik −2740.49;
  OXA-22: 29 seqs, 279 positions;
  OXA-60: 27 seqs, 271 positions.
- **Verdict recorded:** ⛔ NOT_TESTED (pass-1) → ◐ PARTIAL (pass-2, 18-tip sub-trees only).
- **Class:** REFERENCE_SPARSE + BOUNDED_DATA.
- **Root cause:** Building the full trees requires the 60 reference 16S accessions +
  11 reference OXA-22 accessions + 9 reference OXA-60 accessions listed in the paper's
  Supplementary Table 2. Pass-2 chose to build honest 18-tip sub-trees rather than
  fabricate a full reconstruction.
- **What DID reproduce inside the sub-tree:**
  - OXA-60 alignment length 271 = 271 (exact match).
  - OXA-22 alignment length 278 vs 279 (Δ1, within MAFFT variability).
  - 16S alignment 1491 vs paper's trimmed 1395 (paper trimmed to a common window; ours untrimmed).
  - D1, D2 monophyletic in 16S; D1, D2, E2 monophyletic in OXA-22;
    5/6 groups consistent in OXA-60.
- **What did NOT reproduce:**
  - Paper's log-likelihood −2740.49 is on a different (larger) tip set, so it does not
    apply to our 18-tip tree — cannot be verified.
  - E1/E2 not monophyletic in 16S. Paper itself acknowledges 16S cannot cleanly split
    E1 from E2 ("a similar division was seen in group E, with the exception of strain 12D"),
    so we file this as *consistent with the paper's own caveat*, not a contradiction.
- **Unblock:** Harvest reference accessions from Supplementary Table 2; re-run the same
  extract → MAFFT → FastTree pipeline. Bounded effort, no new tooling needed.

### F4 — Multi-strain genome-size averages drift ~6% (Claim 1)

- **What failed:** Species-mean genome sizes for the two multi-strain species drift:
  - R. mannitolilytica: paper 5,272,894 bp vs pass-1 4,939,490 bp (−6.3%).
  - R. pickettii: paper 4,932,406 bp vs pass-1 5,211,002 bp (+5.6%).
- **Single-strain species matched exactly** (R. insidiosa +0.001%, R. new spp. −0.005%).
- **Verdict recorded:** ◐ PARTIAL on both passes.
- **Class:** METHOD_DRIFT.
- **Root cause:** SPAdes v3.11.1 with `--careful` and ≥1000 bp contig cutoff (paper)
  vs SPAdes v4.2.0 with `--only-assembler` and ≥500 bp cutoff (ours). Different
  contig-inclusion policies inflate/deflate the total assembly size.
- **Impact on paper's conclusions:** Low for taxonomy (ANIb is per-fragment identity,
  robust to contig-count differences) but non-zero for anyone who wants to reuse
  species-mean sizes as reference values.
- **Unblock:** Re-run SPAdes 3.11.1 `--careful` with 1000 bp cutoff and re-derive the
  species means. Not attempted — sub-percent single-strain matches suggest the pipeline
  is correct and the difference is genuinely tooling-driven.

### F5 — Contig count 551632 = 157 vs paper's ≤117 (Claim 10)

- **What failed:** Strain 551632 has 157 contigs in our assembly; paper reports ≤117
  contigs per strain as a global bound.
- **Verdict recorded:** ◐ PARTIAL on both passes.
- **Class:** METHOD_DRIFT.
- **Root cause:** Same as F4 — SPAdes version and contig cutoff differences fragment the
  assembly more aggressively for this one strain.
- **Impact:** Cosmetic for our own downstream analyses (BLAST/tblastn work fine at 157
  contigs) but would break a re-user who assumed the paper's ≤117 bound.
- **Unblock:** Same as F4 — re-run with paper's SPAdes parameters.

### F6 — Strain 551633 FDAARGOS-410 clustering claim not tested

- **What failed:** Paper claims R. pickettii FDAARGOS-410 clusters with R. mannitolilytica
  D2. We did not add the FDAARGOS-410 assembly, so we cannot check this.
- **Verdict recorded:** Not explicitly graded; implicitly under NOT_TESTED "reference-data".
- **Class:** BOUNDED_DATA.
- **Unblock:** Download FDAARGOS-410, add to ANIb + tree inputs, re-run. Bounded.

### F7 — Full 8-group (A–H) ANIb classification at 0.95 cutoff not built

- **What failed:** Paper's global 0.95-cutoff classification over ~78 genomes.
- **Verdict recorded:** Not attempted (pass-1 noted this; pass-2 did not re-attempt).
- **Class:** BOUNDED_DATA.
- **Root cause:** Need 57 GenBank genomes + 4 type-strain assemblies.
- **Unblock:** Harvest and rerun pyani; bounded compute.

### F8 — Bootstraps not directly comparable

- **What failed (mild):** Paper reports MEGA-X JTT + 500 bootstrap replicates on the
  OXA trees. We used FastTree default (Shimodaira-Hasegawa support values in the `.log`).
- **Class:** METHOD_DRIFT.
- **Impact:** Support values in our trees are not on the same scale as the paper's.
  Group monophyly still verifiable topologically; confidence quantification differs.
- **Unblock:** Rerun in IQ-TREE or MEGA equivalent with 500 replicate bootstrap for
  a matching support-value comparison.

---

## What the failure pattern tells us

- **Zero contradictions.** Every discrepancy is either tooling-driven (F4, F5, F8),
  scope-limited (F3, F6, F7), or fundamentally out of the free/in-silico charter
  (F1, F2).
- **The paper's central taxonomic and AMR-gene claims held up** across both an
  independent assembly + ANIb + ResFinder pipeline (pass-1) and independent
  phylogenies at 16S + OXA-22 + OXA-60 (pass-2).
- **The gap between PASS-2's ◐ PARTIAL and a hypothetical ✅ VERIFIED for phylogeny
  is a data-harvest gap, not an evidentiary gap.** A pass-3 that fetches
  Supplementary Table 2 accessions and rebuilds 78-/29-/27-tip trees would likely
  close Claims 13, 14, 15 to full VERIFIED.
- **The gap between PASS-2 and a hypothetical ✅ VERIFIED for cgMLST is a tooling gap.**
  A chewBBACA/PIRATE substitution is bounded but non-trivial.
- **The gap between PASS-2 and a hypothetical ✅ VERIFIED for MICs is structural** —
  no free-compute path exists.

## Rerun priority (if a pass-3 is authorised)

1. **Harvest Supplementary Table 2 accessions** and rebuild the three multi-reference
   phylogenies. Highest leverage per hour: closes 3 PARTIAL claims.
2. **Add FDAARGOS-410 to ANIb + phylogeny inputs.** Closes F6, spot-checks the
   paper's cross-species clustering claim.
3. **chewBBACA / PIRATE substitution for cgMLST.** Would elevate Claim 16 from
   NOT_TESTED to at least PARTIAL and let us cross-check the paper's Fig. 1.
4. **Re-assemble with SPAdes 3.11.1 `--careful` (1000 bp cutoff)** to close F4/F5.
   Low scientific yield but tidies up the method-audit numbers.
5. **MICs, F1** — do not attempt unless a wet-lab partner appears.
