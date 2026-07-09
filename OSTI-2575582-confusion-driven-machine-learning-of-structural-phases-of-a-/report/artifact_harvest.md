# Artifact harvest

## Paper PDF
- URL: https://www.osti.gov/servlets/purl/2575582
- Local: `work/paper.pdf`
- Size: 9,186,197 bytes
- HTTP: 200
- Verified: `pdftotext` extracted 971 lines of text.

## Authors' companion code
- URL: https://github.com/dilinanp/ml-confusion-polymer
- Cloned to: `uicgpu:/tmp/ml-confusion-polymer/` (also inspected here)
- Contents: `notebook/confusion_method.ipynb` (single notebook implementing the confusion sweep in TensorFlow/Keras), `requirements.txt`, `README.md`, MIT license.
- Purpose: reference for the algorithm and input-data format. We do **not** run this notebook for the replication — we write our own PyTorch implementation.

## Raw configuration data (Zenodo)
- URL: https://zenodo.org/records/15851811/files/data_eta_0.02.tar.gz
- Downloaded to: `uicgpu:/tmp/data_eta_0.02.tar.gz`
- Size: 3,086,699,279 bytes (~2.9 GB compressed → ~10 GB uncompressed with 524,987 files: half `.dat` (features), half `.pdb` (visualization))
- HTTP: 200
- After extraction: `uicgpu:/tmp/confusion_repl/long_run_19_walkers_equilibrated_runs_eta_0.02/production/`
- File count: 524,987 total; 518,669 files match `Chain_bin*.dat` (the format expected by the confusion pipeline); 200 distinct energy bins (`bin00000` … `bin00199`).
- Data format: 100 rows × 6 columns per file. Columns are (x, y, z, μ_x, μ_y, μ_z) for each of the 100 monomers of the polymer chain. Energy is inferred from the bin index via the paper's mapping `E = bin*100/21.16 − 1145` for η=0.02.

## What we did NOT harvest (out of scope)
- `data_eta_0.06.tar.gz` — comparable ~3 GB tarball for the second η value studied. Would enable independent verification of the three-peak claim (paper Fig. 9). Skipped to keep this replication compact and within the token budget for one subagent.
- The raw REWL simulation code (from Perera/Vogel Wang–Landau papers refs 108–110). Regenerating configurations from scratch is a several-day HPC run; out of scope for this replication which uses the authors' Zenodo-hosted equilibrium configurations directly.
