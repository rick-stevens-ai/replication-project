# Failure Analysis — LL16 Milerienė 2023 Replication

**Verdict:** PARTIAL (Coverage 8, Agreement 8 on 9-point scale). 23 VERIFIED / 8 PARTIAL / 5 NOT_TESTED / **0 CONTRADICTED** across 36 tested claims.

This document catalogs, honestly, everywhere the replication came up short of "fully VERIFIED" and traces each failure to its root cause. The distinction that matters: **honest tool-scope / wet-lab blockers** vs. **replication work that could have been done but wasn't.**

## 1. Blockers by class (with counts)

| Blocker class | Count | Examples |
|---|---|---|
| A. Web-only tool with no FOSS equivalent | 4 | PathogenFinder probability (claim #11), BAGEL4 specific bacteriocin identity (#24, #25), KEGG BlastKOALA (#36), RAST SEED subsystems (#3) |
| B. Web-only tool WITH a FOSS equivalent that wasn't run | 2 | antiSMASH BGC delineation (#13) — could have been run locally; MobileElementFinder / ISfinder strain-level IS names (#22) — ISfinder DB queryable |
| C. Assembly / data availability | 1 | 4.5% smaller NCBI assembly (#1) — NCBI contamination filtering, not diagnosed at contig level |
| D. Prokka ↔ PGAP nomenclature divergence | 4 | D-LDH specific name (#16), lacR/lacE/F/X (#27), xylanase / HtrA (#26), EPS operon name (#14) |
| E. Fragmented-draft artifact | 2 | CRISPR canonical 3-spacer/23-DR array (#23), some claim #14 EPS operon adjacency |
| F. Reference-database gap | 1 | pCI2000 99.57% plasmid identity (#21) — pCI2000 reference not pulled + BLASTed |
| G. Wet-lab, non-computational | 3 | GABA-in-milk (#34), antibacterial vs. 8 pathogens (#35), FAA lactate (in-methods) |

## 2. Per-claim failure inventory (only PARTIAL and NOT_TESTED)

### Class A — Legitimately unavoidable

| Claim | Description | Root cause | Fixable? |
|---|---|---|---|
| #3 RAST SEED subsystems (246) | RAST is a hosted server; output metric is tool-specific | Web-only + tool-specific | No (unless re-submitted to RAST) |
| #11 PathogenFinder probability 0.212 | PathogenFinder is web-only; the probability score is model-specific | Web-only | No (unless PathogenFinder is submitted) |
| #24 Lactococcin B (37.5% identity via BAGEL4) | BAGEL4 database contains specific bacteriocin references (lactococcin B specifically); PGAP only annotates family (Lactococcin 972) | Web-only DB scope | Partially — a local BACTIBASE / DRAMP query could give a specific-name answer |
| #25 Enterolysin A (62.9% identity via BAGEL4) | Same — enterolysin A is a BAGEL4-database-specific classification | Web-only DB scope | Same — local bacteriocin DB query would help |
| #36 KEGG pathway analysis | BlastKOALA is web-only | Web-only | Partially — KOfamScan (FOSS) would give KO assignments |

### Class B — Could have been fixed, wasn't

| Claim | Description | What was missed | Cost to fix |
|---|---|---|---|
| #13 T3PKS region (antiSMASH BGC delineation) | Confirmed a polyketide synthase regulator (WP_281162533.1), but did not delineate the full T3PKS cluster boundaries | antiSMASH 7.x is FOSS and installs cleanly; running it locally would delineate the T3PKS BGC and cross-check whether the nis cluster is also present | ~1 hour + antiSMASH install |
| #22 IS-element strain-level names (ISS1B, ISS1N, ISLla3) | 21 IS transposases were counted at family level (6 IS6, 9 IS3 incl. IS-LL6/IS981, 4 IS982, 1 IS4, 1 IS5). Paper names 3 specific strain-level elements | ISfinder DB is publicly queryable; MobileElementFinder is FOSS. Running either would produce strain-level names | ~30 min |

### Class C — Data-availability

| Claim | Description | Root cause | Fixable? |
|---|---|---|---|
| #1 Genome size (2,473,617 vs. paper 2,589,406) | 4.5% smaller NCBI assembly | NCBI contamination filtering removed ~116 kb; we attributed this but did not verify which contigs / regions were removed | Yes — pull raw SRA reads, re-assemble with SPAdes v3.15.3 (paper's exact version), diff against the deposited GCF assembly. Would resolve whether the paper's genome size is defensible or included contaminants |
| #4 CDS count (2,514 PGAP + 218 pseudo = 2,732; paper 2,878 Prokka) | Related to #1 — smaller assembly + different pipeline gives fewer CDS | See #1; additionally, Prokka and PGAP have different pseudogene-calling conventions | Same fix as #1, plus a direct Prokka v1.14.6 run on the same assembly |

### Class D — Prokka ↔ PGAP nomenclature divergence

| Claim | What PGAP gave us | What Prokka would probably give | Verified via workaround? |
|---|---|---|---|
| #16 D-lactate dehydrogenase | Only "D-2-hydroxyacid dehydrogenase" (broad family) — 3 L-LDH VERIFIED | Prokka typically emits "ldhD" as a specific name | Not tested — we did not actually run Prokka v1.14.6 on the same assembly to verify our "naming, not biology" hypothesis. **This is a cheap fix that would move #16 back to VERIFIED.** |
| #26 Enzymes (xylanase, HtrA/DegP) | 3 α-amylase, 17 lipase/esterase, 49 protease/peptidase VERIFIED; xylanase and HtrA not annotated | Prokka may emit HtrA under that name; xylanase is genuinely rare in *L. lactis* | Same — Prokka run would resolve HtrA; xylanase probably absent even in Prokka |
| #27 lac operon (lacR, lacE, lacF, lacX not called by PGAP) | Core enzymatic lac operon VERIFIED; regulatory + PTS subunit naming differs | Prokka typically emits these subunit names | Same — Prokka run would settle this |
| #14 EPS operon name | Confirmed capsular polysaccharide biosynthesis-related gene; no contiguous "EPS operon" name from PGAP | Prokka may or may not emit "eps*" naming — this one is a real ambiguity | Same |

### Class E — Fragmented-draft artifact

| Claim | Description | Root cause | Fixable? |
|---|---|---|---|
| #23 CRISPR canonical 3-spacer / 23-DR array | Cas2 confirmed by PGAP (contig 069); MinCED default 0 arrays; MinCED loose 16 candidate regions | The paper's canonical array likely lives across a contig break in the 372-contig draft; MinCED can only see arrays that fit within a single contig | Partially — CRISPRDetect (FOSS, more sensitive than MinCED on fragmented drafts) could re-detect; SRA-based re-assembly might close the break; CRISPRCasFinder web tool remains most sensitive |

### Class F — Reference DB gap

| Claim | Description | Root cause | Fixable? |
|---|---|---|---|
| #21 Plasmid 99.57% identity to pCI2000 | RepB family / repUS-type replication initiator confirmed on contig 143; specific numeric identity to pCI2000 not measured | We did not pull the pCI2000 reference and run BLAST/ANI against contig 143 | **Trivially fixable** — fetch pCI2000 (GenBank AE003143 or equivalent), run BLASTn + skani. Would either VERIFY or CONTRADICT the paper's numeric claim. This is arguably the single most fixable gap in the whole report. |

### Class G — Wet-lab, non-computational

| Claim | Description | Fixable computationally? |
|---|---|---|
| #34 GABA production in milk | In vitro fermentation assay | No — gene basis (gadB, gadC) verified as claim #19 |
| #35 Antibacterial activity vs. 8 pathogens | In vitro agar spot assay | No — bacteriocin genes present, but functional activity requires bench work |
| Paper's FAA lactate quantification | In vitro HPLC / enzymatic assay | No — L-LDH gene basis verified |

## 3. What actually replicated well (for calibration)

To keep this analysis honest, the failure list above is bounded by 23 claims that DID fully verify:

- Species identity via two independent ANI tools (skani 98.70%, FastANI 98.24%, both within 0.5 pp of paper's OrthoANI 98.73%)
- Complete tryptophan biosynthetic operon (trpE-D-C-B-A + anthranilate synthase II) on contig 016
- GAD operon (gadB + gadC contiguous on contig 048)
- Full chaperone set (GroES, GroEL, DnaK, DnaJ, GrpE, 3× cold-shock proteins, ClpB/X/P)
- All 5 vitamin biosynthetic pathways (B1, B2, B6, B7, B9)
- No acquired AMR, no VFDB virulence hits, no biogenic-amine decarboxylases
- 5 of 6 adhesion gene categories (enolase, fibronectin-binding, TPI, sortase A, F0F1 ATP synthase 8-subunit operon, EF-Tu, 4 LPXTG anchors)
- 5 of 6 acid/bile tolerance gene categories
- L-LDH paralogs (3 confirmed)
- Plasmid presence (RepB + mobilization proteins on contig 143)
- Core lac operon (lacA, lacB, lacC, lacD, lacG, β-galactosidase)

And **0 claims were CONTRADICTED** across three passes.

## 4. Priority ranked next-pass actions (highest value first)

1. **BLAST contig 143 vs. pCI2000** → resolves #21 (single trivial fix; would verify or refute a specific numeric paper claim).
2. **Run Prokka v1.14.6 on the deposited assembly** → resolves #16, #26 (HtrA), #27, #14 all at once as "naming, not biology."
3. **Run antiSMASH 7.x locally** → delineates the T3PKS BGC boundaries (#13) AND screens for the nis (nisin) biosynthesis cluster, which the paper does not analyze but is a decisive dairy-relevance question for *L. lactis* subsp. *lactis*. (See `open_questions.json` OQ1.)
4. **Re-assemble from SRA reads with SPAdes v3.15.3** → resolves #1 and #4 by identifying which contigs / regions NCBI's contamination screen removed.
5. **Query ISfinder DB for strain-level IS names** → resolves #22.
6. **Run CRISPRDetect on the fragmented assembly** → resolves #23 (or produces a stronger PARTIAL).
7. **Cross-check AMR with NCBI AMRFinderPlus** → doubles the AMR safety statement, addresses `open_questions.json` OQ4.
8. **Pan/core-genome vs. subsp. *cremoris* + additional dairy starters** → addresses `open_questions.json` OQ3 (comparative genomics gap the paper itself has).

## 5. Root-cause categories, one-line summary

Of the 13 PARTIAL + NOT_TESTED claims:

- **~5 (Class A):** genuinely unavoidable web-only-tool blockers.
- **~4 (Class D):** cheap Prokka-vs-PGAP nomenclature runs that would clear immediately.
- **~2 (Class B):** FOSS tools that exist and simply weren't installed / run.
- **~1 (Class C+F):** a re-assembly and a single BLAST run would clear the biggest data-availability gaps.
- **3 (Class G):** wet-lab, permanently unreproducible computationally.

**Bottom line:** the "8 PARTIAL / 5 NOT_TESTED" is honest but not exhaustive. A next-pass analyst with ~1 day of local compute could plausibly move 6-8 claims from PARTIAL to VERIFIED, taking the 9-point Agreement score toward 9. The remaining PARTIALs would be the truly-unavoidable web-only-and-wet-lab set, which is the correct floor for a computational-only replication.
