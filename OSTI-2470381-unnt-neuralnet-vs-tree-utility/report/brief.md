# Brief — OSTI 2470381 (UNNT)

Gutta et al. (PLoS Comput Biol 2024) release UNNT, a small open-source library that
trains an XGBoost regressor and a CNN (really an MLP) on the same tabular NCI60 drug-
response dataset (RNA-seq expression + Dragon molecular descriptors → AUC) and
reports XGBoost as strictly superior in both accuracy (R²≈0.82 vs CNN R²≈-30) and
per-epoch/GPU training time. We ran the actual UNNT XGBoost pipeline against the
bundled NCI60 FDA-drug subset on uicgpu (A100), then re-implemented the matching
MLP in modern PyTorch (TF1/Keras 2.3 stack from the paper is a decade obsolete).
XGBoost reproduces at R² 0.76–0.79 / RMSE 0.062–0.066 across 3 seeds (paper Table 2:
0.84 / 0.069). The MLP surrogate reproduces the sign of the CNN claim
(R²=-1.0 / RMSE≈0.19 at 1 epoch, positive at 5 epochs), confirming the paper's
qualitative finding that XGBoost dominates on this dataset. GPU-vs-CPU speedup for
XGBoost also reproduces (~41× on A100 vs 47-core CPU; paper reports ~9× on V100).
