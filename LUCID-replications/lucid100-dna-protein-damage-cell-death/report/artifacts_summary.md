# Artifacts inventory

## Top-level (pre-existing)
| Path | Size class | Purpose |
|------|------|---------|
| `README.md` | small | Slot orientation |
| `FIRST_PASS_REPORT.md` | small | Original subagent notes from 2026-06-09 |
| `REPORT.md` | ~15 KB | Canonical Markdown report (10-section, honest verdict PARTIAL) |
| `PROGRESS.md` | small | Chronology of harvest commands + reruns |
| `MANIFEST.json` | small | Machine-readable manifest of artifacts + model parameters |

## `artifacts/`
| File | Origin | Purpose |
|------|--------|---------|
| `paper_oai.xml` (~80 KB) | PMC OAI-PMH `GetRecord` for `oai:pubmedcentral.nih.gov:3580191` | Full JATS: body, all 5 equations, all figure captions, both tables, all 24 refs. Model was reconstructed from this file. |
| `paper.txt` (~25 KB) | Derived from JATS XML | Plain-text body extract for quick grep |
| `europepmc_abstract.html` | EuropePMC API | Abstract HTML fallback |
| `unpaywall.json` | Unpaywall API (DOI 10.1667/RR2877.1) | `oa_status=green`, `is_oa=true`, best OA location = PMC3580191 |

## `scripts/`
| File | Purpose |
|------|---------|
| `smoke_shuryak_2012.py` | Pure-Python NumPy implementation of Eqs. 1-5 with Table 1 best-fit parameters hard-coded and strain-specific logistic $F(D)$ placeholders. Runs all 10 strain/radiation cells, emits per-strain CSVs + `summary.csv` + 2 log-survival PNGs. `--plot` flag generates the matplotlib figures. |

## `results/`
| File | Content |
|------|---------|
| `summary.csv` | 10 rows, one per strain*radiation. Columns: `D_end, P_end, Q1_end, Q2_end, S_end, logQ1_over_logS, logQ2_over_logS, dominant_mechanism`. Source of §3 quantitative claim audit. |
| `Dr_R1_gamma.csv`, `Dr_R1_UV.csv` | *D. radiodurans* R1 WT full-grid `Dose, P, Q1, Q2, S` |
| `Dr_recA_gamma.csv`, `Dr_recA_UV.csv` | *D. radiodurans* recA$^-$ full-grid |
| `Ec_WT_gamma.csv`, `Ec_WT_UV.csv` | *E. coli* MG1655 WT full-grid |
| `Ec_Res_gamma.csv`, `Ec_Res_UV.csv` | *E. coli* CB1000/CB2000 radioresistant full-grid |
| `Ec_IC_gamma.csv`, `Ec_IC_UV.csv` | $\lambda$-phage infective centers ($Q_1 \equiv 1$, $S = Q_2$) |
| `survival_gamma.png`, `survival_UV.png` | Log-survival curves, 5 strains each |

## `notes/`
Working notes and scratch from the original replication pass (kept as-is).

## `report/` (this backfill, 2026-07-06)
| File | Purpose |
|------|---------|
| `REPORT.tex` | LaTeX version of REPORT.md with an added Critique section and `\input{open_questions_section.tex}` |
| `open_questions.json` | 5 machine-readable open questions with `q/basis/next_steps` |
| `open_questions_section.tex` | LaTeX Open Questions section (inputted into REPORT.tex) |
| `workflow.md` | Reproducer + tools + work estimate + blockers |
| `artifacts_summary.md` | This file |
| `failure_analysis.md` | Honest critique + verdict cross-check |

## `extraction/` (this backfill)
| File | Purpose |
|------|---------|
| `nougat.mmd` | Stub with SHA256 pointer to source PDF (no GPU parse this pass; JATS XML was superior anyway) |

## Traces
- **Command trace:** `PROGRESS.md` documents the harvest curls and the smoke run invocation.
- **CSV traces:** all 11 CSVs in `results/` are re-derivable in ~1 s via
  `python3 scripts/smoke_shuryak_2012.py --plot`.

## Friction tags
- `paywall`: PNAS 2010 direct PDF returns HTTP 403 to `curl`.
- `captcha`: PMC and EuropePMC binary figure endpoints return reCAPTCHA HTML under headless
  fetch — blocks WebPlotDigitizer input harvest.
- `code-not-released`: Author FORTRAN random-restart simulated-annealing fitter not on
  GitHub / Zenodo / Figshare.
- `figure-only-data`: Krisko & Radman 2010 F(D) and S(D) exist only inside figures, no
  tabular SI.
- `verdict-mismatch`: queue says REPLICATED, actual (per REPORT.md) is PARTIAL.
  See `failure_analysis.md`.
