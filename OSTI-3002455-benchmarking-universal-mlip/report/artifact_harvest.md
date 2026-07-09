# Artifact Harvest

| Artifact | Source | Size / notes |
|---|---|---|
| Paper PDF | https://www.osti.gov/servlets/purl/3002455 | 3.99 MB, PDF v1.7, downloaded via uicgpu (CherryRd cannot reach osti.gov directly) |
| Paper text (pdftotext) | derived from `work/paper.pdf` | `work/paper_extracted.txt`, 601 lines |
| Paper repo | https://github.com/maplewen4/phonon_uMLIP | cloned into `work/phonon_uMLIP/` — contains 4 conda env yml files (`env_phonon_uMLIP{0_8,1-5_7_9_10,11,6_12}.yml`) and 4 driver scripts (`mlff_phonon_{0_8,1-5_7_9_10,11,6_12}.py`) that our replication mirrors |
| Paper Zenodo dataset | https://doi.org/10.5281/zenodo.15298435 | 4869-crystal DFT phonon database (POSCARs + FORCE_SETS + phonopy.yaml). NOT downloaded in this run (large); paper's crystal set derived from Materials Project MP IDs. |
| MACE-MP-0 checkpoint | https://github.com/ACEsuit/mace-mp/releases/download/mace_mp_0/2023-12-03-mace-128-L1_epoch-199.model | 42.4 MB, auto-downloaded by `mace_mp(model="medium")`. Cached to `~/.cache/mace/20231203mace128L1_epoch199model` on uicgpu. |
| CHGNet checkpoint | shipped inside pip pkg `chgnet==0.3.0` | 412,525 params |
| Reference DFT/experimental max phonon frequencies (Si, Ge, NaCl, MgO, diamond) | classical INS/Raman literature (Weber 1977 for Si, Raunio for NaCl, Sangster for MgO, standard values in every solid-state textbook, e.g. Kittel; Materials Project phonon DB reproduces these to within ~2 meV) | inline in `work/run_phonon_repl.py` and REPORT §3 |

## Locally-produced evidence

| File | What |
|---|---|
| `report/evidence/phonon_results.json` | Raw json of all 5 crystals × 2 uMLIPs: max/min freq, all 6 Γ-point frequencies, supercell dims, wall-clock, force-count |
| `report/evidence/phonon_run.log` | Full stdout/stderr of the replication run on uicgpu (log-only; download progress lines stripped in text views) |
| `report/evidence/fig_replication_vs_ref.png` | Bar chart: max phonon freq vs reference + relative-error panel |

## Environment (uicgpu)

- Conda env: `mlip3002455` (Python 3.11, torch 2.12.1+cu130 — CUDA fell back to CPU because A100 driver = 12.8 too old for cu130 wheels; MACE-MP-0 and CHGNet ran on CPU and completed in minutes because unit cells are tiny)
- Packages: `mace-torch`, `chgnet==0.3.0`, `ase==3.23`, `pymatgen`, `phonopy`, `matplotlib`
- Compute: single CPU thread of the uicgpu login/A100 node, `OMP_NUM_THREADS` not set explicitly (paper reports OMP=2 for their timing)
