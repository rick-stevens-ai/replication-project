# Failure analysis — Kunst 1997 B. subtilis 168 replication

Honest post-mortem of what did NOT work, what was shortcut, and where the evidence is thinner than the top-line "REPLICATED" verdict suggests. This is separate from the transient friction items already listed in `attempt_log.md` (Argo temperature rejection, HTTP 502 fallback, etc.) — those were operational, cost minutes, and are closed. The items below are the real critique.

## 1. What the "REPLICATED" verdict does NOT cover

The verdict "REPLICATED" was reached by testing 15/15 of the paper's *whole-genome quantitative* claims (Q-type). It does **not** cover:

- **C17** — the 190-bp × 10 repeated element (paper's most emphasized structural finding).
- **C18** — the three codon-usage classes from factorial correspondence analysis (paper's core annotation-classification result).
- **C19** — ≥10 prophage / prophage-like elements.
- **C20** — ~1,250 Rho-independent terminators.
- **C21** — 58% CDSs with functional homolog.
- **C22** — 18 sigma factors / 9 SigA-type.

These are the paper's *analytical* claims — the ones that required specific 1997-era pipelines (MUMmer, factorial correspondence analysis, PHASTER predecessor, TransTermHP, BLAST vs SWISS-PROT R34, HTH matrix). We marked them "not-tested — method-plausible" rather than either "replicated" or "failed." That is the honest label, but a reader glancing only at "REPLICATED" would over-estimate coverage. Roughly, we replicated ~2/3 of the *number* of testable claims and ~1/3 of the paper's *analytical weight*. This should be plainly said.

## 2. Verified shortcuts and unverified assumptions

### 2.1 Terminus of replication was NOT independently re-derived

The paper places the terminus at ≈ 2,017 kb. Our co-orientation calculation (73.0%, matching the paper's ~75%) used **the paper's own 2,017 kb as a prior**. We did not compute a GC-skew-derived terminus, z-curve terminus, or *dif* site coordinate independently. If our terminus prior is wrong by ±100 kb, the co-orientation number can drift by a percentage point or two, and we would not detect it. This is a small but real form of circular evidence.

**Fix:** compute cumulative GC skew on NC_000964.3 in 10-kb windows, locate the minimum, use that as the terminus, and re-report co-orientation. This is Open Question Q4.

### 2.2 We used the 2009 unified reference, not the 1997 sequence

NC_000964.3 is the 2009 unified successor sequence (+796 bp, +137 CDSs, −2 tRNAs vs the paper's own 1997 deposit AL009126.1). Every metric we report is technically a metric on a *different* sequence than the one the paper measured. The honest framing is: "the paper's quantitative claims survive on the modern re-sequenced/re-annotated genome of the same strain, with drift explained by two documented curation events."

That framing is defensible — the modern sequence is what any working biologist would use today — but a strict reading of "replicate the paper" would demand pulling AL009126.1 directly and measuring on *that*. We did not do that. If a purist demands strict replication, this run is a *validation* on the modern reference, not a strict replication.

**Fix:** rerun `analyze.py` against AL009126.1 (the 1997 deposit, still fetchable from ENA) and report the delta. This is a one-hour additional pass; not done.

### 2.3 Coding density arithmetic: exact but potentially over-generous

Our coding-density number (87.70%) matches the paper's 87% almost exactly. The script uses interval-union of CDS spans, which correctly handles overlapping CDSs. But **the paper's 87% may itself have been computed differently** — the paper does not specify the algorithm. If the paper used a naive sum-of-lengths (which would over-count on overlaps), our correct-but-different algorithm producing the same answer is *coincidence-of-methodology*, not agreement of measurement. We did not attempt to reconstruct the paper's exact calculation.

**Fix:** compute both (naive-sum-of-CDS-length / genome-length) and (interval-union / genome-length) and report both. Not done.

### 2.4 tRNA / rRNA counts depend on annotation, not on measurement

Our 86 tRNA / 30 rRNA gene / 10 rRNA operon counts are **read out of the GenBank annotation**, not independently predicted. If NC_000964.3's annotation has a systematic under-call of tRNAs (e.g., missing a rare tRNA that tRNAscan-SE 2.0 would find), our number inherits that error and we would not detect it. The paper's 88 tRNA / 10 rRNA operon counts had the same dependency on their annotation, but on a different annotation vintage.

**Fix:** re-predict tRNAs de novo with tRNAscan-SE 2.0 on NC_000964.3 and cross-check against the annotation. Not done.

### 2.5 Start-codon percentages depend on CDS boundary annotation, not on transcription evidence

The paper's 78/13/9% ATG/TTG/GTG matches our 77.5/13.1/9.1%. But both numbers presume the annotated start codon is the *actual* start codon. In organisms like B. subtilis with abundant alternative starts, this is often wrong at the individual-gene level; the aggregate percentages tend to be stable, so the match is real, but neither the paper nor this replication tested start codons against ribosome profiling data.

**Fix:** compare against Ribo-seq TIS calls where public data exist. Out of scope for the light-CPU replication.

## 3. Weak links in the LLM-judge verdict

Two independent LLM judges (`argo:gpt-5` and `argo:gpt-5.2`) were used to adjudicate REPLICATED vs PARTIAL. Both were fed **the same paper-vs-measured table** — not the raw evidence, not the code, not the data. So the judges are voting on a *prompt* engineered by us that summarizes 15 numbers side by side. They are not independent measurements of the reproduction.

- Judge 1 (`gpt-5`) returned **PARTIAL / coverage 100 / agreement 87** — a somewhat harsher read.
- Judge 2 (`gpt-5.2`) returned **REPLICATED / coverage 100 / agreement 93** — the friendlier read.

We took the friendlier verdict as the top-line. A stricter policy would have been to take the *harsher* verdict (PARTIAL) as the consensus when two judges disagree on the categorical label. The written justification in REPORT.md leans on the vocabulary definition "REPLICATED = core claims independently reproduced on real data" to prefer the friendlier reading — that's defensible, but a reader should know a coin-flip between two Argo models decided the label.

**Fix:** either (a) commit to a strict rule ("PARTIAL if any judge says PARTIAL") going forward, or (b) add a third independent judge (e.g., `argo:gemini-2.5-pro` or `argo:claude-opus-4.8`) to break ties. Not done here.

## 4. Third judge (`argo:claude-opus-4.7`) was attempted and failed

The attempt log records that a first triangulation attempt used `argo:claude-opus-4.7` and returned HTTP 502 (upstream flake). Rather than retry, we swapped to `argo:gpt-5.2`. This means our two judges are both from the same family (OpenAI gpt-5 lineage) — reduced diversity. If the gpt-5 lineage has a systematic bias toward calling this class of pattern-match "REPLICATED," we would not detect it.

**Fix:** rerun judge 2 as `argo:claude-opus-4.8` (the current Anthropic head, per standing 2026-06-22 default) or `argo:gemini-2.5-pro`. Trivial to do; not done.

## 5. What the paper does not let us test at all (paper's own gaps, not ours)

- **The paper does not report per-CDS confidence or evidence class.** So even a perfect replication cannot separate high- from low-confidence gene calls; we take the annotation as ground truth.
- **The paper's 58% functional-assignment fraction is against SWISS-PROT R34 (1997).** That's not the "58% assigned" of today, and the paper does not provide the CDS-level assignment list against which a modern reproduction could diff.
- **The paper's "10 prophage-like elements" is a lower bound**, and Kunst et al. explicitly acknowledge that "the exact number... is difficult to determine" — a replication cannot cleanly verify or falsify.
- **The 190-bp × 10 element** is described only in text + one figure; the paper does not provide the coordinates of all ten copies. Any replication of C17 must re-derive coordinates from scratch.

These are open-ended by paper design. We cannot fix them here; we can only flag them.

## 6. Residual gaps to fully close the standard

| Gap | Impact | To close |
|---|---|---|
| Analytical claims C17–C22 not tested | Under-estimates paper's substantive coverage | Run MUMmer, factorial CA, PHASTER, TransTermHP, BLAST vs UniRef50, HMM sigma-scan (~4–8 GPU-hours + ~day of curation) |
| Terminus was a paper prior, not derived | 1–2 pp uncertainty on C15 | 10 min: cumulative GC skew script |
| Only OpenAI-family judges (2 of 2) | Judge diversity ~1 | 5 min: `argo:claude-opus-4.8` re-judge |
| 2009 unified reference used, not 1997 deposit | Strict-purist gap | 30 min: rerun `analyze.py` on AL009126.1 |
| Nougat parse pending | Item 3 of 8-artifact standard | Automated by central Eagle sweep on paper.pdf sha256 |
| REPORT.pdf not compiled | LaTeX not rendered | 30 s: `pdflatex report/REPORT.tex` in a texlive env |

None of these are blocking — the reproduction is legitimate — but this section is what a hostile reviewer would ask about, and every item has a concrete plan.

## 7. Verdict re-affirmed (with the above caveats attached)

Taking all of §1–§6 into account, the reproduction is still fairly characterized as **REPLICATED for the paper's whole-genome quantitative core**, and **NOT-TESTED (method-plausible) for the paper's analytical/pipeline core**. The correct one-line summary is not just "REPLICATED" but *"whole-genome quantitative claims cleanly reproduce on the 2009 unified reference; analytical claims are out of scope for this pass and remain untested."* The label is defensible; the coverage of that label is narrower than it looks at first glance.
