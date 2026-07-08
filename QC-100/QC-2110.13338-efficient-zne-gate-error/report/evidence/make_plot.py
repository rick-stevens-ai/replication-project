#!/usr/bin/env python3
"""Plot: reproduces the shape of Fig 2 from arXiv:2110.13338."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
data = json.loads((HERE / "results.json").read_text())
recs = data["records"]

nc = [r["num_cnots"] for r in recs]
raw = [r["raw_shots"] for r in recs]
raw_exact = [r["raw_exact"] for r in recs]
full = [r["zne_full"] for r in recs]
eff = [r["zne_eff"] for r in recs]

fig, ax = plt.subplots(figsize=(6, 4.2))
ax.axhline(1.0, color="k", ls=":", alpha=0.5, label="Noiseless truth (=1.0)")
ax.plot(nc, raw_exact, "s-", color="#888888", label="Raw (exact noisy)", ms=5)
ax.plot(nc, raw, "o", color="#000000", label=f"Raw (shots={data['config']['shots']})", ms=5)
ax.plot(nc, full, "^-", color="#c00000",
        label=f"Full ZNE  (3 scales, global fold, {data['records'][0]['shots_full']} shots/pt)")
ax.plot(nc, eff, "d-", color="#0060c0",
        label=f"Efficient ZNE (2 scales, random fold, {data['records'][0]['shots_eff']} shots/pt)")
ax.set_xlabel("Number of CNOT gates")
ax.set_ylabel(r"Pr(measure $|11\rangle$)")
ax.set_title(r"arXiv:2110.13338 Fig 2 replication ($\varepsilon=1\%$, $T_1=50\,\mu s$, $T_{CNOT}=200\,ns$)")
ax.set_ylim(0.4, 1.15)
ax.legend(fontsize=8, loc="lower left")
ax.grid(True, alpha=0.3)
plt.tight_layout()
out = HERE / "fig2_replication.png"
plt.savefig(out, dpi=140)
print(f"Wrote {out}")
