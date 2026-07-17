# Artifacts Summary — göbel2024 (arXiv:2410.00820)

## Inventory

### Inputs / extraction
- `paper.pdf` — source paper (11.9 MB).
- `extraction/marker.md` — clean pdftotext extraction incl. full Methods (Eqs. 1–11).
- `extraction/nougat.mmd` — nougat stub (unnecessary; marker was complete).
- `report/method_extract.md` — distilled computational recipe + claim inventory (C1–C5) + feasibility.

### Compute (DONE — not recomputed in this phase)
- `work/reproduce.py` — pure-numpy real-space s-d TB + ED + Kubo Hall (charge/spin/orbital) + FM subtraction + λ sweep.
- `work/results.json` — per-λ numbers + per-claim verdicts (source of truth for all numbers below).
- `work/COMPUTE_NOTES.md` — detailed compute narrative + per-claim reasoning.
- `work/figs/scaling.png` — σ_charge / σ_spin / σ_orbital vs λ.
- `work/run*.log`, `work/run_final.log` — run logs.

### Report (this phase)
- `report/REPORT.tex` (+ `REPORT.pdf` if pdflatex present) — full write-up.
- `report/open_questions.json` — 5 new grounded open questions (Q1–Q5).
- `report/workflow.md` — environment + step-by-step workflow.
- `report/artifacts_summary.md` — this file.
- `report/failure_analysis.md` — the operator-choice + finite-cell gaps.

## Key numbers trace (all from work/results.json, FM-subtracted, L=28, t=1, m=5eV, Néel skyrmion, nocc=69)

| λ (a) | gap (t) | σ_charge | σ_spin | σ_orbital |
|------|---------|----------|--------|-----------|
| 2 | 0.0941 | 3.28e-13 | −0.722 | 2893.4 |
| 3 | 0.0612 | 8.10e-13 | −1.695 | 4662.4 |
| 4 | 0.0448 | −6.08e-13 | −3.387 | 6036.0 |
| 5 | 0.0346 | 1.19e-12 | −6.659 | 7261.0 |

- **Orbital/spin ratio (λ=5):** 7260.96 / 6.659 ≈ **1090** (≈3 orders of magnitude).
- **Charge Hall:** ~0 (1e-12) at all λ — no global charge gap for a single skyrmion in a finite cell.
- **Scaling slopes (vs λ):** orbital ~1.005; charge ~1.19; spin ~2.40; accumulated ⟨L_z⟩ ~1.44 (linear-in-area mechanism reproduced).
- **Runtime:** 228.7 s (~4 min), CPU, pure numpy.

## Verdict
**PARTIAL (headline REPLICATED).**
- C1 (finite orbital Hall, no SOC): ✅ CONFIRMED — σ^Lz = 2893–7261 a.u., texture-induced.
- C3 (orbital ≫ spin): ✅ CONFIRMED — ratio ~1090. Charge quantization sub-point: ⚠️ not reproduced (needs skyrmion-crystal supercell).
- C2 (orbital area² vs spin/charge area¹): ⚠️ PARTIAL — mechanism (⟨L_z⟩ ∝ area) reproduced; strict exponent separation not (needs modern orbital-magnetization operator).
- C4 (AFM/bimeron pure OHE): — not run this pass.
