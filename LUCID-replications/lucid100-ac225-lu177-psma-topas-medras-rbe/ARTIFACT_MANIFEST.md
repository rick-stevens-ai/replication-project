# Artifact Manifest — LUCID100 slot 37

| Path | Source | Provenance | License | SHA-1 (or size) | Notes |
|------|--------|------------|---------|-----------------|-------|
| `artifacts/paper.pdf` | EJNMMI Physics open-access endpoint `ejnmmiphys.springeropen.com/counter/pdf/10.1186/s40658-023-00567-2` | downloaded 2026-06-09 13:54 CDT | CC-BY 4.0 | 3 874 329 B | the full paper |
| `artifacts/paper.txt` | `pdftotext -layout` of paper.pdf | local conversion | derivative of CC-BY 4.0 | 92 833 B | text extraction; preserves table layout |
| `artifacts/supplementary_MOESM1.docx` | Springer static-content `static-content.springer.com/esm/art%3A10.1186%2Fs40658-023-00567-2/MediaObjects/40658_2023_567_MOESM1_ESM.docx` | downloaded 2026-06-09 13:54 CDT | CC-BY 4.0 | 1 954 681 B | full Supplementary Information (physics/chemistry modules, MEDRAS params, compute env, uncertainty derivation) |
| `artifacts/supplementary_MOESM1.txt` | `pandoc -f docx -t plain` | local conversion | derivative of CC-BY 4.0 | 288 lines | text extraction (LaTeX equations fall through unrendered; OK for reference) |
| `artifacts/supplementary_landing.html` | Springer landing page snapshot | curl 2026-06-09 13:54 CDT | publisher metadata | ~509 kB | provenance for download URLs |
| `code/rbe_analytical.py` | written 2026-06-09 | this work | (no license set — internal LUCID replication artifact) | — | reproduces paper Tables 3 & 4 and Eqs. 6/7 analytically |
| `code/medras_smoke.py` | written 2026-06-09 | this work | (no license set) | — | drives `damageModel.generateExposure` + `medrasrepair.repairSimulation` for α vs β surrogates |
| `code/plot_smoke.py` | written 2026-06-09 | this work | (no license set) | — | plots smoke dose-response |
| `results/rbe_low_dose_limit_per_config.csv` | `code/rbe_analytical.py` | this work | derivative of paper (CC-BY 4.0) | — | full Tables 3 & 4 fit parameters + computed RBE_init and RBE_repair low-dose limits per (geom × intern × 2D/3D) |
| `results/medras_smoke_summary.csv` | `code/medras_smoke.py` | this work | (no license set) | — | per (Z, dose) mean initial/misrep DSB counts |
| `results/sdd_smoke/` | `code/medras_smoke.py` | this work, MEDRAS-MC v current | BSD-2-Clause (input format) | 20 SDDv1.0 files | "minimal" SDD output for 1 MeV e⁻ (Z=0) and α at 5.83/6.34/7.07/8.38 MeV (Z=2), 0.1/0.5/1/2 Gy, 3 repeats |
| `logs/medras_smoke_repair.log` | `code/medras_smoke.py` stdout capture | this work | — | full MEDRAS Fidelity output, tab-separated DSB/misrepair per break-set |
| `logs/smoke_summary.txt` | `code/medras_smoke.py` | this work | — | human-readable summary of computed slopes and RBEs |
| `figures/fig9_repro_3D_internalized.png` | `code/rbe_analytical.py` | this work | derivative of CC-BY 4.0 paper | — | analytical reproduction of paper Fig 9 (3D, internalized) using published fit parameters |
| `figures/smoke_doseresponse.png` | `code/plot_smoke.py` | this work | — | smoke dose-response plot |
| `README.md`, `PROGRESS.md`, `FIRST_PASS_REPORT.md`, `HPC_JOB_PLAN.md` | written 2026-06-09 | this work | — | replication documentation |

## Dependencies (not vendored here)
- **MEDRAS-MC** upstream lives in sibling slot at `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-medras-mc/Medras-MC/` (BSD-2-Clause, github.com/sjmcmahon/Medras-MC). `code/medras_smoke.py` imports from it via absolute path.
- **scipy / numpy / matplotlib / pandoc / poppler (pdftotext)** — system installs on CherryRd.

## What's NOT here (and why)
- **TOPAS input decks**: not released by authors; would need to be reconstructed from supplement.
- **Raw TOPAS-nBio SDD output (millions of files)**: not released; not generable on CherryRd.
- **SPECT-derived source-point distributions** from Resch et al. (lesion-by-lesion activity concentrations): not released as data files.
- **Authors' own analysis scripts (Python curve_fit driver, RBE plotting)**: not released.
