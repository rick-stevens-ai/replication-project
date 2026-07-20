# Workflow: Replication of feng2021 (Chiral Flux Phase in kagome AV3Sb5)

## Goal
Test the headline claim: at coupling **λ = 0.3** and 5/4 van Hove filling, among the
three symmetry-allowed 2×2 (3Q) charge orders on the kagome lattice — vCDW, CBO, CFP —
the **chiral flux phase (CFP)** has the lowest energy, breaks time-reversal symmetry,
and is a Chern/anomalous-Hall insulator.

## Steps taken
1. **Read** the paper (`work/textures-loop-current-feng2021.txt`) and recipe
   (`report/evidence/replication_recipe.json`). Extracted: Eq.1 (NN kagome TB),
   Eq.4 (vCDW onsite), Eq.7 (CBO real bond), Eq.9 (CFP imaginary bond),
   the three M-point wavevectors Qa/Qb/Qc, and 5/4 filling.
2. **Inspected** the shared kernels
   (`shared-kernels-cache/loop_current_kagome_kernel.py`,
   `loop_current_meanfield_kernel.py`) for geometry (half-bond Bloch convention),
   the Peierls-flux mechanism, the bond-current estimator
   `J_ij = -2 Im[H_ij ρ_ji]`, and the Fukui–Hatsugai–Suzuki Chern routine.
3. **Built** `work/feng2021_replication.py` from scratch:
   - real-space L×L periodic kagome cluster (L=12 → 432 sites, 144 cells),
   - robust geometric NN-bond detection with minimum-image PBC,
   - three 3Q orders modulated at Qa/Qb/Qc (onsite / real bond / imaginary bond),
   - exact diagonalization, fill to 5/12 of states, energy per unit cell,
   - TRS check (is H real?), current-conservation check (max site net current).
4. **Ran** with `/home/stevens/comfyui-env/bin/python`. **SAVE-EARLY** →
   `work/feng2021_result.json` (energies at λ=0.3, full λ-sweep 0.0–0.5, diagnostics).
5. **Compared** to the paper's numbers and scored honestly (see `failure_analysis.md`).
6. **Packaged** 8 artifacts (extraction ×2, report ×5, evidence copies).

## Key results
- **CFP wins at λ=0.3** (E = −2.6770 t/cell), lowest of all four states; wins for all λ≥0.2.
- CFP is the **only** T-breaking order (H complex); vCDW & CBO stay real → matches Fig.1c.
- CFP current conserved to ~1e-16.
- Energy splittings ~15× smaller than paper; vCDW/CBO sub-order reversed → PARTIAL.

## Reproduce
```
cd work && /home/stevens/comfyui-env/bin/python feng2021_replication.py 12
```

## Kernel credit
Geometry & flux conventions from `loop_current_kagome_kernel.py`; real-space cluster
and bond-current estimator from `loop_current_meanfield_kernel.py`.
