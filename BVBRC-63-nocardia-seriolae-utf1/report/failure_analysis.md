# Failure Analysis — BVBRC-63 (Yasuike et al. 2017, *N. seriolae* UTF1)

## What failed, was skipped, or is weaker than it looks

### 1. C8/C9 enrichment claims tested on the WRONG gene set (real scope gap)
The paper claims unknown-function (C8) and ABC-transporter (C9) enrichment specifically WITHIN the 1,982 UTF1-unique genes. Our keyword proxy counted these categories across the ENTIRE proteome of each strain, not restricted to the unique set. So "partial" here honestly means **we did not test the paper's actual claim**, not that we tested it and it half-held. **Impact: moderate** — these two claims remain effectively unverified. Fix = Q1 (COG/eggNOG enrichment on the unique gene set with hypergeometric testing).

### 2. Functional categorization is regex-on-descriptions, not proper functional annotation
All category counts (mobile elements, ABC, hypothetical, virulence) come from keyword matching on RefSeq `.faa` description lines. This is a coarse direction-of-enrichment proxy. Real COG/eggNOG/Pfam assignment was not done. **Impact: moderate for C7-C9, low for C1-C6** (which are pure sequence/count claims independent of functional annotation).

### 3. RBH orthology thresholds not sensitivity-tested
Core (2,718) and unique (1,967) counts used a single loose cutoff (pid>=25%, cov>=40%). The 99% agreement is excellent but conditioned on this choice; no threshold sweep was run. **Impact: moderate** — the headline comparative-genomics numbers could shift under different cutoffs. Fix = Q2.

### 4. CDS-count discrepancy across sources unreconciled
Paper 7,697; RefSeq 7,650; Prokka 7,648; and one per-species table shows UTF1 at 7,130 under a different annotation. The 99.4% agreement masks WHICH specific gene models are gained/lost between annotation pipelines. We reported all counts but did not diff the gene sets. **Impact: low** — all within ~1%, does not affect the replication verdict, but the exact provenance of the difference is unresolved.

### 5. Virulence claim (C10) is presence-only, orthology-unconfirmed
We confirmed the virulence-factor CLASSES exist (Mce, catalase/SOD, siderophore, efflux, beta-lactamase) but did NOT confirm these are the SAME orthologs the paper highlights, nor that they are functionally relevant. **Impact: low for verdict** (paper's claim was also presence-level), but it means "confirmed" here is weak. Fix = Q4.

### 6. Comparison set frozen at 2017's 4 genomes
The paper's (and our) comparative genomics used only the 4 complete Nocardia genomes available in 2017. The "1,982 unique" figure may substantially shrink against the larger current genome set — a known small-comparison-set inflation risk (cf. BVBRC-35). Not tested. Fix = Q5.

### 7. Single LLM judge (below policy ideal)
Verdict scored by one Argo judge (opus-4.7). Policy prefers 3-judge. Defensible given C1-C6 exact/near-exact agreement, but noted.

## Backfill-process note (2026-07-05, meta)
The first subagent attempt (bf_bvbrc63_inline) terminated in **4 seconds with no output** (transient spawn glitch / immediate no-op, only 6 output tokens — distinct from the "announce-then-die" pattern). Parent (Ollie main) verified files were missing and wrote all 5 report items INLINE from the existing 8.4 KB REPORT.md. Inline-parent-write remains the reliable fallback whenever a subagent crashes or REPORT.md is already rich.

## Net assessment
The **quantitative** replication is strong (C1-C6 all within 1% or exact, mobile-element enrichment dramatically confirmed). The **weaknesses are honestly in the qualitative/functional claims** (C8/C9 tested on the wrong gene subset; C10 presence-only; functional annotation coarse) — none contradicted, but two effectively untested. The real forward work is proper COG-based enrichment on the unique gene set (Q1) and threshold-robustness (Q2).
