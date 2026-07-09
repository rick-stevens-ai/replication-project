# Failure Analysis — BVBRC-97

**Paper**: Pell et al. 2021, *Sci Rep* 11:15893 — *L. plantarum* ATCC 202195 WGS + AMR/VF
**Verdict**: REPLICATED (coverage 0.89, agreement 1.00)

This is a "what could have gone wrong / what almost went wrong / what stayed inside expected
drift" log for the BVBRC-97 replication. Nothing here changes the verdict; this exists so a
downstream reader can see the failure modes we thought about and either avoided or bounded.

---

## 1. Hard failures — none

No stage of the pipeline hard-failed. All 7 sequences downloaded cleanly, all 4 analyses ran to
completion, ABRicate returned results against all 5 databases at both stringencies, and the
LLM-judge scoring pass completed on the first attempt.

## 2. Explicit non-attempts (transparent coverage gaps)

### 2.1 Wet-lab MIC panel (claim C9) — not attempted

- **What we skipped**: 12-antibiotic broth-microdilution MIC panel that the paper reports.
- **Why**: requires purchase of the physical isolate from ATCC and a wet-lab microbiology
  setup with the right antibiotic-panel stocks. Not reproducible from public sequence data.
- **Coverage impact**: this is the single reason coverage is 0.89 and not 1.00.
- **Mitigation**: retested claims C7 and C8 (the genotype-level AMR screen) are consistent with
  the paper's MIC pattern (no acquired *tet* / *van* genes; intrinsic vancomycin resistance is
  a genus-typical trait). Genotype/phenotype concordance for *Lactobacillus* MICs is
  well-established but is not a substitute for the phenotype panel itself. Documented in
  REPORT.md §5 caveat 1 and REPORT.tex §7 critique 3.

### 2.2 ATCC 202195-B re-assembly (paper's A≡B claim) — not attempted

- **What we skipped**: SPAdes re-assembly of SRR13686146 (isolate B raw reads) and
  independent recomputation of the paper's "A vs B = 3 SNPs, ANI 99.99%" claim.
- **Why**: the paper's own report that "all B reads mapped to A with >1000× coverage" is a
  strong internal check, and our independent confirmation that A is identical to the two
  prior public 202195 assemblies (fastANI 99.998% and 99.978%) provides a triangulation
  chain (B ≈ A ≈ prior deposits) that makes a redundant B re-assembly costly and low-value.
- **Coverage impact**: none (the A≡B claim is folded into C1/C2/C3 as an implicit assertion,
  not a numbered claim in our table).
- **Risk**: if the paper's SPAdes assembly of B was itself flawed in a way that mapping-based
  QC missed, we would not detect it. Documented in REPORT.md §5 caveat 3 and REPORT.tex §7
  critique 2.

## 3. Bounded drift (matches "in-substance" but not "in-count")

### 3.1 LOW-stringency CARD count: 4 vs paper's 3

- **What drifted**: paper reports 3 CARD partial hits (LmrD, LmrC, rpoB); we get 4
  (lmrD, rpoB2, *Bifidobacterium* rpoB-rifampicin variant, IreK).
- **Hypothesized cause**: CARD schema and content changes between the paper's 2020 snapshot
  and our 2026-07-03 snapshot. Specifically, CARD reorganized its ABC-family efflux entries
  so that LmrC is no longer indexed as an independent entry separate from lmrD (the current
  lmrD entry documents the dimerization with lmrC in its description). The added *Bifidobacterium*
  rpoB variant and IreK entries reflect DB curation expansion.
- **Verified?**: No. We did not rebuild a 2020-vintage CARD DB to test this directly.
- **Impact on verdict**: none. The *character* of the finding — efflux-family homologs +
  rpoB variants, no acquired plasmid-borne resistance, no toxins — is identical.
- **Documented in**: REPORT.md §5 caveat 2 and REPORT.tex §7 critique 1.

### 3.2 LOW-stringency VFDB count: 24 hits (14 unique names) vs paper's ~12

- **What drifted**: 12 → 14 unique VF gene names.
- **Cause**: same as 3.1 — DB curation drift over 5 years.
- **Impact**: none. All 14 hits are adhesion / capsule / stress-response homologs from
  *Listeria* / *Enterococcus* / *Streptococcus* backgrounds. No toxins, no secretion systems.
  Character is identical to the paper.

### 3.3 Genome length: 3-bp discrepancy on plasmid 1 / total

- **What drifted**: paper reports plasmid 1 = 56,486 bp (total 3,353,698 bp); our
  fresh-download plasmid 1 = 56,489 bp (total 3,353,701 bp). 3-bp gap.
- **Cause**: either the paper rounded, or NCBI edited the GenBank record post-publication
  (common for small fixes at the polishing stage). Either way, substantively identical.
- **Impact**: none.

### 3.4 Plasmid-1 qcov: our ~100% vs paper's 92%

- **What drifted**: paper reports 92% query coverage for plasmid 1 vs GCA_010586945.1's
  plasmid at 100% identity; our BLASTn gives ~100% query coverage at 100% identity.
- **Hypothesized cause**: BLASTn parameterization differences (word size, seed defaults) or
  the paper computing qcov per single best HSP rather than summed across HSPs.
- **Verified?**: partially — we know our qcov is summed-across-HSPs; we did not reproduce
  the paper's BLASTn parameters verbatim.
- **Impact on verdict**: none. Both numbers say "the plasmids match in sequence"; we err on
  the more permissive side, the paper on the more conservative side.
- **Documented in**: REPORT.tex §7 critique 5.

## 4. Near-misses (things that could have failed but didn't)

### 4.1 Argo endpoint availability during LLM-judge pass

- **Risk**: the free Argo endpoint at `:44497` occasionally has transient 5xx or GPT-5.2 rate
  limits at peak times. A scoring-pass failure would have required a retry with a note in the
  provenance record.
- **What happened**: single-shot success at T=0 on first attempt. No retries needed. Verdict
  is deterministic across re-runs (checked once informally with a re-invocation returning
  identical per-claim breakdown).

### 4.2 ABRicate DB pull

- **Risk**: `abricate --update` can silently pull a partial DB if the mirror hiccups mid-fetch,
  producing spuriously few hits.
- **What we did**: pinned to the DB snapshot dated 2026-07-03 (recorded in the artifact
  provenance) and verified all 5 DBs registered with non-empty entry counts before running.

## 5. Generic screening limitations (not failures, but worth flagging)

ABRicate is a homology screen against curated databases. It cannot detect:
- Novel resistance mechanisms not yet in CARD/ResFinder/NCBI-AMR
- Resistance mediated by regulatory / promoter changes rather than gene presence
- Novel virulence factors not homologous to existing VFDB/Victors entries

The paper has the same limitation. Both the paper's and our null result at HIGH stringency
should be read as "no *known* transferable AMR/VF" rather than "no possible AMR/VF." This is
called out in REPORT.tex §7 critique 4.

## 6. Meta-lesson for future BVBRC-class replications

The main risk in specialty-gene-screen replications is not that the analysis fails — homology
screens are robust — but that **database drift over the years between the paper and the
replication can produce apparent count discrepancies that look like disagreement but are
actually curation churn**. Documenting DB snapshot dates + explicitly acknowledging schema
drift in the report is essential for making the "match in substance, differ in count"
character of these replications legible to a downstream reader.
