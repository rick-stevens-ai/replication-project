#!/usr/bin/env python3
"""Generate figures for the re-pass analyzable-claim results."""
import json
import os
import sys
from pathlib import Path
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import cantera as ct

HERE = Path(__file__).resolve().parent
RES = HERE.parent.parent / "results" / "repass"
RES.mkdir(parents=True, exist_ok=True)


def fig_z_mr():
    """Autoignition delay vs mixture fraction Z (paper §5.2 Z_mr ≈ 0.004)."""
    gas = ct.Solution("gri30.yaml")
    P_mix = 1e5
    T_ox = 2100.0
    T_fu = 456.0
    Z = np.linspace(0.0005, 0.05, 40)
    tau = np.full_like(Z, np.nan)
    Y_O2 = 0.233
    Y_N2 = 0.767
    for i, z in enumerate(Z):
        T_mix = (1 - z) * T_ox + z * T_fu
        Y = np.zeros(gas.n_species)
        Y[gas.species_index("CH4")] = z
        Y[gas.species_index("O2")] = (1 - z) * Y_O2
        Y[gas.species_index("N2")] = (1 - z) * Y_N2
        gas.TPY = T_mix, P_mix, Y
        r = ct.IdealGasConstPressureReactor(gas, clone=False)
        net = ct.ReactorNet([r])
        t = 0.0
        T0 = gas.T
        Ts = [T0]
        ts = [0.0]
        n = 0
        while t < 0.05 and n < 8000:
            try:
                t = net.step()
            except Exception:
                break
            Ts.append(r.T)
            ts.append(t)
            n += 1
        Ta = np.array(Ts)
        ta = np.array(ts)
        if len(Ta) > 3 and (Ta.max() - T0) > 50:
            dT = np.diff(Ta) / np.maximum(np.diff(ta), 1e-12)
            tau[i] = ta[int(np.argmax(dT)) + 1]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.semilogy(Z, tau * 1e6, "o-", color="C0", label="0-D ignition delay (GRI-3.0)")
    Z_mr_ours = Z[np.nanargmin(tau)]
    ax.axvline(Z_mr_ours, ls="--", color="C0",
               label=f"our Z_mr = {Z_mr_ours:.4f}")
    ax.axvline(0.004, ls="--", color="C3", label="paper Z_mr ≈ 0.004")
    ax.set_xlabel("Mixture fraction Z")
    ax.set_ylabel(r"Ignition delay $\tau_{ig}$ ($\mu$s)")
    ax.set_title("Most-reactive mixture fraction (CH4/air, T_ox=2100 K)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(RES / "fig_z_mr.png", dpi=120)
    plt.close(fig)
    print(f"[fig] wrote {RES / 'fig_z_mr.png'}")


def fig_T_ad_vs_pelec():
    """Bar plot: T_ad,HP vs T_ad,UV vs PeleC T_late_max and T_end per phi."""
    g = ct.Solution("gri30.yaml")
    phis = [0.6, 0.8, 1.0, 1.2]
    T_ad_HP = []
    T_ad_UV = []
    for phi in phis:
        g.TP = 456.0, 1e5
        g.set_equivalence_ratio(phi, "CH4", "O2:1, N2:3.76")
        g.equilibrate("HP")
        T_ad_HP.append(g.T)
        g.TP = 456.0, 1e5
        g.set_equivalence_ratio(phi, "CH4", "O2:1, N2:3.76")
        g.equilibrate("UV")
        T_ad_UV.append(g.T)
    # PeleC v6 from REPORT_v6
    T_late_max = [620, 2262, 3023, 3140]
    T_end = [456, 459, 2666, 2705]

    x = np.arange(len(phis))
    w = 0.2
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.bar(x - 1.5*w, T_ad_HP,    w, label="T_ad,HP (Cantera)", color="C0")
    ax.bar(x - 0.5*w, T_ad_UV,    w, label="T_ad,UV (Cantera)", color="C1")
    ax.bar(x + 0.5*w, T_late_max, w, label="PeleC v6 T_late_max", color="C2")
    ax.bar(x + 1.5*w, T_end,      w, label="PeleC v6 T_end",      color="C3")
    ax.set_xticks(x)
    ax.set_xticklabels([f"phi={p}" for p in phis])
    ax.set_ylabel("Temperature (K)")
    ax.set_title("Late-time PeleC T vs Cantera adiabatic flame T")
    ax.legend(loc="upper left")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(RES / "fig_T_ad_vs_pelec.png", dpi=120)
    plt.close(fig)
    print(f"[fig] wrote {RES / 'fig_T_ad_vs_pelec.png'}")


def fig_ip_curve():
    """Restate the IP-vs-phi curve including paper, v6 (uicgpu), and v5
    (polaris)."""
    phis = [0.6, 0.8, 1.0, 1.2]
    paper = [0.0, 0.20, 0.65, 0.90]
    v6 = [0.0, 0.0, 1.0, 1.0]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(phis, paper, "s-", color="k", label="paper Fig 7 (exp IP)")
    ax.plot(phis, v6, "o--", color="C2", label="PeleC v6 (uicgpu, N=1)")
    for x, py, ny in zip(phis, paper, v6):
        ax.annotate(f"|Δ|={abs(py-ny):.2f}", (x, max(py, ny) + 0.04),
                    fontsize=8, ha="center")
    L1 = sum(abs(p - n) for p, n in zip(paper, v6))
    ax.set_xlabel(r"Equivalence ratio $\phi$")
    ax.set_ylabel("Ignition probability / propensity")
    ax.set_title(f"OSTI 1559043 Fig 7 restated — L1 distance = {L1:.2f}")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(RES / "fig_IP_vs_phi.png", dpi=120)
    plt.close(fig)
    print(f"[fig] wrote {RES / 'fig_IP_vs_phi.png'}")


if __name__ == "__main__":
    print("[figs] Cantera", ct.__version__)
    fig_ip_curve()
    fig_T_ad_vs_pelec()
    fig_z_mr()
    print("[done]")
