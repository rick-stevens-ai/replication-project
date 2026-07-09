# Artifacts Summary — `lucid100-mgm-dna-damage-protons-helium`

Machine-readable inventory of on-disk artifacts for this replication.
Backfill pass: 2026-07-06.

## Top-level documentation

| File | Purpose | Size |
|---|---|---|
| `REPORT.md` | Primary human report (post-promotion, 2026-06-27) | 20 KB |
| `REPORT.md.bak-pre-promo` | Prior SPOT-CHECK report (preserved) | 19 KB |
| `FIRST_PASS_REPORT.md` | Initial pass (2026-06-26) | 10 KB |
| `NO_GO_REPORT.md` | Original NO-GO screening notes | 2.4 KB |
| `PROGRESS.md` | Timeline & status log | 1.8 KB |
| `PROMO_RESULT.txt` | Single-line verdict (`VERDICT=PARTIAL COVERAGE=4/10 AGREEMENT=7/10`) | 0.8 KB |
| `README.md` | Slot README | 4.8 KB |
| `artifact_manifest.json` | Original artifact manifest (JSON) | 4.9 KB |

## Backfill-added documentation (2026-07-06)

| File | Purpose |
|---|---|
| `report/REPORT.tex` | LaTeX version of the report with `\input{open_questions_section.tex}`; contains explicit Critique section flagging queue-vs-on-disk verdict mismatch. |
| `report/open_questions.json` | Bare JSON list of 5 open-question objects (`q`, `basis`, `next_steps`). |
| `report/open_questions_section.tex` | LaTeX rendering of the 5 open questions, included by `REPORT.tex`. |
| `report/workflow.md` | Reproduction workflow (prerequisites, commands, non-steps, provenance). |
| `report/artifacts_summary.md` | This inventory. |
| `report/failure_analysis.md` | Honest critique + verdict-mismatch flag. |
| `extraction/nougat.mmd` | Nougat/paper-extraction stub; paper.pdf SHA-256 recorded. |

## Source artifacts (in `artifacts/`)

| File | What | Origin |
|---|---|---|
| `paper.pdf` | Onecha 2025 PDF (25 pp) | EuropePMC `PMC12905799?pdf=render` |
| `paper.txt` | Text extraction | `pdftotext` local |
| `mgm2023.pdf` | Bertolet 2023 MGM theory paper | Front. Oncol., CC-BY |
| `mgm2023.txt` | Text extraction | `pdftotext` local |
| `europepmc.html` | EuropePMC landing page | EuropePMC |
| `europepmc_meta.json` | EuropePMC metadata | EuropePMC REST |
| `mgm-repo/` | Full clone of MGHPhysicsResearch/MGM v1.0.1 (Python, MIT) | GitHub |

`paper.pdf` SHA-256:
`3a7c1cad4b590eedd0be983fabbee00213fe4a743fa7be50c68b90c142d2c476`.

## Scripts (in `scripts/`)

| File | Purpose |
|---|---|
| `smoke_mgm.py` | First-pass smoke: 5 anchors through MGM. |
| `extended_audit.py` | SPOT-CHECK claims C1–C9 (E1–E5). |
| `promotion_audit.py` | Promotion checks P1–P5. |
| `smoke_results.json` | Numerical output of smoke. |
| `out/` | Intermediate outputs (JSON/plots per script). |

## Results (in `results/`)

| File | What |
|---|---|
| `extended_results.json` | SPOT-CHECK numerical output. |
| `promotion_results.json` | Promotion numerical output (P1–P5). |
| `plots/P2_full_sweep.png` | MDS/Gy/Gbp + mean C vs LET, p + He (29 anchors). |
| `plots/P3_he_over_p_ratio.png` | MGM He/p MDS-per-dose ratio at matched LET (documents MGM LIMIT: ~1 at LET ≤ 35 keV/μm). |
| `plots/P4_yF_spectrum_norm.png` | Spectrum-avg MDS for 20 MeV p across 4 log-normal spectra (all 9.4–11.6, none reaches paper's 30). |

## External dependencies (NOT staged locally)

| Missing artifact | Effect | Notes |
|---|---|---|
| TOPAS-MGM C++ extension source | Blocks Figs 4 (per-cell histograms), 5 (FWHM), 6 (Bragg-peak scan), 7 (RPT), Table 1 (timing) | Author org `MGHPhysicsResearch` has 8 repos, none is TOPAS-MGM; no code-availability statement in paper. |
| TOPAS-nBio yF spectra per (E, particle) | Prevents exact Fig 3 numerical reproduction; forces LET-only anchor in P3 | Paper plots them but does not table them numerically. |
| PMC SI PDF for PMC12905799 | Contains a(yF)/b(yF) fitted parameters, AAPM TG-268 reporting, per-MDS histograms | reCAPTCHA-gated on PMC; needs human browser session. |
| TOPAS + TOPAS-nBio installation + HPC allocation | Even with the extension, MC runs need multi-day HPC job | CherryRd disallowed for heavy MC per project policy; uicgpu / Aurora is the correct target. |

## Artifact-count check

- Top-level docs: 8 items (REPORT.md, REPORT.md.bak-pre-promo,
  FIRST_PASS_REPORT.md, NO_GO_REPORT.md, PROGRESS.md, PROMO_RESULT.txt,
  README.md, artifact_manifest.json).
- `report/` docs (backfill): 6 items.
- `extraction/` stub: 1 item.
- Source artifacts under `artifacts/`: 7 items (paper.pdf, paper.txt,
  mgm2023.pdf, mgm2023.txt, europepmc.html, europepmc_meta.json,
  mgm-repo/).
- Scripts: 3 code files + 1 JSON + `out/` dir.
- Results: 2 JSON + 3 PNG plots + `plots/` dir.

**Total identifiable artifact groups: > 8 (meets standard).** Backfill
adds 7 new documentation artifacts under `report/` + `extraction/`.
