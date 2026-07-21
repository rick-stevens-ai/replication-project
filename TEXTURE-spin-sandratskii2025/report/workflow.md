# Workflow: sandratskii2025 (arXiv:2501.11327) altermagnet replication

## Pipeline stages
1. **ACQUIRE** — `curl -sL https://arxiv.org/pdf/2501.11327 -o sandratskii2025.pdf`
   - Verified: header `%PDF-1.5`, size 651 KB (>10 KB). OK.
2. **PARSE** — `pdftotext sandratskii2025.pdf work/textures-spin-sandratskii2025.txt`
   - 2385 lines extracted.
3. **RECIPE** — read text; identified method (direct-DFT constrained magnons + SSG)
   and the ONE testable electronic headline (altermagnetic spin splitting with zero
   net moment). Wrote `report/evidence/replication_recipe.json`.
4. **PHYSICS** — built from-scratch tight-binding altermagnet surrogate of alpha-MnTe.
   Runner: `/home/stevens/comfyui-env/bin/python` (numpy 2.3.5). SAVE-EARLY to
   `work/sandratskii2025_result.json`.
5. **COMPARE** — scored 5 predictions + 1 null test = 6/6 qualitative passes.
6. **PACKAGE** — 8 artifacts (see artifacts_summary.md).
7. **JUDGE** — `judge_verdict.py ... --model argo:claude-opus-4.5 --njudges 1`.

## Method-class routing
- Class = spin (altermagnet). Paper method = DFT magnons — too heavy for <8 min.
- Chose the **model-surrogate route**: reproduce the paper's minimal physics
  (two-sublattice altermagnet electronic structure) via tight-binding, not DFT.
- Provided kernels (spin_ed_probes.py = many-body ED skyrmion; gobel2024 Kubo Lz)
  were NOT applicable (this is a band spin-splitting / symmetry claim, not ED or
  transport), so a bespoke TB model was written from scratch.

## Key physics decision
The altermagnet defining relation eps_down(k) = eps_up(R^-1 k) with R = C6z (the
sublattice-connecting spin-space-group op) was imposed exactly, so the spin
splitting emerges purely from lattice symmetry + one anisotropic hopping — the
correct minimal altermagnet construction.

## Runtime
Total wall time < 8 min; physics compute < 5 s on a 121x121 k-grid.
