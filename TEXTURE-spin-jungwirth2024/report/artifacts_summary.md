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

## Headline numbers (traced to evidence JSON)
| Quantity | d-wave (`runs_dwave.nk96`) | g-wave (`runs_gwave.nk96`) | JSON key |
|----------|------|------|----------|
| Net magnetization / cell | **0** (exact) | **0** (exact) | `M_net_per_cell` |
| BZ-avg spin splitting | ~6e-18 (≈0) | ~5e-20 (≈0) | `M_from_split_BZavg` |
| Max spin splitting | 0.5612 t_nn | 0.2671 t_nn | `max_spin_splitting_over_tnn` |
| Dominant angular harmonic m | **2** | **4** | `dominant_angular_harmonic_m` |
| Number of nodal lines | **2** | **4** | `n_nodal_lines` |
| Node residual (axes+diag) | 0 (1e-16) | 0 (1e-16) | `node_on_*_maxabs` |
| C4 residual | odd: 0 | even: 0 | `C4_odd_residual` / `C4_even_residual` |
| Diagonal-mirror-odd residual | — | 0 (1e-16) | `diag_mirror_odd_residual` |
| Analytic sign match | **100%** | **100%** | `analytic_sign_match_fraction` |
| Reduces to d-wave at alpha=0 | — | **true** | `reduces_to_dwave_at_alpha0` |
| Checks passed | — | **15/15** | `checks` |

## Verdict
Self-assessed **REPLICATED** (mechanism + symmetry-exact d-wave AND g-wave splitting with M=0,
unified by an alpha knob that reduces g→d exactly). Coverage-flip extension adds the g-wave
(m=4, MnTe/CrSb) class to the original d-wave prototype. Coverage still capped because the paper
is a Perspective with no quantitative benchmark and also spans the i-wave case + Pomeranchuk/3He
analogy + ab-initio + relativistic effects. Final verdict assigned by LLM judge.

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
