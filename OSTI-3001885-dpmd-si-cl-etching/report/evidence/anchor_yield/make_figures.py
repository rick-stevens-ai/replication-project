#!/usr/bin/env python3
"""Plot Cl/Ar+ Si-yield: paper DeepMD vs Chang 1997 exp vs Sigmund fits."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

E_ClAr    = np.array([35.0, 60.0, 100.0])
Y_DP      = np.array([1.32, 2.01, 2.49]); dY_DP = np.array([0.05,0.06,0.05])
Y_REBO    = np.array([0.7, 1.1, 1.5]);    dY_R  = np.array([0.1,0.1,0.3])
Y_Chang   = np.array([0.3, 1.3, 2.4])

def sigmund(E,A,Eth):
    return np.where(E>Eth, A*(np.sqrt(E)-np.sqrt(max(Eth,0))), 0)

Egrid = np.linspace(10, 120, 400)
# fits from yield_analysis.py
A_dp, Eth_dp   = 0.24634700, -2.3130         # nonphysical, forced
A_ex, Eth_ex   = 0.51321426, 27.9772
A_rb, Eth_rb   = 0.20726949,  6.2664

fig, ax = plt.subplots(figsize=(7,5))
ax.errorbar(E_ClAr, Y_DP,   yerr=dY_DP, fmt='o', color='C0', ms=8, capsize=4, label='Paper DeepMD (This work)')
ax.errorbar(E_ClAr, Y_REBO, yerr=dY_R,  fmt='s', color='C2', ms=8, capsize=4, label='Vella REBO')
ax.plot(    E_ClAr, Y_Chang, '^', color='C3', ms=10, label='Chang 1997 (exp.)')

ax.plot(Egrid, np.maximum(sigmund(Egrid, A_dp, Eth_dp), 0), '-',  color='C0', lw=1.3, alpha=0.7, label=f'Sigmund fit DP (Eth={Eth_dp:.1f} eV, A={A_dp:.2f})')
ax.plot(Egrid, np.maximum(sigmund(Egrid, A_ex, Eth_ex), 0), '--', color='C3', lw=1.5, label=f'Sigmund fit Chang exp (Eth={Eth_ex:.1f} eV, A={A_ex:.2f}, R²=0.999)')
ax.plot(Egrid, np.maximum(sigmund(Egrid, A_rb, Eth_rb), 0), ':',  color='C2', lw=1.2, alpha=0.8, label=f'Sigmund fit REBO Vella (Eth={Eth_rb:.1f} eV)')

# expected physical Eth from Si cohesion 2-4x
ax.axvspan(9.26, 18.52, alpha=0.10, color='gray', label='Physical Eth window (2-4×Si cohesion)')

ax.set_xlabel("Ar$^+$ ion energy (eV)")
ax.set_ylabel("Si etch yield (Si atoms per Ar$^+$)")
ax.set_title("Cl / Ar$^+$ Si etching, neutral:ion=100  —  OSTI-3001885 Table I vs Chang 1997")
ax.set_xlim(0, 120); ax.set_ylim(0, 3.2)
ax.legend(fontsize=8, loc='upper left')
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig("ClAr_yield_comparison.png", dpi=140)
print("wrote ClAr_yield_comparison.png")

# Second figure: Cl+ only vs REBO Brichon
E_Clp    = np.array([5.0, 10.0, 25.0, 50.0, 100.0])
Y_ClpDP  = np.array([0.09, 0.16, 0.19, 0.26, 0.42])
dY_ClpDP = np.array([0.02, 0.02, 0.03, 0.01, 0.04])
Y_ClpREBO= np.array([0.03, 0.10, 0.25, 0.35, 0.45])

fig2, ax2 = plt.subplots(figsize=(7,5))
ax2.errorbar(E_Clp, Y_ClpDP,   yerr=dY_ClpDP, fmt='o', color='C0', ms=8, capsize=4, label='Paper DeepMD (This work)')
ax2.plot(    E_Clp, Y_ClpREBO, 's-', color='C2', ms=8, label='Brichon 2015 REBO')
ax2.set_xlabel("Cl$^+$ ion energy (eV)")
ax2.set_ylabel("Si etch yield (Si atoms per Cl$^+$)")
ax2.set_title("Cl$^+$-only Si etching  —  OSTI-3001885 Table I vs Brichon 2015 REBO")
ax2.set_xlim(0,120); ax2.set_ylim(0,0.6)
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3)
fig2.tight_layout()
fig2.savefig("Clp_yield_comparison.png", dpi=140)
print("wrote Clp_yield_comparison.png")
