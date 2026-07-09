# LUCID100 — slot 28 (Wave 3): Fractionated low-dose IR → DNA damage, epigenetic dysregulation, behavior

**Paper:** Koturbash I, Jadavji NM, Kutanzi K, Rodriguez-Juarez R, Kogosov D, Metz GAS, Kovalchuk O. *Fractionated low-dose exposure to ionizing radiation leads to DNA damage, epigenetic dysregulation, and behavioral impairment.* Environmental Epigenetics 2(4): dvw025, 2016.

- **DOI:** 10.1093/eep/dvw025
- **PMID:** 29492301
- **PMCID:** PMC5804539
- **Open access:** YES (Europe PMC full-text XML + PDF retrieved)
- **Citations (S2/master TSV):** 24
- **LUCID100 master row:** rank=59, wave=Wave 3, tier=A, priority=15, status=candidate_curated
- **Master worktype tag:** "omics/signature replication"
- **Actual worktype:** **wet-lab biomarker discovery + behavioral phenotyping** — *no omics, no signature, no code, no public data*

## Quick verdict
**NO-GO for computational replication.** This is a 2016 wet-lab study in C57BL/6 mice (n=8 control, n=60 treated). Endpoints are:
1. DNA-strand-break ROPS assay (scintillation [3H]dCTP DPM) → bar charts only (Fig. 2).
2. Western blot densitometry for p38, DNMT1, DNMT3a, DNMT3b, MeCP2 (Fig. 3, Fig. 5).
3. HpaII-based global methylation assay → bar charts only (Fig. 4).
4. Ladder-rung walking task + open-field exploration → bar charts (Fig. 6, Fig. 7).

There is **no transcriptome, methylome, or any omics deposit** in GEO/SRA/ENA/ArrayExpress, **no GitHub/Zenodo/figshare/Dryad code or data**, **no supplementary materials of any kind** (Europe PMC supplementaryFiles endpoint returns the standard "no supplements" landing page; the JATS XML contains zero `<table-wrap>` and zero `<supplementary-material>` elements). The master-TSV theme tag "omics / biomarkers / signatures" is incorrect — there are no omics in this paper.

The only computational content is **Student's t-test with Bonferroni correction (α/m, m=5)** and **one-way ANOVA + Tukey HSD** on the behavioral data, both performed in MS Excel 2007 and SPSS 11.5. No raw numerical tables are published.

## Replication scoping
| Layer | Feasibility | Notes |
|---|---|---|
| Wet-lab end-to-end | NO | 68 mice, 6-day fractionated 0.1 Gy/day X-ray irradiation, 4 brain tissues, scintillation counter, Western blots, two behavioral apparatuses. Out of scope for any computational replication. |
| Raw-data re-analysis | NO | No raw DPM counts, no Western densitometry CSV, no behavioral CSV released. |
| Figure digitization → re-fit | POSSIBLE BUT LOW VALUE | All 7 bar-chart figures could be digitized with WebPlotDigitizer; t-tests can be rerun. Yields only a check that the published p-values are arithmetically consistent — does not validate the biology. |
| Statistical methodology sanity check | YES (done) | `scripts/bonferroni_smoke.py` reproduces the α/m=0.01 threshold and demonstrates the Bonferroni correction logic explicitly stated in the paper. |
| Pipeline / signature replication | NA | No pipeline, no signature. |

## QA recommendation for `LUCID100_SOLID_MASTER_QA.tsv` row 72 (rank=59)
- **Retag worktype** from `omics/signature replication` to `wet-lab biomarker discovery — no replication target` or simply `wet-lab — figure digitization only`.
- **Retag themes:** drop `omics / biomarkers / signatures` (no omics in paper). Keep `dose-rate / low-dose response`. Drop `computational model / simulation` (no model). Add `epigenetics (global methylation, DNMT/MeCP2)`, `mouse brain regions`, `behavioral phenotyping`.
- **qa_decision recommendation:** change from `KEEP: relevant and replication-plausible` to **`KEEP for context, NO-GO for computational replication`** or drop tier from A to C/triage.

## Files
- `artifacts/` — harvested upstream artifacts (Crossref, Europe PMC search, JATS XML, PDF, OUP landing stub)
- `scripts/bonferroni_smoke.py` — minimal runnable smoke (Bonferroni-corrected t-test on synthetic FELDIR-shaped data)
- `notes/claims.md` — extracted quantitative claims from text (fold changes, p-values)
- `ARTIFACT_MANIFEST.tsv` — manifest with provenance + checksums
- `PROGRESS.md` — chronological log
- `FIRST_PASS_REPORT.md` — full verdict + scoping report
- `NO_GO_REPORT.md` — symlink/copy of FIRST_PASS_REPORT for the no-go path

## Heavy compute
None required. All work runs in <1 s on CherryRd Python 3. No GPU, no cluster job plan needed.

## Author contact
Not attempted (task rule). Authors would need to be contacted for any raw DPM / Western densitometry / behavioral CSVs, but the paper's computational footprint is too small to justify that even if data were obtained.
