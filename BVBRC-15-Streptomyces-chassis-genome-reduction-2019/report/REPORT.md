# Replication Report: Bu et al. (2019)
## "Rational construction of genome-reduced and high-efficient industrial *Streptomyces* chassis based on multiple comparative genomic approaches"

**Paper:** Bu QT, Yu P, Wang J, Li ZY, Chen XA, Mao XM, Li YQ. *Microbial Cell Factories* 18:16 (2019).
**DOI:** [10.1186/s12934-019-1055-7](https://doi.org/10.1186/s12934-019-1055-7)
**PMC:** PMC6348691 — **PMID:** 30691531
**Open access:** ✅ (CC BY 4.0 / BMC)

**Report Date (re-pass):** 2026-06-27
**Analyst:** Ollie (OpenClaw AI) — BVBRC Replication Project, promotion-audit subagent
**Prior verdict:** NO-GO (coverage 2/10, agreement 8/10) — Wave-4 audit later reconciled to SPOT-CHECK
**Re-pass verdict:** **SPOT-CHECK** — confirmed; re-anchored on verifiable numerics, prior accession error corrected

---

## 1. Paper

Builds two genome-reduced *Streptomyces chattanoogensis* chassis strains — **L320** (≈ −1.3 Mb) and **L321** (≈ −0.7 Mb) — from the industrial natamycin producer **L10**, using comparative genomics + essentiality predictors to locate large non-essential regions and an optimized Cre/loxP system to excise them. Reports improved growth, transformation efficiency, ATP/NADPH balance, and heterologous polyketide/eGFP/IndC expression in L321.

Key disk-verified quantitative claims from the paper's full text:
- Deletion-1 (L320): "1.3 Mb-size located at 499,650–1,841,266 bp"
- Deletion-2 (L321): "0.7 Mb-size located at 7,994,797–8,731,201 bp"
- Two strains: L320 (large deletion, slower growth) and L321 (smaller deletion, healthy chassis)
- Cleaner secondary-metabolite HPLC profile in L321 (loses natamycin BGC inside the deleted block)
- Higher intracellular ATP and NADPH/NADP⁺ in L321
- Improved heterologous expression of eGFP (pL100), IndC (pTEindC), actinorhodin BGC (pMM1)

## 2. Claims tested

| # | Claim | Type | Testable from public artifacts? |
|---|---|---|---|
| C1 | Comparative-genomics identifies large non-essential regions in *S. chattanoogensis* L10. | Computational | ❌ No — L10 reference genome is NOT publicly deposited (see §5). |
| C2 | Cre/loxP can excise multi-hundred-kb regions in *Streptomyces* with high efficiency. | Wet lab | ❌ No — requires the authors' plasmids + recipient strain. |
| C3 | L320 (−1.34 Mb) and L321 (−0.74 Mb) are viable engineered strains. | Wet lab | ❌ No — strains not deposited under those names. |
| C4 | L321 shows better ATP/NADPH ratio, transformation efficiency, and heterologous polyketide titers than L10. | Phenotypic | ❌ No — requires constructed strains + HPLC + luminescence assays. |
| **CN1** | The reported deletion coordinates (499,650–1,841,266 bp and 7,994,797–8,731,201 bp) actually correspond to 1.3 Mb and 0.7 Mb. | Numerical | ✅ Yes — pure arithmetic on the paper's own numbers. |
| **CN2** | The L10 genome size is consistent with the deletion-2 endpoint at 8,731,201 bp. | Numerical (vs species) | ✅ Yes — checkable against the 5 NCBI *S. chattanoogensis* genomes. |
| **CN3** | The deletion magnitudes are plausible compared to existing genome-reduced *Streptomyces* chassis (e.g. M145 → M1146/M1152). | Literature-context | ✅ Yes — well-precedented. |

## 3. Method (this re-pass)

1. Pulled full Bu 2019 XML from Europe PMC (`PMC6348691/fullTextXML`) and grep-mined the Data-Availability statement, deletion coordinates, and any NCBI/BioProject accessions.
2. Re-queried NCBI Assembly for all current *S. chattanoogensis* entries (esearch + esummary, 2026-06-27).
3. Re-queried NCBI Assembly specifically for the L10, L320, L321 strain names.
4. Fetched the assembly-stats file for the *S. chattanoogensis* NRRL ISP-5002 type strain (`GCF_001294335.1`) from NCBI FTP and parsed its total length to anchor the species genome size.
5. Pulled total-length statistics for the other four *S. chattanoogensis* assemblies (NPDC001124/01300/01496/040912) directly from NCBI FTP.
6. Re-computed the paper's two deletion sizes from the coordinates given in the body of the paper, with bp precision.
7. Verified the prior REPORT.md's claim that the L10 reference lives at `NZ_AGSW00000000 / PRJNA208758` by querying that accession.

## 4. Numerical results vs paper (disk-verified)

| Claim | Paper value | This pass (re-computed) | Status |
|---|---|---|---|
| L320 deletion size | "≈ 1.3 Mb" | `1,841,266 − 499,650 + 1 = 1,341,617 bp = 1.342 Mb` | ✅ **verified** (matches paper to 3% — paper rounds down) |
| L321 deletion size | "≈ 0.7 Mb" | `8,731,201 − 7,994,797 + 1 = 736,405 bp = 0.736 Mb` | ✅ **verified** (matches paper to 5%) |
| Sum of deleted DNA | ~2.0 Mb | `1,341,617 + 736,405 = 2,078,022 bp = 2.078 Mb` | ✅ verified |
| Genome size of L10 | not stated directly in the paper; required to be ≥ deletion-2 endpoint = 8,731,201 bp | All 5 sequenced *S. chattanoogensis* genomes: 8.32–9.13 Mb (mean 8.80 Mb). Deletion endpoint at 8.73 Mb is internally consistent. | ✅ plausible |
| L320 as fraction of L10 genome | not stated as %; ≈ 15% with an ~8.7 Mb baseline | `1.342 / 8.7 = 15.4%` | ✅ within published range for streamlined *Streptomyces* chassis (M145→M1146/M1152 deleted ~1.4 Mb ≈ 17%) |
| L321 as fraction of L10 genome | not stated; ≈ 8% with an ~8.7 Mb baseline | `0.736 / 8.7 = 8.5%` | ✅ plausible |

### NCBI inventory of *S. chattanoogensis* (2026-06-27, disk-verified)

| RefSeq Assembly | Strain | Total length (bp) | Submitter |
|---|---|---|---|
| GCF_055593425.1 | NPDC040912 | 9,097,055 | UF Scripps |
| GCF_053597175.1 | NPDC001496 | 8,677,362 | UF Scripps |
| GCF_042897175.1 | NPDC001124 | 8,758,962 | UF Scripps |
| GCF_042896485.1 | NPDC001300 | 8,317,831 | UF Scripps |
| GCF_001294335.1 | NRRL ISP-5002 (type) | 9,129,105 | UIUC |

**Strains L10, L320, L321: 0 hits in NCBI Assembly.**
**Bu 2019 (PMID 30691531): 0 linked nucleotide records via ELink.**

## 5. Why the engineering claims are NOT reproducible from public data

The paper's verbatim Data Availability statement (fetched from EuropePMC full-text XML, 2026-06-27):

> "The datasets used and/or analysed during the current study are available from the corresponding author on reasonable request."

This means none of the following are deposited in a public repository:
- The L10 reference genome assembly used for the comparative-genomics analysis (the paper cites no BioProject / GenBank accession for it; PubMed → nuccore ELink returns 0 hits).
- The L320 and L321 mutant genome sequences (would have allowed direct verification of the deleted block by alignment).
- The Cre/loxP suicide plasmid sequences (pSETD / pSETP / pSET66 / pKC71 are described as the universal scaffolds but no GenBank deposits are cited).
- The lists of "essential" genes inferred from DEG / Geptop / OGEE for the L10 genome.

**Correction to the prior REPORT.md (2026-06-17):** that report stated the L10 reference genome lives at `NZ_AGSW00000000 / PRJNA208758 (Liu et al. 2013)`. This is wrong. Direct lookup of `AGSW00000000.1` returns a *Streptomyces sp. W007* WGS project (taxid 1055352, BioProject 74679, BioSample SAMN02472142) — not *S. chattanoogensis* L10. There is no publicly indexed L10 reference genome.

## 6. Verdict

**SPOT-CHECK** (re-affirmed from Wave-4 reconciliation, not promoted).

Three numerical claims (CN1, CN2, CN3) and one species-level metadata claim are verifiable from public data, and all check out. The four wet-lab / engineered-strain claims (C1–C4) are not reproducible from any public artifact because the L10 reference, the L320/L321 reduced genomes, and the Cre/loxP plasmids were never deposited. This is a **true non-reproducibility due to data deposition**, not a problem of audit effort.

**Why this is not promotable to PARTIAL:** PARTIAL requires reproducing a fraction of the *paper's* analyses on the *paper's* data. Without the L10 reference, none of the comparative-genomics steps (Mauve synteny, essentiality calls, IslandViewer GIs, ISsaga2 IS calls, antiSMASH BGCs) can be re-run. Without the L320/L321 sequenced derivatives, the deletion-block extents cannot be independently confirmed by re-alignment. The only thing we can confirm is that the **arithmetic on the coordinates is self-consistent and the magnitudes are biologically plausible** — which is exactly what SPOT-CHECK already means in this protocol.

**Why this is not a NO-GO either:** the original NO-GO label was earned by the engineering deliverables but underweighted the verifiable numerical content. The 2026-06-20 Wave-4 multi-judge panel correctly moved it to SPOT-CHECK; this re-pass agrees and *strengthens* the SPOT-CHECK by replacing a misattributed accession with a direct numerical verification of the deletion coordinates.

## 7. Coverage / Agreement (per AUDIT_PROTOCOL.md)

- **Coverage: 3 / 10** — bibliographic + species-genome inventory + disk-verified deletion-coordinate arithmetic + corrected accession claim. Still well below 50% scope (no L10 alignment, no essentiality re-run, no wet-lab anything).
- **Agreement: 9 / 10** on what *was* checked — every numerical claim that can be checked from the paper's own numbers + the public NCBI species-genome distribution checks out exactly (deletion sizes match to within rounding, genome-size envelope is consistent, deletion-as-fraction-of-genome lands in the documented range for streamlined *Streptomyces* hosts). The 1-point withhold is for the prior-report accession error that misdirected for ~10 days.

## 8. 6/22-rule blockers (named, in priority order)

Replication is blocked on **author-only deposition**. The exact missing artifacts are:

1. **L10 reference genome assembly (FASTA + GFF)** — corresponding author Y.-Q. Li, Zhejiang University. Without this, none of the comparative-genomics / essentiality / IslandViewer / antiSMASH / ISsaga2 calls in the paper can be regenerated.
2. **L320 and L321 sequenced derivatives (FASTA)** — without these, the deletion endpoints (claimed at 499,650 / 1,841,266 / 7,994,797 / 8,731,201 bp) cannot be confirmed by re-alignment to L10. Currently only the paper's own coordinate arithmetic is checkable.
3. **Universal Cre/loxP suicide plasmid sequences (pSETD, pSETP, pSET66, pKC71)** — without these, the engineering method (C2) cannot be reproduced.
4. **Essential-gene call tables from DEG, Geptop, OGEE on the L10 background** — without these, the rational-design step (which non-essential regions to delete and why) cannot be audited even if the L10 genome were released.

**Standing offer:** if the corresponding author releases items 1 + 2 above to NCBI (even as raw WGS / Nanopore reads), this paper becomes PARTIAL-viable for a follow-up pass — L10 vs L320 vs L321 alignment alone would let us verify both deletion endpoints to bp resolution and re-derive the deleted gene catalogs.

## 9. Resources used

| Resource | Use | Cost |
|---|---|---|
| Europe PMC REST API + full-text XML | Bibliographic harvest, data-availability statement, deletion coordinates. | Free. |
| NCBI E-utilities (esearch, esummary, elink) | Strain / assembly / nuccore / bioproject probes. | Free. |
| NCBI FTP (`ftp.ncbi.nlm.nih.gov/genomes/all/GCF/...`) | Assembly-stats files for all 5 *S. chattanoogensis* genomes. | Free. |
| BV-BRC public API | Strain / genome metadata (carried over from 2026-06-17 pass). | Free. |
| Compute | curl + python3 + bash on workspace host. | Negligible. |

LLM endpoint used for this re-pass: **argo:claude-opus-4.7** (free, per standing rule).

## 10. Tools / Datasets / Hardware

**Used in this pass:** Europe PMC, NCBI E-utilities, NCBI FTP, curl, python3.
**Required for full replication (still not used):** L10 / L320 / L321 genome FASTAs (author-held), Mauve / Mummer / DEG / Geptop / OGEE / IslandViewer 4 / ISsaga2 / antiSMASH, optimized loxP/Cre plasmids (author-held), HPLC for natamycin titer, ATP / NADPH luminescence kits, *Streptomyces* fermentation hardware.

## 11. Limitations

- No actual re-alignment performed (would require the L10 reference, which is not deposited).
- The plausibility argument for the deletion magnitudes uses the species-level genome-size distribution (8.32–9.13 Mb across 5 strains), not the L10 genome specifically.
- We did NOT contact the corresponding author for the L10 reference — that's a >day-scale process and out of scope for a free-endpoint promotion-audit pass.
- The full-text XML grep is text-based; if a BioProject accession is hidden inside an image, table image, or supplementary file we did not download, we would have missed it. EuropePMC's "Data references" panel showed 0 entries for this article, which makes that scenario unlikely.

---

## Audit Trail

- **2026-06-17** original Ollie pass → NO-GO, coverage 2/10, agreement 8/10. Cited `NZ_AGSW00000000 / PRJNA208758` as the L10 reference — **wrong accession** (W007, not L10).
- **2026-06-20** Wave-4 multi-judge audit (subagent; judges argo:gpt-5, argo:gemini-2.5-pro, argo:claude-opus-4.6) → reconciled to SPOT-CHECK by 3/3 panel vote. Median panel: coverage 2/10, agreement 8/10. Source: `/tmp/audit_bvbrc_wave4_judges.json`.
- **2026-06-27** promotion-audit re-pass (this report; argo:claude-opus-4.7 subagent):
  - Verdict re-affirmed at **SPOT-CHECK**.
  - Coverage **2/10 → 3/10** (added disk-verified deletion-coordinate arithmetic and corrected accession claim).
  - Agreement **8/10 → 9/10** (every numerical claim checkable from public data now checks out, plus W007 accession error fixed).
  - Original report preserved as `REPORT.md.bak-pre-promo`.
