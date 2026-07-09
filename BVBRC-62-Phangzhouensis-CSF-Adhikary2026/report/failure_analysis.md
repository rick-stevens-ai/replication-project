# Failure Analysis — BVBRC-62
## What did not replicate, why, and how bad it is

Adhikary et al. 2026 (MRA e01372-25) — *Providencia hangzhouensis* HL_Adamas-11.
Verdict: **PARTIAL** (Argo `gpt-5.2` LLM judge, temp 0; Coverage 8/10, Agreement 7/10).

This document enumerates every replication miss, classifies severity, assigns a root cause, and states what remediation would look like. Findings are grounded strictly in `report/REPORT.md`; no external claims are introduced.

---

## Failure 1 — GC content: paper 49.5% vs true ~42.4%

| Field | Value |
|---|---|
| Paper claim | GC = **49.5%** |
| My independent recompute (Biopython on deposited FASTA) | **42.35%** |
| NCBI's own assembly-report GC field for the same deposit | **42.5%** |
| Delta | ~7 percentage points |
| Severity | **HIGH (as a paper defect); LOW (as a scientific-conclusion risk)** |
| Root cause | Manuscript transcription/reporting error. The deposited sequence is unambiguously ~42.4% GC by two independent methods on two independent code paths. |
| Reproducible by anyone from public data? | Yes — the paper is wrong; the sequence is right. |
| Blocker for the core claim (MDR CSF *P. hangzhouensis* isolate)? | No. |
| Remediation | Erratum. GC should be corrected to 42.4% (± rounding). |
| Genus-plausibility check | *Providencia* is a ~41–42% GC genus; 49.5% would be biologically anomalous and would itself trigger a species-misassignment suspicion. That suspicion is fully resolved by ANI. |

**Interpretation:** This is the single hardest numeric failure but the cheapest to explain. Every other architecture number (contigs 493, N50 16,147, coverage 91.664×, CDS 4,935, tRNA 59, rRNA 4, plasmid count 4) matches exactly — arguing strongly that only the GC digit is wrong, not the underlying sequence.

---

## Failure 2 — MLST: paper ST-356 vs my ST-unassigned

| Field | Value |
|---|---|
| Paper claim | ST-356 (PubMLST *Providencia* scheme) |
| My call | ST = `-` (unassigned/novel); alleles fusA(17) gyrB(105) ileS(29) lepA(~49) leuS(49) |
| Tool | `mlst` v2.33.1 (Torsten Seemann) with bundled PubMLST *Providencia* scheme |
| Severity | **MEDIUM (methodological); LOW (biological)** |
| Root cause | **Scheme/DB-version mismatch.** The `mlst` package ships the classic PubMLST *Providencia* scheme (largely built around *P. stuartii*). The live PubMLST DB has since added *P. hangzhouensis* profiles. Without the pinned scheme version / download date the authors used, ST-356 cannot be deterministically reproduced. |
| Reproducible in principle? | Only if the paper had disclosed (a) PubMLST download date, or (b) the per-locus allele numbers, or (c) the exact allele-profile file used. |
| Blocker for the core claim? | No — species assignment rests on ANI (98.46–98.62%, well above the 95% threshold), not MLST. |
| Remediation | Authors could republish (a) PubMLST DB snapshot date + (b) the 7- or 5-locus allele profile they called. Any future replicator could then either recreate ST-356 or issue a corrected ST number under the current live scheme. |

**Interpretation:** Not necessarily a contradiction — an information gap. The paper is not falsified; it is under-specified.

---

## Failure 3 — Allele-nomenclature drift in the AMR cassette

| Field | Value |
|---|---|
| Paper says | `aph(3')-V` |
| Real gene | `aph(3')-VI` (there is no valid `aph(3')-V`) |
| Paper says | `aadA21` |
| My AMRFinderPlus resolves to | `aadA1` + `aadA2` |
| Severity | **LOW** |
| Root cause | Likely manuscript typos and/or different reference-DB allele-naming conventions (paper appears to have used CARD v6.0.5 + ResFinder v4.7.2; my replication used AMRFinderPlus v4.2.7 with DB 2026-05-15.1). |
| Reproducible? | Class-level resistance (aminoglycoside modification) — yes, unambiguously. Exact allele label — no, differs by tool/DB. |
| Blocker for the core claim? | No. |
| Remediation | Erratum to correct `aph(3')-V` → `aph(3')-VI`; note tool/DB provenance for `aadA` sub-alleles. |

---

## Failure 4 — CheckM completeness/contamination not re-run

| Field | Value |
|---|---|
| Paper values | Completeness 93.78%, Contamination 5.14% |
| My values | Not measured (out of scope) |
| Severity | **LOW (soft coverage gap)** |
| Root cause | CheckM v1.2.4 needs a heavy lineage DB; excluded from this replication scope. |
| Reproducible? | Yes, in principle — CheckM v1.2.4 on the deposited assembly would either confirm or refute. |
| Blocker for the core claim? | No, but contamination 5.14% sits above the MIMAG ``<5%`` high-quality threshold — worth a check in a follow-up. |
| Remediation | Add CheckM (or CheckM2) run in a future pass. |

---

## Failure 5 — Total assembly length: 5,034,782 bp (paper) vs 5,024,867 bp (mine)

| Field | Value |
|---|---|
| Delta | −9,915 bp (−0.20%) |
| Severity | **NEGLIGIBLE** |
| Root cause | GenBank routinely filters/removes short or low-quality contigs at deposit; the paper's number likely reflects the pre-deposit assembly, mine reflects the deposited FASTA. |
| Reproducible? | Yes — this is the expected GenBank filtering behavior. |
| Blocker for the core claim? | No. |
| Remediation | None needed; document. |

---

## Non-failures that could have gone wrong but did not

- **All 5 β-lactamases** including blaNDM-1 (carbapenemase) and blaOXA-181 (OXA-48-like carbapenemase) — recovered exactly.
- **All 5 macrolide/phenicol genes** (mph(E), msr(E), mrx(A), catA1, cmlA5) — recovered exactly.
- **armA** (16S methyltransferase, pan-aminoglycoside) — recovered exactly.
- **Species assignment** by ANI (98.46–98.62%) — matches paper's 98.75% within 0.3%.
- **Plasmid count** — 4 distinct plasmid contig names in NCBI assembly match paper's "chromosome + 4 plasmids".
- **CDS / tRNA / rRNA counts** — all exact.

---

## Summary table

| Failure | Severity | Root cause | Blocks core claim? | Remediable? |
|---|---|---|---|---|
| GC 49.5% vs 42.4% | HIGH (paper) / LOW (science) | Manuscript typo | No | Yes — erratum |
| MLST ST-356 unconfirmed | MEDIUM (method) / LOW (bio) | Scheme-version mismatch | No | Yes — pin PubMLST snapshot |
| aph(3')-V / aadA21 nomenclature | LOW | Typo + tool DB differences | No | Yes — erratum |
| CheckM not re-run | LOW | Out of scope | No | Yes — future CheckM pass |
| Length −0.20% | NEGLIGIBLE | GenBank filtering | No | N/A — expected |

---

## Meta-conclusion

The core scientific findings of the paper (MDR *P. hangzhouensis* CSF isolate carrying blaNDM-1 + blaOXA-181 + armA + a broad macrolide/phenicol/co-trimoxazole/tetracycline resistome across chromosome + 4 plasmids) are **fully replicable** from public data using free/OSS tools. The **PARTIAL** verdict is driven by:

1. A wrong GC number in the manuscript (unambiguously refuted by the deposited sequence).
2. An under-specified MLST call (scheme version not pinned; live PubMLST has drifted).
3. Two allele-name typos in the AMR cassette (class-level resistance unaffected).

None of these erode the paper's central announcement claim; they are QC/reporting issues that would benefit from a short erratum. The MDR announcement is if anything **understated** — a modern AMRFinderPlus screen recovers substantially more resistance determinants than the paper enumerates.
