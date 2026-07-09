# Artifacts Summary

## Paper artifacts (`artifacts/`)
| Path | Size / count | Notes |
|---|---|---|
| `artifacts/paper.pdf` | 9,170,352 B, sha16 `008cb5c8…` | CC BY 4.0, from `pub.mdpi-res.com` (MDPI front door 403s to curl). |
| `artifacts/figures/fig{001..012}.jpg` | 12 files, 550-px wide | Same CDN; no 1500-wide variants available. |
| `artifacts/article_text.txt` | 1,095 lines, layout mode | `pdftotext -layout` extraction for claim mining. |
| `artifacts/artifact_manifest.json` | inventory | Machine-readable list of artifacts. |

## Replication outputs (`outputs/`)
| Path | Description |
|---|---|
| `outputs/fig1_repair_fraction.png` | Analytical replica of Fig 1: f(D) [%] vs D [mGy], 0–200 mGy, `T=120 h`. 10–45 mGy "≈100 %" band shaded. Mean 99.61 %, min 97.50 %, max 99.93 % over 1 mGy grid → verifies claim C5. |
| `outputs/fig12_global_fraction.png` | Analytical replica of Fig 12 theoretical curve: f(D)·P_hit(D) [%], 0–200 mGy. Peak ≈7 % at D≈64 mGy (analytical upper bound; paper's MC value = 0.126 %, consistent with ~×55 MC erosion). |
| `outputs/par_peak_heatmap.png` | 2-D heatmap of Eq (2) P_AR(D,k) over (0–80 mGy) × (0–80 h). Analytical maximum at (D*=25.19 mGy, k*=24.04 h) marked → verifies claims C2a, C2b. |
| `outputs/pc_dose_rate_table.png` | Eq (5) P_C table for the four §3.4 constant-dose-rate scenarios, with qualitative paper text per scenario. Surfaces the MISMATCH at C4c. |
| `outputs/extended_claim_audit.json` | Full machine-readable claim-by-claim audit (14 quantitative claims + status + numeric values + tolerances). |
| `outputs/smoke_summary.json` | Pre-existing summary of Fig 1 + Fig 12 numeric checks from the original smoke script. |

## Scripts (`scripts/`)
| Path | Purpose |
|---|---|
| `scripts/smoke_adaptive_response.py` | Analytical replica: Eqs 1–4, N₀=493k, T₀=120 h, vectorised NumPy, generates fig1 + fig12 PNGs + smoke_summary.json. |
| `scripts/extended_claim_audit.py` | Adds Eq 5 P_C, unit consistency (yr↔h), P_hit point checks, analytical PAR peak, §3.4 MISMATCH check, PAR heatmap + P_C table. Writes extended_claim_audit.json. |

## Reports (top-level + `report/`)
| Path | Description |
|---|---|
| `REPORT.md` | Full audit report, 22,726 B (2026-06-22 audit). Verdict: PARTIAL (coverage 6/10, agreement 8/10). |
| `FIRST_PASS_REPORT.md` | Earlier first-pass report from 2026-06-09 (5,881 B). |
| `PROGRESS.md` | Slot progress log (2,997 B). |
| `README.md` | Slot README (4,861 B). |
| `report/REPORT.tex` | **[backfill 2026-07-06]** LaTeX version of REPORT.md, with genuine critique + open-questions input. |
| `report/open_questions.json` | **[backfill]** 5 grounded open questions (MC tree, priming-window kinetics, mechanism reducibility, cell-line/LET generalizability, §3.4 label-swap resolution). |
| `report/open_questions_section.tex` | **[backfill]** LaTeX Open Questions section, `\input` into REPORT.tex. |
| `report/workflow.md` | **[backfill]** Workflow, tools, versions, work estimate, reproducer. |
| `report/artifacts_summary.md` | **[backfill]** This file. |
| `report/failure_analysis.md` | **[backfill]** Honest critique of what didn't work + residual uncertainty. |
| `extraction/nougat.mmd` | **[backfill]** Stub — paper.pdf sha256 pointer + note that no GPU parse was run (per backfill policy: don't spend GPU on already-cached mid-quality claim-mining text). |

## Extraction traces
- No nougat/marker parse run for this backfill. `artifacts/article_text.txt`
  (poppler `pdftotext -layout`, 1,095 lines) was used for claim extraction and was
  sufficient for §3.4 numerical inconsistency detection (which required exact reading
  of the four scenario bullets). Nougat would improve equation LaTeX fidelity but is
  not on the critical path for this replication's verdict.

## Friction tags
- **`data-not-released`** (critical): Fornalski 2022 (*Dose-Response*) parent MC tree
  has no public code release. Blocks Figs 2, 3–11 and 3 of 4 §4 headline numbers.
- **`paper-internal-inconsistency`** (medium): §3.4 attributes P_C = 0.45 to
  scenario 3 (in-vitro, 0.17 mGy/h), but Eq (5) at those parameters gives 0.155.
  Probable scenario 2 ↔ 3 label swap in the discussion paragraph.
- **`no-machine-readable-calibration`** (medium): raw human-lymphocyte / X-ray
  dose-response data behind α_i, μ_i lives in Polish-language B.Sc./M.Sc. theses
  on ResearchGate (refs [21,22,25]); not machine-readable, not re-fitted here.
- **`cdn-only-figures`** (low): 550-px JPGs are the largest available; no
  vector/large-raster variant for pixel-diff.
- **`vision-endpoint-down`** (low): during 2026-06-22 audit, all vision endpoints
  (Anthropic, OpenAI, Gemini-Flash) were unavailable → substituted numeric-band
  claim C5 verification for pixel-diff.
- **`title-vs-content-mismatch`** (subjective): "mechanistic" in title is
  phenomenological in practice (three empirical constants, no pathway mapping).
  See open question #3.
