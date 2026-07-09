# Artifacts summary

**Slot:** `lucid100-cho-low-dose-rate-dna-repair-deficient`
**Snapshot:** 2026-07-06 backfill.

## Root-level artifacts

| Path | Role | Friction tags |
|---|---|---|
| `REPORT.md` | Canonical human-readable audit report (2026-06-22) + re-tier header (2026-06-25). **Verdict: NO-GO** (was SPOT-CHECK). | queue-mismatch (queue says REPLICATED, on-disk says NO-GO) |
| `FIRST_PASS_REPORT.md` | 2026-06-09 first-pass reproduction matrix; superseded by REPORT.md, retained for provenance. | superseded |
| `README.md` | Slot overview + panel reconstruction. | ok |
| `PROGRESS.md` | Chronological work log (2026-06-09). | ok |
| `ARTIFACT_MANIFEST.tsv` | 19-row artifact list from first pass. | ok |

## `report/` (this backfill, 2026-07-06)

| Path | Role |
|---|---|
| `report/REPORT.tex` | LaTeX version of REPORT.md with claims table, method, results-vs-paper, honest Critique section, and `\input` of the open questions. |
| `report/open_questions.json` | 5 truly-open scientific questions with `basis` + `next_steps` (JSON list). |
| `report/open_questions_section.tex` | LaTeX mirror of open_questions.json for `\input` into REPORT.tex. |
| `report/workflow.md` | Pipeline stages, tools/versions, work estimate, reproducer. |
| `report/artifacts_summary.md` | This file. |
| `report/failure_analysis.md` | Honest critique of what didn't work + residual uncertainty. |

## `extraction/`

| Path | Role | Friction tags |
|---|---|---|
| `extraction/nougat.mmd` | Stub with paper.pdf sha256 pointer; no GPU parse done because publisher PDF is not on disk (paywall). | paywall-blocked, no-pdf, no-parse |

## `scripts/`

| Path | Role |
|---|---|
| `scripts/replicate_smoke.py` | LQ + Lea--Catcheside G($\lambda$) + phenomenological NHEJ IDRE analytical smoke model. ~10 KB Python, deterministic, ~1 s runtime. |

## `data/`

| Path | Role |
|---|---|
| `data/smoke_summary.json` | Pass/fail booleans + numeric SF values for C1/C2/C3 from smoke model. Not a reproduction of paper numbers (those are paywalled). |

## `figures/`

| Path | Role |
|---|---|
| `figures/acute_survival.png` | C1 acute LQ panel curves (WT / HR$^-$ / NHEJ$^-$). |
| `figures/dose_rate_sparing.png` | C2/C3 SF vs $\dot D$ at $D=4$ Gy; IDRE visible for NHEJ$^-$. |

## `notes/`

| Path | Role |
|---|---|
| `notes/claims.md` | 8 extracted claims with reproduction status (matches REPORT.md table). |

## `artifacts/` (companion papers + metadata evidence)

| Path | Role | Friction tags |
|---|---|---|
| `artifacts/buglewicz_cas15972_carbon_PMC.pdf` | OA companion Buglewicz 2023 *Cancer Sci.* (PMC10727999) --- same lab, same panel. Used as SER anchor. | substitute |
| `artifacts/buglewicz_cas15972_carbon.pdf` | Duplicate carrier of companion PDF. | duplicate-ok |
| `artifacts/buglewicz_cas15972_fullText.xml` | JATS XML of companion. | ok |
| `artifacts/kato_2019_42600_carbon.pdf` | OA companion Kato 2019 *Sci. Rep.* (PMC6467899) --- CHO+xrs5 methodology. | substitute |
| `artifacts/kato_2019_42600_carbon.txt` | `pdftotext` dump of Kato 2019. | ok |
| `artifacts/kato_2020_uvb_panel.xml` | Additional Kato-lab panel reference. | substitute |
| `artifacts/crossref.json` | Crossref work record for target DOI (21 refs). | ok |
| `artifacts/europepmc.json` | EuropePMC probe for target DOI (no OA). | ok |
| `artifacts/pubmed.xml` | PubMed EFetch for PMID 38271835 (abstract + MeSH). | ok |
| `artifacts/semscholar.json` | Semantic Scholar record (`openAccessPdf.status = CLOSED`). | ok |
| `artifacts/unpaywall.json` | Unpaywall record (`is_oa=false`, `oa_status=closed`, locations=0). | ok |
| `artifacts/sciencedirect_landing.html`, `sciencedirect_page.html` | Paywall evidence (403 on full-content fetch). | paywall-evidence |
| `artifacts/smoke_run_output.txt` | Captured stdout of smoke model. | ok |

## Traces

- No wet-lab traces (no experiments run; the whole slot is analytical + metadata).
- No simulation traces beyond the deterministic smoke model output in `data/` and `figures/`.
- Metadata provenance traces are the JSON/XML files under `artifacts/`.

## Friction summary

| Friction | Impact |
|---|---|
| Paywalled Elsevier BBRC paper (no OA copy anywhere) | Blocks 5/8 claims outright; blocks numerical verification for 3/8 attempted claims. |
| No author-deposited source data (GEO / SRA / Zenodo / Figshare / OSF / Dryad / Mendeley Data all empty) | Blocks $\gamma$-H2AX foci reproduction, cell-cycle reproduction, growth-curve reproduction, and clonogenic-count-level statistical reproduction. |
| No CSU dissertation copy for Dylan Buglewicz | Blocks fallback route through thesis Methods section. |
| Orchestrator pipeline silently skipped paper staging | REPORT.md audit had to substitute companion papers + metadata; no `paper.pdf` / `paper.md` / `paper.txt` staged for this slot. |
| Queue label ``REPLICATED'' contradicts on-disk NO-GO | Verdict cross-check per Rick's 2026-07-06 rule: **on-disk NO-GO preserved**; queue label should be corrected upstream. |
