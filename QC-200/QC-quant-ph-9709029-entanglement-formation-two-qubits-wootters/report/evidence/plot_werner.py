#!/usr/bin/env python3
"""Plot Werner-state concurrence and entanglement of formation vs mixing parameter p."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

with open("report/evidence/results.json") as f:
    r = json.load(f)

ps = [d["p"] for d in r["werner_sweep"]]
Cs = [d["C"] for d in r["werner_sweep"]]
Es = [d["E"] for d in r["werner_sweep"]]
Cs_ana = [d["C_analytic"] for d in r["werner_sweep"]]

fig, ax = plt.subplots(1, 2, figsize=(10, 4))
ax[0].plot(ps, Cs, "o-", label="Wootters (numerical)")
ax[0].plot(ps, Cs_ana, "k--", lw=1, label="Analytic max(0,(3p-1)/2)")
ax[0].axvline(1/3, color="red", ls=":", label="Separability p=1/3")
ax[0].set_xlabel("p")
ax[0].set_ylabel("Concurrence C")
ax[0].set_title("Werner state: concurrence vs p")
ax[0].legend(); ax[0].grid(alpha=0.3)

ax[1].plot(ps, Es, "s-", color="tab:green")
ax[1].axvline(1/3, color="red", ls=":", label="Separability p=1/3")
ax[1].set_xlabel("p")
ax[1].set_ylabel("Entanglement of formation E")
ax[1].set_title("Werner state: E of formation vs p")
ax[1].legend(); ax[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig("report/evidence/werner_sweep.png", dpi=140)
print("Saved report/evidence/werner_sweep.png")

# Also plot C vs E for random states
Cs2 = []
Es2 = []
from numpy.random import default_rng
import sys; sys.path.insert(0, "report/evidence")
from wootters_concurrence import random_2qubit_mixed, concurrence, entanglement_of_formation
rng = default_rng(20260705)
N = 1000
for _ in range(N):
    rho = random_2qubit_mixed(rng)
    Cs2.append(concurrence(rho))
    Es2.append(entanglement_of_formation(rho))

fig2, ax2 = plt.subplots(figsize=(5.5, 4.5))
ax2.scatter(Cs2, Es2, s=6, alpha=0.5, label="1000 random mixed states")
Cline = np.linspace(0, 1, 200)
xline = 0.5 * (1 + np.sqrt(1 - Cline**2))
Eline = np.where((xline > 0) & (xline < 1),
                 -xline*np.log2(np.clip(xline,1e-30,1)) - (1-xline)*np.log2(np.clip(1-xline,1e-30,1)),
                 0.0)
ax2.plot(Cline, Eline, "r-", lw=2, label="Wootters E(C) curve")
ax2.set_xlabel("Concurrence C"); ax2.set_ylabel("Entanglement of formation E")
ax2.set_title("Random 2-qubit mixed states: E vs C")
ax2.legend(); ax2.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("report/evidence/random_states_E_vs_C.png", dpi=140)
print("Saved report/evidence/random_states_E_vs_C.png")
