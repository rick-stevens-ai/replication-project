# Artifact Harvest — WaveTrain replication

All artifacts fetched are open-source / open-access.

| # | Artifact | URL / accession | Size / commit | Notes |
|---|---|---|---|---|
| A1 | `wave_train` source | https://github.com/PGelss/wave_train (git clone --depth 1) | HEAD @ 2026-07-04 (Riedel et al 2023 code) | Cloned into `work/wave_train/`. Contains `test_scripts/{Exciton,Phonon,Exc_Pho_Coupling,Bath_Map_1,Exciton_Krylov}/` |
| A2 | `scikit_tt` source (tensor-train backend) | https://github.com/PGelss/scikit_tt (via `pip install git+...`) | HEAD | Installed into venv; ALS/EVP solvers used by wave_train |
| A3 | Paper (J. Chem. Phys. 158, 164801) | https://doi.org/10.1063/5.0147314 | ~open-access at pubs.aip.org | Metadata + method verified through GitHub README (paywall on PDF prevented direct extraction) |
| A4 | Bundled example script | `wave_train/test_scripts/Exciton/tise_1.py` | 68 lines Python | This is the exact primary benchmark run |

**Data used for validation.** None external — the paper's replication target is analytical (tight-binding spectrum) and the software's own bundled examples. No secondary datasets required.

**Python env used.**
- macOS 25.3.0, Python 3.12.13, NumPy 1.26.4 (pinned <2 for scikit_tt compatibility), SciPy 1.16.x, Matplotlib installed but not exercised
- `wave_train` installed from source (`pip install ./wave_train`)
- `scikit_tt` installed from git (`pip install git+https://github.com/PGelss/scikit_tt`)
