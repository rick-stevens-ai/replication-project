# Artifacts Summary — lucid-mcmahon-2016-medras-original

**Slot:** LUCID / lucid-mcmahon-2016-medras-original
**Paper:** McMahon et al. 2016, _Sci Rep_ 6:33290, CC BY 4.0
**Verdict:** REPLICATED (COVERAGE=9/10, AGREEMENT=10/10)

All paths relative to
`~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-mcmahon-2016-medras-original/`.

---

## Upstream (fetched, hash-pinned)

| Artifact | Path | Role | Friction |
|---|---|---|---|
| Main paper PDF | `artifacts/srep33290.pdf` | primary source | none |
| Supplementary Methods PDF (35 pp) | `artifacts/supplementary_methods.pdf` | derivations §S1–§S5 | none |
| Supplementary Code ZIP | `artifacts/supplementary_code.zip` | 6 Python modules + 2 CSVs | py2, no internal manifest |
| Paper text extract | `artifacts/srep33290.txt` | grep-able | derived (`pdftotext`) |

## Derived (from fetched artifacts)

| Artifact | Path | How | Friction tags |
|---|---|---|---|
| Author Python source (6 modules, Py3-ported) | `code_py3/*.py` | unzip + 3-line Py2→Py3 port | `py2-migration` |
| Curated DNA dataset (188 rows) | `code_py3/Full DNA Data Sets.csv` | unzip (unchanged) | none |
| Curated survival dataset (192 rows) | `code_py3/Full Survival Data Sets.csv` | unzip (unchanged) | `implicit-cell-line-index` |
| Fig. 1 model curves | `results/Model Data - Foci Yields.tsv` | `python3 CellModelOutputs.py` | none |
| Fig. 2 model curve | `results/Model Data - Misrepaired Breaks.tsv` | `CellModelOutputs.py` | none |
| Fig. 3a model curves | `results/Model Data - Aberration Yield.tsv` | `CellModelOutputs.py` | none |
| Fig. 3b model curves | `results/Model Data - Aberration Kinetics.tsv` | `CellModelOutputs.py` | none |
| Fig. 4 model curve | `results/Model Data - Mutation Yield.tsv` | `CellModelOutputs.py` | none |
| Fig. 5 + Fig. 6 model curves | `results/Model Data - Survival.tsv` | `CellModelOutputs.py` | none |
| Fig. 5 4-panel PNG | `figures/fig5_reproduction_survival.png` | `scripts/plot_survival.py` | none |
| DNA fit log | `logs/dna_fit.log` | captured stdout of `DNAModelFit.py` | none |
| Survival fit log | `logs/survival_fit.log` | captured stdout of `SurvivalFit.py` | none |
| Cell-model output log | `logs/cell_model_outputs.log` | captured stdout of `CellModelOutputs.py` | none |

## Reports

| Artifact | Path | Role |
|---|---|---|
| Consolidated report (md) | `REPORT.md` | canonical 8-section report |
| First-pass report | `FIRST_PASS_REPORT.md` | Wave 7 long-form, retained for provenance |
| Manifest | `MANIFEST.md` | SHA-256 of every artifact + port diff |
| Slot README + progress | `README.md`, `PROGRESS.md` | slot context |
| Backfill report (LaTeX) | `report/REPORT.tex` | 8-artifact standard (this backfill) |
| Open questions (JSON) | `report/open_questions.json` | 5 truly-open audit-actionable questions |
| Open questions (LaTeX section) | `report/open_questions_section.tex` | mirror of JSON for `\input{}` into REPORT.tex |
| Workflow doc | `report/workflow.md` | tools, versions, work estimate, reproducer |
| This inventory | `report/artifacts_summary.md` | you are here |
| Failure analysis | `report/failure_analysis.md` | honest critique |
| Nougat extraction stub | `extraction/nougat.mmd` | placeholder + sha256 pointer |

## Compute traces

| Trace | Path | Content |
|---|---|---|
| DNA fit run | `logs/dna_fit.log` | `Chisq: 241.00226334052684` + full 9-parameter dict |
| Survival fit run | `logs/survival_fit.log` | ψ = 0.00848 ± 0.00106, φ = 0.01371 ± 0.00163 |
| Curve regen run | `logs/cell_model_outputs.log` | writes the 6 model-curve TSVs |
| Port diff | `MANIFEST.md` (bottom) | 3 textual Py2→Py3 changes across 6 files |

## Friction tags (glossary)

- `py2-migration` — upstream code is Python 2.7 (2016 vintage); trivially portable (3 lines) but not runnable cold on modern Python 3.
- `implicit-cell-line-index` — `Full Survival Data Sets.csv` uses a numeric cell-line index; primary-reference mapping is in SI Table S1 but not shipped as a joined TSV.
- `missing-mc-code` — the Monte Carlo run that pinned geometry constants `A = 0.757` and `B = 5.39` (SI Fig. S2) is *not* in the supplementary archive; only the resulting constants are.
- `no-requirements-pin` — supplementary archive has no `requirements.txt` or `SHA256SUMS`; environment reconstruction is by inference.

## Notably **absent** artifacts

- **Fig. 7 observed-vs-predicted MID scatter PNG** — not regenerated in this audit (open question #1).
- **A/B re-derivation Monte Carlo trace** — not attempted here (open question #2). Sibling `lucid-medras-mc/` is the plausible source.
- **GPU-parse extraction (`nougat.mmd`)** — placeholder only; this paper's text was extracted with `pdftotext`, which is sufficient for grep, and no equations/tables from the PDF drive the replication (the SI PDF text was read manually for method comparison).
