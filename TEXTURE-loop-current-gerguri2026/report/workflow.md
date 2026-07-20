# Workflow --- Surrogate replication of Gerguri et al. 2026 (CeRu3Si2 q=1/2 charge order)

## Goal
Test the headline: *DFT+U reproduces the experimentally dominant q=1/2 (Pmma) charge
order in CeRu3Si2 only for Ce-4f U>6 eV, with q=1/3 (Imma) nearly degenerate; f-as-core
fails to stabilize q=1/2.* DFT+U scoped out --> build a tight-binding + mean-field surrogate.

## Steps executed
1. **Read** paper text (`work/textures-loop-current-gerguri2026.txt`, lines ~288-363) and
   `report/evidence/replication_recipe.json`. Extracted the model system (P6/mmm parent;
   CO Pmma q=1/2; CO-II Imma q=1/3; CO* q=1/4 in f-as-core), the U-crossover claim
   (degenerate at 6 eV, q=1/2 wins for U>6 eV), and the f-as-core failure mode.
2. **Inspected kernels** `loop_current_kagome_kernel.py` and
   `loop_current_meanfield_kernel.py` in `/home/stevens/shared-kernels-cache/`.
   Reused kagome geometry (A1,A2, sublattice offsets, NN bonds) and the
   occupied-density / sum-of-occupied-energies pattern.
3. **Built** `work/gerguri2026_replication.py`: a kagome supercell (3 Ru + 1 Ce-4f per
   cell), Ru-Ru hopping t, Ru-f hybridization tf, f level eps_f = eps_f0 + kU*U.
   Charge order imposed as onsite Ru modulation at q=1/n. Order selection via the CDW
   Landau susceptibility chi_q = -(E(+d)+E(-d)-2E(0))/d^2.
4. **First attempt failed**: naive condensation-energy minimization pinned delta at the
   sweep boundary and made q=1/2 win trivially even in the core control (contradicting the
   paper). Replaced with the susceptibility (Landau-curvature) criterion at fixed small
   delta -> honest competition emerged.
5. **Ran** the U-sweep (U=0..9) + f-as-core control with the physics runner
   `/home/stevens/comfyui-env/bin/python` (numpy 2.3.5). Runtime ~0.3 s.
6. **SAVE-EARLY** to `work/gerguri2026_result.json`.
7. **Compared** to the headline and self-scored.
8. **Packaged** 8 artifacts (extraction x2, REPORT.tex, open_questions.json, workflow.md,
   artifacts_summary.md, failure_analysis.md) and copied result JSON + code + both kernels
   to `report/evidence/`.

## Key result
q=1/3 favored at U=0; crossover to q=1/2 at U~=5 (paper: 6 eV) with near-degeneracy
around U=4-5; f-as-core control -> q=1/4 (CO*) winner, q=1/3 suppressed, q=1/2 not ground
state. Three qualitative agreements with the paper.

## Runner / environment
- Physics: `/home/stevens/comfyui-env/bin/python` (numpy 2.3.5, scipy 1.17.0)
- Kernels: `/home/stevens/shared-kernels-cache/loop_current_{kagome,meanfield}_kernel.py`
