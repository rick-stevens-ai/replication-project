# Artifacts Summary — tazai2025

| # | Artifact | Path | Description |
|---|----------|------|-------------|
| 1 | Extraction marker | `extraction/marker.md` | Structured key-quantity extraction |
| 2 | Nougat MMD | `extraction/nougat.mmd` | pdftotext interim extraction + header |
| 3 | Report | `report/REPORT.tex` | Full replication report (LaTeX) |
| 4 | Open questions | `report/open_questions.json` | 5 questions + next_steps |
| 5 | Workflow | `report/workflow.md` | Step-by-step reproduction log |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file |
| 7 | Failure analysis | `report/failure_analysis.md` | What matched / didn't and why |
| 8 | Evidence | `report/evidence/` | result JSON + runner code + kernel + recipe |

## Evidence contents
- `tazai2025_result.json` — full sweep output (λ_d,λ_s vs T and η, eigenvector).
- `replicate_tazai2025.py` — from-scratch runner.
- `loop_current_kagome_kernel.py` — credited kernel (KagomeModel conventions).
- `replication_recipe.json` — prep recipe.

## Verdict
**PARTIAL** — Coverage 8/10, Agreement 6/10.

## Headline result (from `tazai2025_result.json`)
- λ_d vs T @ η=0.014: rises 0.196 (8 meV) → 0.360 (0.1 meV) — sharp low-T upturn ✓
- λ_d vs η @ T=0.5 meV: resonant **peak at η=0.014** (0.270), above η=0.010 (0.205)
  and η=0.016 (0.213) — matches paper's 0.01–0.016 window ✓
- Chiral (1,ω²,ω) eigenvector overlap ≈ 0.63 ✓ (partial)
- λ_s > λ_d throughout — chiral d does NOT globally overtake s-wave in this kernel ✗
- LC suppresses s-wave (λ_s: 1.19 → 0.44 as η: 0 → 0.02) ✓
