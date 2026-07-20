# Workflow — tazai2025 replication

## Goal
From-scratch replication of the headline claim: pure loop-current (LC) order
η = 0.014 on a 12-site kagome supercell drives a chiral d-wave SC instability
(Δ_μ ∝ (1, ω², ω), χ_d = −1) whose eigenvalue λ_d rises sharply below ~5 meV.

## Steps executed
1. **Read** paper text (`work/textures-loop-current-tazai2025.txt`) + recipe
   (`report/evidence/replication_recipe.json`). Extracted model params, LC form
   factor δt^c_ij = iη f_ij, gap equation Eqs. 1–2, cutoff Θ, and chiral pattern.
2. **Extraction:** `pdftotext -layout` → `extraction/_raw.txt`;
   `extraction/marker.md` (structured) + `extraction/nougat.mmd` (header + raw).
3. **Build from scratch** (`work/replicate_tazai2025.py`, run with
   `/home/stevens/comfyui-env/bin/python`):
   - 2×2 kagome supercell (12 sites), min-image NN/NNN bonds.
   - LC order as staggered Peierls flux i·η·f_ij circulating each triangle.
   - Bloch H(k) on folded-BZ k-mesh; μ fixed by filling n=11/12.
   - Pair kernel Γ_ml = (T/N) Σ_{k,n} G_k^ml G_{-k}^ml Θ; Matsubara sum ±64.
   - Diagonalize g·Γ; project eigenvectors onto s-wave and chiral (1,ω²,ω).
4. **Sweeps:** λ_d,λ_s vs T at η=0.014; λ_d,λ_s vs η at T=0.5 meV;
   chiral eigenvector phase structure at low T.
5. **SAVE-EARLY** → `work/tazai2025_result.json` (also copied to evidence/).
6. **Compare** to claims, score honestly → PARTIAL.
7. **Package** 8 artifacts + copy result JSON + code + kernel to `report/evidence/`.

## Runtime
~3 s on CPU (nuc-class target). nk=8, nmats=64.

## Tools / kernel credit
- Runner: `/home/stevens/comfyui-env/bin/python`.
- Kagome tight-binding + Peierls LC conventions from
  `shared-kernels-cache/loop_current_kagome_kernel.py` (KagomeModel).
- 12-site supercell, Γ_ml gap kernel, sweeps: built from scratch here.
