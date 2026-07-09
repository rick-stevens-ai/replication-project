# Failure Analysis — BVBRC-103 (Fraser et al. 1995, *M. genitalium* G37)

## What failed or could not be done

### 1. PDF unobtainable (hard external block)
Fraser 1995 *Science* is paywalled; Unpaywall reports `is_oa=false` (zero OA locations) for DOI 10.1126/science.270.5235.397. Artifacts 1 (paper.pdf), 2 (marker.md), and 3 (nougat.mmd) are therefore stubs. **Impact: low** — the object of replication is the genome sequence, which is fully open at NCBI (NC_000908.2) and provenance-linked to the paper. The abstract (public) supplied all headline claims.

### 2. Not an ab initio re-sequencing (methodological scope limit)
We re-analyzed the curated RefSeq descendant (6 bp corrected over 30 years), not the raw 1995 shotgun reads. The paper's **assembly, gap-closure, and error-rate claims are untestable** from public artifacts and were not checked. This is inherent to any genome-era replication decades later, not a fixable failure — but it means "REPLICATED" applies to sequence-derived claims, not the 1995 wet-lab + assembly process.

### 3. C3 gene-count comparison is structurally apples-to-oranges (unresolved)
Fraser's ~470 ORFs (1995 gene-finders) vs our 504 intact CDS (2020s PGAP) cannot be directly equated. We did **not** rerun a 1995-era gene-finder to recover the actual 1995 call set, so the "annotation drift" explanation, while plausible, is **unproven**. This is the single largest interpretive gap and is now Open Question Q1/Q2.

### 4. Single-judge scoring (below policy ideal)
Scoring used one LLM judge (argo:gpt-4o, T=0.1). Standing policy prefers 3-judge scoring. The verdict is defensible because the numbers are unambiguous, but the scoring layer is thinner than ideal. **Fix:** re-score with 3 free judges if this dir is ever revisited for a rigor pass.

### 5. Untested paper content (scope)
Minimal-gene-set derivation vs *H. influenzae* Rd (Fig. 2), energy-metabolism/cell-envelope/replication-repair completeness, GC-skew, and individual functional predictions were not re-executed. Scoped out of a same-day quantitative-claim replication.

## Backfill-process failures (2026-07-05, meta)
This dir's report items (4–8) took **four subagent attempts** to land:
- `bf_bvbrc103_fraser` (3m5s), `bf_bvbrc103_finish` (3m8s), `bf_bvbrc103_light` (2m53s) all announced "writing the 5 files now" then the run terminated **before the batched final write executed**. Root causes: (a) subagents ingested the 780 KB `work/*.gb` genome file despite instructions, inflating context to 131–344 K input tokens; (b) the "write all 5 in parallel" pattern batches writes into one final block that never executes if the run ends first.
- **Resolution:** parent (Ollie main) wrote all 5 files inline from REPORT.md directly, bypassing the subagent failure mode. Lesson logged to failure-log.md; BACKFILL_BRIEF updated with a CONTEXT DIET rule (never read work/ sequence files) and a write-one-at-a-time (not "in parallel") directive.

## Net assessment
The **scientific** replication is solid (REPLICATED, all sequence claims reproduced). The **failures are (a) an external paywall with negligible scientific impact and (b) a backfill-tooling issue since resolved.** The honest interpretive caveat that matters for future work is the unresolved 1995-vs-2026 gene-call reconciliation (Q1/Q2).
