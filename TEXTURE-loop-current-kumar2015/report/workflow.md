# Workflow — Kumar, Sun & Fradkin (2015) replication

## Pipeline: acquire → parse → extract → build → run → compare → report

1. **Acquire / parse.** Paper PDF already in corpus; body text extracted with
   `pdftotext` → `work/textures-loop-current-kumar2015.txt` (2859 lines).
2. **Read recipe.** `report/evidence/replication_recipe.json`
   (method=model-Hamiltonian; headline: XY-regime chirality term → zero-field
   CSL, σ_xy^s = 1/2).
3. **Extract physics** (Secs. II–IV of paper):
   - Model: kagome spin-1/2 XXZ AFM + chirality term
     `H_ch = h Σ_△ S_i·(S_j×S_k)`; main claim at zero external field.
   - Mechanism: flux attachment → fermions + kagome Chern-Simons gauge field;
     chirality term → Peierls phase `φ = arctan[(h/J)(1/2−n)]`, → ±π/2 in XY
     limit → (2π, π/2, π/2) chiral flux state → Chern band → σ_xy^s = C/2.
4. **Build from scratch.** `work/run_kumar2015.py` drives the reusable
   `loop_current_kagome_kernel.py` (`KagomeModel`): NN kagome tight-binding +
   directed Peierls loop-current flux + Fukui–Hatsugai–Suzuki Chern number +
   loop-current order parameter (Im⟨c_A†c_B⟩).
5. **Run.** Sweep chirality-induced flux φ from 0 (Heisenberg) into the chiral
   regime at zero external field (lowest band filled). Compute gap, C, loop
   current, σ_xy^s = C/2. SAVE-EARLY → `work/kumar2015_result.json`.
6. **Compare.** φ=0 → gap≈0, C=0 (TRS, no chiral order). Finite φ → gap opens,
   C=+1, σ_xy^s = 1/2, spontaneous loop current. Matches headline exactly on
   the topological invariant.
7. **Report / package.** 8 artifacts (below) + evidence copies.

## Tools / runners
- Physics runner: `/home/stevens/comfyui-env/bin/python` (numpy 2.3.5, scipy 1.17.0).
- Kernel: `/home/stevens/shared-kernels-cache/loop_current_kagome_kernel.py`.
- Extraction: `pdftotext` (poppler).

## Artifacts produced
- `extraction/marker.md`, `extraction/nougat.mmd`
- `report/REPORT.tex`, `report/open_questions.json`, `report/workflow.md`,
  `report/artifacts_summary.md`, `report/failure_analysis.md`
- `report/evidence/`: `kumar2015_result.json`, `run_kumar2015.py`,
  `loop_current_kagome_kernel.py`, `replication_recipe.json`

## Reproduce
```bash
cd /home/stevens/textures-100/corpus/textures-loop-current-kumar2015/work
/home/stevens/comfyui-env/bin/python run_kumar2015.py
```
