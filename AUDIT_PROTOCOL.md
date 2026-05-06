# Replication Audit Protocol
*Owner: Ollie. Applies to every paper in REPLICATE-PROJECT.*

A subagent saying "COMPLETE" means nothing until I audit it. Do NOT report a paper as "done" to Rick until ALL of the following are checked.

## 1. Scope Audit
- Pull the paper's actual scope from Methods/Results: how many organisms/proteins/datasets/figures does the paper analyze?
- Compare to what the replication actually covered.
- **Coverage threshold for "done":** ≥80% of the paper's primary analyzable units, OR a documented data-availability blocker for the gap.
- Anything below that is a "spot check" or "partial validation" — label it explicitly, don't call it a replication.

## 2. Claim Audit
- List every testable quantitative claim in the paper (Abstract + Results headline numbers + Tables).
- For each: did the replication test it? What's the result (verified / partial / contradicted / not tested)?
- A "verified" claim must have the replication's number within a reasonable tolerance of the paper's number; document the tolerance.
- **Threshold for "done":** ≥80% of testable claims tested, with explicit verified/contradicted status.

## 3. Method Audit
- Did the replication actually use the paper's methods (or a justified substitute)?
- Are critical thresholds, parameters, and statistical procedures matched (FDR, multiple-testing correction, exact identity cutoffs, etc.)?
- Substitutions must be documented and defended.

## 4. Output Audit
- REPORT.md exists, has methods + results + comparison table + honest verdict.
- Self-score is honest: if FDR was skipped, say so. If only 5/32 organisms were processed, the coverage score is 5/32, not 7/10.
- Generated artifacts (sequences, alignments, fitness tables, figures) are present and inspectable.

## 5. Verdict
For each paper, produce a single line in `STATUS_AUDIT.md`:
- **REPLICATED**: ≥80% scope, ≥80% claims, methods matched, paper supported.
- **PARTIAL**: clear gaps but useful signal.
- **CONTRADICTED**: replication disagrees with paper.
- **BLOCKED**: data/tools unavailable.
- **SPOT-CHECK ONLY**: <50% scope; needs more work.

## Anti-pattern: "subagent self-declares COMPLETE"
- Subagents are biased toward declaring success.
- Always verify against actual paper, not the subagent's summary.
- If in doubt, re-launch with explicit scope requirements.
