# Workflow — wang2024 (arXiv:2411.00315) Topological Orbital Hall Effect

## Pipeline
1. **Extraction** — `extraction/marker.md` (pdftotext fallback; clean). OAM operator
   (Eq.1) and Kubo/feature-Berry formulas (Eqs.2-4) legible. `report/method_extract.md`
   captured the 5 central claims + computational recipe.
2. **Model build** — minimal Kane-Mele honeycomb TB, 4 bands (2 sublattice x 2 spin),
   germanene-like params `t=1.3 eV`, `lambda_SO=0.043 eV`, `lambda_R=0`, `Delta=0`.
3. **Vectorized diagonalization** — `H(k)`, `v_x`, `v_y` built over a 60x60
   Monkhorst-Pack mesh; single batched `numpy.linalg.eigh` over the whole mesh.
4. **Operators** — itinerant orbital operator `L_z = 0.5*(X v_y - Y v_x)` via
   Berry-connection matrix elements `A^a_nm = i v^a_nm / (E_m - E_n)`; orbital current
   `j^L_x = 0.5*{L_z, v_x}`. Spin `S_z = tau0 (x) sigma_z`, `j^S_x = 0.5*{S_z, v_x}`.
5. **Kubo Hall sweep** — T=0 clean DC Chern-like sum over occ/unocc pairs, swept over
   `E_F` across the SOC gap → orbital & spin Hall conductivity curves.
6. **Validation + figures** — gap vs Kane-Mele theory `2*3*sqrt(3)*lambda_SO`; plateau
   flatness (std over in-gap EF window); `figs/bands.png`, `figs/ohc_vs_EF.png`.
7. **Report** — `report/REPORT.tex` (+ PDF), open questions, artifacts summary,
   failure analysis.

## Compute
- **Engine:** pure NumPy, vectorized `eigh` over the batched k-mesh (no loops over k).
- **Host:** CPU (nuc13-class); no GPU / no DFT SCF required (TB is parametrized).
- **Runtime:** ~10 min wall on CPU for the 60x60 mesh + EF sweep.
- **Reproduce:** `python3 work/reproduce.py` → writes `work/results.json` + `work/figs/*`.

## Key outputs
- Orbital Hall plateau `-8.83` (std `0.000`); spin Hall plateau `2.85`.
- SOC gap `0.447 eV` == KM theory `0.4469 eV` (4 dp).
- Orbital >> Spin (`8.83` vs `2.85`).
