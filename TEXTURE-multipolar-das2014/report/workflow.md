# Workflow — Das (2014) SODW replication

Paper: T. Das, *Spin-orbit density wave: A new phase of matter applicable to the
hidden order state of URu2Si2*, Phil. Mag. (2014), arXiv:1406.5271v2.
Method (recipe): DFT (WIEN2k) + model-Hamiltonian + RPA + mean-field.
Headline: *the SODW gap reproduces the hidden-order gap phenomenology and predicts
Bc ~ 35 T.*

## Scope decision
- **Skipped:** the DFT band-structure input (WIEN2k downfolding of URu2Si2 5f
  bands). Material-specific, not reproducible in this environment on the time budget.
- **Built from scratch:** the MODEL-HAMILTONIAN SODW mean field — a transparent
  two-orbital spin-orbit-split tight-binding band nested by Q, the paper's SODW
  Nambu Hamiltonian (Eq. 2), and the self-consistent interorbital gap equation
  (Eqs. 7, 10).

## Steps executed
1. **Read** paper text (`work/textures-multipolar-das2014.txt`) + recipe
   (`report/evidence/replication_recipe.json`). Located Eq. 2 (Nambu H), Eqs. 7-8
   (self-consistent vertices + susceptibilities), Eq. 10 (SODW order parameter),
   Eqs. 11-12 (GL free energy), and the key numbers: Th=17.5 K, ~24% entropy loss,
   ~40% FS spectral-weight loss, Delta0 ~ 10 meV, V ~ 0.6 eV, Bc ~ 35 T.
2. **Inspected the prior (502-interrupted) attempt.** The earlier 4x4 Nambu build
   *ran* but the self-consistent gap collapsed to ~1e-5 meV with Th=0 — a broken
   fixed point (cancelling coherence factors in the 4x4 M-operator trace). See
   `failure_analysis.md`.
3. **Rebuilt** the mean field as a clean, physically-nested 2x2 particle-hole
   block with a standard density-wave gap equation (`report/evidence/sodw_meanfield.py`).
4. **Ran** on `/home/stevens/comfyui-env/bin/python` (numpy 2.3.5, scipy 1.17.0),
   128x128 k-grid. **SAVE-EARLY** to `work/das2014_result.json`.
5. **Extracted:** Delta(V) + critical V; Delta(T) + Th; DOS(PM vs HO); entropy
   release across Th; Zeeman Bc estimate.
6. **Compared** to paper targets and **self-scored** (honest, model-band caveats).
7. **Packaged** the 8 artifacts and copied code + result JSON into `report/evidence/`.

## Reproduce
```bash
/home/stevens/comfyui-env/bin/python \
  /home/stevens/textures-100/corpus/textures-multipolar-das2014/report/evidence/sodw_meanfield.py
# writes work/das2014_result.json (~30 s)
```

## Key results
| Quantity | Model | Paper |
|---|---|---|
| SODW gap Delta0 | 6.15 meV | 5-10 meV |
| Th | 17.9 K | 17.5 K |
| Vc | ~0.30 eV | V ~ 0.6 eV |
| FS spectral-weight loss | ~6% | ~40% |
| Entropy release | ~0.006 kB ln2 | ~24% R ln2 |
| Zeeman Bc | ~106 T | ~35 T |

Gap magnitude, Th and interaction scale reproduced; integrated-FS quantities
under-reproduced by the thin model band -> **PARTIAL**.

## Credit
Scaffolding informed by `ollie_multipolar_stevens_landau_kernel.py` (Ollie
multipolar Stevens/Landau kernel). SODW nesting, gap equation, DOS and entropy
built from scratch.
