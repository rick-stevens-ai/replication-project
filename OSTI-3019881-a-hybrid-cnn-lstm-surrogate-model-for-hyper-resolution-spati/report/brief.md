# Brief — OSTI 3019881 replication

**What.** Wang et al. 2026 (J. Hydrol. Reg. Stud. 64:103234) build a hybrid DeepLabv3+ CNN + LSTM
surrogate that maps 8 past 15-min water-depth maps (plus DEM, TWI, rainfall, tide) to 4 future 15-min
water-depth maps at 2.5-m resolution over 12 flood-prone AOIs in Norfolk, VA, trained against TUFLOW
2D/1D hydrodynamic simulations. Headline: avg MAE 0.024 m, RMSE 0.044 m across the 12 AOIs, 4-6 h → 3.2 min
per-event runtime speedup vs TUFLOW.

**Why replicate.** OSTI OA, method+hyperparams explicitly specified, authors ship a HydroShare bundle
(`43244f815e7947e6bac6b6705a9f7941`) with paired input/output tensors from the exact TUFLOW runs.
Ideal candidate: real data, physics-based ground truth, single-A100 training, no proprietary code paths.

**What we did.** Downloaded the HydroShare zip (108 MB, md5 `9bb7a12f1ae2819c2f035bcb198c540c`) via
uicgpu, verified 300 paired samples across 2 events (Aug 29 2017, Sep 30 2022), reconstructed the
DeepLabv3+-encoder + LSTM head + upsample-decoder architecture from the paper (the zip ships tensors
only — no `.py`), and trained under the paper's hyperparameters (Adam lr=1e-4, MSE, batch=4, 200 max
epochs, patience=20, dropout=0.2, 80/20 split) on a single A100. 200 epochs in ~10 min.

**Verdict — PARTIAL.** Independent CNN-LSTM trained on the released data reaches MAE 0.0048 m /
RMSE 0.019 m on the held-out 20% split, and reproduces the paper's qualitative RMSE-vs-horizon growth
pattern (t+1..t+4 RMSE 0.019→0.020 m). Absolute numbers are *better* than the paper because the
released "Example Dataset" covers only 2 of the 12 AOIs and 2 events — within-event generalization is
easier than the paper's 12-AOI cross-scenario evaluation. Method is fully plausible and the released
tensors are real. Full 12-AOI cross-scenario replication is NOT achievable from the released bundle
alone.
