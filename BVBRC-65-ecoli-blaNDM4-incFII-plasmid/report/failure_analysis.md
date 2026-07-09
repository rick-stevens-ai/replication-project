# Failure Analysis — BVBRC-65 (pMOL412_FII)

**Target:** Diaconu et al. 2020, *J Antimicrob Chemother* 75(12):3475–3479.
**Verdict as issued:** REPLICATED (spot-check).
**Date:** 2026-07-03.

This document is deliberately adversarial. It catalogues (a) failures that occurred during the replication, (b) failures that were *avoided but could have occurred*, and (c) failures that would only surface under a stricter replication standard than the one applied. This is the pair to the "Genuine Critique" section in `REPORT.tex`.

## A. Actual failures encountered

| # | Failure | Severity | Resolution |
|---|---------|----------|------------|
| A1 | Whole-genome assembly for host isolate MOL412 not present in NCBI (elink from BioSample `SAMEA6863320` to `assembly` returned 0 hits) | Blocking for C5, C6 only | Documented as spot-check-unverifiable rather than replicated or contradicted; scope explicitly narrowed to the deposited plasmid |

That is the entire actual-failure inventory. The replication otherwise ran clean end-to-end in ~5 minutes.

## B. Failures that were avoided (partial-credit)

| # | What could have gone wrong | Why it did not | Residual risk |
|---|----------------------------|----------------|---------------|
| B1 | Record identification could have returned the wrong plasmid (there are other IncFII / NDM-carrying plasmids in NCBI) | The plasmid name `pMOL412_FII` is highly specific and returned exactly 2 hits (INSDC + RefSeq mirror of the same submission); author + date + BioProject cross-matched paper metadata | Low — but the check was implicit, not asserted in the report |
| B2 | The abricate hit for `blaNDM-4` could be a mis-annotation of `blaNDM-1` (they differ by a single SNP) | Independent SNP-level check: extracted ORF, translated, verified Leu at residue 154 (M154L is the NDM-4-diagnostic substitution) | Small — but M154L is necessary, not sufficient (see A3 in Genuine Critique in `REPORT.tex`: NDM-5 also has M154L). abricate's 100/100% hit against the curated NDM-4 reference NG_049336.1 closes the gap; the M154L check is corroboration, not standalone proof |
| B3 | plasmidfinder could have missed the replicon or called it as a different Inc group | 100% identity + 98.85% coverage against IncFII_1 reference (AY458016) leaves no ambiguity | Very low |
| B4 | The 1-bp size delta (53,043 paper vs 53,044 GenBank) could have signalled a silent record versioning (LR812026.**1** → .**2**) | Assumed to be a start-position submission convention; not independently verified this pass | **Low but unverified.** A stricter pass would confirm record version and compare paper Figure 1 coordinates to `FEATURES` |
| B5 | Tool version drift could produce different hits on re-run | Tool + DB versions frozen (abricate 1.4.0, NCBI 8232 seqs 2026-Jul-3, plasmidfinder 488 seqs 2026-Jul-3) in `tool_versions.txt` | Contained by version-locking, but downstream re-runs against newer DBs may add hits |

## C. Failures under stricter replication standards

If the replication standard were tightened from "spot-check the deposited artifact" to "reproduce the paper's biology," the following would count as failures rather than out-of-scope items:

| # | Stricter standard | Would this pass? | What would be needed |
|---|-------------------|------------------|----------------------|
| C1 | "Confirm the plasmid assembles from the authors' raw reads" | ❌ Would fail | Raw reads not deposited; would require author outreach |
| C2 | "Confirm the isolate types as ST641 / O108:H23 from WGS" | ❌ Would fail | WGS not deposited; would require author outreach for reads or a fresh sequencing pass |
| C3 | "Confirm blaTEM-1B and sul3 are present in the isolate (C6)" | ❌ Would fail | Same reason as C2; the plasmid-only scan is silent, consistent with them being non-pMOL412_FII, but non-presence on the plasmid ≠ presence elsewhere |
| C4 | "Confirm the paper's phenotypic MIC panel matches" | ❌ Out of scope even in principle | Would require regrowing the isolate |
| C5 | "Independently place pMOL412_FII on a global NDM-4 IncFII plasmid tree (C7)" | ❌ Would fail | Deferred as out of scope this pass; a one-line `blastn` vs `nr` would partially close this at negligible cost |
| C6 | "Prove NDM-4 allele authenticity beyond M154L" | ⚠ Partially passes | The 100/100% abricate hit against NG_049336.1 (NDM-4 reference) is strong; the M154L residue check is corroborating but non-exhaustive (NDM-5 also has M154L + V88L). Full 270 aa alignment against the NDM allele set would be stricter |
| C7 | "Run negative controls (e.g. absence of KPC / OXA-48)" | ❌ Not performed | Would confirm pipeline is not saturating on every gene |

## D. Failure-mode classification (for downstream aggregation)

- **Data-availability failure:** 1 (A1 — authors deposited plasmid only, not WGS).
- **Tooling / pipeline failure:** 0.
- **Compute / infrastructure failure:** 0.
- **Interpretation failure (present):** 0 confirmed; ≥ 1 candidate (B4 — 1-bp offset accepted without independent verification of record version).
- **Scope-elision failure (would-fail-under-stricter-standard):** 6 (C1–C7 above, treating C6 as partial).

## E. What would flip the verdict

The verdict `REPLICATED` would need to be revised to:

- **CONTRADICTED** if any of the following were shown:
  - The deposited plasmid `LR812026.1` does not carry `blaNDM-4` (e.g. abricate hit is spurious).
  - The `blaNDM-4` ORF, when translated, does not have Leu at 154 and cannot be reconciled with the NDM-4 reference.
  - The plasmidfinder call is IncF but not IncFII, or is a different Inc group entirely.
  - The plasmid length differs from the paper by an order of magnitude (not by 1 bp).

- **INCONCLUSIVE** if:
  - The GenBank record were withdrawn or superseded to a different sequence content.
  - The paper's `pMOL412_FII` name were shown to refer to a different accession than the one we retrieved.

- **REPLICATED (full)** if in addition:
  - Raw reads were deposited and independently reassembled to the same plasmid.
  - WGS assembly confirmed ST641 / O108:H23 / TEM-1B / sul3.
  - Comparative analysis confirmed the pM109_FII relationship (C7).

Nothing seen in this pass moves the verdict off `REPLICATED (spot-check)`.

## F. Lessons for downstream targets in the BVBRC-100 wave

1. **Always run `elink → assembly` early.** Discovering that only the plasmid was deposited saved wasted effort trying to type the host and made the C5/C6 flagging honest rather than sheepish.
2. **SNP-level authentication of key alleles is cheap and worth doing every time**, even when abricate reports 100% identity, because it adds an independent line of evidence that survives DB corruption. (Consider extending: always translate the full ORF and align against the curated allele set, not just check one diagnostic residue.)
3. **Freeze DB build dates in the evidence directory.** Cost: one line in `tool_versions.txt`. Benefit: reruns are actually comparable.
4. **Do the negative control.** Missing here; add to the template for the next target.
5. **Do a cheap `blastn vs nr` for comparative claims (C7-class), even when out of primary scope**, because it partially closes the gap at negligible cost and is often the epidemiologically interesting claim.
