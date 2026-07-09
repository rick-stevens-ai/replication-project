"""
Overlay digitized data points on the re-implemented model curves for the
three panels we have read off from Figure S1 (A, F, L). This gives a visual
check of agreement.
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
from lucid_model import simulate, SCALE_NBS1

FIGDIR = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(FIGDIR, exist_ok=True)

# Panels and our best LET assignments (from scale-factor matching to the model)
PANELS = [
    ("A", 170.0,   "low LET (170 keV/µm, ~C-ions)"),
    ("F", 237.0,   "low LET replicate (scale-implied ~237 keV/µm)"),
    ("L", 10290.0, "high LET (10290 keV/µm, ~Au-ions)"),
]

# Digitized read-offs (t in s, signal in a.u.)
DIGITIZED = {
    "A": dict(plateau=2000.0, t100=475.0,  t300=1650.0, t_half=140.0),
    "F": dict(plateau=2800.0, t100=1300.0, t300=2450.0, t_half=100.0),
    "L": dict(plateau=4450.0, t100=2900.0, t300=4250.0, t_half=50.0),
}

fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), sharey=False)

for ax, (label, let, desc) in zip(axes, PANELS):
    r = simulate(let, t_end=700.0, n_out=701)
    scale = SCALE_NBS1[label]
    raw = r.nbs1_total()
    plateau_model = raw[-1] if raw[-1] > 0 else 1.0
    sig = raw * (scale / plateau_model)

    ax.plot(r.t, sig, "-", color="C0", lw=2, label="this work (ODE model)")

    d = DIGITIZED[label]
    ts = np.array([100.0, 300.0, 700.0])
    vs = np.array([d["t100"], d["t300"], d["plateau"]])
    ax.errorbar(ts, vs, yerr=vs * 0.08, fmt="o", color="C3", capsize=4,
                label="digitized data points\n(from Figure S1)")
    # also mark t_half
    ax.axhline(d["plateau"] * 0.5, color="gray", ls=":", lw=0.8)
    ax.axvline(d["t_half"], color="C3", ls=":", lw=0.8,
               label=f"data t½ ≈ {d['t_half']:.0f}s")

    ax.set_title(f"Panel {label}: {desc}")
    ax.set_xlabel("time after irradiation [s]")
    ax.set_ylabel("recruited NBS1 signal [a.u.]")
    ax.set_xlim(0, 700)
    ax.grid(alpha=0.3)
    ax.legend(loc="lower right", fontsize=8)

fig.suptitle("Replicated model vs digitized Figure-S1 data points\n"
             "(Tobias et al., PLOS ONE 2013)", fontsize=11)
fig.tight_layout()
out = os.path.join(FIGDIR, "data_overlay.png")
fig.savefig(out, dpi=140)
print(f"Wrote {out}")
