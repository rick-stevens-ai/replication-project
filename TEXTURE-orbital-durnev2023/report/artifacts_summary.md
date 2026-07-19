# Artifacts Summary — durnev2023 (arXiv:2306.08509)

Paper: M. V. Durnev, *Faraday and Kerr rotation due to photoinduced orbital
magnetization in a two-dimensional electron gas* (2023).
Analytic Boltzmann/kinetic-theory; Gaussian/CGS units.

## Verdict
**REPLICATED** — Coverage ~7/10, Agreement ~9/10.

## 8-Artifact Package

| # | Artifact | Path | Purpose |
|---|----------|------|---------|
| 1 | Extraction (marker) | `extraction/marker.md` | pdftotext interim (marker binary absent) |
| 2 | Extraction (nougat) | `extraction/nougat.mmd` | pdftotext interim (nougat binary absent) |
| 3 | Report | `report/REPORT.tex` | Full LaTeX replication report |
| 4 | Open questions | `report/open_questions.json` | 5 questions + next_steps |
| 5 | Workflow | `report/workflow.md` | End-to-end reproduction steps |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file |
| 7 | Failure analysis | `report/failure_analysis.md` | Gaps, discrepancies, limits |
| 8 | Evidence | `report/evidence/` | result JSON, script, run log, recipe |

### Evidence contents
- `durnev2023_result.json` — machine-readable results + verdict
- `durnev2023_replicate.py` — the physics implementation (NumPy, CGS)
- `run_output.txt` — captured console output of the run
- `replication_recipe.json` — original method/parameter recipe

## Headline Numbers
- Resonance: Omega*tau1 = 1 → Omega_res = 1.59 THz
- Peak Faraday angle: 0.0441 deg (Eq 26) / 0.0417 deg (Eq 5+25) — agree ~6%
- Synthetic magnetic field: B_syn = 0.088 T (paper ~0.1 T)

## Cross-Checks (all match paper)
| Quantity | This work | Paper | Δ |
|----------|-----------|-------|---|
| eps_F (meV) | 63.90 | 64.0 | <0.2% |
| 2π·σ0/(c·n̄) | 0.0708 | 0.071 | <1% |
| T(Ω) | 0.699 | [0.63, 0.70] | in range |
| B_syn (T) | 0.088 | ~0.1 | 12% |

## Reproduce
```
/home/stevens/comfyui-env/bin/python \
  /home/stevens/textures-100/corpus/textures-orbital-durnev2023/work/durnev2023_replicate.py
```
