# FIRST_PASS_REPORT — LUCID100 Wave 3 Slot 24

**Paper:** Buglewicz, Haskins, Haskins, Su, Gius, Kato. *Exploring DNA repair deficient CHO cell response to low dose rate radiation.* BBRC **698**: 149539 (2024).
**DOI:** 10.1016/j.bbrc.2024.149539 · **PMID:** 38271835
**Master row:** rank 55, Wave 3, Tier A, priority 16, worktype tag `omics/signature replication` *(incorrect — see retag recommendation)*.
**Date:** 2026-06-09 (UTC).

## Verdict

| Aspect | Verdict |
|---|---|
| Full quantitative reproduction of paper's reported numbers | **NO-GO** — paper paywalled (Elsevier BBRC, oa_status=closed), no PMC, no preprint, no public dataset, no code. |
| Methodological scoping / claim-extraction | **GREEN** — claims fully enumerated from abstract + keyword list + Crossref references. |
| Cell-line panel reconstruction | **AMBER-GREEN** — recovered the likely 10B2/V3/51D1/xrs5/EM9 + irs/UV mutant panel from the Crossref reference list and the lab's two open-access companion papers; exact panel for this paper requires the paywalled PDF. |
| Smoke replication of qualitative central claims | **GREEN PARTIAL** — LQ + Lea-Catcheside G(λ) + NHEJ-IDRE smoke model qualitatively reproduces C1 (acute ordering), C2 (WT/HR dose-rate sparing), and C3 (NHEJ inverse dose-rate effect). 3/3 pass criteria. |
| Wet-lab endpoint reproduction (foci, growth inhibition, cell-cycle) | **BLOCKED** — wet-lab assays with no data deposit; not recoverable without author contact (out of scope). |

**Overall first-pass verdict:** **PARTIAL FIRST-PASS / SCOPING-ONLY.** The slot is a *wet-lab, paywalled, no-data-deposit* radiobiology paper. We can frame and qualitatively model the central claims using open-access companion data from the same lab, but we cannot quantitatively reproduce any number that appears in the BBRC paper itself.

## Reproduction matrix

| Claim ID | Description | Reproduction status | Evidence |
|---|---|---|---|
| C1 | NHEJ-deficient and HR-deficient CHO mutants are more radiosensitive than WT under acute γ. | **SMOKE PASS** | `data/smoke_summary.json["C1_acute_LQ_ordering"]`: SF(2 Gy) = 0.7261 (WT) > 0.5379 (HR-) > 0.3198 (NHEJ-); panel ordering consistent with Buglewicz 2023 PMC10727999 Table 1 SER values (1.00 / 1.63 / 1.72). |
| C2 | WT and HR-deficient cells show classical dose-rate sparing. | **SMOKE PASS** | LDR/acute SF ratio at D=4 Gy: WT = 1.548, HR- = 1.567. |
| C3 | NHEJ-deficient cells show an inverse dose-rate effect (IDRE). | **SMOKE PASS (mechanism)** | NHEJ- SF at acute = 0.0948, SF at worst LDR = 0.0451, ratio = 0.476 (<<1). Demonstrates the IDRE mechanism qualitatively; the actual Ḋ window and magnitude in the BBRC paper are unknown. |
| C4 | LDR alters cell cycle and induces giant-cell formation. | **BLOCKED** | Flow / microscopy data not deposited. |
| C5 | γ-H2AX foci accumulate during sustained LDR. | **BLOCKED** | Foci-count tables / image stacks not deposited. |
| C6 | Growth-inhibition assay shows pathway-specific LDR sensitivity. | **BLOCKED** | Growth-curve numbers paywalled. |
| C7 | HR mutants "align with" responses to other DNA-damaging agents. | **BLOCKED** | Cross-agent reference panel not in abstract. |
| C8 | Specific cell-line panel and dose-rate window. | **BLOCKED** | Requires the BBRC PDF. |

## Worktype reclassification recommendation

Master labels this slot `omics/signature replication`. This is **incorrect**.

The paper has **no omics component** (no transcriptomic, proteomic, epigenomic, or other high-throughput signature). It is pure wet-lab radiobiology: clonogenic assays, growth inhibition, γ-H2AX foci microscopy, cell-cycle analysis on a CHO-mutant panel.

Recommended retag:
- `worktype` → `wet-lab clonogenic + γ-H2AX foci panel comparison; no public data; OA-companion-anchored qualitative smoke only`
- `qa_decision` → `KEEP-as-scoping-only / RETAG`
- `verdict_or_plan` → `SCOPING ONLY: paywalled; no GEO/SRA/Zenodo/Figshare; smoke replication via LQ + Lea-Catcheside G(λ) anchored to Buglewicz 2023 PMC10727999 reproduces C1/C2/C3 qualitatively; C4-C8 blocked without BBRC PDF.`

This is **not a NO_GO** — the slot is still useful in the corpus as a clean case of a wet-lab radiobiology paper where qualitative-only replication via OA companion data is the maximum feasible. But the master's "omics" classification should be cleaned up to keep downstream consumers from expecting a dataset that does not exist.

## Compute and deliverables footprint

- All work executed on CherryRd in <2 minutes wall, CPU-only, no GPU, no HPC, no paid endpoints, no author contact.
- ~5 MB total artifact footprint (mostly the two OA companion PDFs).
- No heavy job plan needed; recorded job-plan section: **N/A**.

## Recommended next actions

1. **Master retag.** Update `LUCID100_SOLID_MASTER_QA.tsv` row `rank=55`:
   - `worktype`: `omics/signature replication` → `wet-lab clonogenic + γ-H2AX foci; no data deposit`
   - `status`: `candidate_curated` → `partial_first_pass_scoping_only`
   - `verdict_or_plan`: replace with the SCOPING-ONLY summary above.
2. **Keep the slot** in the corpus; it is the cleanest 2024 reference for the IDRE-in-NHEJ-mutants claim and complements the open-access companion papers we already have full text for.
3. **If a follow-up wave allows author contact or paid PDF purchase**, the BBRC paper's actual α/β and Ḋ values would let us replace the illustrative LQ parameters in `scripts/replicate_smoke.py` with measured ones and convert C1/C2/C3 from qualitative-pass to quantitative-pass.
4. **Cross-reference** with classic CHO LDR studies already cited (bib6 Jones 1986; bib7 Joshi/Ngo irs-20; bib12 Mateos 1989) — these may have already established the IDRE-in-NHEJ-mutants pattern, in which case the 2024 paper's novelty is the extended Fanconi/PARP panel and the γ-H2AX foci accumulation data, both of which are wet-lab-only.

## Blockers

- Closed-access publisher (Elsevier BBRC), `oa_status=closed`, no OA mirror.
- No PMC, no preprint, no thesis copy found at CSU Mountain Scholar.
- No GEO/SRA/ArrayExpress/Zenodo/Figshare/OSF deposit linked from any catalog we queried.
- Crossref reference list available; Semantic Scholar reference list elided by publisher policy.
- Wet-lab assays with no source-data spreadsheet deposit.

## Files of record

```
README.md                                      - overview + verdict
PROGRESS.md                                    - chronological log
FIRST_PASS_REPORT.md                           - this file
ARTIFACT_MANIFEST.tsv                          - 19 artifact rows
notes/claims.md                                - 8 extracted claims with reproduction status
scripts/replicate_smoke.py                     - LQ + Lea-Catcheside G + NHEJ-IDRE smoke
data/smoke_summary.json                        - numeric pass/fail
figures/acute_survival.png                     - C1 visualization
figures/dose_rate_sparing.png                  - C2/C3 visualization (IDRE shown)
artifacts/europepmc.json                       - EuropePMC search result
artifacts/semscholar.json                      - Semantic Scholar paper record
artifacts/unpaywall.json                       - Unpaywall record (oa=false)
artifacts/pubmed.xml                           - PubMed EFetch XML (MeSH + keywords)
artifacts/crossref.json                        - Crossref work record (21 references)
artifacts/sciencedirect_landing.html           - DOI redirect stub
artifacts/sciencedirect_page.html              - paywall page (403)
artifacts/buglewicz_cas15972_fullText.xml      - OA companion 2023 JATS
artifacts/buglewicz_cas15972_carbon_PMC.pdf    - OA companion 2023 PDF (2.1 MB)
artifacts/kato_2019_42600_carbon.pdf           - OA companion 2019 PDF (2.5 MB)
artifacts/kato_2019_42600_carbon.txt           - OA companion 2019 plain text
artifacts/smoke_run_output.txt                 - smoke script stdout
```
