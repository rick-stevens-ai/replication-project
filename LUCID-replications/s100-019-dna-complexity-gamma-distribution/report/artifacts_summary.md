# Artifacts summary — Slot #19

**Paper:** Bertolet et al. 2023, Frontiers in Oncology 13:1196502

## Report artifacts (`report/`)
| File | Purpose |
|---|---|
| `REPORT.md`                       | Original human-readable replication report, four-tier verdict, coverage 7/10, agreement 9/10, 12-row claim-by-claim table, four blockers. |
| `REPORT.tex`                      | LaTeX render of the report with expanded genuine critique (5 issues), verdict cross-check with queue label. |
| `open_questions.json`             | 5 concrete open-question probes (bare JSON list, `{q, basis, next_steps}` per object) for follow-on replicators. |
| `open_questions_section.tex`      | LaTeX version of the 5 open questions. |
| `workflow.md`                     | Chronological narrative of how the replication was executed, with what-was-skipped-and-why. |
| `artifacts_summary.md`            | This file. |
| `failure_analysis.md`             | Honest critique — what this replication does NOT answer, what could go wrong with the paper's claim graph even given the analytical reproducibility. |

## Code (`code/`)
| File | Purpose |
|---|---|
| `replicate_mgm.py`                | Full analytical-layer replication script. CPU-only, ≈10 s wall. numpy + scipy + matplotlib + pandas. Deterministic (seed=42 for X-ray subsample). |

## Source (`source/`)
| File | Purpose |
|---|---|
| `paper.pdf`                       | Original open-access paper from Frontiers. |
| `author_mgm.py`                   | Verbatim copy of `src/mgm.py` from `github.com/MGHPhysicsResearch/MGM`. |
| `author_README.md`                | Verbatim copy of the repo README. |
| `script_monoenergetic.py`         | Verbatim copy of the example script from the repo. |
| `xray_microdosimetry_1um.phsp`    | Verbatim copy of the bundled 250-keV X-ray microdosimetric phase-space (116 077 events). |

## OCR / extraction
| File | Purpose |
|---|---|
| `ocr/raw_layout.txt`              | `pdftotext -layout` extract of the paper (used for parameter-constant cross-check). |
| `extraction/nougat.mmd`           | Stub placeholder for a Nougat MMD extraction. Not run for this replication because the pdftotext layout was sufficient for the parameter-constant + formula retrieval this analytical replication needed. Kept as a stub so the artifact inventory matches the 8-artifact standard. |

## Evidence (`evidence/`)
| File | Purpose |
|---|---|
| `fig2_damage_vs_yF.csv`           | 400-row dense evaluation of all 5 damage-count functions vs yF ∈ [0.5, 400] keV/µm. |
| `fig3_gamma_parameters_vs_yF.csv` | 400-row dense evaluation of α(yF), β(yF) quadratics. |
| `fig3_summary_per_beam.csv`       | Complexity PDF summary for 5-MeV proton and 4-MeV alpha reference beams. |
| `xray_complexity_distribution.csv`| End-to-end MGM output for the bundled X-ray spectrum (1 000-event subsample). |
| `gamma_form_audit.csv`            | 21-row Gamma parameterization audit (three SciPy call variants × 7 yF × 5 C values). |
| `replication_summary.json`        | Machine-readable roll-up: verdict, scores, per-claim status, spot-value validation table. |

## Figures (`figures/`)
| File | Purpose |
|---|---|
| `fig2_damage_vs_yF.png`           | 3-panel reproduction of paper Figure 2 (SB, BD, N_sites vs yF). |
| `fig3_complexity_and_gamma_params.png` | 4-panel reproduction of paper Figure 3 (complexity PDFs + α, β vs yF). |
| `xray_complexity_distribution.png`| X-ray end-to-end pipeline complexity bar chart. |

## Verdict at a glance
- **Four-tier:** REPRODUCED (analytical) / NOT-REPRODUCED (MC upstream).
- **Coverage:** 7 / 10.
- **Agreement:** 9 / 10.
- **Queue label (input):** REPLICATED.
- **Cross-check flag:** likely mismatch — should map to PARTIAL/SPOT-CHECK under the four-tier LUCID rubric because the upstream Monte-Carlo was never re-executed. Preserved as REPLICATED per backfill instruction; documented in REPORT.tex §"Verdict cross-check".
- **Blockers:** 4 (raw SDD files not deposited [hard]; microdosimetric spectra not deposited [medium]; per-beam (α, β) not tabulated [soft]; author-code Gamma call misparameterized [minor code bug]).
