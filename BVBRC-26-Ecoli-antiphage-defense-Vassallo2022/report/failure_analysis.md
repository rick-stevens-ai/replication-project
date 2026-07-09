# Failure Analysis — BVBRC-26 (Vassallo et al. 2022)

Structured accounting of what did **not** replicate, what partially replicated, and what methodological choices in this replication constitute weaknesses a reviewer should push back on. This document exists so the "PARTIAL REPLICATION (strong)" verdict is a substantive judgement, not a rhetorical hedge.

## Summary

| Claim | Verdict | Failure mode | Root cause | Fixable? |
|---|---|---|---|---|
| C1 (corpus of 71 strains) | AGREE | none | — | n/a |
| C2 (per-system provenance to source strain) | AGREE | none (see §4 for weak-test caveat) | — | n/a |
| C3 (distribution) | **PARTIAL** | Only 71-strain within-panel rarity replicated; cross-phyla ("bacterial classes") not run in this pass | Deferred to sibling NCBI-nr analysis (`36123438-Anti-phage-defense-Ecoli/`) | Yes — re-run BLASTP vs. NCBI-nr in this dir |
| C4 (MGE / hotspot) | AGREE with caveat | 5/21 systems with 0 MGE neighbours; keyword-based calls not orthogonal | Draft-assembly fragmentation (5/21); annotation-inheritance (all 21) | Partially — long-read reassembly for 5/21; PHASTER/geNomad for orthogonality |
| C5 (novelty vs. Gao 2020) | AGREE | Novelty inherited from Gao 2020 coverage, not audited against modern DefenseFinder/PADLOC | Table S4 re-read, no independent modern-catalogue check | Yes — see OQ2 in `open_questions.json` |
| **C6 (functional defence, wet lab)** | **CANNOT-TEST** | Entirely un-reproduced | **No SRA deposition of tab-selection raw reads** | **No** (blocked by data availability) |

## §1. C6 — the hard failure (no wet-lab reproducibility)

**What the paper claims (C6):** The 21 systems provide functional anti-phage defence, demonstrated by fosmid/tab selection, MOI growth assays, and adsorption assays against T4, λvir, and T7.

**What was reproduced:** Nothing. Zero.

**Root cause:** Vassallo et al. did not deposit raw selection-screen reads (no SRA record); the fosmid constructs, phage stocks, and wet-lab pipeline are not recoverable from any public repository this replication could access.

**Consequence:** The paper's central scientific claim — that these 32 proteins are functional anti-phage defence factors — is not independently verified by this replication. Everything replicated here (C1, C2, C3-panel, C4, C5) is genomic bookkeeping downstream of a wet-lab selection whose false-discovery rate is not measurable from the deposited artifacts. If the fosmid selection had, say, a 10% adsorption-artifact carryover past the 117-clone counter-screen, we would not see it in this replication. The honest statement is: "the paper's genomic bookkeeping is watertight; its functional claim is uncontested here but also unverified here."

**This alone is why the verdict is PARTIAL, not REPLICATED.**

**Fix path:** Deposition of the tab-selection raw reads (SRA) plus enough construct metadata to re-derive the surviving-clone → fosmid-insert → candidate-ORF pipeline would make C6 computationally testable. Absent that, C6 remains gated by data availability, no matter how much genomic bookkeeping is verified.

## §2. C3 — the partial-completion failure (cross-phyla not run)

**What the paper claims (C3):** Systems are distributed across *E. coli* and conserved across bacterial classes.

**What was reproduced:** Distribution within the 71-strain panel — all 21 systems detected in ≥1 strain, mean 2.9/71, min 1, max 11. Consistent with the paper's own statement that >10,000 of 21,149 gene clusters exist in only 1–2 strains.

**What was NOT reproduced:** The cross-phyla ("bacterial classes") half of the claim. This replication scopes to the 71 source strains as a BV-BRC group. The pan-bacterial breadth was deferred to a sibling directory (`36123438-Anti-phage-defense-Ecoli/`), which established via NCBI-nr BLASTP that 8/21 systems are present in ≥100 organisms.

**Root cause:** Explicit scope choice — this replication is the "BV-BRC-centred" re-analysis; the sibling directory is the NCBI-nr breadth re-analysis; the workspace convention is to leave the sibling read-only.

**Consequence:** C3 is honestly marked "◑ Partial" (not "AGREE") in REPORT.md. A reviewer reading only this directory would need to be pointed to the sibling for the cross-phyla evidence.

**Fix path:** Re-run BLASTP of the 21 representatives against NCBI-nr inside this replication directory, or explicitly import + cite the sibling evidence. Either is straightforward; the current state is a scope choice, not a methodological block.

## §3. C4 — the draft-assembly failure (5/21 systems)

**What the paper claims (C4):** Systems are carried on prophages / mobile genetic elements, clustered in defence hotspots.

**What was reproduced:** 16/21 systems with ≥1 MGE-signature neighbour within ±20 genes; 14/21 in a multi-defence hotspot. Several systems (PD-T4-6, PD-T4-8, PD-T7-3) have 33–34 MGE neighbours, i.e. sit in bona-fide prophage/IS regions.

**What partially failed:** 5/21 systems have 0 MGE neighbours (PD-T4-1, PD-λ-6, PD-T7-2, PD-T7-4, PD-T7-5).

**Root cause (attributed, not tested):** These 5 systems sit on shorter/fragmented source contigs where the flanking mobile context is truncated by assembly gaps — a well-known limitation of draft (multi-contig) genomes. The evidence for this attribution is circumstantial (short contig length in Table S2 for these cases), not experimentally verified.

**Weakness in this explanation:** This replication asserts "assembly fragmentation" but does not test it. A proper test would re-scaffold or long-read-resequence a subset of the 5 source contigs and re-run the MGE scan. Short of that, the C4 hotspot claim is "16/21 replicated + 5/21 unresolved," not "21/21 replicated."

**Fix path:** For the 5 affected source strains (UMB0934, UMB6655, UMB1091, UMB1727, UMB0934), pull any available long-read assemblies (PacBio HiFi, Oxford Nanopore) from ENA/SRA and rerun `mge_context.py` on the reassembled contigs. If MGE neighbours emerge, the draft-assembly hypothesis is confirmed and C4 becomes 21/21; if not, the paper's MGE-hotspot claim has a genuine 5/21 exception.

## §4. C2 — the weak-test failure (self-hit is a bookkeeping check)

**What the paper claims (C2):** 21 novel systems / 32 proteins are traceable to named source strains.

**What was reproduced:** 21/21 systems recovered in exactly their paper-declared source strain (self-identity ≥98%, coverage ≥90%).

**Weakness of the test:** "The declared source protein BLASTPs back to itself in the declared source strain's proteome at ≥98% identity, ≥90% coverage" is a bookkeeping check. It confirms:
- The correct FASTA was deposited under the correct accession.
- The paper did not mis-label its systems.

It does NOT confirm:
- The system was originally discovered in that strain (as opposed to being reassigned post-hoc).
- The fosmid insert coordinates were correct.
- The protein ORF boundary (start codon) is right.

**Consequence:** C2 as replicated is "deposition provenance is internally consistent," which is a real result but narrower than the phrase "provenance recovered" might imply.

**Fix path:** This is largely a definitional / framing issue rather than a re-runnable methodology failure. A stronger C2 test would coordinate-verify each protein by 6-frame translating the declared genomic region on a freshly downloaded contig — which is precisely what the 2026-07-03 independent reproduction did for 9/9 sampled proteins across 6 systems, all matching within 0–500 bp. The self-hit test in the primary pass could be upgraded to a coordinate-verify test for all 32 proteins.

## §5. Methodological weaknesses in this replication (not paper failures)

### §5.1 Annotation-based MGE and hotspot calls

Both the "MGE neighbour" and "defence-like neighbour" scores are keyword matches over BV-BRC product-name strings. This is fast and free but inherits every annotation error in the underlying assemblies (mis-called integrases, missed phage genes labelled "hypothetical protein," etc.).

**Impact:** The C4 numbers would not change under an independent recomputation *using the same annotations* — but they could shift under a genuinely orthogonal annotation pipeline (PHASTER, PHASTEST, geNomad, VirSorter2 for prophages; DefenseFinder, PADLOC for defence-system calls).

**Honest characterisation:** The C4 replication is "consistent with the paper's annotation" more than "independently confirmed on orthogonal annotation."

**Fix path:** Run geNomad + PHASTEST on the 21 source contigs; run DefenseFinder + PADLOC on the same contigs; compare per-system MGE and defence-like counts against the keyword-based numbers. Any large discrepancy is a real finding.

### §5.2 BV-BRC dual annotation inflated CDS counts

BV-BRC returns both RefSeq and PATRIC annotation sets for the same assemblies, roughly doubling raw CDS counts. This is flagged in REPORT.md §4.4 as "presence signal robust" — which is true for the CRISPR/RM 71/71 binary presence call, but strictly, exact CDS ratios should be re-derived from a single deduplicated annotation source before being reported cleanly.

**Impact:** Does not affect the qualitative "CRISPR-Cas and RM are ubiquitous in E. coli" conclusion; would affect any per-genome count-of-defence-genes analysis that this replication does not run.

**Fix path:** In `crispr_survey.py`, dedupe features by (contig, start, stop) tuple before counting, keeping the RefSeq annotation preferentially. Not needed for the current conclusion; needed if downstream analysis quantifies defence-gene load per genome.

### §5.3 LLM-judge is a coherence check, not an audit

The Argo `gpt-o3` LLM-judge returned Coverage 8/10, Agreement 9/10, verdict PARTIAL. These numbers are reported side-by-side with the human verdict of Coverage 8/10, Agreement 9/10, PARTIAL.

**Weakness:** The two agreeing does not independently validate the verdict — the LLM was fed the same result summaries the human wrote. It is a coherence check (does the writeup make internal sense to a fresh reader?), not an audit (does the writeup accurately reflect what the code produced?).

**Fix path:** For a true audit, an independent subagent should re-derive the numbers from the raw output files (`blast/rep_vs_all71.tsv`, `mge_context_summary.json`) without reading REPORT.md first, then compare to what REPORT.md claims. The 2026-07-03 independent reproduction is much closer to this — it re-derived 13/13 checkable numbers from primary sources without reusing this replication's scripts — and constitutes the stronger validation.

### §5.4 No negative control for C2

This replication does not run the C2 self-hit test on a set of proteins that *should not* recover in the 71-strain panel (e.g. 21 random *Salmonella* proteins).

**Weakness:** Without that, "21/21 recovered" is not calibrated: we know the positive rate is 100% but not the false-positive rate of the recovery pipeline.

**Practical impact:** Very low in this case — self-identity ≥98%, coverage ≥90% is a stringent criterion, and the probability of a random Salmonella protein passing it against an E. coli proteome is vanishingly small. But a proper replication would show the null.

**Fix path:** Run BLASTP of 21 random Salmonella (or Klebsiella, or Pseudomonas) proteins against the 71-strain E. coli proteome DB with the same tier thresholds; report expected 0/21 recovered.

### §5.5 C5 novelty inherits Gao et al. 2020 coverage

The 18/32 "not detected by Gao" number is a straight re-read of Table S4. Any coverage gap in the Gao et al. 2020 seed-cluster set (e.g. if their computation missed defence-island signals for reasons unrelated to novelty) would inflate our novelty count.

**Consequence:** C5 as replicated is "Table S4 as-published is internally consistent," not an independent novelty audit against a modern DefenseFinder / PADLOC database.

**Fix path:** See `open_questions.json` OQ2 — run current DefenseFinder + PADLOC on all 32 proteins, classify as (i) now a named family, (ii) partial hit, (iii) still unclassified; update C5 accounting.

## §6. Failures NOT in this replication (paper-level concerns)

These are limitations of the Vassallo et al. 2022 study itself, not defects in this replication, but a reviewer would ask about them:

- **Panel composition bias:** 52 ECOR + 19 UMB clinical isolates is entirely host-associated (enteric or urinary); no soil, water, or wildlife environmental isolates. Novel-system prevalence in an environmental panel is unknown. See `open_questions.json` OQ1.
- **Phage set bias:** The tab selection used only T4, λvir, T7 — 3 lytic dsDNA phages from three phage families. Systems active against Mu, P1, T5, N4, filamentous phages, or ssDNA/RNA phages are not addressable by this selection. See `open_questions.json` OQ2.
- **No cost-of-carriage measurement:** The paper does not measure the fitness cost of any of the 21 systems in phage-free conditions. For Abi-type systems this cost is expected to be nontrivial. See `open_questions.json` OQ4.
- **No counter-defence exploration:** The paper does not test whether T4/λ/T7 (or close relatives) encode counter-defence factors against any of the 21 systems. See `open_questions.json` OQ5.
- **Singleton dominance:** 14/21 systems are detected in only 1 of the 71 panel strains (the source strain). This is compatible with real rare defences or lineage-restricted mobile passengers whose defence function might not generalise; the paper does not distinguish these hypotheses.

## §7. Reproducibility failures (would-be issues, none observed)

For completeness — the following are common replication failure modes that could have hit this project but did not:

- **BV-BRC API downtime:** did not occur during the run; `curl --max-time` bounds every call.
- **NCBI Datasets rate-limit hit:** did not occur; 71 sequential fetches were within courtesy limits.
- **BLAST DB build failure on large concatenation:** did not occur; 140 MB / 348k proteins is well within `makeblastdb` capacity on standard OpenClaw hosts.
- **Argo proxy tunnel down during LLM-judge:** did not occur, but is a known intermittent risk on the `:44497` canonical port; if it fails, retry.
- **openpyxl parse crash on Vassallo suppl xlsx:** did not occur; xlsx is well-formed.
- **BV-BRC assembly_accession key mismatch vs. GCA versioning (`GCA_XXX.1` vs `GCA_XXX.2`):** did not occur here; the 2026-07-03 independent reproduction did surface one GCA→GCF consolidation (`GCF_003892355.1`) but resolved it to keep 71/71.

## Bottom line

The **only genuine failure** is **C6** (wet-lab functional defence, not computationally reproducible due to absent SRA deposition). Everything else is either (i) an AGREE with a methodological caveat that a reviewer should hear, (ii) a scope choice (C3 cross-phyla deferred to sibling), or (iii) an artifact of draft-assembly fragmentation (5/21 in C4).

The 2026-07-03 independent reproduction confirmed 13/13 checkable numbers, closing the residual concern that any of the AGREE claims might have been produced by reusing the same code paths — they were re-derived from primary sources with no code sharing.

**Verdict remains PARTIAL REPLICATION (strong)** because and only because of C6. If SRA were deposited, this would become a full REPLICATION.
