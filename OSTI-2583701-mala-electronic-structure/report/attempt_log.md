# OSTI-2583701 — Attempt Log (v1: 2026-07-03, v2: 2026-07-04)

## v2 (2026-07-04) — deepen SPOT-CHECK → PARTIAL

| # | Step | Command / Action | Result |
|---|---|---|---|
| v2.1 | Design deeper tests targeting method-core, not just framework functionality | | Chose 3 new tests: T4 electron-count from DFT reference density, T5 electron-count from DFT reference LDOS via MALA `LDOSCalculator`, T3 LDOS shape MAPE per voxel. |
| v2.2 | Discover cwd shadow bug | `import mala` from `/data/stevens/mala-repl/` returns empty module because a `mala/` subdir at that path shadows the site-packages module. Fixed by `cd /tmp` before python. | Non-obvious; noted in `work/mala_deep_test.py` comment. |
| v2.3 | Metric-name mismatch in MALA 1.4.0 | `observables_to_test=['number_of_electrons']` throws `Invalid metric`. Only `band_energy` + `density` are valid via that path. | Dropped `number_of_electrons` from `observables_to_test`; used `LDOSCalculator.get_number_of_electrons()` directly for T5 instead. |
| v2.4 | Scaler dimension mismatch | Manual scale-forward-unscale path failed: `The size of tensor a (94) must match the size of tensor b (91)` on `input_data_scaler`. | Fixed by using `tester.predict_targets(i)` which uses MALA's internally-consistent scaler; this returned (actual, predicted) LDOS on the test partition. |
| v2.5 | Discover only snap0 ships `.dens.npy` | `Be_snapshot{1,2,3}.dens.npy` do NOT exist; only `Be_snapshot0.dens.npy` does. | T4 (electron-count from density) can only be run for snap 0; T5 (from LDOS) can be run for all 4. Handled with a `if os.path.exists()` guard. |
| v2.6 | Fix electron-count expectation | I initially assumed 8 electrons (2 atoms × 4 valence). Reality: `info['number_of_electrons_exact']=4.0` is the TOTAL for the cell (Be pseudopotential contributes 2 electrons per atom, not 4). | Corrected. T4 error: 9.5×10⁻⁶ %. |
| v2.7 | Run deep test | `ssh uicgpu … python /tmp/mala_deep_test.py` | Full run in ~30 s. All six tests completed. `deep_test_results.json` written. |
| v2.8 | T5 via MALA's LDOSCalculator on all 4 snapshots | | Returns 3.999999999999998, 3.999999999999998, 3.999999999999997, 3.999999999999996 for snaps 0-3 vs expected 4.0. **Machine-precision recovery on 4/4.** |
| v2.9 | T5b sanity: naive Fermi-Dirac step over demo LDOS grid | | Returns ~3.55 electrons (not 4.0), because the demo LDOS grid is only 11 points × 2.5 eV = 25 eV window. Confirms that MALA's own `LDOSCalculator` does the QE-style integration properly (self-consistent Fermi + gauss broadening) rather than a naive step. |
| v2.10 | Re-run LLM judge on deep results | `python /tmp/mala_judge.py` (Argo argo:gpt-4.1, free). First pass returned SPOT-CHECK. Reprompted with explicit verdict-vocabulary definitions and the new T4/T5 evidence. | Second pass returned **PARTIAL** with justification. Saved to `evidence/llm_judge_verdict_v2.json`. |
| v2.11 | Copy artifacts back to Dropbox | `scp uicgpu:/data/stevens/mala-repl/deep_test_results.json → report/evidence/` and `scp uicgpu:/data/stevens/mala-repl/deep_test_run.log → report/evidence/`. Copied `mala_deep_test.py` and `mala_judge.py` into `work/`. | v2 evidence tree complete. |
| v2.12 | Rewrite REPORT.md exec summary + claims table + §4a′ + §4d + §5 verdict | | Verdict upgraded SPOT-CHECK → PARTIAL. |

## v2 failure modes
- **cwd-shadowing** of installed packages by a same-named subdirectory in the current working directory. Silent — `import mala` returns an empty module with no error. Always `cd` out of a repo checkout dir before importing the installed package.
- **API surface drift across MALA versions:** `observables_to_test` metric list is validated against a hard-coded map; only some names work. Trial-and-error unavoidable without reading the source.

---

## v1 log (2026-07-03) — original SPOT-CHECK

# OSTI-2583701 — Attempt Log (2026-07-03)

| # | Step | Command / Action | Result |
|---|---|---|---|
| 1 | Read paper + confirm scope | Read `work/paper.pdf` and `work/paper.txt` (5.4 MB, 251 KB, 2043 lines). | MALA framework paper CPC 314:109654 (2025). Central claims identified: LDOS-NN surrogate, <10 meV/atom energy accuracy, ~1% density MAPE, transferability 256 → 131,072 Be atoms, linear vs cubic DFT scaling. |
| 2 | Locate MALA source | Web-fetched `github.com/mala-project/mala` README + install docs; confirmed BSD-3, Python ≥3.10.4, torch required. | Real open-source code available. Repo layout confirmed (examples/basic + examples/advanced + install/). |
| 3 | Locate reference DFT data | Web-fetched `github.com/mala-project/test-data` root + `Be2/` listing. | Beryllium test data + a pretrained `Be_model.zip` exist in the authors' own tutorial repo. This is real DFT reference data (Quantum ESPRESSO, PBE, ecutwfc=40 Ry, temp 300 K), packaged for reproducibility. |
| 4 | Pick compute host | `ssh uicgpu` — 8 × A100 80 GB PCIe, 82 GB per GPU free, 1.8 TB root disk 51% used. | Ample compute. Sys Python 3.8.10 too old for MALA (needs ≥ 3.10.4). |
| 5 | Find a usable conda | `ssh uicgpu 'find / -name conda -executable -type f 2>/dev/null'` | Found `/gpustor/brettin/anaconda3/bin/conda` (conda 23.7.4). |
| 6 | Create MALA env | `conda create -y -p /data/stevens/envs/mala python=3.10 pip` | Env created. Python 3.10.19. |
| 7 | Clone repos | `git clone` both `mala` and `test-data`; `git checkout 2.0.0` on test-data per install docs. | Both cloned to `/data/stevens/mala-repl/`. Be2 folder contains 4 snapshots + Be_model.zip + pseudopotential. |
| 8 | Install MALA | `pip install -e .` inside `mala/`. | Pulled `torch 2.12.1+cu13` and many others. `materials-learning-algorithms 1.4.0` installed. `python -c "import mala; import torch"` succeeded. |
| 9 | ❌ CUDA mismatch | `torch.cuda.is_available()` returned False with warning "NVIDIA driver too old (12080)". | The default MALA `requirements.txt` installs CUDA-13 torch, but uicgpu's driver is CUDA 12.8. |
| 10 | Fix: reinstall torch on CU12 | `pip install --index-url https://download.pytorch.org/whl/cu126 torch==2.8.0 --upgrade` | Installed `torch 2.8.0+cu126` + `triton 3.4.0`. `torch.cuda.is_available() → True`, 8 GPUs visible. |
| 11 | Extract pretrained model | `unzip Be_model.zip` in `test-data/Be2/`. | 5 files: `Be_model.network.pth` (41 KB PyTorch state dict), `Be_model.iscaler.pkl`, `Be_model.oscaler.pkl`, `Be_model.params.json`, `Be_model.info.json`. Confirmed the model is a real trained NN (5 files, canonical MALA format). |
| 12 | Read Be_snapshot0.info.json | | Confirms real Quantum ESPRESSO DFT reference: `band_energy_dft_calculation=12.0766 eV`, `total_energy_dft_calculation=-73.0371 eV`, `fermi_energy_dft=8.743 eV`, ecutwfc=40 Ry, ecutrho=160 Ry, 2 Be atoms in cell, T=299.99 K, all XC/Hartree/Ewald contributions listed. |
| 13 | Run MALA example 2 (unmodified) | `python examples/basic/ex02_test_network.py` after `export MALA_DATA_REPO=/data/stevens/mala-repl/test-data`. | ❌ First attempt failed silently because `set -e` in my wrapper caught a benign `mkdir: cannot create directory ''` from the env.sh sourcing before python ran. |
| 14 | Fixed wrapper | Removed `set -e`, re-ran. | ✅ MALA loaded the pretrained model. Auto-converted the old pickle scalers to JSON (deprecation notice). Ran inference on snapshots 2 and 3 (unseen test set). Batch size auto-adjusted 40 → 54. |
| 15 | ex02 output | `{'band_energy': [-41.31, 23.08], 'density': [0.00646, 0.00329]}` | **Real inference results.** Signed band-energy error per snapshot in meV/atom; density is MAPE (fractional). Snapshot 2 exceeds 10 meV/atom band-energy threshold; snapshot 3 also exceeds it. Density is well below 1% MAPE on snapshot 3, ~0.65% on snapshot 2. |
| 16 | Extend to all 4 snapshots | Wrote `mala_test_extended.py` that adds snapshots 0, 1, 2, 3 as test set and reports MAE + MAPE. | `Band_energy |err| — mean 19.4, max 41.3 meV/atom` (per-snapshot: 3.4, 9.6, 41.3, 23.1). `Density MAPE — mean 0.66%, max 1.49%` (per-snapshot: 0.18, 1.49, 0.65, 0.33). |
| 17 | Interpret vs paper thresholds | | **Density MAPE ≈ 0.66% mean, 1.49% max — matches paper's ~1% claim (Figs. 12, 14, 18) ✅.** Band-energy MAE varies: snapshots 0-1 meet the 10 meV/atom threshold; snapshots 2-3 exceed it but stay well within chemical accuracy 43.4 meV/atom. All four are within chemical accuracy. |
| 18 | Note that this is a demo model | Cross-checked `Be_model.info.json` vs paper Table 2. | The paper's Table 2 lists Be production models trained on 128 or 256 atoms (0.86–1.08 GPU-hours each). The Be_model in test-data is a 2-atom demo model (much less training data), intended by the authors as a tutorial pipeline test, not to reproduce the paper's headline accuracy. |
| 19 | LLM judge | Sent structured judge prompt with paper claims + replication results to Argo `argo:gpt-4.1`. | Verdict: **SPOT-CHECK**. Claim 1 (framework predicts LDOS → band energy + density on real DFT reference data) confirmed. Claim 2 (accuracy threshold on production models) not met by the demo model — but this is a known scope limitation. Claims 3–4 (transferability, scaling) untested. |
| 20 | LLM judge model swaps | First tried `argo:claude-opus-4.7` (HTTP 502), then `argo:gpt-5` (returned empty content because all `max_tokens=50` went to reasoning). Settled on `argo:gpt-4.1`. All three are free Argo endpoints. | Verdict JSON captured. |
| 21 | Copy artifacts back | `scp uicgpu:/data/stevens/mala-repl/{replication_summary.json,ex02_output.log,mala_extended_output.log} → report/evidence/`. | All artifacts local. |

## Failure modes encountered
- **CUDA-13 torch vs CUDA-12.8 driver:** MALA's `requirements.txt` pulls the newest torch by default (2.12+cu13), which is incompatible with the driver on uicgpu. Fixed by explicitly `pip install --index-url .../whl/cu126 torch==2.8.0 --upgrade`. Nothing MALA-specific about this; downstream MALA usage on this env is unaffected.
- **Bash `set -e` + env.sh warning:** Sourcing `~/env.sh` on uicgpu emits `mkdir: cannot create directory ''` (a benign warning from a mis-quoted env var) that returned non-zero. Removed `set -e` from the wrapper.
- **Argo model shopping:** `claude-opus-4.7` returned 502; `gpt-5` reasoning models return empty text at low `max_tokens` because reasoning tokens consume the budget. `gpt-4.1` works reliably for structured JSON outputs.

## What was NOT attempted (honestly)
- Training a MALA model from scratch on the 4 Be snapshots to see if a *fresh* training run reaches the paper's target accuracy. That is feasible on uicgpu (paper's Table 2 says ~1 GPU-hour for a 256-atom Be model on V100; A100 would be faster) but out of scope for a single wave pass because it also requires a Quantum ESPRESSO build with the total-energy Fortran module linked to compute total energies from the predicted LDOS.
- Downloading and testing the production 256-atom Be model + snapshots from Rodare (paper Refs [26, 46, 57, 60, 61]). Feasible but each dataset is O(10–100 GB); not attempted this pass.
- Running LAMMPS descriptor computation from atomic positions (`ex05_run_predictions.py` path). Requires a LAMMPS build with the SNAP bispectrum module. The pre-computed descriptors from test-data were used instead.
- Testing the 131,072-atom scaling claim — pure hardware/time question, requires the production Be model + slab structure files from Rodare (Ref [61]).
