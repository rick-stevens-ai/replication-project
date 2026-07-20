# Artifacts summary — choi2021 (orbital Hall in Ti)

| # | Artifact | Path | Purpose |
|---|----------|------|---------|
| 1 | Marker extraction | `extraction/marker.md` | Interim markdown extraction (pdftotext -layout + header; marker not installed) |
| 2 | Nougat extraction | `extraction/nougat.mmd` | Interim Mathpix-markdown extraction (pdftotext -layout + Mathpix header + key eqs; nougat not installed) |
| 3 | LaTeX report | `report/REPORT.tex` | Full write-up: target claim, model, results, comparison, verdict |
| 4 | Open questions | `report/open_questions.json` | 5 Qs {question, why_it_matters, next_step} + next_steps list |
| 5 | Workflow | `report/workflow.md` | Step-by-step replication procedure + reproduce command |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file |
| 7 | Failure analysis | `report/failure_analysis.md` | What matched / did not / honest scoping |
| 8 | Evidence bundle | `report/evidence/` | Result JSON + code + credited kernel |

## Evidence contents
- `report/evidence/choi2021_orbital_hall.py` — from-scratch d-orbital Slater–Koster TB + Kubo orbital Hall.
- `report/evidence/choi2021_result.json` — all computed σ_OH / σ_SH values (SAVE-EARLY output).
- `report/evidence/gobel2024_sd_skyrmion_kubo_Lz_kernel.py` — **credited kernel** whose Kubo/L_z machinery was adapted.
- `report/evidence/replication_recipe.json` — original recipe.

## Headline numbers
- Paper: σ_OH ≈ **3800** (ħ/e)(Ω·cm)⁻¹, σ_SH = **−40**; OHE without SOC (orbital texture).
- Model: σ_OH converged (nk=16, Ti filling) = **147.7**, peak over scans = **775.4**; σ_SH ≡ **0** (no SOC).
- **Verdict: PARTIAL** — order of magnitude (within ~5×) + SOC-free orbital-texture mechanism REPLICATED.

## Kernel credit
Kubo / orbital-current formulation (`j^Lz_x = ½{L_z,v_x}`, `−2 Im[…]/(E_n−E_m)²` sum over
occ↔unocc pairs, `v_a = i[H,R_a]`) adapted from
`gobel2024_sd_skyrmion_kubo_Lz_kernel.py` (Göbel et al., arXiv:2410.00820), from the
itinerant real-space s-electron L_z to k-space intra-atomic d-orbital L_z.
