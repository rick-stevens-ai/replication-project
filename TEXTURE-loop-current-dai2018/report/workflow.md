# Workflow: dai2018 replication (arXiv:1802.03009v2)

## Pipeline executed
1. **ACQUIRE** — `curl -sL https://arxiv.org/pdf/1802.03009 -o dai2018.pdf` → 4.6 MB, verified `%PDF-1.5`.
2. **PARSE** — `pdftotext dai2018.pdf work/textures-loop-current-dai2018.txt` → 2092 lines.
3. **RECIPE** — Identified paper as cuprate PDW/CDW vortex-halo theory (Dai, Zhang, Senthil, Lee). **Class mislabel**: filed as "loop-current" but loop currents are only a one-line intro citation. Extracted testable headline = split-peak FFT discriminator (PDW-driven vs CDW-driven period-8 CDW). → `report/evidence/replication_recipe.json`.
4. **PHYSICS** — Built from-scratch real-space order-parameter fields (paper Eqs. 9/14/15) on a 256² grid, FFT'd, tested 4 signatures. Kagome kernel is wrong model → credited for provenance only; ran it once as a scalar cross-tie. → SAVE-EARLY `work/dai2018_result.json`.
5. **COMPARE** — 4/4 qualitative checks pass; split magnitude grid-limited (honest caveat).
6. **ARTIFACTS** — 8 artifacts built (below).
7. **JUDGE** — `judge_verdict.py` re-run.

## Model
- d-wave vortex: Δ_D ∝ r/√(r²+r0²)·e^{iθ}, r0=3.5a
- PDW envelope: Δ_P ∝ exp(1−√(r²+ξ²)/ξ), ξ=15a
- PDW-driven Q/2 CDW: ρ = F(r)·cos(θ−θ_a)·sin(Q_x·r)  ← angular factor = winding signature
- CDW-driven Q/2 CDW: ρ = e^{−r/ξ}·sin(Q_x·r)  ← no angular factor

## Runner
`/home/stevens/comfyui-env/bin/python code/dai2018_replicate.py` (<10 s, coarse grid).

## Key results
| check | PDW-driven | CDW-driven |
|---|---|---|
| peaks near Q/2 | 2 (split) | 1 (single) |
| center/max at Q/2 | 0.0 (node) | 1.0 (peak) |
| real-space nodal line | yes | — |
| Re(FFT) sign change | yes | yes |

## Provenance
Kernel: `loop_current_meanfield_kernel.py` (Ollie) — methodology credit only; kagome model not applicable to this cuprate paper.
