# CAMELS Multifield Replication - Progress Log

**Paper:** Villaescusa-Navarro et al. 2022, ApJS 259, 61  
**DOI:** 10.3847/1538-4365/ac5ab0  
**Started:** 2026-05-26 15:49 CDT  

## Phase 1: Setup (COMPLETE - ~25 min)
- Read paper abstract and explored data/code URLs
- Found inference scripts at: https://users.flatironinstitute.org/~fvillaescusa/priv/DEPnzxoWlaTQ6CjrXqsm0vYi8L7Jy/CMD/2D_maps/inference/scripts/
  - architecture.py (122.8KB) - all CNN architectures
  - train.py (12.94KB) - training loop (uses Optuna for HPO)
  - data.py (34.76KB) - data loading with normalization
  - test.py (10.16KB) - evaluation
- Key architecture: `model_e3_err` (6-layer CNN with circular padding + moment network)
- Key loss: `log(MSE_mean) + log(MSE_variance)` — moment network loss
- Data URL discovered: Maps_Mgas_IllustrisTNG_LH_z=0.00.npy (3.932 GB)
- Params URL: params_LH_IllustrisTNG.txt (1000 sims × 6 params)

## Phase 2: Implementation (COMPLETE - ~30 min)
- Created `code/camels_cnn.py` — self-contained CNN implementation
- Created `code/camels_cnn_v2.py` — improved version (hidden=12, ReduceLROnPlateau)
- Architecture: model_e3_err, 2.138M params (v1 hidden=8), 4.803M params (v2 hidden=12)
- Data pipeline: log10 transform → z-score normalize, split by simulation (critical)
- Data augmentation: random rotations (0/90/180/270) + horizontal flip
- Environment: conda venv at /data/stevens/CAMELS/.venv, Python 3.11, PyTorch 2.5.1+cu121

## Phase 3: Training (COMPLETE)
### Run v1 (hidden=8, 50 epochs, cosine LR):
- GPU: A100 80GB PCIe
- Wall time: 0.072 hours (~4.3 minutes)
- Test: Omega_m = 8.30% rel_err, R² = 0.919
- Test: sigma_8 = 7.17% rel_err, R² = 0.620
- Issue: cosine LR oscillation → noisy validation

### Run v2 (hidden=12, 100 epochs, ReduceLROnPlateau):
- GPU: A100 80GB PCIe
- Wall time: 0.126 hours (~7.6 minutes)
- Test: **Omega_m = 4.59% rel_err, R² = 0.971** ← matches paper!
- Test: **sigma_8 = 5.07% rel_err, R² = 0.796** ← matches paper!
- Paper target: ~3-5% Omega_m, ~4-6% sigma_8 ✓

## Phase 4: Evaluation & Report (COMPLETE)
- Scatter plots saved: results/scatter_test_v2_final.png
- Training curves: results/training_curves_v2.png
- JSON results: results/test_results_v2.json
- REPORT.md written

## Data Files
- `/data/stevens/CAMELS/data/Maps_Mgas_IllustrisTNG_LH_z=0.00.npy` (3.932 GB)
- `/data/stevens/CAMELS/data/params_LH_IllustrisTNG.txt` (48 KB)
- Results synced to: `~/Dropbox/REPLICATE-PROJECT/CAMELS-Multifield-VillaescusaNavarro2022/results/`

## Status: **COMPLETE** ✓
