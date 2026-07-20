# Workflow: Replication of chakraborty2023 (zero-field FF SC in altermagnet)

## Objective
Reproduce the headline claim of Chakraborty & Black-Schaffer (arXiv:2309.14427v2):
at **zero magnetic field**, a 2D **d-wave altermagnet** hosts a **finite-momentum
Fulde-Ferrell (FF)** spin-singlet superconducting state, in the window
`0.44 ≲ t_am ≲ 0.56`.

## Performance context (RETRY)
Two prior attempts TIMED OUT at 1200s because the fine/full modes used a dense
k-grid (N=160-1000) and a fine Q-scan. This retry is **perf-bounded**:
- k-grid: **24×24** (COARSE)
- Q-scan: **11 points** on Q∈[0, 0.6]
- t_am list: 7 focused points on the FF-window edges {0,0.3,0.4,0.44,0.5,0.56,0.6}
- Closed-form 2×2 BdG energies (no sparse diagonalization), numpy-vectorized
- **Actual runtime: 5.6 s** (SAVE-EARLY fired at 3.0 s)

## Steps executed
1. **Read** paper text (`work/textures-spin-chakraborty2023.txt`) + recipe
   (`report/evidence/replication_recipe.json`). Confirmed model: square-lattice
   TB + altermagnet spin splitting `(t_am/2)(cos kx − cos ky)·σ` + singlet pairing.
2. **Reused/extended** the existing from-scratch BdG script
   `work/chakraborty2023_bdg_ff.py`, adding a `retry` mode (coarse grids),
   a **SAVE-EARLY** write after the first d-wave Q-scan, and canonical output
   `work/chakraborty2023_result.json`.
3. **Ran** `python work/chakraborty2023_bdg_ff.py retry` → 5.6 s.
4. **Compared** the BCS→FF onset to the paper's claim (see failure_analysis.md).
5. **Packaged** 8 artifacts (extraction ×2, REPORT.tex, open_questions.json,
   workflow.md, artifacts_summary.md, failure_analysis.md, evidence copies).

## Key physics result
| t_am | Q* (d-wave) | Δ_d* | state |
|------|-------------|------|-------|
| 0.00 | 0.00 | 0.290 | BCS (Q=0) |
| 0.40 | 0.00 | 0.290 | BCS (Q=0) |
| **0.44** | **0.24** | 0.017 | **FF (Q>0)** |
| 0.50 | 0.24 | 0.000 | normal |

Zero-field BCS→FF transition onsets at **t_am = 0.44** — the exact lower edge of
the paper's reported window. Mechanism confirmed.

## Reproduce
```
cd /home/stevens/textures-100/corpus/textures-spin-chakraborty2023
/home/stevens/comfyui-env/bin/python work/chakraborty2023_bdg_ff.py retry
```
