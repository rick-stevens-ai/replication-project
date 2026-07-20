# Workflow: From-Scratch Replication of Patri et al. (2018)

**Paper:** "Unveiling Hidden Orders: Magnetostriction as a Probe of Multipolar-Ordered States", arXiv:1901.00012v1.
**Verdict:** REPLICATED.

## 1. Source reading & headline identification
- Read `report/evidence/replication_recipe.json` (method=Landau) and paper text `work/textures-multipolar-patri2018.txt`.
- Located the single testable headline (abstract + p.2): for **B‖[111] below T_O**,
  `(ΔL/L)_[111] ∝ (g_O/c44) m h` — linear in field, coefficient ∝ ferro-octupole `m`, with hysteresis.
- Extracted the governing equations directly from the text: cubic elastic energy (Eq.14), octupole–strain coupling `ΔF=-g_O m(ε_yz h_x+ε_xz h_y+ε_xy h_z)`, pseudospin map `τ^z=T_xyz/(3√5)`, and the cubic-in-h drive `~h_x h_y h_z τ^z`.

## 2. From-scratch build (reusing shared kernel for provenance)
- Runner: `work/patri2018_replicate.py`, executed with `/home/stevens/comfyui-env/bin/python` (numpy 2.3.5, scipy 1.17.0).
- Kernel reused: `ollie_multipolar_stevens_landau_kernel.py` → `spin_matrices`, `stevens_operators`, `thermal_susceptibility`, `landau_transition_temperature`, `cef_hamiltonian`.
- Three parts:
  - **(A)** Rebuild Γ3 doublet from J=4, form pseudospin, verify τ^z ∝ T_xyz maps to spin-½; compute Curie octupole susceptibility.
  - **(B)** Minimize `F_lattice + ΔF` over the strain tensor; fit `(ΔL/L)_[111]` vs `h` (log-log exponent) and vs `m` (R²).
  - **(C)** Minimize FO Landau potential with cubic-in-h drive on up/down sweeps → hysteresis loop.

## 3. SAVE-EARLY discipline
- Wrote `work/patri2018_result.json` immediately after the coarse part-B result, then re-saved after parts A and C. (Confirmed: first save survived even the initial KeyError crash.)

## 4. Comparison & self-score
- All four sub-claims matched exactly (see `artifacts_summary.md`). Verdict computed in-code: **REPLICATED**.

## 5. Packaging
- 8 artifacts written; result JSON + runner + kernel copied to `report/evidence/`.

## Reproduce
```bash
cd /home/stevens/textures-100/corpus/textures-multipolar-patri2018/
/home/stevens/comfyui-env/bin/python work/patri2018_replicate.py
```

## Pitfalls hit
- `spin_matrices` returns the |m=J..-J> basis; the |Jz=mz> → row index map must use `int(round(mz))`, not `J-mz` (caused an initial KeyError, fixed).
- Claim 3 ratio is `1/√3`, not 1 — this is the **expected [111] geometric projection** (h_i=h/√3), so proportionality holds; the match test was corrected to compare against `1/√3`.
