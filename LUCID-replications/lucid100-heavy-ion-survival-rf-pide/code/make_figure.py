#!/usr/bin/env python3
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

r = json.load(open("../results/pipeline_results.json"))
rep = r["reproduced"]; pap = r["paper_targets"]
models = ["LQM", "LocReg", "RF"]

fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
x = np.arange(len(models)); w = 0.35

# R2
ax[0].bar(x - w/2, [pap[m]["R2"] for m in models], w, label="Paper", color="#4477aa")
ax[0].bar(x + w/2, [rep[m]["R2_mean"] for m in models], w, label="Reproduced",
          color="#ee6677", yerr=[rep[m]["R2_std"] for m in models], capsize=4)
ax[0].set_xticks(x); ax[0].set_xticklabels(models)
ax[0].set_ylabel("R² (mean over 100 MC-CV splits)")
ax[0].set_title("R²: dose-only (LQM, LocReg) vs dose+LET (RF)")
ax[0].set_ylim(0.75, 1.0); ax[0].legend(); ax[0].grid(axis="y", alpha=0.3)

# RMSE
ax[1].bar(x - w/2, [pap[m]["RMSE"] for m in models], w, label="Paper", color="#4477aa")
ax[1].bar(x + w/2, [rep[m]["RMSE_mean"] for m in models], w, label="Reproduced",
          color="#ee6677", yerr=[rep[m]["RMSE_std"] for m in models], capsize=4)
ax[1].set_xticks(x); ax[1].set_xticklabels(models)
ax[1].set_ylabel("RMSE (surviving fraction)")
ax[1].set_title("RMSE")
ax[1].legend(); ax[1].grid(axis="y", alpha=0.3)

fig.suptitle("Debreceni et al. 2024 (Toxics 12:545) — NB1RGB heavy-ion survival\n"
             "Structural replication (reconstructed dataset; PIDE email-gated)",
             fontsize=11)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig("../figures/model_comparison.png", dpi=130)
print("wrote ../figures/model_comparison.png")
