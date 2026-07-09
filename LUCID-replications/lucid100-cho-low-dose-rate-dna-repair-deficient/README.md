# LUCID100 Wave 3 Slot 24 — CHO Low-Dose-Rate DNA Repair-Deficient

**Paper:** Buglewicz, Haskins, Haskins, Su, Gius, Kato. *Exploring DNA repair deficient CHO cell response to low dose rate radiation.* Biochem Biophys Res Commun (BBRC) **698**: 149539 (2024).
**DOI:** [10.1016/j.bbrc.2024.149539](https://doi.org/10.1016/j.bbrc.2024.149539) · **PMID:** 38271835
**Master rank:** 55 · **Tier:** A · **Priority:** 16
**Master worktype:** omics/signature replication *(see worktype reclassification below)*
**Source of truth:** `/Users/stevens/.openclaw/workspace/lucid-replications/LUCID100_SOLID_MASTER_QA.tsv` row `rank=55`.

## Verdict (first-pass)

**RED / partial-scope NO-GO for direct quantitative reproduction; AMBER for scoping + companion-paper smoke replication.**

Direct quantitative reproduction of the BBRC 2024 paper is **not feasible** from public artifacts:
- Closed-access Elsevier paper, `oa_status=closed`, no OA PDF anywhere (Unpaywall, EuropePMC, ResearchGate, CSU Mountain Scholar, bioRxiv all empty / 403).
- No PMC record (only PubMed MED record).
- Reference list elided from Semantic Scholar by the publisher; recovered via Crossref (21 refs).
- No GEO / SRA / ArrayExpress / Zenodo / Figshare deposit linked anywhere we can find. No code or supplementary spreadsheets accessible without subscription/purchase.
- This is a pure wet-lab / radiobiology paper: clonogenic assays, growth-inhibition assays, and γ-H2AX foci microscopy on a panel of CHO DNA-repair-mutant cell lines exposed to acute and low-dose-rate (LDR) γ-ray irradiation. No transcriptomic / omics data product is produced — the paper has **no signature dataset to deposit even if the authors wanted to.**

A constructive partial replication is feasible at scoping level using the same lab's open-access companion paper (Buglewicz et al. 2023, *Cancer Sci.*, PMC10727999) which uses the same CHO mutant panel (10B2 WT, 51D1 HR-, V3 NHEJ-) with similar clonogenic-survival methodology. We:
1. Extract D10 / SER values from the OA carbon-ion companion paper.
2. Build a closed-form linear-quadratic (LQ) + Lea-Catcheside G(λ) factor smoke model that reproduces the **qualitative direction** of the BBRC paper's central claims: HR mutants show a normal-to-large dose-rate sparing (G < 1 at low Ḋ); NHEJ mutants paradoxically show an **inverse dose-rate effect** (effective α boosted at low Ḋ).
3. Document what cannot be done without the BBRC PDF or the corresponding author's spreadsheets.

## Worktype reclassification

Master labels this slot `omics/signature replication`. Based on the abstract + MeSH + reference list, the correct classification is:

> **wet-lab clonogenic / γ-H2AX foci radiobiology; small-N panel comparison; no omics.**

Recommended retag: `wet-lab clonogenic + γ-H2AX foci; no data deposit; OA-companion-based smoke replication only`. The "omics" tag should be removed at the master level.

## Cell-line panel (reconstructed from abstract + companion papers + Crossref refs)

| Line   | Defect / pathway       | Source ref          |
|--------|------------------------|---------------------|
| 10B2 / AA8 / CHO-K1 | wild type | companion 2023 |
| V3     | DNA-PKcs / NHEJ        | companion 2023; bib11/14 |
| xrs5/6 | Ku80 / NHEJ            | bib7, bib11        |
| XR-1   | XRCC4 / NHEJ           | bib20              |
| irs-1 / irs1SF | XRCC2 or BRCA2 / HR | bib11        |
| irs-2  | HR / cell-cycle PLD    | bib7, bib12        |
| irs-3  | RAD51C / HR            | bib11              |
| 51D1   | RAD51D / HR            | bib8; companion 2023 |
| UV5 / UV41 | ERCC2/4 / NER     | bib11              |
| UV61   | ERCC6 / TC-NER         | bib11              |
| EM-C11 / EM9 | XRCC1 / PARP-axis | bib10           |
| (Fanconi mutant — e.g. UV40 / KO40) | FANCD2-axis | (not in refs; assumed from abstract) |

This is the most likely panel; exact panel and dose-rates require the actual BBRC PDF.

## Endpoints studied (from abstract)

1. **Clonogenic survival** under acute γ vs LDR γ — LQ fits and dose-rate sparing factors.
2. **Cell growth inhibition / population doubling** under sustained LDR exposure.
3. **γ-H2AX foci** accumulation during LDR exposure — DSB induction-vs-repair steady state.
4. **Cell cycle distribution** under LDR — claim: shifts + giant cell formation.

## Folder layout

```
artifacts/        # raw harvested artifacts (JSON metadata, PDFs of OA companion papers, JATS XML)
data/             # reconstructed data tables (D10, SER, dose-rate matrix from companion paper)
scripts/          # python smoke / fitting scripts
notes/            # claim list, methodology notes
figures/          # smoke-model output figures
PROGRESS.md       # per-step log
FIRST_PASS_REPORT.md  # final verdict + reproduction matrix
ARTIFACT_MANIFEST.tsv # one row per artifact
```

## Compute footprint

CPU-only. Runs in seconds on CherryRd. No HPC needed; no GPU; no internet at run time.

## See also

- `FIRST_PASS_REPORT.md` — reproduction matrix and verdict.
- `PROGRESS.md` — chronological work log.
- `notes/claims.md` — extracted testable claims with reproduction status.
- `scripts/replicate_smoke.py` — LQ + G(λ) inverse-dose-rate effect smoke model.
