# Artifacts Summary — lucid-pariset-53bp1-mouse-strains

## Directory inventory (delivered artifacts)

### From original pass
| Artifact | Path | Purpose | Friction |
|---|---|---|---|
| Paper PDF | `data/paper.pdf` | Source (12 MB, 16 pp) | Vendor PDF; no supplement |
| Replication code | `code/replicate_pariset.py` | Full model + stats | none |
| Digitized (τ, q) | `data/digitized_fig4.csv` | 15 strains × HZE + 4Gy X-ray | ±0.5 h / ±0.01 eyeball error |
| Paper Table 1 verbatim | `data/table1_paper_reported.csv` | Comparator | Manual transcription |
| Paper Fig 7C digitized | `data/fig7c_cancer_correlations.csv` | 19 organ × r-values | Manual digitization |
| Recreated Fig 4 | `figures/fig4_recreated.png` | Sanity of digitization | none |
| Model kinetics | `figures/model_kinetics_examples.png` | Sensitivity plots | none |
| Results text dump | `results/replication_results.txt` | Correlations + MC | none |

### Added in re-pass (2026-06-23)
| Artifact | Path | Purpose | Friction |
|---|---|---|---|
| Re-pass code | `code/repass/repass_pariset.py` | CLAIMS C–L | none |
| Paper layout text | `data/repass/paper_layout.txt` | 780-line pdftotext -layout | Poppler-formatted; some column-drift |
| Paper plain text | `data/repass/paper_plain.txt` | 1223-line pdftotext plain | For prose grep |
| Re-pass results text | `results/repass/repass_results.txt` | Human-readable log | none |
| Re-pass results JSON | `results/repass/repass_results.json` | Machine-readable | none |
| CLAIM F table | `results/repass/claim_F_table2_classification.csv` | Per-strain quadrant match 11/15 | none |
| CLAIM G table | `results/repass/claim_G_cancer_pvalues.csv` | Per-organ Fig 7C r + p + Bonf | none |
| CLAIM J table | `results/repass/claim_J_forward_sim_4Gy.csv` | Forward-sim RIF/cell at 4/8/24/48 h × 15 strains | none |
| Parser provenance | `PARSER_PROVENANCE.md` | Where each number came from | none |
| Pass-1 REPORT | `REPORT.pass1.md` | Preserved for diff | none |
| Re-pass REPORT | `REPORT.md` | Current canonical narrative | none |

### Added by 2026-07-06 backfill (this action)
| Artifact | Path | Purpose | Friction |
|---|---|---|---|
| LaTeX report | `report/REPORT.tex` | Compilable full report | none |
| Open questions JSON | `report/open_questions.json` | 5 grounded open questions | none |
| Open questions TeX | `report/open_questions_section.tex` | \input into REPORT.tex | none |
| Workflow doc | `report/workflow.md` | Method + versions + reproducer | none |
| This inventory | `report/artifacts_summary.md` | | none |
| Failure analysis | `report/failure_analysis.md` | Honest critique | none |
| Nougat stub | `extraction/nougat.mmd` | Placeholder pointer | No GPU parse produced |

## Provenance traces

- **Marker/Nougat MMD:** not present for DOI 10.1667/RADE-20-00122.1 in
  `_LUCID100_ADMIN/marker_md_uicgpu_20260622/merged/` as of 2026-06-23.
- **Fallback parser:** Poppler `pdftotext -layout` and plain — outputs listed above.
- **Every consumed paper number** is traceable to a specific line in
  `data/repass/paper_layout.txt`; full mapping table is in `PARSER_PROVENANCE.md`.
- **No LLM used** for numeric extraction.

## Friction tags

| Friction | Where it hit | Impact |
|---|---|---|
| No supplement / no data deposit | Whole paper | Table 1A + Fig 6 + Fig 7B raw un-replicable |
| Marker parse absent for this DOI | Re-pass entry | Forced pdftotext fallback (adequate but coarser) |
| Fig. 4 is only source of per-strain (τ, q) | Digitization step | Introduces ±0.5 h / ±0.01 eyeball error |
| Fig. 7C statistical language over-reaches at n=4 | Text vs stats mismatch | Surfaced as CLAIM G — a paper-side critique |
| Fig. 7B r=0.61 statistically borderline (p≈0.061) | Central translational claim | Marked PARTIAL (CLAIM I) |
| Per-particle (40Ar, 56Fe) breakdown absent | Table 1A | Completely blocked (CLAIM L) |
| Second-annotator digitization not done | Table 2 4/15 misses | Cannot cleanly separate paper vs digitization noise |

## Verdict impact

**Coverage 8/10** and **Agreement 8/10** — the 2-point gap on each is honestly
tied to the friction tags above, primarily the missing raw data and the missing
per-particle breakdown. Attempting to score higher would require either (a)
obtaining the raw data from the Costes lab, or (b) fabricating comparisons —
neither is done. Verdict PARTIAL preserved.
