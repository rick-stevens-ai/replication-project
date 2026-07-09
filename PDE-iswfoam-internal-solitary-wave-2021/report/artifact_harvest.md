# Artifact Harvest

## Public artifacts pulled

| URL / DOI | Description | Size | Notes |
|---|---|---:|---|
| https://doi.org/10.5194/gmd-15-105-2022 | Paper PDF (CC BY 4.0) | 13,446,840 B | `work/iswfoam_gmd_2022.pdf` |
| https://doi.org/10.5281/zenodo.5069480 | ISWFOAM v1.1.1 archive (GPL-v3) | 1,331,155 B | Zip; extracted to `work/iswfoam_src/`, 136 files |
| https://zenodo.org/api/records/5069480 | Zenodo metadata JSON | ~5 kB | `work/zenodo_meta.json` (previously cached) |

## Zenodo archive contents (`work/iswfoam_src/`)

- `LICENSE.txt` = GPL v3, 35,148 B
- `README.md` = author's project readme, 594 B
- `manual-ISWFoam.pdf` = user manual, 178,850 B
- `ISWFoam/ISWFoam-master/` = main solver source (UEqn.H, pEqn.H, rhoEqn.H, ISWFoam.C, createFields.H, ...)
- `ISWFoam/densityTurbulenceModels-master/` = modified k-omega-SST density-aware closure (12 files)
- `ISWFoam/setUFields/setUFields.C` = velocity initial-condition utility (eKdV Eqs. 34-37, 40, 41, 42; verified verbatim)
- `ISWFoam/setRhoFields/setRhoFields.C` = density initial-condition utility (eKdV Eqs. 34-37 + Eq. 43 tanh pycnocline profile)
- `ISWFoam/tutorial/FlatBottom-eKdV/` = eKdV-initialized flat-bottom tutorial (rho1=996, rho2=1030)
- `ISWFoam/tutorial/FlatBottom-DJLES/` = DJL-initialized flat-bottom tutorial

## Generated artifacts (`report/evidence/`)

| File | Size | Description |
|---|---:|---|
| `ekdv_spotcheck.py` | 7,073 B | Original spot-check (Session 1) |
| `ekdv_spotcheck.out` | 1,613 B | Case B first-pass output |
| `ekdv_case_A.out` | 1,604 B | Case A first-pass output |
| `ekdv_case_B.out` | 1,634 B | Case B first-pass output |
| `ekdv_pde_solve.out` | 2,287 B | NEW. Full pseudospectral PDE-solve output, both cases |
| `ekdv_pde_case_A.json` | 1,221 B | NEW. Structured results Case A |
| `ekdv_pde_case_B.json` | 1,239 B | NEW. Structured results Case B |
| `ekdv_pde_case_A.npz` | 2,246,374 B | NEW. Full spatiotemporal snapshots + peak tracking, Case A |
| `ekdv_pde_case_B.npz` | 2,254,677 B | NEW. Full spatiotemporal snapshots + peak tracking, Case B |
| `ekdv_pde_case_A.png` | 162,026 B | NEW. 3-panel figure Case A |
| `ekdv_pde_case_B.png` | 178,339 B | NEW. 3-panel figure Case B |
| `ekdv_amplitude_sweep.out` | 1,156 B | NEW. Amplitude-sweep table |
| `ekdv_amplitude_sweep_case_A.json` | 1,472 B | NEW. Sweep results Case A |
| `ekdv_amplitude_sweep_case_B.json` | 1,463 B | NEW. Sweep results Case B |
| `velocity_field_check.out` | 902 B | NEW. Eq. (42) mass-conservation verification |
| `velocity_field_check.json` | 385 B | NEW. Structured velocity-check results |
| `llm_judge.json` | 1,246 B | NEW. Argo GPT-5 LLM-judge response |
| `llm_judge_prompt.txt` | 3,641 B | NEW. LLM-judge input prompt |
