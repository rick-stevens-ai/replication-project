# Artifacts summary — textures-polar-zhang2024 (arXiv:2411.05576)

| Artifact | Path |
|---|---|
| Source PDF | `zhang2024.pdf` |
| Parsed text | `work/textures-polar-zhang2024.txt` |
| Result JSON (save-early) | `work/zhang2024_result.json` |
| Replication code | `code/replicate_zhang2024.py` |
| Marker extraction | `extraction/marker.md` |
| Nougat extraction | `extraction/nougat.mmd` |
| Main report | `report/REPORT.tex` |
| Open questions (5) | `report/open_questions.json` |
| Workflow | `report/workflow.md` |
| Failure analysis | `report/failure_analysis.md` |
| Artifacts summary | `report/artifacts_summary.md` |
| Evidence: result | `report/evidence/zhang2024_result.json` |
| Evidence: code | `report/evidence/replicate_zhang2024.py` |

## Verdict
- **Recommendation:** REPLICATE (partial) — NOT a drop. Paper has a reproducible analytic theory core.
- **Verdict:** PASS-PARTIAL. **C = 0.6, A = 0.7.**
- **Key result:** elementary hex SPP lattice Q = +1.00 per cell reproduced exactly (validates Eq.1→4 + Berg–Lüscher pipeline); moiré cluster Q = −3 partial (needs Supplemental σ_j / moiré-cell definition).

## Provenance
Berg–Lüscher topological-charge kernel adapted from `~/shared-kernels-cache/ollie_berg_luscher_topological_charge_kernel.py`. CPU-only, numpy.
