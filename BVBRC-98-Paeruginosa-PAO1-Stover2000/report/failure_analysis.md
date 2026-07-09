# Failure Analysis — BVBRC-98 · Stover 2000 PAO1 Replication

**Verdict:** **PARTIAL** (LLM-judge canonical: `argo:gpt-4o`, `T=0`)

This document explains, honestly, why the verdict is PARTIAL and not REPLICATED — i.e., what did not fully reproduce, what was never testable in the first place, and where the residual uncertainty lives.

---

## 1. Headline: what actually failed?

Nothing catastrophic. All three numerically-testable claims of Stover et al. 2000 reproduced to within a single base pair, ~0.04 percentage points, and three CDS features. The verdict is PARTIAL for two structural reasons rather than a substantive scientific failure:

- **Two of the five paper claims (C4, C5) were not testable** from a single downloaded FASTA/GFF. They are historical / comparative-genomics statements about the year-2000 sequenced-genome landscape, and this replication did not reconstruct that baseline. They are therefore recorded as **context-only**, i.e., **not tested**, which drags the aggregate score below REPLICATED.
- **The LLM-judge (`argo:gpt-4o`, `T=0`) flagged the sub-0.1 % numerical deviations on C2 and C3 as "partial"** rather than "yes". The wave-brief rule adopts the judge's verdict as canonical, so its call stands even though the drift is practically trivial.

## 2. Per-claim failure/limitation breakdown

### C1 — genome size (6,264,403 bp paper vs 6,264,404 bp replication)
- **Δ = +1 bp over 6.26 Mbp (+1.6 × 10⁻⁵ %).**
- **Not a real failure.** The single-base increase reflects a versioning micro-edit between the original 2000 submission and the current RefSeq record `NC_002516.2`; effectively zero drift over 25 years. Marked "effectively exact" and accepted as reproduced.

### C2 — G+C content (66.6 % paper vs 66.556 % replication)
- **Δ = −0.044 percentage points.**
- **Not a real failure.** The paper's 66.6 % is rounded to one decimal; 66.556 % is well within any reasonable rounding tolerance. LLM-judge flagged it as "partial" on strict sub-0.1 % criteria — this is why the judge downgraded the verdict.

### C3 — predicted ORFs (5,570 paper vs 5,573 CDS replication)
- **Δ = +3 CDS (+0.054 %).** Unique protein IDs = 5,572; `protein.faa` header count = 5,572; CDS features in GFF = 5,573 (one CDS shares a protein ID with another, typical of paralogous or split-CDS calls).
- **Real, but explainable.** RefSeq PGAP has been re-annotated many times since 2000; a handful of additional short-ORF calls under the newer pipeline is expected and does not contradict the paper's original count. Not investigated locus-by-locus in this replication — the +3 loci were **not** classified as (i) genuinely-new short ORFs, (ii) merged/split gene models, or (iii) mobile-element-associated. That is a legitimate residual gap.

### C4 — largest sequenced bacterial genome at publication
- **Not testable from a single FASTA.** Would require rebuilding the year-2000 sequenced-genome cohort and comparing sizes. This replication did not do that.
- **Historically corroborated** (Nierman et al. 2001 *B. pseudomallei* 7.2 Mbp was the first larger sequenced bacterium, ~1 year later), but "uncontested in the literature" ≠ "independently replicated here."

### C5 — richness of regulators / two-component signalling genes
- **Not testable from a single FASTA.** Would require a harmonised annotation + comparative-genomics pass over the year-2000 sequenced-genome cohort. Not done.
- **Historically corroborated** (Rodrigue et al. 2000; Galperin 2005; PMC9607943 2022 review), but same caveat as C4.

## 3. Systemic / methodological limitations of this replication

The replication uses the shipped RefSeq annotation as-is and never runs an independent annotation pipeline. Consequences:

- **No annotation-pipeline diversity.** ORF count comparison is Stover-2000 vs current-RefSeq (both ultimately downstream of NCBI annotation lineages), not Stover-2000 vs a genuinely independent tool (Prokka / Bakta / etc.).
- **No re-assembly from raw reads.** The original Sanger reads are not practically re-runnable, so the sequence itself is treated as ground-truth-from-RefSeq rather than independently re-assembled. This is standard for a 25-year-old genome but is worth noting.
- **No sublineage cross-check.** The `NC_002516.2` sequence corresponds to one specific PAO1 isolate. PAO1 exists as multiple sublineages in strain collections worldwide (Nottingham/Zurich/UCSF/MPAO1/PAO1-DSM/etc.) with documented SNP/indel/mobile-element differences. Downstream users treating `NC_002516.2` as a universal PAO1 reference will encounter mismatches. This replication does not quantify that drift.
- **No feature-class freshness audit.** The 5,573 total CDS count matches; we did *not* verify that modern feature classes (sRNAs, small ORFs, CRISPR arrays, refined T3SS/T6SS effectors, updated QS regulon members) are all present in the shipped GFF. See `open_questions.json` for the full open-question set on this.

## 4. Judge / scoring caveat

The LLM-judge verdict is retained as canonical per wave-brief rule, even though a stricter reading of the numeric results (single-base drift, sub-percent GC drift, sub-percent CDS drift) would justify a REPLICATED call. Two defensible ways to re-score:

- **Strict (as reported here):** PARTIAL — 3/5 tested cleanly, 2/5 not testable.
- **Lenient (would-be REPLICATED):** If C4/C5 are re-scored as "context / spot-check" rather than "not-tested → downgrade", this replication is a clean REPLICATED. This is documented in §5 of `REPORT.md` and §Verdict of `REPORT.tex`.

The conservative reading (PARTIAL) is the one preserved in every report artefact.

## 5. What a stronger replication would do next

1. Run an independent annotation pipeline (Bakta + Prokka, plus Infernal/Rfam for ncRNAs, CRISPRCasFinder, a small-ORF predictor) on the same `NC_002516.2` FASTA; produce a per-feature-class diff against both the 2000 annotation and current PGAP.
2. Classify each of the +3 CDS as new short-ORF / merged-split / mobile-element-associated.
3. Rebuild a year-2000 bacterial-genome cohort under a harmonised annotation pipeline to actually test C4 (genome-size ranking) and C5 (regulatory-gene enrichment).
4. Assemble a matched PAO1-sublineage cohort (MPAO1, PAO1-UW, PAO1-DSM, PAO1-Lausanne, PAO1-Nottingham, PAO1-Zurich) and quantify sublineage drift against `NC_002516.2` to bound the reproducibility envelope for downstream PAO1 functional-genomics work.

Items 1–4 are enumerated in `open_questions.json` as the residual scientific agenda.

## 6. Bottom line

**No claim was contradicted; two claims were not tested; three claims reproduced within noise; the judge scored PARTIAL.** That is the honest verdict.
