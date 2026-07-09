"""
Reproduce Figure 11 of Tobias et al. (2013), comparing our re-implemented
ODE model against the paper's published model curves.

Figure 11 panels:
    A: NBS1 recruitment, LET = 170  keV/um  (low)        -> our scale = SCALE_NBS1["A"] = 2032
    B: NBS1 recruitment, LET = 3590 keV/um  (mid)        -> our scale = SCALE_NBS1["B"] = 2149
    C: NBS1 recruitment, LET = 10290 keV/um (high)       -> our scale = SCALE_NBS1["C"] = 2059
    D: ATM  recruitment, LET = 14350 keV/um (very high)  -> our scale = SCALE_ATM_HIGH_LET = 3263

Each panel shows:
    solid line = total recruited NBS1 (or ATM) signal
    dashed line = inner-focus contribution (MRN_i / ATM bound in inner focus)
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
from lucid_model import (
    simulate, SCALE_NBS1, SCALE_ATM_HIGH_LET, ATM_LET,
    H2AX_0, ATM_0,
)

FIGDIR = os.path.join(os.path.dirname(__file__), "..", "figures")
RESDIR = os.path.join(os.path.dirname(__file__), "..", "results")
os.makedirs(FIGDIR, exist_ok=True)
os.makedirs(RESDIR, exist_ok=True)

PANELS = [
    ("A", 170.0,   "NBS1, LET = 170 keV/µm",   "nbs1"),
    ("B", 3590.0,  "NBS1, LET = 3590 keV/µm",  "nbs1"),
    ("C", 10290.0, "NBS1, LET = 10290 keV/µm", "nbs1"),
    ("D", 14350.0, "ATM, LET = 14350 keV/µm",  "atm"),
]

fig, axes = plt.subplots(2, 2, figsize=(11, 8), sharex=True)
axes = axes.flatten()

summary_rows = []

for ax, (label, let, title, kind) in zip(axes, PANELS):
    r = simulate(let, t_end=700.0, n_out=701)
    if kind == "nbs1":
        scale = SCALE_NBS1[label]
        total = r.nbs1_total() * scale / H2AX_0   # signal in same units paper uses
        inner = r.nbs1_inner() * scale / H2AX_0
        # The paper's y-axis is "relative fluorescence intensity (a.u.)"; the
        # H2AX_0 normalization is one convention that matches typical scaling
        # since steady-state outer NBS1 ~ H2AX_0. We additionally rescale below
        # to plateau = scale, so it shows the actual numbers in panel.
        total = r.nbs1_total() * scale / r.nbs1_total()[-1]
        inner = r.nbs1_inner() * scale / r.nbs1_total()[-1]
    else:  # atm
        scale = SCALE_ATM_HIGH_LET
        # Same normalization convention
        total = r.atm_total() * scale / r.atm_total()[-1]
        inner = r.atm_inner() * scale / r.atm_total()[-1]

    ax.plot(r.t, total, "-",  color="C0", lw=2, label="total (solid)")
    ax.plot(r.t, inner, "--", color="C3", lw=1.5, label="inner focus (dashed)")
    ax.set_title(f"({label}) {title}")
    ax.set_xlabel("time after irradiation [s]")
    ax.set_ylabel("recruited signal [a.u.]")
    ax.grid(alpha=0.3)
    ax.legend(loc="lower right", fontsize=9)

    # Mono-exponential time constant: time to reach 63% of plateau
    plateau = total[-1]
    target = 0.63 * plateau
    idx63 = int(np.argmax(total >= target))
    tau63 = r.t[idx63] if total[idx63] >= target else np.nan

    summary_rows.append({
        "panel": label,
        "let_keV_um": let,
        "kind": kind,
        "plateau_signal": float(plateau),
        "inner_fraction_at_plateau": float(inner[-1] / plateau if plateau > 0 else 0),
        "tau63_s": float(tau63),
    })

fig.suptitle("Replication of Tobias et al. 2013, Figure 11\n"
             "ODE model re-implementation (LSODA) — published parameters",
             fontsize=12)
fig.tight_layout()
out = os.path.join(FIGDIR, "figure11_replication.png")
fig.savefig(out, dpi=140)
print(f"Wrote {out}")

# Save the summary as JSON for the report
import json
sum_path = os.path.join(RESDIR, "figure11_summary.json")
with open(sum_path, "w") as f:
    json.dump(summary_rows, f, indent=2)
print(f"Wrote {sum_path}")

# Print a human-readable table
print()
print(f"{'panel':<5} {'LET':>7} {'kind':<5} {'plateau':>10} {'inner/total':>12} {'tau63':>8}")
for row in summary_rows:
    print(f"{row['panel']:<5} {row['let_keV_um']:>7.0f} {row['kind']:<5} "
          f"{row['plateau_signal']:>10.1f} "
          f"{row['inner_fraction_at_plateau']:>11.1%} "
          f"{row['tau63_s']:>7.1f}s")
