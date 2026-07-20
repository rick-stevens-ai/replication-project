# Workflow — christensen2022 Landau-theory replication

## Goal
Reproduce the reproducible core of Christensen et al. (arXiv:2207.12820v2): the
coupled iCDW–rCDW Landau free energy on kagome AV3Sb5 and its two generic mixed
phases (3Q-3Q, 2Q-1Q). DFT/group-theory VHS derivation deliberately skipped.

## Steps
1. **Read** recipe (`report/evidence/replication_recipe.json`) + paper text
   (`work/textures-loop-current-christensen2022.txt`). Located the free energy
   at lines 727–850 (Eqs. 10–13) — the exact symmetry-allowed polynomial.
2. **Encode** the free energy `F = Fr + Fi + Fir` verbatim in
   `work/christensen2022_landau.py`, with the critical TRS input: iCDW forbids a
   Φ1Φ2Φ3 trilinear, so the mixed γ_ir trilinear is the only cubic that lowers
   the iCDW energy → selects 3Q-3Q vs 2Q-1Q.
3. **Minimize** F over the 6-D OP space via multistart Nelder–Mead (33 seeds:
   disordered, pure 1Q/2Q/3Q of each, both mixed states, + random). Classify the
   global minimum by counting nonzero N_i, Φ_i.
4. **Sweep** a 6×6 grid in (a_r,a_i)∝(T−Tr,T−Ti) for two coefficient sets:
   - Scenario A (large γ_ir/γ_r, small biquadratics) → 3Q-3Q.
   - Scenario B (large λ_ir(1) penalty) → 2Q-1Q.
5. **Verify**: (a) both mixed phases appear as global minima; (b) pure iCDW is
   never a stand-alone minimum (cooling only Φ gives pure-1Q iCDW); (c) 2Q-1Q
   has a single N-component → C3 broken → orthorhombic.
6. **SAVE-EARLY** to `work/christensen2022_result.json`.
7. **Package** 8 artifacts + copy result JSON, runner code, and kernel into
   `report/evidence/`.

## Runner
`/home/stevens/comfyui-env/bin/python work/christensen2022_landau.py`
Runtime ~28 s.

## Kernel credit
`shared-kernels-cache/loop_current_meanfield_kernel.py` (Ollie) — loop-current
order-parameter / geometry conventions and TRS interpretation.
