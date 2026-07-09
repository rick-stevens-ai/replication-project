# OSTI-2583701 — Artifact Harvest (v1: 2026-07-03, v2: 2026-07-04)

## v2 (2026-07-04) new artifacts

| Path | Origin | Size | Notes |
|---|---|---|---|
| `report/evidence/mala_deep_test_results.json` | uicgpu:/data/stevens/mala-repl/deep_test_results.json | 5.7 KB | All 6 tests T1-T6 structured. |
| `report/evidence/mala_deep_test_run.log` | uicgpu:/data/stevens/mala-repl/deep_test_run.log | ~2 KB | Full stdout of v2 test. |
| `report/evidence/llm_judge_verdict_v2.json` | Argo argo:gpt-4.1 (free) | 0.7 KB | v2 judge: PARTIAL. |
| `work/mala_deep_test.py` | Ollie authored | ~11 KB | Six-test deep-replication script (T1-T6). |
| `work/mala_judge.py` | Ollie authored | ~5 KB | LLM judge script (Argo free endpoint). |

No new external artifacts were downloaded in v2 (same MALA + test-data as v1); only new *computed* artifacts.

---

## v1 publication artifacts
- **Paper PDF** (already on disk): `work/paper.pdf`, `work/paper.txt` (5.4 MB / 251 KB). OSTI ID 2583701. Published: Computer Physics Communications 314 (2025) 109654. DOI: 10.1016/j.cpc.2025.109654. CC BY 4.0.
- **Program library entry** (CPC's own DOI): <https://doi.org/10.17632/vbrxhnrvf2.1> (Mendeley Data).
- **MALA Zenodo:** <https://doi.org/10.5281/zenodo.5557254> (v1.3.0). Latest v1.4.0 on GitHub.

## Code (live, cloned, install-verified)
- **MALA source repository:** `https://github.com/mala-project/mala` — cloned to `uicgpu:/data/stevens/mala-repl/mala`. Master branch. License BSD-3. `pip install -e .` succeeded into `/data/stevens/envs/mala` (Python 3.10 conda env). Installed package name/version: `materials-learning-algorithms 1.4.0`.
- **Torch:** `torch 2.8.0+cu126` (installed from PyTorch's CUDA-12.6 wheel index because uicgpu's NVIDIA driver reports CUDA runtime 12.8; the default `torch 2.12.1+cu13` shipped with MALA's `requirements.txt` was too new for the driver — see attempt_log for the fix). CUDA available, 8 GPUs visible (all A100 80 GB PCIe).
- **Key MALA runtime deps installed:** `ase 3.29.0`, `openpmd-api 0.17.1`, `optuna 4.9.0`, `mendeleev 1.1.0`, `scikit-spatial 9.0.1`, `matplotlib 3.10.9`, `pandas 2.3.3`, `scipy 1.15.3`, `numpy 2.2.6`, `tensorboard 2.21.0`. Full `pip freeze` snapshot available in `evidence/mala_pip_freeze.txt` (see below).

## Data (live, downloaded)
- **`mala-project/test-data`** (GitHub, tag `2.0.0`) — the paper authors' own tutorial DFT reference data. Cloned to `uicgpu:/data/stevens/mala-repl/test-data`. Directory `Be2/` contents (2-atom hcp Be cell at 300 K, PBE + Quantum ESPRESSO ecutwfc=40 Ry):
  - `Be.pbe-n-rrkjus_psl.1.0.0.UPF` (560 KB) — pseudopotential.
  - `Be_model.zip` (56 KB) — pretrained MALA network for Be2 cell. Contents when unzipped: `Be_model.network.pth` (41 KB, PyTorch state dict), `Be_model.iscaler.pkl`, `Be_model.oscaler.pkl` (input/output scalers), `Be_model.params.json` (2.5 KB, MALA hyperparameters), `Be_model.info.json` (1.8 KB).
  - `Be_snapshot{0..3}.in.npy` — bispectrum descriptors, one per snapshot (3.3 MB each).
  - `Be_snapshot{0..3}.out.npy` — reference LDOS from Quantum ESPRESSO.
  - `Be_snapshot{0..3}.dens.npy` / `.dos.npy` — electron density and DOS references (small).
  - `Be_snapshot{0..3}.info.json` — DFT reference values: `band_energy_dft_calculation`, `total_energy_dft_calculation`, `fermi_energy_dft`, cell + atom positions, ecutwfc/ecutrho, temperature (299.99 K), electrons_per_atom, all Hartree/XC/Ewald components.
  - `.h5` (OpenPMD-encoded HDF5) mirrors of the above.

  DFT reference values loaded and used as ground truth for scoring in this replication:
  - Snapshot 0: band_energy_DFT = 12.0766 eV; total_energy_DFT = -73.0371 eV; Fermi = 8.743 eV.
  - Snapshot 1: band_energy_DFT = 12.1915 eV; total_energy_DFT = -72.6575 eV; Fermi = 8.366 eV.
  - Snapshot 2: band_energy_DFT = 12.1022 eV; total_energy_DFT = -72.9590 eV; Fermi = 8.592 eV.
  - Snapshot 3: band_energy_DFT = 12.0902 eV; total_energy_DFT = -72.9883 eV; Fermi = 8.694 eV.

## LLM judge (Argo, free)
- Endpoint: `http://localhost:44497/v1/chat/completions` (Argo proxy, free, key=`stevens`).
- Model used: `argo:gpt-4.1`. First attempt with `argo:claude-opus-4.7` returned HTTP 502; `argo:gpt-5` returned empty content at `max_tokens=50` (all reasoning tokens); `argo:gpt-4.1` succeeded. All free.
- Judge prompt + JSON verdict captured in `evidence/llm_judge_verdict.txt`.

## NOT harvested (out of scope, would need multi-day compute)
- **Production Be/Al/B models** (128–256-atom cells, ~1–24 GPU-hours training each per Table 2). Not distributed in `test-data`; the paper cites Refs [26, 46, 57, 60, 61] with per-model data on Rodare.
- **131,072-atom Be slab data** (Fig. 15) — cited to Ref [61], hosted separately on Rodare/HZDR. Not attempted.
- **Full DFT reference generation** for accuracy/transferability rerun — requires Quantum ESPRESSO + LAMMPS builds with the total-energy Fortran module linked, plus days of DFT runtime for the larger cells.
- **VASP GPU comparison** for Fig. 20 scaling — VASP is proprietary/paid.
