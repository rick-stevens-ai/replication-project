# Artifacts summary — Jungwirth 2024/2025 altermagnetism

| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Source paper | `textures-spin-jungwirth2024.pdf` | present |
| 2 | Marker extraction (prose) | `extraction/marker.md` | pdftotext -layout interim (marker not installed) |
| 3 | Nougat extraction (math) | `extraction/nougat.mmd` | pdftotext interim + hand-transcribed key eqs (nougat not installed) |
| 4 | Report | `report/REPORT.tex` | complete (source; pdflatex not run) |
| 5 | Open questions | `report/open_questions.json` | 5 questions + next_steps array |
| 6 | Workflow | `report/workflow.md` | complete |
| 7 | Artifacts summary | `report/artifacts_summary.md` | this file |
| 8 | Failure analysis | `report/failure_analysis.md` | complete |
| + | Evidence | `report/evidence/jungwirth2024_result.json`, `report/evidence/code/jungwirth2024_altermagnet.py`, `report/evidence/replication_recipe.json` | present |
| + | Work | `work/jungwirth2024_altermagnet.py`, `work/jungwirth2024_result.json`, `work/*.txt` | present |

## Headline numbers (traced to evidence JSON `runs.nk96`)
| Quantity | Value | JSON key |
|----------|-------|----------|
| Net magnetization / cell | **0** (exact) | `M_net_per_cell` |
| BZ-avg spin splitting | ~6e-18 (≈0) | `M_from_dwave_split_BZavg` |
| Max spin splitting | **0.5612 t_nn** | `max_spin_splitting_over_tnn` |
| Diagonal-node max\|Δ\| | 0 (to 1e-16) | `nodal_split_on_diagonal_maxabs` |
| Split along ΓX / ΓY | −0.2246 / +0.2246 (opposite) | `split_along_kx_mean` / `split_along_ky_mean` |
| C4 antisymmetry residual | 0 (to 1e-16) | `C4_antisymmetry_residual` |
| d-wave sign match | **100%** | `dwave_sign_match_fraction` |
| Checks passed | **6/6** | `checks` |

## Verdict
Self-assessed **REPLICATED** (mechanism + symmetry-exact d-wave splitting with M=0).
Coverage capped because the paper is a Perspective with no quantitative benchmark and covers
d/g/i-wave + Pomeranchuk/3He analogy, of which only the d-wave prototype is built.
Final verdict assigned by LLM judge.

## Reproduce block
```bash
cd /home/stevens/textures-100/corpus/textures-spin-jungwirth2024/work
/home/stevens/comfyui-env/bin/python jungwirth2024_altermagnet.py
python3 -c "import json;print(json.load(open('jungwirth2024_result.json'))['checks'])"
```

## Extraction fidelity note
marker/nougat binaries are not installed on this host; artifacts 2+3 are the documented
pdftotext interim fallback. Unicode/math rendering is degraded in the raw dumps — this is a
tooling limitation, **not a physics gap**. Authoritative equation transcriptions live in
`report/REPORT.tex` and in the `\section*{Key equations}` block of `extraction/nougat.mmd`.
Regenerate with `marker_single <pdf> ./extraction/` / `nougat <pdf> -o ./extraction/ --markdown`.
