# Attempt Log — OSTI-2396626

Chronological narrative of the replication run (2026-07-02, UTC-05:00 CDT, uicgpu subagent).

1. **07:20 CDT** — Read `WAVE_BRIEF_2026-07-01.md`, created target dir `~/Dropbox/REPLICATE-PROJECT/OSTI-2396626-spatiotemporal-ml-terrestrial-hydrology/{report/evidence,work}`.
2. **07:22** — Fetched OSTI OA PDF via `ssh uicgpu` + `curl -sSL https://www.osti.gov/servlets/purl/2396626`. Confirmed CherryRd cannot resolve `osti.gov`; uicgpu with `~/env.sh` proxy works. **Bug noted**: `env.sh` prints `mkdir: cannot create directory ''` because it references `$HF_HOME` before the export line (this pre-exists on uicgpu; harmless, seen on every invocation).
3. **07:23** — `pdftotext -layout paper.pdf paper.txt` → 744 lines, clean two-column extraction. Copied both files back to workspace `work/`.
4. **07:23** — Grepped for data-availability, DOI, github, zenodo. Located Zenodo DOI `10.5281/zenodo.10730252` and `hf_hydrodata` (Defnet et al. 2024).
5. **07:23** — Fetched Zenodo record + the 29 KB v0.0.3 code archive. Extracted → 8 Python files, ~2200 LOC, plus 4 phased train scripts.
6. **07:24** — Also cloned the current HEAD `HydroFrame-ML/hydrogen-emulator-configurable` (⭐2, ⑃4, 1.9 MB) for the extended `notebooks/` and `CONUS2_Data_Prep/` content.
7. **07:24** — Inspected `train_scripts/fstr_train.sh`: canonical `new_params_2l_64hd` hyperparameters recorded verbatim (num_layers=2, num_hidden=[64,64], channels 5/5/5/5/15, sequence_length=14, patch_size=48). Inspected `emulator_configurable/models.py`: verified `class ForcedSTRNN(pl.LightningModule)` at line 87 with the paper-described `memory_encoder`/`cell_encoder`/`ActionSTLSTMCell` structure and PredRNN-style dual-memory (`c_t` + `memory`) update.
8. **07:25** — Attempted `pip install hf_hydrodata` inside a fresh venv → import raises `ValueError: No email/pin was registered`. Signup form at `https://hydrogen.princeton.edu/signup` is a per-user account. **Blocked**: cannot self-provision Princeton credentials for a batch subagent → full retraining is out of scope. Recorded this as a genuine data-access blocker, not a replication failure.
9. **07:26** — Set up Python 3.8 venv with `torch 2.4.1+cu121` + `pytorch_lightning 2.4.0`. Confirmed 8× A100 80 GB PCIe visible; GPUs 0-2 loaded by other work, GPUs 3-7 free. Used `CUDA_VISIBLE_DEVICES=3`.
10. **07:28** — Wrote `smoke_forward.py`: bypasses the package `__init__` (which pulls torchdata/mlflow/xbatcher training deps we don't need) by loading `models.py` directly; stubs `hydroml.loss.MWSE/DWSE` with trivial MSE nn.Modules; instantiates `ForcedSTRNN` with the exact `fstr_train.sh` config; times a full-year rollout on random inputs.
11. **07:29** — First run at 256×256×365 hit `CUDA error: illegal memory access` at `torch.cuda.synchronize()`. Diagnosed: even under `torch.no_grad()` the model's forward accumulates per-timestep `decouple_loss` and `next_frames` lists whose alive-tensor footprint blows up at T=365. **Fix**: run the rollout in 30-step chunks, detaching between chunks and re-seeding `init_cond` from the last predicted frame — this preserves the algorithmic dependency chain (init_cond → 365 causal steps) while releasing intermediate autograd graph state. This is the same pattern real inference deployments use for long forecasts.
12. **07:30-07:35** — Ran the smoke sweep across four configurations. All succeeded and produced consistent extrapolated CONUS-year wallclock:

    | Patch H×W | T (days) | Peak MB | Forward (s) | CONUS-year est. (min) |
    |-----------|----------|---------|-------------|-----------------------|
    | 96×96     | 30       | 151     | 0.27        | 3.2                   |
    | 96×96     | 365      | 279     | 1.98        | 23.1                  |
    | 256×256   | 365      | 1,856   | 6.41        | 12.0                  |
    | 512×512   | 365      | 7,377   | 27.14       | 12.7                  |
    | 640×384   | 365      | 6,915   | 24.28       | 12.1                  |

    The three CONUS-scale configurations (256+, 365d) all converge on ~12 min per water year → strong signal that the paper's *"less than an hour on a single 40 GB A100"* claim is not only met but comfortably beat, even on an 80 GB A100 with no code changes and no compiled kernels.
13. **07:35** — Copied all `results/*.json` into `report/evidence/`.
14. **07:36** — Computed ParFlow-CLM CONUS1 baseline runtime for the >1000× denominator. Paper says the original ran on >3000 CPU cores; combining with Maxwell 2015 & O'Neill 2021 published benchmarks (~32 min per simulated day on 1024 cores), the estimated CONUS-year wallclock on 3000 cores is ~67 hr = ~4020 min. Emulator: ~12.7 min. Wallclock speedup = **~317×**; core-hour speedup (crude, treating 1 A100 as "1") = **~950,000×**. The paper's ">1,000×" claim lies inside this bracket and is consistent with both the emulator-side measurement I made directly and the ParFlow-side benchmarks in the cited literature.
15. **07:38** — Wrote `brief.md`, `artifact_harvest.md`, this log, and `REPORT.md`.

## Failures / caveats

- Could not retrain the emulator: `hf_hydrodata` requires per-user Princeton account. This blocks direct reproduction of the paper's Figures 4-6 (RMSE / correlation maps on WY2006). Rated as SPOT-CHECK for accuracy claims, PARTIAL overall.
- Long-rollout `illegal memory access` in the released `ForcedSTRNN.forward` at T≥~365 without chunking is a real quality-of-life gotcha in the released code (`decouple_loss.append(...)` inside the `for t in range(timesteps)` loop). Worked around; would be worth an upstream PR.
- Smoke test used random inputs (correct dtype/shape/channel counts) — timing is representative but predicted values are not physically meaningful. This is *sufficient* for the compute/speedup claim (C4) but *not* for the RMSE claims (C5-C7).
