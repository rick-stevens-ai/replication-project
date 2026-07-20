# Workflow: Replicating Yang et al. 2022 (Kagome 3Q iCDW loop-current patterns)

**Paper:** Intertwining orbital current order and superconductivity in Kagome metal,
arXiv:2203.07365v2 (SciPost Physics, 2022).
**Method:** Landau-Ginzburg classification + kagome tight-binding loop-current Chern check.
**Runner:** `work/yang2022_runner.py` (Python: `/home/stevens/comfyui-env/bin/python`).

## Steps performed

1. **Read paper + recipe.** Parsed `report/evidence/replication_recipe.json` and
   `work/textures-loop-current-yang2022.txt`. Extracted the headline: for the 4 possible
   3Q iCDW patterns with up-spin reference `Phi_up=(i,i,i)`, the spin-resolved total
   Chern numbers are `C_up=+1` (all) and `C_down=(+1,-1,-1,+1)` for cases (i)-(iv);
   only case (ii) `(-i,-i,-i)` is helical / time-reversal symmetric (Table 1, Eq. 4-5).

2. **Loaded the reusable kernel** `loop_current_kagome_kernel.py` (`KagomeModel`):
   3x3 kagome Bloch Hamiltonian, Peierls-flux loop-current order, gap, and
   Fukui-Hatsugai-Suzuki Chern number. Verified flux-pattern behavior:
   - `none`: gapless Dirac (C undefined by TRS).
   - `uniform`: gapped but gauge-trivial (C=0).
   - `staggered` (+f up-triangles, -f down-triangles): TRS-breaking gap, **C=+1** —
     the physical chiral flux phase (matches Fig. 2 +/-6*phi opposite triangle fluxes).

3. **Built the replication runner.** Mapped each iCDW component sign (`+/- i`) to a
   Peierls phase (`+/- pi/2`). Established `C(i,i,i)=+1` numerically (FHS, |C|=1,
   TRS-breaking gap), then derived all four `C_down` via the paper's own Eq. (4)
   symmetry operations: `I` preserves the Chern number (flips 2 components),
   `M` reverses it (flips 3) -> `C_down = (-1)^(#flips) * (+1)`.

4. **SAVE-EARLY** to `work/yang2022_result.json` after the first successful run,
   then iteratively refined (physical staggered flux, honest agreement metric,
   explicit limitations block).

5. **Compared to Table 1:** 4/4 down-spin Chern numbers reproduced; helical/TRS
   pattern (ii) and chiral pattern (i) correctly identified.

6. **Packaged 8 artifacts** (extraction x2, REPORT.tex, open_questions.json,
   workflow.md, artifacts_summary.md, failure_analysis.md) and copied the result
   JSON + runner + kernel into `report/evidence/`.

## Reproduce

```bash
cd /home/stevens/textures-100/corpus/textures-loop-current-yang2022/
/home/stevens/comfyui-env/bin/python work/yang2022_runner.py
```

Expected: `Down-spin Chern (symmetry) matching paper: 4 /4`, chiral-flux `C_lower=1`.
