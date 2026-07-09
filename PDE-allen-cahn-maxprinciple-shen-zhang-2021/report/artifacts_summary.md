# Artifacts Summary — Shen & Zhang (2022), 4th-order AC/DMP replication

Paper: arXiv:2104.11813v1 → Commun. Math. Sci. 20(5), 1447–1474 (2022).
Verdict: **REPLICATED** (unanimous across 3 Argo judges).

---

## Code artifacts (all under `work/`, from-scratch Python)

| File                    | Purpose                                                                 |
|-------------------------|-------------------------------------------------------------------------|
| `fdmats.py`             | Build 4th-order Q2-derived `(D1, D2)` and 2nd-order companion stencils (eqs. 2.7–2.8) |
| `solver.py`             | Assemble 2D convection–diffusion operator via Kronecker product; interior/boundary split |
| `validate_steady.py`    | Steady conv-diff sanity: manufactured `sin²x sin y`, confirms superconvergence (Remark 1) |
| `table61.py`            | Table 6.1: Allen–Cahn accuracy, µ=0.1, ε=0.05, u=v=sin(y−x), BDF3 IMEX, splu |
| `table62.py`            | Table 6.2: stream-vorticity, periodic BC, µ=0.1, BDF3 IMEX, splu; 320² runs on uicgpu |
| `monotonicity.py`       | C2 gate: form `L̄ = I/Δt + conv − µΔ_h`, dense inverse, entrywise non-negativity check |
| `maxprinciple.py`       | Out-of-regime probe at paper Sec 6.2 illustrative settings (239², Δt=Δx/6) |

Dependencies: Python 3, numpy, scipy (`splu`, `linalg.inv`), sympy (manufactured sources).
Free endpoints only. No paper code consulted.

## Report artifacts (under `report/`)

| File                    | Purpose                                                                 |
|-------------------------|-------------------------------------------------------------------------|
| `REPORT.md`             | Full narrative Markdown report (paper summary, method, tables, caveats, verdict) |
| `REPORT.tex`            | LaTeX version, includes dedicated Genuine Critique section              |
| `open_questions.json`   | 5 truly open follow-ups (CH extension, NS coupling / vector-valued, higher-order MBP, adaptive dt under MBP, sharp-interface ε→0 limit) |
| `workflow.md`           | Phase-by-phase reproduction workflow                                    |
| `artifacts_summary.md`  | (this file)                                                             |
| `failure_analysis.md`   | Honest failure/near-miss log                                            |

## Numeric results — key tables

### Table 6.1 — Allen–Cahn accuracy (l∞), T=0.2
| Grid     | 4th paper l∞ | 4th mine l∞ | 4th mine order | 2nd paper l∞ | 2nd mine l∞ | 2nd order |
|----------|--------------|-------------|----------------|--------------|-------------|-----------|
| 9×9      | 2.66E-1      | 2.79E-1     | –              | 2.38E-1      | 2.48E-1     | –         |
| 19×19    | 5.23E-2      | 5.36E-2     | 2.38           | 8.80E-2      | 8.20E-2     | 1.60      |
| 79×79    | 1.21E-4      | 1.20E-4     | 4.40           | 4.75E-3      | 4.99E-3     | 2.02      |
| 159×159  | 7.15E-6      | 7.00E-6     | 4.11           | 1.19E-3      | 1.24E-3     | 2.00      |

### Table 6.2 — Stream-vorticity accuracy (periodic BC), T=0.2
| Grid     | 4th paper l1 | 4th mine l1 | order | 4th paper l∞ | 4th mine l∞ | order |
|----------|--------------|-------------|-------|--------------|-------------|-------|
| 40×40    | 5.69E-5      | 5.65E-5     | –     | 2.30E-4      | 2.43E-4     | –     |
| 80×80    | 3.67E-6      | 3.68E-6     | 3.94  | 1.51E-5      | 1.57E-5     | 3.96  |
| 160×160  | 2.27E-7      | 2.31E-7     | 3.99  | 9.47E-7      | 9.78E-7     | 4.00  |
| 320×320  | 1.41E-8      | 1.45E-8     | 4.00  | 5.91E-8      | 5.99E-8     | 4.03  |

### Steady conv-diff superconvergence (validation)
| Grid     | 4th l1 order | 2nd l1 order |
|----------|--------------|--------------|
| 19×19    | 3.21         | 2.16         |
| 39×39    | 3.81         | 2.08         |
| 79×79    | 3.98         | 2.04         |
| 159×159  | 4.00         | 2.02         |

### C2 — Theorem 3.9 inverse-positivity (DMP)
| Case                       | n  | h·‖u‖/µ | Δt·µ/h² | min inv entry | % neg entries | pos? |
|----------------------------|----|---------|---------|---------------|---------------|------|
| in-regime                  | 19 | 0.317   | 3.15    | +5.5E-10      | 0.0%          | yes  |
| in-regime                  | 39 | 0.317   | 3.15    | +1.9E-17      | 0.0%          | yes  |
| lower-Δt violated          | 19 | 0.317   | 0.05    | −3.4E-5       | 16.1%         | no   |
| lower-Δt violated          | 39 | 0.317   | 0.05    | −1.7E-5       | 4.4%          | no   |

## Compute + provenance

- Local (CherryRd / m1 class): all `work/*.py` runs except the 320² Table 6.2 grid.
- uicgpu (8×A100, `source ~/env.sh`): 320² Table 6.2 (`python3 -u table62.py`).
- No paid endpoints touched. Judging on Argo (gpt-5.2, gemini-2.5-pro, gpt-4.1) — all free.

## Multi-judge verdict (Argo, free)

| Judge          | Verdict    |
|----------------|------------|
| gpt-5.2        | REPLICATED |
| gemini-2.5-pro | REPLICATED |
| gpt-4.1        | REPLICATED |

Unanimous; Opus excluded per wave rule.
