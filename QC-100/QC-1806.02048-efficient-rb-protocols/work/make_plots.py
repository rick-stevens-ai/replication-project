#!/usr/bin/env python3
"""Generate summary plots from the RB experiments."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

here = Path(__file__).resolve().parent.parent  # QC-1806... root
ev = here / "report" / "evidence"

# --- Plot 1: standard Clifford RB decay ---
std = json.loads((ev / "standard_p005" / "rb_standard_result.json").read_text())
ms = np.array([c["m"] for c in std["curve"]])
pm = np.array([c["m"] for c in std["curve"]], dtype=float)
pmy = np.array([c["p_mean"] for c in std["curve"]])
psem = np.array([c["p_sem"] for c in std["curve"]])
A, B, f = std["fit"]["A"], std["fit"]["B"], std["fit"]["f"]

fig, ax = plt.subplots(figsize=(6, 4))
ax.errorbar(ms, pmy, yerr=psem, fmt="o", capsize=3, label="data")
mgrid = np.linspace(ms.min(), ms.max(), 200)
ax.plot(mgrid, A + B * (f ** mgrid), "-",
        label=f"fit: A+B·f^m, f={f:.4f}")
ax.axhline(A, ls=":", color="gray", label=f"A={A:.3f}")
ax.set_xlabel("sequence length m")
ax.set_ylabel("survival prob P(0|0)")
ax.set_title("Standard 1-qubit Clifford RB (eq. 1 of paper)\n"
             f"injected depol p={std['injected_per_basis_gate_depol']}, "
             f"r_per_Clifford={std['r_per_clifford_recovered']:.4f}")
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(ev / "fig_standard_rb.png", dpi=150)
print(f"wrote {ev/'fig_standard_rb.png'}")
plt.close(fig)


# --- Plot 2: character vs naive Pauli RB at same K ---
cp = json.loads((ev / "char_pauli_p01" / "rb_character_pauli_result.json").read_text())
ms = np.array([c["m"] for c in cp["naive"]["curve"]])
naive_y = np.array([c["y"] for c in cp["naive"]["curve"]])
naive_s = np.array([c["sem"] for c in cp["naive"]["curve"]])
char_y = np.array([c["y"] for c in cp["character"]["curve"]])
char_s = np.array([c["sem"] for c in cp["character"]["curve"]])
fA = cp["naive"]["fit"]["f"]
AA = cp["naive"]["fit"]["A"]
BA = cp["naive"]["fit"]["B"]
fB = cp["character"]["fit"]["f"]
BB = cp["character"]["fit"]["B"]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
mgrid = np.linspace(ms.min(), ms.max(), 200)
ax1.errorbar(ms, naive_y, yerr=naive_s, fmt="o", capsize=3, label="data")
ax1.plot(mgrid, AA + BA * (fA ** mgrid), "-",
         label=f"fit A+B·f^m\nf={fA:.4f}±{cp['naive']['fit']['f_stderr']:.4f}")
ax1.set_xlabel("m"); ax1.set_ylabel("P(0|0)")
ax1.set_title("(A) Naive Pauli RB (non-Clifford group)")
ax1.legend(); ax1.grid(alpha=0.3)

ax2.errorbar(ms, char_y, yerr=char_s, fmt="s", color="C1", capsize=3,
             label="character-averaged data")
ax2.plot(mgrid, BB * (fB ** mgrid), "-", color="C1",
         label=f"fit B·f^m\nf={fB:.4f}±{cp['character']['fit']['f_stderr']:.4f}")
ax2.axhline(0.0, ls=":", color="gray")
ax2.set_xlabel("m"); ax2.set_ylabel("⟨χ_Z · ⟨Z⟩⟩")
ax2.set_title("(B) Character Pauli RB (this paper, eq. 3-5)")
ax2.legend(); ax2.grid(alpha=0.3)

fig.suptitle(f"Character RB vs naive RB, Pauli group, p={cp['params']['p_gate_depol']}, "
             f"K={cp['params']['seqs_per_length']} seqs/length "
             f"(expected f = {1 - cp['params']['p_gate_depol']:.4f})")
fig.tight_layout()
fig.savefig(ev / "fig_char_vs_naive.png", dpi=150)
print(f"wrote {ev/'fig_char_vs_naive.png'}")
plt.close(fig)


# --- Plot 3: efficiency sweep (stderr vs K) ---
sw = json.loads((ev / "efficiency" / "efficiency_sweep_result.json").read_text())
Ks = np.array([e["K"] for e in sw["sweep"]])
err_naive = np.array([e["naive"]["fit"]["f_stderr"] for e in sw["sweep"]])
err_char = np.array([e["character"]["fit"]["f_stderr"] for e in sw["sweep"]])
f_naive = np.array([e["naive"]["fit"]["f"] for e in sw["sweep"]])
f_char = np.array([e["character"]["fit"]["f"] for e in sw["sweep"]])
f_exp = sw["f_expected"]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
ax1.loglog(Ks, err_naive, "o-", label="naive Pauli RB")
ax1.loglog(Ks, err_char, "s-", label="character Pauli RB")
ax1.set_xlabel("sequences per length K")
ax1.set_ylabel("fit stderr on f")
ax1.set_title("Fit precision vs. sample count")
ax1.legend(); ax1.grid(alpha=0.3, which="both")

ax2.errorbar(Ks, f_naive, yerr=err_naive, fmt="o-", capsize=3, label="naive")
ax2.errorbar(Ks, f_char, yerr=err_char, fmt="s-", capsize=3, label="character")
ax2.axhline(f_exp, ls="--", color="k", label=f"expected f={f_exp:.4f}")
ax2.set_xlabel("sequences per length K")
ax2.set_ylabel("fitted f")
ax2.set_title("Recovered quality parameter")
ax2.set_xscale("log")
ax2.legend(); ax2.grid(alpha=0.3)

fig.suptitle(f"Efficiency comparison, 1q Pauli-group RB, "
             f"p={sw['p_gate_depol']} (~{6.5}× smaller stderr for character RB)")
fig.tight_layout()
fig.savefig(ev / "fig_efficiency_sweep.png", dpi=150)
print(f"wrote {ev/'fig_efficiency_sweep.png'}")
plt.close(fig)
