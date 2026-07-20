# Artifacts Summary — Tian et al. 2026 (RSLC / ridgetronics)

**Verdict: REPLICATED** (tight-binding scope) | Coverage 7/10 | Agreement 9/10

| # | Artifact | Path | Description |
|---|----------|------|-------------|
| 1 | Extraction (marker) | `extraction/marker.md` | Metadata + key equations (Eqs. 1–4) + symmetry facts + headline |
| 2 | Extraction (nougat) | `extraction/nougat.mmd` | pdftotext -layout interim text + Nougat-compatible header (408 lines) |
| 3 | Report | `report/REPORT.tex` | REVTeX PRL-style replication report with results table |
| 4 | Open questions | `report/open_questions.json` | 5 Qs {question, why_it_matters, next_step} + global next_steps |
| 5 | Workflow | `report/workflow.md` | End-to-end replication workflow |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file |
| 7 | Failure analysis | `report/failure_analysis.md` | What was NOT reproduced (DFT, layer P(k), Hall effect) + why |
| 8 | Evidence | `report/evidence/tian2026_result.json`, `report/evidence/tian2026_replication.py`, `report/evidence/replication_recipe.json` | Result JSON + from-scratch code + recipe |

## Physics summary (3 lines)
1. The RSLC two-band model H = ε + diag(π₀cos k_x + δ cos k_y, π₀cos k_y + δ cos k_x) produces, in the ridge limit δ→0, two **orthogonal flat "ridges"** — spin-up flat along k_y (conducts only along x), spin-down flat along k_x (conducts only along y).
2. Semiclassical Boltzmann transport gives σ_yy^↑ = σ_xx^↓ = 0 **exactly**, so the conductivity spin polarization SP_xx = +1 and SP_yy = −1 — **100% spin-polarized, direction-locked** currents, reproducing Fig. 3(c-III).
3. Finite ridge curvature (δ>0) degrades this smoothly: |SP| = 0.997 at δ=0.05π₀, 0.956 at δ=0.2π₀ — quantifying the "quasi" in quasi-1D transport.

## Kernel credit
Semiclassical Boltzmann/velocity transport approach in the spirit of the gobel2024 itinerant-texture kernel; spin-projection probes analogous to spin_ed_probes.py. (Named kernels not present on disk in this profile; the required transport physics — σ_ab ∝ e²τ⟨v_a v_b(−∂f/∂E)⟩ — was implemented from scratch per the recipe.)

## Reproduce
```bash
/home/stevens/comfyui-env/bin/python work/tian2026_replication.py
```
Runtime ≈0.05 s (numpy 2.3.5, scipy 1.17.0).
