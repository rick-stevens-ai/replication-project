# FIRST PASS REPORT — LUCID100 slot 28 (Wave 3)

**Paper:** Koturbash I, Jadavji NM, Kutanzi K, Rodriguez-Juarez R, Kogosov D, Metz GAS, Kovalchuk O.
*Fractionated low-dose exposure to ionizing radiation leads to DNA damage, epigenetic dysregulation, and behavioral impairment.*
Environmental Epigenetics 2(4): dvw025, 2016. **DOI:** 10.1093/eep/dvw025 · **PMCID:** PMC5804539

**Verdict: NO-GO for computational replication.** Recommend QA retag on master TSV row 72 (rank=59).

---

## 1. What this paper actually is
A small in-vivo C57BL/6 mouse study (n=8 sham, n=60 treated; ages 60 d) testing whether five daily 0.1 Gy whole-body X-ray fractions (cumulative 0.5 Gy) produce:

1. DNA strand breaks in 4 brain regions (ROPS assay, [3H]dCTP scintillation).
2. Changes in stress-kinase p38 (Western blot).
3. Changes in global cytosine methylation (HpaII extension + scintillation).
4. Changes in DNMT1/3a/3b and MeCP2 (Western blot).
5. Behavioral changes (ladder rung walking, open field).

All seven figures are bar charts. There are **no tables**, **no supplementary materials of any kind**, and **no deposited data** (no GEO/SRA/ENA/ArrayExpress/ProteomeXchange/MetaboLights/BioStudies/EMPIAR/figshare/Zenodo/Dryad/GitHub entries appear anywhere in the JATS XML).

The master TSV (`LUCID100_SOLID_MASTER_QA.tsv`, row 72) tags this paper with:
- themes: `dose-rate / low-dose response; omics / biomarkers / signatures; computational model / simulation`
- worktype: `omics/signature replication`

**Neither omics nor a computational model is present in the paper.** Two of three theme tags are incorrect.

## 2. What is replicable computationally
Effectively only the **statistical methodology** described in the Statistical analysis section:

- Student's / Welch's t-test (DNA damage + Western blot panels), Bonferroni correction α/m with α=0.05, m=5 → per-test threshold **0.01**.
- One-way ANOVA + Tukey HSD on behavioral data, α=0.05.

`scripts/bonferroni_smoke.py` is a zero-dependency stdlib reproduction that:
1. Confirms 0.05/5 = 0.01 (matches the paper exactly).
2. On FELDIR-shaped synthetic cerebellum data (n=8 sham mean=1.0, n=6 treated mean=1.5, σ=0.10 — matching the paper's reported 1.5× Day-1 cerebellum DSB increase at P<0.005), the Welch t-test rejects H0 at the Bonferroni-corrected α=0.01 (observed p ≈ 5e-6).
3. Null synthetic data (no signal) fails to reject at α=0.01 (observed p ≈ 0.72).

Smoke runs in well under 1 s on CherryRd Python 3.13. **No heavy compute needed; no job plan required.**

## 3. What would be needed to do anything beyond the smoke
| Option | Cost | Value |
|---|---|---|
| WebPlotDigitizer on Figs 2–7 → rerun t-tests / ANOVA on digitized means and inferred SEMs | ~2–4 h of careful digitization, no compute | Low — only validates that the paper's published p-values are arithmetically consistent with their figures. Does not validate biology. |
| Wet-lab re-run (mice, irradiator, ROPS, HpaII assay, Westerns, behavioral apparatus) | Out of scope; months and IACUC approval | Not applicable to this campaign. |
| Author contact for raw DPM/densitometry/behavioral CSVs | Excluded by task rule | — |

## 4. QA recommendation for `LUCID100_SOLID_MASTER_QA.tsv` row 72 (rank=59)
**Retag:**
- **worktype:** `omics/signature replication` → `wet-lab biomarker discovery — no replication target` (or `figure-digitization only`).
- **themes:** drop `omics / biomarkers / signatures` and `computational model / simulation`; keep `dose-rate / low-dose response`; add `epigenetics — global methylation`, `mouse brain regions`, `behavioral phenotyping`.
- **qa_decision:** change from `KEEP: relevant and replication-plausible` to **`KEEP for context — NO-GO for computational replication`**.
- **tier:** A → C (or move to triage).

Effect on backlog: removes one Wave-3 tier-A slot from the replication queue and frees attention for papers that actually expose raw data or code.

## 5. Artifacts produced
See `ARTIFACT_MANIFEST.tsv` for the complete list with byte counts and sha256 hashes.

- `artifacts/crossref.json` — 22.9 KB Crossref metadata
- `artifacts/europepmc_search.json` — 6.1 KB EuropePMC search (confirms OA, PMC5804539)
- `artifacts/europepmc_fullText.xml` — 134 KB JATS full text
- `artifacts/europepmc_PMC5804539.pdf` — 1019 KB rendered PDF (13 pages)
- `artifacts/europepmc_supplementaryFiles.html` — 10 KB landing page (no supplements available)
- `artifacts/oup_landing.html` — 5.5 KB OUP page (Cloudflare-walled; informational only)
- `artifacts/paper_methods_results.txt` — 46 KB extracted methods/results/discussion text
- `scripts/bonferroni_smoke.py` — runnable Bonferroni-corrected t-test smoke (PASS)
- `notes/claims.md` — extracted quantitative claims (fold changes + p-values) per tissue/timepoint
- `README.md`, `PROGRESS.md`, `FIRST_PASS_REPORT.md`, `NO_GO_REPORT.md`

## 6. Blockers and next actions
**Blockers:** none. Work is complete within scope.

**Next actions** (recommended priority):
1. **Apply QA retag** on `LUCID100_SOLID_MASTER_QA.tsv` row 72 (rank=59) per §4 above.
2. (Optional, low value) Digitize Figs 2–5 with WebPlotDigitizer if a Bonferroni-consistency audit of the paper's p-values is wanted.
3. **Do not contact authors** (per task rule), and do not allocate further compute or human effort to slot 28.

## 7. Author contact / paid endpoints / heavy compute
- Author contact: not attempted (task rule).
- Paid endpoints: not used.
- Heavy compute: not required; smoke runs in <1 s on CherryRd Python stdlib. No CherryRd-avoidance issue; no job plan needed.
