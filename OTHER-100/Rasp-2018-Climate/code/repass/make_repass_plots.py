#!/usr/bin/env python
"""Generate figures for the re-pass report."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
import json

OUT = Path("/Users/stevens/Dropbox/REPLICATE-PROJECT/Rasp-2018-Climate/results/repass")
FIGS = Path("/Users/stevens/Dropbox/REPLICATE-PROJECT/Rasp-2018-Climate/figs")
FIGS.mkdir(exist_ok=True, parents=True)

d = np.load(OUT / "climatology_profiles.npz")
lat = d["lat"]; ch_t = d["ch_truth"]; ch_n = d["ch_nn"]; cm_t = d["cm_truth"]; cm_n = d["cm_nn"]

# Figure: zonal-mean column heating, NN vs truth
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
ax = axes[0]
ax.plot(lat, ch_t, "k-", lw=2, label="SPCAM truth")
ax.plot(lat, ch_n, "r--", lw=2, label="NN diagnostic")
ax.axvline(5.0, color="b", lw=0.7, ls=":", label="paper ITCZ ~5°N")
ax.set_xlabel("Latitude (°N)"); ax.set_ylabel("Col. heating Q (W/m²)")
ax.set_title("C10/C12: zonal-mean column heating\n(NN vs SPCAM truth, 48-snapshot sample)")
ax.legend(loc="upper left", fontsize=8); ax.grid(alpha=0.3); ax.set_xlim(-90,90)

ax = axes[1]
ax.plot(lat, cm_t, "k-", lw=2, label="SPCAM truth (Lv * col-moistening)")
ax.plot(lat, cm_n, "r--", lw=2, label="NN diagnostic")
ax.axvline(5.0, color="b", lw=0.7, ls=":")
ax.set_xlabel("Latitude (°N)"); ax.set_ylabel("Lv × col. moistening (W/m²)")
ax.set_title("C11: zonal-mean column latent heating")
ax.legend(loc="lower right", fontsize=8); ax.grid(alpha=0.3); ax.set_xlim(-90,90)

plt.tight_layout()
plt.savefig(FIGS / "repass_climatology.png", dpi=130, bbox_inches="tight")
plt.close()
print(f"wrote {FIGS / 'repass_climatology.png'}")

# (energy-balance scatter generated on uicgpu; see code/repass/make_scatter_uic.py)

# Figure: val-loss curve C5
with open(OUT / "C5_18_epoch.json") as f:
    c5 = json.load(f)
if c5.get("epochs"):
    ep = [e["epoch"] for e in c5["epochs"]]
    val = [e["val_loss"] for e in c5["epochs"]]
    tr = [e.get("train_loss") for e in c5["epochs"]]
    fig, ax = plt.subplots(figsize=(6,4))
    if all(t is not None for t in tr):
        ax.plot(ep, tr, "C0-", label="train")
    ax.plot(ep, val, "C3-", lw=2, label="val")
    ax.axvline(18, color="b", lw=1, ls=":", label="paper epoch=18")
    ax.set_xlabel("epoch"); ax.set_ylabel("normalized MSE loss")
    ax.set_title("C5: 18-epoch sufficiency (PASS-1 9×256 control)")
    ax.grid(alpha=0.3); ax.legend()
    plt.tight_layout()
    plt.savefig(FIGS / "repass_C5_loss_curve.png", dpi=130, bbox_inches="tight")
    plt.close()
    print(f"wrote {FIGS / 'repass_C5_loss_curve.png'}")
